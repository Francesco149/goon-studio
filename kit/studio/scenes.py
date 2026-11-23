"""scenes.py: the page's Scene tab - multi-shot videos by hand, on the same story format and the
same renderer as the agent's stories (kit/studio/story.py, docs/STORY.md).

A scene is a story file. Starters are the stories in kit/stories/ (read only); the user's scenes are
copies in my/private/scenes/<id>.json (private, like their pictures), each with a state file
<id>.made.json: {"made": {job name: file}, "takes": {job name: [files]}, "cut": file}. Renders go to
<data_dir>/studio/scenes/<id>/ and are recorded as the user's (private) pictures.

The page edits a scene as a shot list (one card per shot: how it starts, keyframe tags, clip
script, length, cadence) and runs one shot's keyframe or clip, everything missing, or the cut.
"""
import json, os, random, re, tempfile, time

import core
import story as ST

KIT_STORIES = os.path.join(core.KIT, "stories")
MINE = os.path.join(core.PRIVATE, "scenes")


def _id(x):
    x = re.sub(r"[^a-z0-9_]+", "_", str(x or "").lower()).strip("_")[:48]
    if not x:
        raise ValueError("give the scene a name")
    return x


def _path(sid):
    return os.path.join(MINE, _id(sid) + ".json")


def _state_path(sid):
    return os.path.join(MINE, _id(sid) + ".made.json")


def _write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def state(sid):
    st = core.load_json(_state_path(sid), {}) or {}
    st.setdefault("made", {})
    st.setdefault("takes", {})
    return st


def rnd(sid):
    return "studio/scenes/%s" % _id(sid)


def listing():
    starters = []
    for fn in sorted(os.listdir(KIT_STORIES)) if os.path.isdir(KIT_STORIES) else []:
        if fn.endswith(".json"):
            S = core.load_json(os.path.join(KIT_STORIES, fn), {}) or {}
            starters.append({"id": fn[:-5], "about": S.get("about", ""), "shots": len(S.get("shots", [])),
                             # only the variants a story marks for the page (the rest are experiments)
                             "variants": [v for v in S.get("page_variants", []) if v in S.get("variants", {})]})
    mine = []
    for fn in sorted(os.listdir(MINE)) if os.path.isdir(MINE) else []:
        if fn.endswith(".json") and not fn.endswith(".made.json"):
            S = core.load_json(os.path.join(MINE, fn), {}) or {}
            mine.append({"id": fn[:-5], "about": S.get("about", ""), "shots": len(S.get("shots", [])),
                         "time": os.path.getmtime(os.path.join(MINE, fn))})
    mine.sort(key=lambda m: -m["time"])
    return {"starters": starters, "mine": mine, "blank": blank()}


def blank():
    """A new scene from nothing: the Illustrious keyframe + H3 clip stack of the approved stories."""
    return {
        "name": "new_scene", "about": "", "seed": random.randint(1, 10**6) * 100,
        "still": {"workflow": "wf_illu.json", "width": 1216, "height": 832, "steps": 28, "cfg": 6.0,
                  "negative": "lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, blurry, jpeg artifacts, watermark, text, 3d, realistic, censored, mosaic censoring, bar censor"},
        "clip": {"width": 1152, "height": 768, "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
                 "motion_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "fps": 24, "max_len": 124, "seg_len": 49},
        "blocks": {"style": "masterpiece, best quality, amazing quality, anime screenshot, anime coloring, thin lineart",
                   "character": "1girl, mature female", "setting": "indoors, bedroom, evening, warm lamp light",
                   "script_style": "A 2D anime clip in the flat style of a TV anime, thin clean lines, one fixed camera.",
                   "script_character": "a young adult woman", "script_setting": "in a bedroom in the evening, in warm lamp light"},
        "shots": [{"id": "s1", "seconds": 5, "timing": "off", "template": "anime_ll_headgrab_push",
                   "still": "{style}, {character}, solo, looking at viewer, smile, {setting}",
                   "script": "integrated_multimodal_description: [Shot 1] {script_style} {script_character} sits {script_setting}"
                             " and looks into the camera with a soft smile. (One action, what moves and how, the camera.)"
                             " The camera does not move.\n\noverall_soundscape: quiet room tone, no music and no speech."
                             "\n\nnon_diegetic_music: N/A"}],
    }


def load(source):
    """source "kit:<id>" (a starter, optionally "kit:<id>:<variant>") or "mine:<id>"."""
    kind, _, rest = source.partition(":")
    if kind == "kit":
        sid, _, variant = rest.partition(":")
        S = ST.load(os.path.join(KIT_STORIES, _id(sid) + ".json"), variant or None)
        return {"story": S, "state": {"made": {}, "takes": {}}, "mine": False}
    S = core.load_json(_path(rest))
    if not S:
        raise ValueError("no scene %s" % rest)
    return {"story": S, "state": state(rest), "mine": True, "id": _id(rest)}


def check(S):
    ids = [sh.get("id") for sh in S.get("shots", [])]
    if not ids or any(not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("every shot needs its own id")
    for sh in S["shots"]:
        if sh.get("start_from") and sh["start_from"] not in ids:
            raise ValueError("shot %s starts from %s, which is not in the scene" % (sh["id"], sh["start_from"]))
        sh["seconds"] = float(sh.get("seconds") or 5)


def post(action, b, enqueue):
    if action == "load":
        return load(b["source"])
    sid = _id(b.get("id") or (b.get("story") or {}).get("name"))
    if action == "delete":
        for p in (_path(sid), _state_path(sid)):
            if os.path.exists(p):
                os.remove(p)
        return {"deleted": sid}
    if action == "pick":  # use an earlier take of one job
        st = state(sid)
        if b["file"] not in st["takes"].get(b["name"], []):
            raise ValueError("not a take of %s" % b["name"])
        st["made"][b["name"]] = b["file"]
        _write(_state_path(sid), st)
        return {"state": st}
    if action == "forget":  # drop a job's result so "make what is missing" makes it again
        st = state(sid)
        st["made"].pop(b["name"], None)
        _write(_state_path(sid), st)
        return {"state": st}
    S = b.get("story")
    if S is None:
        S = core.load_json(_path(sid))
    S = dict(S, name=sid)
    check(S)
    _write(_path(sid), S)
    if action == "save":
        return {"id": sid, "state": state(sid)}
    if action == "render":
        only = set(b.get("only") or []) or None
        what = b.get("what", "all")
        if b.get("reseed") and only:  # a new take: a new seed for those shots, kept in the scene
            for sh in S["shots"]:
                if sh["id"] in only:
                    sh["seed"] = random.randint(1, 2**31 - 2)
            _write(_path(sid), S)
        redo = bool(b.get("redo"))

        def run(e):
            st = state(sid)

            def say(msg):
                e["note"] = msg
                e.setdefault("log", []).append(time.strftime("%H:%M:%S ") + msg)

            def record(name, file, job):
                st["made"][name] = file
                st["takes"].setdefault(name, []).append(file)
                _write(_state_path(sid), st)

            ok = ST.render(S, rnd(sid), st["made"], by="me", only=only, keys_only=what == "keys",
                           clips_only=what == "clips", redo=redo, say=say, record=record,
                           stop=lambda: e["status"] == "cancelled", on_job=lambda n: e.update(step=n))
            if not ok and e["status"] != "cancelled":
                raise RuntimeError(e.get("note") or "the scene stopped")
            return {"scene": sid, "files": []}

        label = "scene %s: %s%s" % (sid, {"keys": "keyframe", "clips": "clip"}.get(what, "everything missing"),
                                    " of " + ", ".join(sorted(only)) if only else "")
        return {"queued": enqueue({"scene": sid, "what": what, "only": sorted(only or [])}, label, run), "id": sid}
    if action == "cut":
        def run(e):
            st = state(sid)
            data = core.settings().get("data_dir", core.GALLERY)
            files = ST.clip_files(S, st["made"], data)
            if not files:
                raise RuntimeError("no clips yet: make the shots first")
            out_rel = "%s/%s_cut_%s.mp4" % (rnd(sid), sid, time.strftime("%Y%m%d-%H%M%S"))
            out = os.path.join(data, out_rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with tempfile.TemporaryDirectory() as tmp:
                r = ST.assemble(S, files, out, tmp)
            st["cut"] = out_rel
            _write(_state_path(sid), st)
            rec = {"time": time.strftime("%Y-%m-%dT%H:%M:%S"), "by": "me", "workflow": "scene cut", "template": None,
                   "prompt": "scene %s: %d shots, %.1f s" % (sid, len(files), r["seconds"]), "seed": S.get("seed"),
                   "job": {"scene": sid}, "files": [out_rel]}
            core.append_jsonl(core.PHIST, rec)
            return rec
        return {"queued": enqueue({"scene": sid, "what": "cut"}, "scene %s: cut" % sid, run), "id": sid}
    raise ValueError("unknown scene action %s" % action)
