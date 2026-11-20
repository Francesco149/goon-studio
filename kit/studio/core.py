"""core.py: the NSFW Studio's engine layer (shared by server.py and the command line).

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
WLOCK = threading.RLock()
PH = re.compile(r"\{\{(\w+)\}\}")


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def settings():
    s = load_json(os.path.join(MY, "settings.json"), {}) or {}
    s.setdefault("comfy_url", "http://127.0.0.1:8188")
    s.setdefault("data_dir", GALLERY)
    return s


def presets():
    P = load_json(os.path.join(KIT, "presets.json"), {}) or {}
    mine = load_json(os.path.join(MY, "presets.json"), {}) or {}
    for k in ("templates", "characters", "scenes", "negatives"):
        P.setdefault(k, {}).update(mine.get(k, {}))
    return P


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


def build_prompt(job):
    P = presets()
    t = P.get("templates", {}).get(job.get("template") or "")
    fields = {
        "character": clean(job.get("character") or (t or {}).get("character", "")),
        "scene": clean(job.get("scene") or (t or {}).get("scene", "")),
        "style": job.get("style") or (t or {}).get("style", ""),
    }
    base = job.get("prompt") or (t or {}).get("prompt", "")
    return clean(fill_tags(base, fields))


def build_fields(job):
    P = presets()
    t = P.get("templates", {}).get(job.get("template") or "", {})
    fields = dict(t.get("params") or {})
    for k in ("width", "height", "steps", "cfg", "length", "lora", "strength", "denoise"):
        if k in t:
            fields[k] = t[k]
    for k, v in job.items():
        if k not in ("template", "count", "round", "name", "image", "prompt", "negative", "character", "scene"):
            fields[k] = v
    fields["prompt"] = build_prompt(job)
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
    body = json.dumps({"prompt": graph, "client_id": "nsfw-studio"}).encode()
    out = json.loads(http(s["comfy_url"] + "/prompt", body))
    if "prompt_id" not in out:
        raise RuntimeError(json.dumps(out)[:500])
    return out["prompt_id"]


def outputs_of(hist):
    for _n, out in (hist.get("outputs") or {}).items():
        for key in ("images", "gifs", "videos"):
            for it in out.get(key, []) or []:
                if isinstance(it, dict) and "filename" in it and it.get("type", "output") != "temp":
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
                raise RuntimeError("ComfyUI error")
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
        with open(p, "wb") as f:
            f.write(data)
        out.append(p)
    return out


def run(job, by="me", on_queued=None):
    s = settings()
    P = presets()
    t = P.get("templates", {}).get(job.get("template") or "", {})
    wf = job.get("workflow") or t.get("workflow") or "wf_krea2_nsfw.json"
    graph, defaults = load_workflow(wf)
    fields = dict(defaults)
    fields.update(build_fields(job))
    if job.get("image"):
        fields["image"] = upload_input(job["image"], s)
    if job.get("image1"):
        fields["image1"] = upload_input(job["image1"], s)
    graph = subst(graph, fields)
    t0 = time.time()
    pid = submit(graph, s)
    if on_queued:
        on_queued(pid)
    hist = wait(pid, s)
    dest = os.path.join(s.get("data_dir", GALLERY), job.get("round") or "studio")
    files = pull(hist, dest)
    rec = {"time": time.strftime("%Y-%m-%dT%H:%M:%S"), "by": by, "workflow": wf,
           "template": job.get("template"), "prompt": fields.get("prompt"), "negative": fields.get("negative"),
           "seed": fields.get("seed"), "width": fields.get("width"), "height": fields.get("height"),
           "secs": round(time.time() - t0, 1), "files": [os.path.relpath(p, s.get("data_dir", GALLERY)).replace("\\", "/") for p in files]}
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


def all_records():
    """Every picture this app made, newest first, with its visibility. The page calls this; an agent
    must not read the user's private records (my/private/history.jsonl) unless they were made public."""
    lib = library()
    out = []
    for rec in read_jsonl(PHIST) + read_jsonl(HIST):
        for f in rec.get("files", []):
            out.append({"file": f, "time": rec.get("time"), "by": rec.get("by"), "prompt": rec.get("prompt"),
                        "seed": rec.get("seed"), "template": rec.get("template"),
                        "public": (rec.get("by") != "me") or (f in lib["public"]), "trashed": f in lib["trash"]})
    out.sort(key=lambda r: r.get("time") or "", reverse=True)
    return out
