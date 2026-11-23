"""loras.py: the page's LoRA picker - the store's LoRAs, the user's private ones, and adding any of
them to any workflow graph. Standard library only.

Private LoRAs: drop .safetensors files into my/private/loras/ (any subfolders). The engine sees them
as "private/<name>" through a folder link <models_dir>/loras/private -> my/private/loras that
wire_private() makes (a directory junction on Windows, a symlink elsewhere; local engine only).
They are the user's: the agent never lists that folder, so the store's own listings
(modelstore.disk_files) skip the link, and only the page lists it (private_list) for the user.

Base model: LoRAs only work on the model family they were trained for. A LoRA's family comes from
the registry ("base" in kit/models.json), else its file header (kohya metadata / tensor names),
else the user's own note (my/private/loras/_studio.json); a template's family comes from its
workflow (base_of_workflow). The page warns on a mismatch instead of refusing - the user decides.

inject(graph, extra): add [{name, strength}] after the model loader's existing LoRA chain:
LoraLoader (model + CLIP) on a checkpoint graph (Illustrious/Pony: their LoRAs train the text
encoder), LoraLoaderModelOnly elsewhere. Every consumer of the old chain end moves to the new one.
"""
import json, os, re, struct, subprocess

import modelstore

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(KIT)
PRIVATE_DIR = os.path.join(ROOT, "my", "private", "loras")
SANDBOX = os.environ.get("GOON_STUDIO_SANDBOX")  # a test page: its own private folder, no engine link
if SANDBOX:
    PRIVATE_DIR = os.path.join(SANDBOX, "my", "private", "loras")
SIDECAR = os.path.join(PRIVATE_DIR, "_studio.json")
PREFIX = "private/"

FAMILIES = {
    "sdxl": "SDXL (Illustrious / Pony / NoobAI)",
    "anima": "Anima",
    "krea2": "Krea 2",
    "h3video": "H3 video",
    "h3image": "H3 image",
    "qwen": "Qwen image",
    "wan": "Wan video",
    "flux": "Flux",
    "sd15": "SD 1.5",
}


def base_of_workflow(wf):
    w = (wf or "").lower()
    if "illu" in w or "pony" in w:
        return "sdxl"
    if "anima" in w:
        return "anima"
    if "krea" in w:
        return "krea2"
    if "h3vid" in w:
        return "h3video"
    if "h3img" in w:
        return "h3image"
    if "qwen" in w:
        return "qwen"
    if "wan" in w:
        return "wan"
    return None


# ---- the private folder -----------------------------------------------------------------------
def wire_private(s=None):
    """Make the engine see my/private/loras as loras/private. Returns a short status line."""
    s = s or modelstore.settings()
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    if SANDBOX:
        return "test page (sandbox): no engine link"
    if not modelstore.is_local(s):
        return "engine is not on this PC: private LoRAs need the local engine"
    link = os.path.join(modelstore.models_dir(s), "loras", "private")
    if os.path.lexists(link):
        try:
            if os.path.samefile(link, PRIVATE_DIR):
                return "ok"
        except OSError:
            pass
        return "%s exists and is not the private folder: rename it to use private LoRAs" % link
    os.makedirs(os.path.dirname(link), exist_ok=True)
    try:
        if os.name == "nt":  # a junction needs no admin rights (a symlink does)
            r = subprocess.run(["cmd", "/c", "mklink", "/J", link, PRIVATE_DIR], capture_output=True, text=True)
            if r.returncode != 0:
                return "could not link the private folder: %s" % (r.stderr or r.stdout).strip()
        else:
            os.symlink(PRIVATE_DIR, link, target_is_directory=True)
    except OSError as e:
        return "could not link the private folder: %s" % e
    return "ok"


def header(path):
    """(metadata dict, tensor key sample) from a .safetensors header; ({}, []) when unreadable."""
    try:
        with open(path, "rb") as f:
            n = struct.unpack("<Q", f.read(8))[0]
            if n > 100 * 2**20:
                return {}, []
            h = json.loads(f.read(n))
    except (OSError, ValueError, struct.error):
        return {}, []
    meta = h.pop("__metadata__", {}) or {}
    return meta, list(h)[:400]


def guess_base(meta, keys):
    arch = " ".join(str(meta.get(k, "")) for k in ("modelspec.architecture", "ss_base_model_version", "ss_sd_model_name")).lower()
    if any(x in arch for x in ("xl", "illustrious", "pony", "noob")):
        return "sdxl"
    if "flux" in arch:
        return "flux"
    if any(x in arch for x in ("v1-5", "sd_v1", "sd1")):
        return "sd15"
    if "wan" in arch:
        return "wan"
    k = " ".join(keys)
    if "lora_te2_" in k or ("input_blocks_" in k and "lora_unet" in k):
        return "sdxl"
    if "double_blocks" in k or "single_blocks" in k:
        return "flux"
    return None


def tags_of(meta, top=12):
    """The most frequent training tags: usually the trigger words come first."""
    try:
        freq = json.loads(meta.get("ss_tag_frequency") or "{}")
    except ValueError:
        return []
    count = {}
    for d in freq.values():
        for t, c in (d or {}).items():
            t = t.strip()
            if t:
                count[t] = count.get(t, 0) + int(c or 0)
    return [t for t, _ in sorted(count.items(), key=lambda kv: -kv[1])[:top]]


def notes():
    return modelstore.load_json(SIDECAR, {}) or {}


def save_note(name, note):
    """The user's own line for a private LoRA: base, trigger, strength, about."""
    d = notes()
    clean = {k: note[k] for k in ("base", "trigger", "strength", "about") if note.get(k) not in (None, "")}
    if clean:
        d[name] = clean
    else:
        d.pop(name, None)
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    tmp = SIDECAR + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
    os.replace(tmp, SIDECAR)


def private_list():
    """The user's private LoRAs (page only)."""
    out, N = [], notes()
    if not os.path.isdir(PRIVATE_DIR):
        return out
    for base, _dirs, files in os.walk(PRIVATE_DIR):
        for fn in sorted(files):
            if not fn.lower().endswith(".safetensors"):
                continue
            p = os.path.join(base, fn)
            rel = os.path.relpath(p, PRIVATE_DIR).replace("\\", "/")
            name = PREFIX + rel
            meta, keys = header(p)
            n = N.get(name, {})
            out.append({"name": name, "label": rel, "private": True, "mb": round(os.path.getsize(p) / 2**20, 1),
                        "base": n.get("base") or guess_base(meta, keys), "base_from": "note" if n.get("base") else "file",
                        "trigger": n.get("trigger", ""), "strength": n.get("strength"), "about": n.get("about", ""),
                        "tags": tags_of(meta), "title": meta.get("modelspec.title") or meta.get("ss_output_name") or ""})
    return out


def store_list(s=None):
    """The store's LoRAs the engine can load, with the registry's base / trigger / what."""
    s = s or modelstore.settings()
    reg = modelstore.registry()
    out = []
    for name in sorted(modelstore.available("loras", s)):
        if name.startswith(PREFIX):
            continue
        e = reg.get("loras/" + name) or {}
        if e.get("picker") is False:
            continue
        base, tags = e.get("base"), []
        trig = e.get("trigger") or ""  # a string, or a list of blocks (identity, outfit, ...)
        if not base or not trig:  # read the file's header when it is on this PC
            p = next((os.path.join(d, *name.split("/")) for d in modelstore.search_dirs("loras", s)
                      if os.path.isfile(os.path.join(d, *name.split("/")))), None)
            meta, keys = header(p) if p else ({}, [])
            base = base or guess_base(meta, keys)
            if not trig:
                tags = tags_of(meta)
            low = name.lower()
            base = base or ("qwen" if "qwen" in low else "wan" if "wan2" in low or "wan_" in low else "flux" if "flux" in low else None)
        out.append({"name": name, "label": name, "private": False, "base": base,
                    "trigger": trig, "about": e.get("what", ""), "strength": None, "tags": tags})
    return out


def private_path(name):
    if not name.startswith(PREFIX):
        return None
    p = os.path.normpath(os.path.join(PRIVATE_DIR, name[len(PREFIX):].replace("/", os.sep)))
    return p if p.startswith(os.path.normpath(PRIVATE_DIR)) else None


# ---- the graph --------------------------------------------------------------------------------
TRUNK = ("UNETLoader", "UnetLoaderGGUF", "CheckpointLoaderSimple")
LORA_NODES = ("LoraLoader", "LoraLoaderModelOnly")


def inject(graph, extra, spell=lambda n: n):
    """Add [{name, strength}] LoRAs to every model trunk of a filled graph. Returns the node ids added."""
    extra = [x for x in (extra or []) if x and x.get("name")]
    if not extra:
        return []
    have = {modelstore.norm(n["inputs"].get("lora_name")) for n in graph.values()
            if isinstance(n, dict) and n.get("class_type") in LORA_NODES}
    added = []
    for tid in [k for k, v in graph.items() if isinstance(v, dict) and v.get("class_type") in TRUNK]:
        ckpt = graph[tid]["class_type"] == "CheckpointLoaderSimple"
        model, clip = [tid, 0], ([tid, 1] if ckpt else None)
        while True:  # follow the existing LoRA chain to its end
            nxt = next((k for k, v in graph.items() if isinstance(v, dict) and v.get("class_type") in LORA_NODES
                        and v["inputs"].get("model") == model), None)
            if not nxt:
                break
            model = [nxt, 0]
            if graph[nxt]["class_type"] == "LoraLoader" and clip:
                clip = [nxt, 1]
        end_model, end_clip = model, clip
        mine = set()
        for i, x in enumerate(extra):
            name = modelstore.norm(x["name"])
            if name in have:
                continue
            st = float(x.get("strength", 1.0) if x.get("strength") not in (None, "") else 1.0)
            nid = "xl_%s_%d" % (tid, i)
            if clip:
                graph[nid] = {"class_type": "LoraLoader", "inputs": {"model": model, "clip": clip, "lora_name": spell(name),
                                                                      "strength_model": st, "strength_clip": st}}
                clip = [nid, 1]
            else:
                graph[nid] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": model, "lora_name": spell(name),
                                                                               "strength_model": st}}
            model = [nid, 0]
            mine.add(nid)
            added.append(nid)
        if not mine:
            continue
        for k, v in graph.items():  # consumers of the old chain end now read the new one
            if k in mine or not isinstance(v, dict):
                continue
            for inp, src in list(v.get("inputs", {}).items()):
                if src == end_model:
                    v["inputs"][inp] = model
                elif end_clip and src == end_clip:
                    v["inputs"][inp] = clip
    return added
