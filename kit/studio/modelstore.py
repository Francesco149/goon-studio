"""modelstore.py: where model files live, what each template needs, and where to get them.

One store per install: `models_dir` in my/settings.json (default: the folder an existing
extra_model_paths.yaml points ComfyUI at, else <engine_dir>/ComfyUI/models). It has ComfyUI's own
layout (diffusion_models/, text_encoders/, vae/, loras/, ...); `wire()` points the engine at it.

kit/models.json is the registry: one entry per file, keyed "<folder>/<name as ComfyUI lists it>",
with where it comes from (url, page) and what it is. Every file a template needs must be in it.

What a template needs is read from its workflow graph: every loader node's file, after the
template's own fields are filled in. Shared by the page (kit/studio/server.py, core.py), tools/lab.py
and tools/models/store.py. Standard library only.
"""
import json, os, re, shutil, sys, time, urllib.error, urllib.parse, urllib.request

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(KIT)
REGISTRY = os.path.join(KIT, "models.json")
# the user's private LoRAs (kit/studio/loras.py): the engine sees them as loras/private/<name> through
# a folder link; the store's listings skip that link (the agent never lists the user's private files)
PRIVATE_LORAS = os.path.join(ROOT, "my", "private", "loras")
PH = re.compile(r"\{\{(\w+)\}\}")
EXT = (".safetensors", ".gguf", ".pth", ".ckpt", ".pt", ".bin", ".onnx")
QUANT = re.compile(r"_(int8_convrot|w4a8_mixed|w4a8|nvfp4|int8|fp8\w*|bf16|fp16|fp32)$")
# loader class -> the models/ folder its files live in (anything else falls back to the registry)
FOLDER = {
    "UNETLoader": "diffusion_models", "UnetLoaderGGUF": "diffusion_models",
    "CLIPLoader": "text_encoders", "DualCLIPLoader": "text_encoders",
    "VAELoader": "vae", "LoraLoaderModelOnly": "loras", "LoraLoader": "loras",
    "CLIPVisionLoader": "clip_vision", "LoadBackgroundRemovalModel": "background_removal",
    "UpscaleModelLoader": "upscale_models", "CheckpointLoaderSimple": "checkpoints",
    "ModelPatchLoader": "model_patches",
    "FrameInterpolationModelLoader": "frame_interpolation",
}
# older ComfyUI folder names that still work
ALIASES = {"diffusion_models": ["diffusion_models", "unet"], "text_encoders": ["text_encoders", "clip"]}
WIRED_FOLDERS = ["diffusion_models", "text_encoders", "vae", "loras", "clip_vision", "background_removal",
                 "upscale_models", "checkpoints", "model_patches", "frame_interpolation"]


# ---- settings and places ----------------------------------------------------------------------
def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def settings():
    s = load_json(os.path.join(ROOT, "my", "settings.json"), {}) or {}
    s.setdefault("comfy_url", "http://127.0.0.1:8187")
    if os.environ.get("GOON_COMFY_URL"):          # a bench engine (tests), never the user's setting
        s["comfy_url"] = os.environ["GOON_COMFY_URL"]
    return s


def engine_comfy(s=None):
    """<engine_dir>/ComfyUI, or None when the engine folder is unknown."""
    s = s or settings()
    e = s.get("engine_dir")
    if not e:
        return None
    for d in (os.path.join(e, "ComfyUI"), e):
        if os.path.isfile(os.path.join(d, "main.py")):
            return d
    return os.path.join(e, "ComfyUI")


def yaml_sections(path):
    """{section: {key: value}} from a flat extra_model_paths.yaml (enough for what ComfyUI writes)."""
    out, cur = {}, None
    try:
        lines = open(path, encoding="utf-8-sig").read().splitlines()
    except OSError:
        return out
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\S[^:]*):\s*$", line)
        if m:
            cur = out.setdefault(m.group(1).strip(), {})
            continue
        m = re.match(r"^\s+([^:#]+):\s*(.*?)\s*$", line)
        if m and cur is not None:
            cur[m.group(1).strip()] = m.group(2).strip().strip("'\"")
    return out


def models_dir(s=None):
    s = s or settings()
    if s.get("models_dir"):
        return os.path.normpath(s["models_dir"])
    c = engine_comfy(s)
    if c:
        secs = yaml_sections(os.path.join(c, "extra_model_paths.yaml"))
        for name in ["goon_studio"] + [k for k in secs if k != "goon_studio"]:
            if (secs.get(name) or {}).get("base_path"):
                return os.path.normpath(secs[name]["base_path"])
        return os.path.join(c, "models")
    return os.path.join(ROOT, "models")


def search_dirs(folder, s=None):
    """Every directory ComfyUI would look in for this folder on this install."""
    s = s or settings()
    roots = [models_dir(s)]
    c = engine_comfy(s)
    if c:
        roots.append(os.path.join(c, "models"))
        for sec in yaml_sections(os.path.join(c, "extra_model_paths.yaml")).values():
            if sec.get("base_path"):
                roots.append(sec["base_path"])
    out = []
    for r in roots:
        for name in ALIASES.get(folder, [folder]):
            d = os.path.normpath(os.path.join(r, name))
            if d not in out:
                out.append(d)
    return out


def dest_path(folder, name, s=None):
    return os.path.join(models_dir(s), folder, *name.replace("\\", "/").split("/"))


# ---- registry ---------------------------------------------------------------------------------
def registry():
    return (load_json(REGISTRY, {}) or {}).get("files", {})


def save_registry(files):
    d = load_json(REGISTRY, {}) or {}
    d["files"] = dict(sorted(files.items()))
    tmp = REGISTRY + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, REGISTRY)


def norm(name):
    return (name or "").replace("\\", "/")


def stem(name):
    return QUANT.sub("", os.path.splitext(norm(name))[0])


def entry(folder, name, reg=None):
    reg = registry() if reg is None else reg
    return reg.get("%s/%s" % (folder, norm(name)))


# ---- what a template needs --------------------------------------------------------------------
def load_workflow(name):
    w = load_json(os.path.join(ROOT, "workflows", name))
    if not w:
        raise ValueError("no workflow %s" % name)
    defaults = w.get("_params", {}) or {}
    graph = {k: v for k, v in w.items() if not k.startswith("_")}
    return graph, defaults


def graph_files(graph, reg=None):
    """[(node id, class_type, input key, file, folder)] for every model file the graph loads."""
    reg = registry() if reg is None else reg
    out = []
    for nid, n in graph.items():
        if not isinstance(n, dict):
            continue
        ct = n.get("class_type", "")
        for k, v in (n.get("inputs") or {}).items():
            if isinstance(v, str) and v.lower().endswith(EXT):
                folder = FOLDER.get(ct)
                if not folder:
                    hits = [key.split("/", 1)[0] for key in reg if key.split("/", 1)[1] == norm(v)]
                    folder = hits[0] if hits else "?"
                out.append((nid, ct, k, norm(v), folder))
    return out


def fill_graph(graph, fields):
    """Substitute whole-value {{placeholders}} only (enough to see the model names)."""
    def sub(o):
        if isinstance(o, dict):
            return {k: sub(v) for k, v in o.items()}
        if isinstance(o, list):
            return [sub(v) for v in o]
        if isinstance(o, str):
            m = PH.fullmatch(o)
            if m and m.group(1) in fields:
                return fields[m.group(1)]
        return o
    return sub(graph)


def presets():
    P = load_json(os.path.join(KIT, "presets.json"), {}) or {}
    mine = load_json(os.path.join(ROOT, "my", "presets.json"), {}) or {}
    for k in ("templates", "video_templates"):
        P.setdefault(k, {}).update(mine.get(k, {}))
    return P


def template_job(tid, P=None):
    """(workflow, fields) a template runs with. Picture templates and video recipes both."""
    P = P or presets()
    t = P.get("templates", {}).get(tid) or P.get("video_templates", {}).get(tid)
    if t is None:
        raise KeyError("no template %s" % tid)
    fields = dict(t.get("params") or {})
    fields.update({k: v for k, v in t.items() if not isinstance(v, (dict, list))})
    if t.get("lora") and "nsfw_lora" not in fields:
        fields["nsfw_lora"] = t["lora"]          # video recipes name their act LoRA "lora"
    if t.get("strength") is not None and "nsfw_strength" not in fields:
        fields["nsfw_strength"] = t["strength"]
    return t.get("workflow") or "wf_krea2_nsfw.json", fields


def needs(workflow, fields=None):
    """[(folder, file)] a job with this workflow and these fields loads, in graph order, unique."""
    graph, defaults = load_workflow(workflow)
    f = dict(defaults)
    f.update({k: v for k, v in (fields or {}).items() if v not in (None, "")})
    seen, out = set(), []
    for _nid, _ct, _k, name, folder in graph_files(fill_graph(graph, f)):
        if (folder, name) not in seen:
            seen.add((folder, name))
            out.append((folder, name))
    return out


# ---- what this install has --------------------------------------------------------------------
def disk_files(folder, s=None):
    have = set()
    for d in search_dirs(folder, s):
        if not os.path.isdir(d):
            continue
        for base, _dirs, files in os.walk(d):
            if folder == "loras" and base == d and "private" in _dirs:
                _dirs.remove("private")
            for fn in files:
                if fn.lower().endswith(EXT):
                    have.add(norm(os.path.relpath(os.path.join(base, fn), d)))
    return have


_ENGINE = {}


def engine_files(s=None, ttl=20):
    """{(class_type, input key): [file, ...]} from the running ComfyUI, or {} when it is down."""
    s = s or settings()
    url = s["comfy_url"].rstrip("/")
    hit = _ENGINE.get(url)
    if hit and time.time() - hit[0] < ttl:
        return hit[1]
    out = {}
    try:
        with urllib.request.urlopen(url + "/object_info", timeout=20) as r:
            info = json.loads(r.read())
        for ct, spec in info.items():
            for k, v in ((spec.get("input") or {}).get("required") or {}).items():
                if isinstance(v, list) and v:
                    opts = v[0] if isinstance(v[0], list) else (v[1] or {}).get("options") if len(v) > 1 and isinstance(v[1], dict) else None
                    if opts and any(isinstance(o, str) and o.lower().endswith(EXT) for o in opts):
                        out[(ct, k)] = [norm(o) for o in opts if isinstance(o, str)]
    except Exception:
        out = {}
    _ENGINE[url] = (time.time(), out)
    return out


def is_local(s=None):
    s = s or settings()
    return bool(re.match(r"https?://(?:127\.0\.0\.1|localhost|\[::1\])(?::\d+)?(?:/|$)", s.get("comfy_url", "")))


def available(folder, s=None):
    """Files this install can load from a folder: the engine's list when it answers (it is the
    truth, also for a remote engine), plus what is on disk when the engine is local."""
    s = s or settings()
    have = set()
    for (ct, _k), opts in engine_files(s).items():
        if FOLDER.get(ct) == folder:
            have.update(opts)
    if is_local(s) or not have:
        have |= disk_files(folder, s)
    return have


def pick(folder, name, have):
    """The file to load: the name itself, else the same model in another quantization."""
    name = norm(name)
    if name in have:
        return name
    alts = sorted(h for h in have if stem(h) == stem(name))
    return alts[0] if alts else None


def suggest(folder, name, reg=None):
    """Which registry file to fetch for a missing name: an 8 GB variant of the same model first (also on
    16 GB cards: the w4a8 files fit there and beat INT8, docs/PERFORMANCE-16GB.md)."""
    reg = registry() if reg is None else reg
    same = [(k.split("/", 1)[1], e) for k, e in reg.items()
            if k.split("/", 1)[0] == folder and stem(k.split("/", 1)[1]) == stem(name)]
    same.sort(key=lambda kv: (kv[1].get("tier") != "8gb", kv[0] != norm(name)))
    return same[0] if same else (norm(name), None)


def check(workflow, fields=None, s=None):
    """One row per file the job loads: present or not, and where to get it."""
    s = s or settings()
    reg = registry()
    cache, rows = {}, []
    for folder, name in needs(workflow, fields):
        if folder not in cache:
            cache[folder] = available(folder, s)
        use = pick(folder, name, cache[folder])
        fname, e = (use, entry(folder, use, reg)) if use else suggest(folder, name, reg)
        e = e or entry(folder, name, reg) or {}
        rows.append({"folder": folder, "file": name, "present": bool(use), "use": use, "fetch": fname,
                     "dest": dest_path(folder, fname, s), "url": e.get("url"), "page": e.get("page"),
                     "gb": e.get("gb"), "what": e.get("what"), "license": e.get("license"), "login": bool(e.get("login")),
                     "known": bool(e)})
    return rows


def resolve_graph(graph, s=None):
    """Swap every loader's file for the one this install has (same model, other quantization), and
    write every file in the engine's own spelling: a local Windows ComfyUI lists subfolder files
    with backslashes and rejects "h3nsfw/x.safetensors" - for every loader, not only the act LoRA.
    Returns the list of swaps; names nothing matches are left for ComfyUI to report."""
    s = s or settings()
    win = os.name == "nt" and is_local(s)
    cache, swaps = {}, []
    for nid, ct, k, name, folder in graph_files(graph):
        if is_private_lora(folder, name):
            graph[nid]["inputs"][k] = name.replace("/", "\\") if win else name
            continue
        if folder not in cache:
            cache[folder] = available(folder, s)
        if not cache[folder]:
            continue
        use = pick(folder, name, cache[folder])
        if not use:
            continue
        spelled = use.replace("/", "\\") if win else use
        if graph[nid]["inputs"][k] != spelled:
            graph[nid]["inputs"][k] = spelled
        if use != name:
            swaps.append((name, use))
    return swaps


def is_private_lora(folder, name):
    return folder == "loras" and norm(name).startswith("private/")


def graph_missing(graph, s=None):
    """check() rows for the files a filled graph loads that this install does not have."""
    s = s or settings()
    reg = registry()
    cache, rows = {}, []
    for _nid, _ct, _k, name, folder in graph_files(graph, reg):
        if is_private_lora(folder, name):
            if not os.path.isfile(os.path.join(PRIVATE_LORAS, *name.split("/")[1:])):
                rows.append({"folder": folder, "file": name, "present": False, "fetch": name,
                             "dest": os.path.join(PRIVATE_LORAS, *name.split("/")[1:]), "url": None, "page": None, "gb": None})
            continue
        if folder not in cache:
            cache[folder] = available(folder, s)
        if cache[folder] and pick(folder, name, cache[folder]) is None:
            fname, e = suggest(folder, name, reg)
            e = e or entry(folder, name, reg) or {}
            rows.append({"folder": folder, "file": name, "present": False, "fetch": fname,
                         "dest": dest_path(folder, fname, s), "url": e.get("url"), "page": e.get("page"),
                         "gb": e.get("gb")})
    return rows


def missing_message(rows):
    miss = [r for r in rows if not r["present"]]
    if not miss:
        return ""
    parts = []
    for r in miss:
        where = os.path.dirname(r["dest"])
        src = r["page"] or r["url"] or "no download link recorded yet (ask the agent)"
        parts.append("%s (%s) -> put it in %s; get it from %s" % (r["fetch"], "%.1f GB" % r["gb"] if r["gb"] else "size ?", where, src))
    return "Missing model file%s: %s. Or ask the agent to download the models for this template." % (
        "s" if len(miss) > 1 else "", "; ".join(parts))


# ---- changing the store -----------------------------------------------------------------------
def civitai_token():
    t = os.environ.get("CIVITAI_TOKEN", "").strip()
    p = os.path.join(ROOT, "my", ".civitai-token")
    if not t and os.path.exists(p):
        t = open(p).read().strip()
    return t


class _DropAuthOnHostChange(urllib.request.HTTPRedirectHandler):
    """Civitai redirects big files to a signed storage URL (Cloudflare R2) that rejects a request
    still carrying the Civitai token (HTTP 400). Keep the token on civitai.com only."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and urllib.parse.urlsplit(newurl).hostname != urllib.parse.urlsplit(req.full_url).hostname:
            new.remove_header("Authorization")
        return new


def download(url, dest, gb=None, log=print):
    """Resumable download to dest (via dest.part). Civitai links get the token when one is set."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    part = dest + ".part"
    headers = {"User-Agent": "goon-studio/1.0"}
    if "civitai.com" in url and civitai_token():
        headers["Authorization"] = "Bearer " + civitai_token()
    have = os.path.getsize(part) if os.path.exists(part) else 0
    if have:
        headers["Range"] = "bytes=%d-" % have
    req = urllib.request.Request(url, headers=headers)
    try:
        r = urllib.request.build_opener(_DropAuthOnHostChange).open(req, timeout=60)
    except urllib.error.HTTPError as e:
        if e.code == 416 and have:          # the .part is already complete
            os.replace(part, dest)
            return dest
        if e.code in (401, 403) and "civitai.com" in url:
            raise RuntimeError("Civitai wants a login for this file: put an API key in my/.civitai-token "
                               "(civitai.com > Account settings > API Keys) or download it in the browser")
        raise
    with r:
        total = int(r.headers.get("Content-Length") or 0) + (have if r.status == 206 else 0)
        mode = "ab" if r.status == 206 else "wb"
        done = have if r.status == 206 else 0
        t0, last = time.time(), 0
        with open(part, mode) as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
                done += len(chunk)
                if time.time() - last > 5:
                    last = time.time()
                    log("  %s: %.2f / %s GB" % (os.path.basename(dest), done / 1e9, "%.2f" % (total / 1e9) if total else "?"))
    if total and os.path.getsize(part) != total:
        raise RuntimeError("%s: got %d of %d bytes; run it again to resume" % (dest, os.path.getsize(part), total))
    if gb and abs(os.path.getsize(part) / 1e9 - gb) > max(0.05, gb * 0.05):
        log("  note: %s is %.2f GB, the registry says %.2f GB" % (os.path.basename(dest), os.path.getsize(part) / 1e9, gb))
    os.replace(part, dest)
    return dest


def adopt(path, folder, sub="", name=None, meta=None, s=None):
    """Move a file the user downloaded into the store and add it to the registry.
    Returns (registry key, new path). An existing registry entry keeps its fields."""
    s = s or settings()
    if folder not in WIRED_FOLDERS:
        raise ValueError("folder must be one of: " + ", ".join(WIRED_FOLDERS))
    name = norm("/".join(p for p in (sub.strip("/\\"), name or os.path.basename(path)) if p))
    dest = dest_path(folder, name, s)
    if os.path.abspath(path) != os.path.abspath(dest):
        if os.path.exists(dest):
            raise FileExistsError("already in the store: " + dest)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(path, dest)
    reg = registry()
    key = "%s/%s" % (folder, name)
    e = reg.get(key, {})
    e.setdefault("gb", round(os.path.getsize(dest) / 1e9, 2))
    for k, v in (meta or {}).items():
        if v:
            e[k] = v
    e.setdefault("url", "")
    e.setdefault("what", "")
    reg[key] = e
    save_registry(reg)
    return key, dest


def wire(s=None):
    """Make the engine read the store: a `goon_studio:` section in extra_model_paths.yaml. Other
    sections (another app's) are kept. Returns the yaml path, or None without an engine_dir."""
    s = s or settings()
    c = engine_comfy(s)
    if not c:
        return None
    path = os.path.join(c, "extra_model_paths.yaml")
    base = models_dir(s).replace("\\", "/")
    text = open(path, encoding="utf-8-sig").read() if os.path.exists(path) else ""
    text = re.sub(r"(?ms)^goon_studio:\s*\n(?:[ \t]+.*\n?)*", "", text).rstrip()
    block = "goon_studio:\n    base_path: %s\n%s\n" % (base, "".join("    %s: %s\n" % (f, f) for f in WIRED_FOLDERS).rstrip("\n"))
    text = (text + "\n\n" if text else "") + block
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    for f in WIRED_FOLDERS:
        os.makedirs(os.path.join(models_dir(s), f), exist_ok=True)
    return path
