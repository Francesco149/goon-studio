"""core.py: the Goon Studio's engine layer (shared by server.py and the command line).

Builds a ComfyUI graph from a workflow JSON template, sends it to the local ComfyUI, waits, moves
the result into the gallery and records it. Standard library only.

A job is a dict:
  workflow   file name in workflows/ (e.g. "wf_krea2_nsfw.json")
  template   preset id from templates/presets.json (fills the defaults)
  prompt     the prompt; {character}, {scene}, {style} are filled from the template/fields
  negative   negative prompt (optional)
  seed       int (random when missing), count
  width/height/steps/cfg/length and any workflow placeholder (lora, strength, ...)
  image      path to a local picture for image-to-image / video workflows
  round      gallery subfolder (default "studio")
"""
import json, os, random, re, shutil, subprocess, threading, time, urllib.parse, urllib.request

import headroom
import loras
import modelstore

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(KIT)
MY = os.path.join(ROOT, "my")
PRIVATE = os.path.join(MY, "private")
GALLERY = os.path.join(ROOT, "gallery")
HIST = os.path.join(MY, "history.jsonl")          # the agent's pictures
FEED = os.path.join(MY, "feedback.jsonl")
PHIST = os.path.join(PRIVATE, "history.jsonl")    # the user's own pictures (private unless made public)
PFEED = os.path.join(PRIVATE, "feedback.jsonl")
LIB = os.path.join(MY, "library.json")
FAVS = os.path.join(MY, "favorites.json")         # favorites the agent may see (its gens, shared ones)
PFAVS = os.path.join(PRIVATE, "favorites.json")   # favorites among the user's private pictures
# GOON_STUDIO_SANDBOX=<dir>: a test page (port 8291) with its own history, library, private folder and
# gallery under <dir>, so testing the page never shows or touches the user's private pictures.
# my/settings.json (engine, models) and kit/ are still the real ones.
SANDBOX = os.environ.get("GOON_STUDIO_SANDBOX")
if SANDBOX:
    MY = os.path.join(SANDBOX, "my")
    PRIVATE = os.path.join(MY, "private")
    HIST, FEED, LIB, FAVS = (os.path.join(MY, n) for n in ("history.jsonl", "feedback.jsonl", "library.json", "favorites.json"))
    PHIST, PFEED, PFAVS = (os.path.join(PRIVATE, n) for n in ("history.jsonl", "feedback.jsonl", "favorites.json"))
WLOCK = threading.RLock()
PH = re.compile(r"\{\{(\w+)\}\}")


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def settings():
    s = load_json(os.path.join(ROOT, "my", "settings.json"), {}) or {}
    s.setdefault("comfy_url", "http://127.0.0.1:8187")   # Love Live Studio keeps 8188
    s.setdefault("data_dir", GALLERY)
    if SANDBOX:
        s["data_dir"] = os.path.join(SANDBOX, "gallery")
    if os.environ.get("GOON_COMFY_URL"):          # a bench engine (tests), never the user's setting
        s["comfy_url"] = os.environ["GOON_COMFY_URL"]
    return s


def presets():
    P = load_json(os.path.join(KIT, "presets.json"), {}) or {}
    mine = load_json(os.path.join(MY, "presets.json"), {}) or {}
    for k in ("templates", "characters", "scenes", "negatives", "video_templates"):
        P.setdefault(k, {}).update(mine.get(k, {}))
    # the page marks the user's own templates ("Save as my template")
    for k in ("templates", "video_templates"):
        for tid in mine.get(k, {}):
            P[k][tid] = dict(P[k][tid], mine=True)
    return P


def save_my_template(kind, tid, t):
    """Write (or with t=None delete) one of the user's own templates in my/presets.json."""
    path = os.path.join(MY, "presets.json")
    mine = load_json(path, {}) or {}
    sec = mine.setdefault(kind, {})
    if t is None:
        sec.pop(tid, None)
    else:
        sec[tid] = {k: v for k, v in t.items() if k != "mine" and v not in (None, "")}
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(mine, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def workflow_names():
    d = os.path.join(ROOT, "workflows")
    return sorted(f for f in os.listdir(d) if f.endswith(".json"))


def load_workflow(name):
    w = load_json(os.path.join(ROOT, "workflows", name))
    if not w:
        raise ValueError("no workflow %s" % name)
    defaults = w.pop("_params", {}) or {}
    for k in [k for k in list(w) if k.startswith("_")]:
        w.pop(k, None)
    return w, defaults


def fill(text, fields):
    def rep(m):
        return str(fields.get(m.group(1), ""))
    return PH.sub(rep, text or "")


def subst(obj, fields):
    if isinstance(obj, dict):
        return {k: subst(v, fields) for k, v in obj.items()}
    if isinstance(obj, list):
        return [subst(v, fields) for v in obj]
    if isinstance(obj, str):
        if PH.fullmatch(obj):
            k = PH.fullmatch(obj).group(1)
            if k not in fields:
                raise ValueError("workflow needs %s" % k)
            return fields[k]
        return fill(obj, fields)
    return obj


def clean(t):
    t = re.sub(r"(?<!score)_", " ", (t or "").replace("\n", ", "))
    return ", ".join(p.strip() for p in t.split(",") if p.strip())


def fill_tags(text, fields):
    """Fill single-brace prompt fields: {character}, {scene}, {style}."""
    return re.sub(r"\{(\w+)\}", lambda m: str(fields.get(m.group(1), m.group(0))), text or "")


def add_tags(base, extra):
    parts = [p.strip() for p in (base or "").split(",") if p.strip()]
    have = set(parts)
    for p in (extra or "").split(","):
        p = p.strip()
        if p and p not in have:
            parts.append(p)
            have.add(p)
    return ", ".join(parts)


def template(P, tid):
    """A picture template or a video recipe by id ({} when unknown)."""
    return P.get("templates", {}).get(tid or "") or P.get("video_templates", {}).get(tid or "") or {}


def build_prompt(job):
    P = presets()
    t = template(P, job.get("template")) or None
    fields = {
        "character": clean(job.get("character") or (t or {}).get("character", "")),
        "scene": clean(job.get("scene") or (t or {}).get("scene", "")),
        "style": job.get("style") or (t or {}).get("style", ""),
    }
    base = job.get("prompt") or (t or {}).get("prompt", "")
    body = P.get("bodies", {}).get(job.get("body") or "none", "")
    frame = P.get("framings", {}).get(job.get("framing") or "portrait", "")
    if body:
        fields["character"] = add_tags(fields["character"], body)
    if frame:
        fields["scene"] = add_tags(fields["scene"], frame)
    wf = job.get("workflow") or (t or {}).get("workflow", "")
    cock = P.get("cocks", {}).get(job.get("cock") or "template") or {}
    if "h3vid" in wf:
        # H3 video prompts are a MiniMax script: keep `integrated_multimodal_description` and the
        # other section keys exactly as written. A penis type goes at the end of the description
        # so the clip keeps the keyframe's anatomy (the video model redraws what is not named).
        text = (base or "").strip()
        if cock.get("prose"):
            cut = text.find("\n\noverall_soundscape")
            text = (text[:cut] + " " + cock["prose"] + text[cut:]) if cut > 0 else (text + " " + cock["prose"])
        # breast detail (docs/ANIME-TIMING.md): drop the squeeze words that draw fold lines on the
        # inner breasts and describe the smooth result instead (never name what to avoid)
        # dynamics (round a99): the micro-motion paragraph (soft-body jiggle, follow-through) and
        # optionally the smooth h-game opener in place of the TV-anime one
        for opt in (P.get("breasts_video", {}).get(job.get("breasts") or "template") or {},
                    P.get("dynamics_video", {}).get(job.get("dynamics") or "template") or {}):
            text = edit_script(text, opt)
        return text
    if cock.get("tags") and is_tag_prompt(base):
        fields["scene"] = add_tags(fields["scene"], cock["tags"])
    out = fill_tags(base, fields)
    if cock.get("prose") and not is_tag_prompt(base):
        # prose prompts: before a closing camera tag ("... phone photo.") when there is one
        m = re.search(r"\s*(Candid amateur phone photo\.|Natural skin texture[^.]*\.)", out)
        out = (out[:m.start()] + " " + cock["prose"] + out[m.start():]) if m else (out.rstrip() + " " + cock["prose"])
        return re.sub(r"\s+", " ", out).strip()
    return clean(out)


def edit_script(text, opt):
    """apply a Video tab script option to an H3 script: `replace` [[regex, text]] in the description,
    `drop` regexes, then `prose` appended before the soundscape."""
    if not (opt.get("drop") or opt.get("prose") or opt.get("replace")):
        return text
    cut = text.find("\n\noverall_soundscape")
    head, tail = (text[:cut], text[cut:]) if cut > 0 else (text, "")
    for rx, rep in opt.get("replace", []):
        head = re.sub(rx, lambda m: rep, head)
    for rx in opt.get("drop", []):
        head = re.sub(rx, "", head)
    head = re.sub(r"([.!?]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), head)
    if opt.get("prose"):
        head = head.rstrip() + " " + opt["prose"]
    return head + tail


def is_tag_prompt(text):
    """Danbooru-style tag prompts (anime) vs prose (photoreal): tags are short comma-separated items."""
    parts = [p for p in (text or "").split(",") if p.strip()]
    return len(parts) >= 8 and sum(len(p.split()) for p in parts) / len(parts) < 4


def build_late_prompt(prompt, series=None):
    """The Love Live signature trick: the show's name only for the last 30% of the steps, and the
    eye colour weighted up so the name does not recolour her toward a canon character.

    Used by templates that set "late": "signature" (see workflows/wf_anima2_sig.json). A template
    from another show sets "series" (e.g. the Lanzhu character LoRA uses
    "love live! nijigasaki high school idol club")."""
    show = series or "love live! sunshine!!"
    late = (prompt or "").replace("anime screenshot, ", "anime screenshot, %s, " % show, 1)
    return re.sub(r"(?<![(\w])([a-z]+ eyes)(?![:\w])", r"(\1:1.3)", late)


def build_fields(job):
    P = presets()
    t = template(P, job.get("template"))
    fields = dict(t.get("params") or {})
    # everything a template pins down reaches the workflow: size, steps, the model, the LoRAs and
    # the motion booster (a video recipe names its act LoRA "lora"/"strength")
    for k in ("width", "height", "steps", "cfg", "length", "lora", "strength", "denoise", "unet", "sampler",
              "sched", "nsfw_lora", "nsfw_strength", "motion_lora", "motion_strength"):
        if k in t:
            fields[k] = t[k]
    if "lora" in t and "nsfw_lora" not in t:
        fields["nsfw_lora"] = t["lora"]
        if "strength" in t:
            fields["nsfw_strength"] = t["strength"]
    for k, v in job.items():
        if k not in ("template", "count", "round", "name", "image", "prompt", "negative", "character", "scene", "cock", "anime_timing", "breasts", "dynamics", "extra_loras"):
            fields[k] = v
    fields["prompt"] = build_prompt(job)
    late = t.get("late")
    if late == "signature":
        late = build_late_prompt(fields["prompt"], t.get("series"))
    elif late:
        late = clean(fill_tags(late, fields))
    if late:
        fields["late"] = late
    neg = job.get("negative") or t.get("negative") or P.get("negative", "")
    fields["negative"] = clean(neg)
    if not fields.get("seed"):
        fields["seed"] = random.randint(1, 2**31 - 2)
    fields["prefix"] = "gl/%s/%s" % (job.get("round") or "studio", job.get("name") or "img")
    return fields


def http(url, data=None, timeout=120):
    req = urllib.request.Request(url, data=data, method="POST" if data is not None else "GET",
                                 headers={"Content-Type": "application/json"} if data is not None else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def comfy_up(s=None):
    s = s or settings()
    try:
        http(s["comfy_url"] + "/system_stats", timeout=5)
        return True
    except Exception:
        return False


def upload_input(path, s=None):
    s = s or settings()
    r = subprocess.run(["curl", "-s", "-F", "image=@" + path, "-F", "overwrite=true",
                        "-F", "subfolder=nsfw_up", s["comfy_url"] + "/upload/image"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("upload failed")
    j = json.loads(r.stdout)
    return (j.get("subfolder") + "/" if j.get("subfolder") else "") + j["name"]


def submit(graph, s=None):
    s = s or settings()
    body = json.dumps({"prompt": graph, "client_id": "goon-studio"}).encode()
    try:
        out = json.loads(http(s["comfy_url"] + "/prompt", body))
    except urllib.error.HTTPError as e:
        # ComfyUI explains a rejected graph (missing model, bad value) in the body: show that
        raise RuntimeError(comfy_error(e.read())) from None
    if "prompt_id" not in out:
        raise RuntimeError(json.dumps(out)[:500])
    return out["prompt_id"]


def comfy_error(raw):
    """One readable line from ComfyUI's /prompt error JSON."""
    try:
        j = json.loads(raw)
    except ValueError:
        return (raw or b"")[:300].decode("utf-8", "replace")
    msgs = []
    for node, ne in (j.get("node_errors") or {}).items():
        for er in ne.get("errors", []):
            msgs.append("%s (node %s %s): %s" % (er.get("message", ""), node, ne.get("class_type", ""), er.get("details", "")))
    if not msgs:
        er = j.get("error") or {}
        msgs.append(er.get("message", "") + (": " + er["details"] if er.get("details") else ""))
    return "ComfyUI refused the job: " + "; ".join(msgs)[:450]


def outputs_of(hist):
    for _n, out in (hist.get("outputs") or {}).items():
        for key in ("images", "gifs", "videos"):
            for it in out.get(key, []) or []:
                if isinstance(it, dict) and "filename" in it and it.get("type", "output") not in ("temp", "input"):
                    yield it


def wait(pid, s=None, timeout=3600):
    s = s or settings()
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            h = json.loads(http(s["comfy_url"] + "/history/" + pid, timeout=30))
        except Exception:
            time.sleep(2)
            continue
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") == "error":
                ex = [m[1] for m in st.get("messages", []) if m and m[0] in ("execution_error", "execution_interrupted")]
                if ex and ex[0].get("exception_message"):
                    raise RuntimeError("%s: %s" % (ex[0].get("node_type") or "ComfyUI", str(ex[0]["exception_message"]).strip()[:400]))
                raise RuntimeError("ComfyUI stopped the job" if ex else "ComfyUI error")
            if st.get("completed"):
                return h[pid]
        time.sleep(2)
    raise RuntimeError("timed out")


def pull(hist, dest):
    s = settings()
    os.makedirs(dest, exist_ok=True)
    out = []
    for it in outputs_of(hist):
        q = urllib.parse.urlencode({"filename": it["filename"], "subfolder": it.get("subfolder", ""), "type": it.get("type", "output")})
        data = http(s["comfy_url"] + "/view?" + q, timeout=600)
        p = os.path.join(dest, it["filename"])
        # ComfyUI numbers files per engine/output folder: another engine (or a cleaned output
        # folder) restarts at _00001_, which must never overwrite a picture already in the gallery
        stem, ext = os.path.splitext(p)
        n = 1
        while os.path.exists(p):
            p = "%s-%d%s" % (stem, n, ext)
            n += 1
        with open(p, "wb") as f:
            f.write(data)
        out.append(p)
    return out


def local_windows(s=None):
    """True when this process talks to a ComfyUI on the same Windows machine."""
    s = s or settings()
    return os.name == "nt" and bool(re.match(r"https?://(?:127\.0\.0\.1|localhost)(?::\d+)?(?:/|$)",
                                              s.get("comfy_url", "")))


def model_file_field(name, s=None):
    """Windows ComfyUI lists LoRAs with backslashes; Linux boxes use forward slashes."""
    if not name:
        return name
    return name.replace("/", "\\") if local_windows(s) else name


def drop_empty_loras(graph):
    """Bypass LoRA loaders whose LoRA is empty or "none" (the page's "no act LoRA" on a LoRA
    workflow): their consumers read the loader's own model/clip inputs instead."""
    for nid in [k for k, v in graph.items() if isinstance(v, dict)]:
        n = graph[nid]
        if not str(n.get("class_type", "")).startswith("LoraLoader"):
            continue
        name = str(n.get("inputs", {}).get("lora_name", "")).strip()
        if name and name.lower() != "none":
            continue
        ins = n["inputs"]
        outs = {0: ins.get("model"), 1: ins.get("clip")}
        for other in graph.values():
            if not isinstance(other, dict):
                continue
            for k, v in list(other.get("inputs", {}).items()):
                if isinstance(v, list) and len(v) == 2 and str(v[0]) == str(nid) and outs.get(v[1]) is not None:
                    other["inputs"][k] = outs[v[1]]
        del graph[nid]
    return graph


def extend_graph(graph, ctx_start, ctx_len):
    """turn an i2v graph into an extension (round a107): `image` is the previous clip (mp4); its
    ctx_len frames from ctx_start (17k+5: 5, 22, 39) are anchored at frame 0 with MiniMaxH3AddGuide,
    their first frame is also the i2v first frame. The output repeats those frames: drop ctx_len when
    cutting. Continues with half the line-art drift of a single-frame chain (docs/STORY.md a107)."""
    i2v = next((k for k, v in graph.items() if v.get("class_type") == "MiniMaxH3ImageToVideo"), None)
    if not i2v:
        raise ValueError("extend needs an image-to-video workflow (MiniMaxH3ImageToVideo)")
    load = graph[i2v]["inputs"]["first_frame"][0]  # the first frame's LoadImage, through any resize nodes
    while graph[load]["class_type"] != "LoadImage":
        load = graph[load]["inputs"]["image"][0]
    video = graph[load]["inputs"]["image"]
    graph[load] = {"class_type": "ImageFromBatch", "inputs": {"image": ["x_comp", 0], "batch_index": ctx_start, "length": 1}}
    graph["x_video"] = {"class_type": "LoadVideo", "inputs": {"file": video}}
    graph["x_comp"] = {"class_type": "GetVideoComponents", "inputs": {"video": ["x_video", 0]}}
    graph["x_ctx"] = {"class_type": "ImageFromBatch", "inputs": {"image": ["x_comp", 0], "batch_index": ctx_start, "length": ctx_len}}
    for v in graph.values():  # everything that used the i2v conditioning now gets the guided one
        for name, src in v["inputs"].items():
            if src == [i2v, 0]:
                v["inputs"][name] = ["x_guide", 0]
    n = graph[i2v]["inputs"]
    graph["x_guide"] = {"class_type": "MiniMaxH3AddGuide", "inputs": {"positive": [i2v, 0], "vae": n["vae"], "latent": [i2v, 1],
                                                                        "image": ["x_ctx", 0], "frame_idx": 0}}
    return graph


def run(job, by="me", on_queued=None, on_note=None):
    s = settings()
    P = presets()
    t = template(P, job.get("template"))
    wf = job.get("workflow") or t.get("workflow") or "wf_krea2_nsfw.json"
    graph, defaults = load_workflow(wf)
    fields = dict(defaults)
    fields.update(build_fields(job))
    # memory check: tight -> low-memory mode (drop cached models, light encoder), warn, run anyway
    plan = headroom.plan(wf, fields, s)
    note = headroom.summary(plan)
    if note and on_note:
        on_note(note, plan)
    if plan["workflow"] != wf:
        wf = plan["workflow"]
        seed = fields["seed"]
        graph, defaults = load_workflow(wf)
        fields = dict(defaults)
        fields.update(build_fields(dict(job, seed=seed)))
    if plan["unload"]:
        headroom.unload(s)
    for k in ("lora", "nsfw_lora"):
        if fields.get(k):
            fields[k] = model_file_field(fields[k], s)
    if job.get("image"):
        fields["image"] = upload_input(job["image"], s)
    if job.get("image1"):
        fields["image1"] = upload_input(job["image1"], s)
    if job.get("image2"):  # two-picture edits (wf_h3img_2ref): <Picture 2>
        fields["image2"] = upload_input(job["image2"], s)
    if job.get("last"):
        fields["last"] = upload_input(job["last"], s)
    graph = subst(graph, fields)
    drop_empty_loras(graph)
    if job.get("ctx_len"):
        graph = extend_graph(graph, int(job.get("ctx_start", 0)), int(job["ctx_len"]))
    # LoRAs picked on the page (the store's or the user's private ones), after the template's own
    loras.inject(graph, job.get("extra_loras"))
    # same model in the quantization this engine has; a missing file stops here with where to get it
    modelstore.resolve_graph(graph, s)
    miss = modelstore.graph_missing(graph, s)
    if miss:
        raise RuntimeError(modelstore.missing_message(miss))
    t0 = time.time()
    pid = submit(graph, s)
    if on_queued:
        on_queued(pid)
    hist = wait(pid, s)
    dest = os.path.join(s.get("data_dir", GALLERY), job.get("round") or "studio")
    files = pull(hist, dest)
    # anime timing (docs/ANIME-TIMING.md): re-time a finished clip to hand-drawn cadence; the job's
    # choice wins, else the template's default; the untouched clip stays next to it as <name>-raw
    timing = job["anime_timing"] if "anime_timing" in job else t.get("anime_timing")
    if timing and timing != "off":
        try:
            if timing.startswith("smooth"):
                # the opposite (round a99): drop H3's on-2s copies and interpolate (RIFE/FILM)
                import anime_smooth
                for p in files:
                    anime_smooth.apply_mode(p, timing)
            else:
                import anime_timing
                for p in files:
                    anime_timing.apply_mode(p, timing)
        except (ImportError, RuntimeError) as e:
            timing = "skipped (%s)" % e
            if on_note:
                on_note("anime timing skipped (needs PyAV/numpy, and torch + the interpolation model for smooth): %s" % e, plan)
    rec = {"time": time.strftime("%Y-%m-%dT%H:%M:%S"), "by": by, "workflow": wf,
           "template": job.get("template"), "prompt": fields.get("prompt"), "negative": fields.get("negative"),
           "seed": fields.get("seed"), "width": fields.get("width"), "height": fields.get("height"),
           "steps": fields.get("steps"), "length": fields.get("length"),
           # the job as sent, so the page can "use these settings", remake in final quality, chain
           "job": {k: v for k, v in job.items() if k not in ("count",)},
           "anime_timing": timing or "off",
           "memory": plan["profile"], "secs": round(time.time() - t0, 1), "files": [os.path.relpath(p, s.get("data_dir", GALLERY)).replace("\\", "/") for p in files]}
    append_jsonl(HIST if by != "me" else PHIST, rec)
    return rec


# ---- records, privacy -------------------------------------------------------------------------
def append_jsonl(path, rec):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with WLOCK, open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def read_jsonl(path):
    out = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except ValueError:
                        pass
    except OSError:
        pass
    return out


def library():
    d = load_json(LIB, {}) or {}
    d.setdefault("public", {})
    d.setdefault("trash", {})
    d.setdefault("deleted", {})
    return d


def save_library(d):
    os.makedirs(os.path.dirname(LIB), exist_ok=True)
    tmp = LIB + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f)
    os.replace(tmp, LIB)


def is_private(rel, s=None):
    s = s or settings()
    lib = library()
    return rel in lib["trash"] or rel not in lib["public"]


def set_public(files, public):
    lib = library()
    n = 0
    for f in files:
        if public:
            lib["public"][f] = time.time()
        else:
            lib["public"].pop(f, None)
        n += 1
    save_library(lib)
    return n


def trash(files, restore=False, s=None):
    s = s or settings()
    lib = library()
    n = 0
    for f in files:
        p = os.path.join(s.get("data_dir", GALLERY), f)
        if restore:
            lib["trash"].pop(f, None)
        else:
            lib["trash"][f] = time.time()
        n += 1
    save_library(lib)
    return n


def delete_forever(files, s=None):
    s = s or settings()
    lib = library()
    n = 0
    for f in files:
        if f not in lib["trash"]:
            continue
        try:
            os.remove(os.path.join(s.get("data_dir", GALLERY), f))
        except OSError:
            pass
        lib["trash"].pop(f, None)
        lib["deleted"][f] = time.time()
        n += 1
    save_library(lib)
    return n


def feedback_path(rel):
    """Where a rating/note goes: the agent's feedback file only for what the agent may see."""
    if rel.endswith("/_round"):
        return FEED
    if rel in library()["public"]:
        return FEED
    if any(rel in r.get("files", []) for r in read_jsonl(HIST)):
        return FEED
    return PFEED


def _write_json(path, d):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def favorites(private=True):
    """{file: {time, label?}}: the user's favorites (the Favorites tab). Favorites among private
    pictures live in my/private/favorites.json, the rest (agent gens, shared pictures) in
    my/favorites.json, where an agent may read and add to them (tools/favorites.py)."""
    out = dict((load_json(FAVS, {}) or {}).get("files", {}))
    if private:
        out.update((load_json(PFAVS, {}) or {}).get("files", {}))
    return out


def set_favorite(files, fav, labels=None):
    """Mark (fav=True) or unmark pictures/clips as favorites; labels: {file: label} for files that
    have no history record (a story cut, an older round)."""
    labels = labels or {}
    with WLOCK:
        shared, private = load_json(FAVS, {}) or {}, load_json(PFAVS, {}) or {}
        n = 0
        for f in files:
            dest = private if feedback_path(f) == PFEED else shared
            other = shared if dest is private else private
            other.setdefault("files", {}).pop(f, None)
            if fav:
                e = dest.setdefault("files", {}).get(f) or {"time": time.time()}
                if labels.get(f):
                    e["label"] = labels[f]
                dest["files"][f] = e
            else:
                dest.setdefault("files", {}).pop(f, None)
            n += 1
        _write_json(FAVS, shared)
        if private.get("files") or os.path.exists(PFAVS):
            _write_json(PFAVS, private)
    return n


def ratings():
    """{file: (rating, note)}; the latest rating and the latest non-empty note win.
    rating "none" clears it."""
    rate, note = {}, {}
    rows = sorted(read_jsonl(PFEED) + read_jsonl(FEED), key=lambda r: r.get("time") or 0)
    for rec in rows:
        f = rec.get("file")
        if not f:
            continue
        r = rec.get("rating")
        if r == "none":
            rate.pop(f, None)
        elif r:
            rate[f] = r
        if rec.get("note"):
            note[f] = rec["note"]
    return {f: (rate.get(f), note.get(f)) for f in set(rate) | set(note)}


def last_frame(rel, s=None):
    """Save the last frame of a gallery clip as a PNG under uploads/ and return its path."""
    s = s or settings()
    base = s.get("data_dir", GALLERY)
    src = os.path.normpath(os.path.join(base, rel.replace("/", os.sep)))
    if not src.startswith(os.path.normpath(base)) or not os.path.isfile(src):
        raise ValueError("no such clip: %s" % rel)
    out_rel = "uploads/lastframe_%s_%d.png" % (time.strftime("%Y%m%d-%H%M%S"), int(time.time() * 1000) % 1000)
    dst = os.path.join(base, out_rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        import av  # bundled with the ComfyUI portable build
        last = None
        with av.open(src) as c:
            for fr in c.decode(video=0):
                last = fr
        if last is None:
            raise ValueError("the clip has no frames")
        last.to_image().save(dst)
    except ImportError:
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.1", "-i", src,
                            "-update", "1", "-frames:v", "1", dst], capture_output=True, text=True)
        if r.returncode != 0 or not os.path.isfile(dst):
            raise RuntimeError("could not read the last frame (no PyAV, ffmpeg said: %s)" % r.stderr[-300:])
    return out_rel


def all_records(scope="all"):
    """Every picture this app made, newest first, with its visibility.

    scope: "all" | "public" (agent + shared) | "private" (the user's unshared). An agent must only
    read "public"; the My pictures tab uses "private".
    """
    lib = library()
    rate = ratings()
    out = []
    for rec in read_jsonl(PHIST) + read_jsonl(HIST):
        for f in rec.get("files", []):
            public = (rec.get("by") != "me") or (f in lib["public"])
            if scope == "public" and not public:
                continue
            if scope == "private" and public:
                continue
            rt, nt = rate.get(f, (None, None))
            out.append({"file": f, "time": rec.get("time"), "by": rec.get("by"), "prompt": rec.get("prompt"),
                        "seed": rec.get("seed"), "template": rec.get("template"), "rating": rt, "note": nt,
                        "workflow": rec.get("workflow"), "width": rec.get("width"), "height": rec.get("height"),
                        "steps": rec.get("steps"), "length": rec.get("length"), "secs": rec.get("secs"),
                        "job": rec.get("job"), "public": public, "trashed": f in lib["trash"]})
    favs = favorites(private=scope != "public")
    shared = set((load_json(FAVS, {}) or {}).get("files", {}))
    seen = set()
    for r in out:
        r["fav"] = r["file"] in favs
        seen.add(r["file"])
    # favorites with no history record (story cuts, older rounds): only the agent-visible ones, and
    # only files that are still there
    base = settings().get("data_dir", GALLERY)
    for f, e in favs.items():
        if f in seen or f not in shared or scope == "private":
            continue
        if not os.path.isfile(os.path.join(base, f.replace("/", os.sep))):
            continue
        rt, nt = rate.get(f, (None, None))
        out.append({"file": f, "time": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(e.get("time") or 0)),
                    "by": "agent", "label": e.get("label"), "rating": rt, "note": nt, "public": True,
                    "trashed": f in lib["trash"], "fav": True})
    for r in out:
        if r.get("fav"):
            r["fav_time"] = (favs.get(r["file"]) or {}).get("time")
            r.setdefault("label", (favs.get(r["file"]) or {}).get("label"))
    out.sort(key=lambda r: r.get("time") or "", reverse=True)
    return out
