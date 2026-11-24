#!/usr/bin/env python3
"""run_story.py - render a story (kit/stories/*.json) through the page's own engine layer and cut it.

  python tools/rounds/run_story.py kit/stories/emilia_meadow.json <round> [--engine URL]
         [--variant flatter] [--only s1,s3] [--keys-only] [--redo] [--cut-only]

Per shot: the keyframe, then its clip(s) - a continuation clip starts from the last frame of the
one before. Then kit/studio/story.assemble cuts the shots together (per-shot timing, holds, audio)
into <data_dir>/<round>/<story>_cut.mp4. Jobs and results are logged to jobs/<round>_story.log and
written to jobs/<round>_story.jsonl; a rerun skips what is already made (--redo renders again, e.g. with
--only s2 after changing that shot), --keys-only stops after the keyframes, --cut-only only re-cuts.
"""
import json, os, sys, time, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "kit", "studio"))


def main():
    args = sys.argv[1:]
    opt = {}
    for k in ("--engine", "--only", "--variant"):
        if k in args:
            i = args.index(k)
            opt[k] = args[i + 1]
            del args[i:i + 2]
    cut_only = "--cut-only" in args
    keys_only = "--keys-only" in args
    redo = "--redo" in args
    args = [a for a in args if a not in ("--cut-only", "--keys-only", "--redo")]
    if "--engine" in opt:
        os.environ["GOON_COMFY_URL"] = opt["--engine"]
    else:
        sys.path.append(os.path.join(ROOT, "tools"))   # after kit/studio: tools/headroom.py is another module
        import localboxes
        if localboxes.default_url():   # tools/boxes.local.json "_default" (author setups only)
            os.environ["GOON_COMFY_URL"] = localboxes.default_url()
    story_path, rnd = args
    import core, story as ST
    S = ST.load(story_path, opt.get("--variant"))
    only = set(opt["--only"].split(",")) if "--only" in opt else None
    data = core.settings().get("data_dir", core.GALLERY)
    outdir = os.path.join(data, rnd)
    os.makedirs(outdir, exist_ok=True)
    rec_path = os.path.join(ROOT, "jobs", "%s_story.jsonl" % rnd)
    made = {}
    if os.path.exists(rec_path):
        for l in open(rec_path, encoding="utf-8"):
            r = json.loads(l)
            made[r["name"]] = r["file"]
    for sh in S["shots"]:  # a clip_file shot can be a start_from source (an extension of an existing clip)
        if sh.get("clip_file"):
            made["%s_c0" % sh["id"]] = sh["clip_file"]
    log = open(os.path.join(ROOT, "jobs", "%s_story.log" % rnd), "a", encoding="utf-8")

    def say(msg):
        line = "%s %s" % (time.strftime("%H:%M:%S"), msg)
        print(line, flush=True)
        log.write(line + "\n")
        log.flush()

    def record(name, file, job):
        with open(rec_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"name": name, "file": file, "job": job}) + "\n")

    if not cut_only:
        if not ST.render(S, rnd, made, by="agent", only=only, keys_only=keys_only, redo=redo, say=say, record=record):
            return 1
    if keys_only:
        say("keyframes done")
        return 0
    files = ST.clip_files(S, made, data)
    out = os.path.join(outdir, "%s_cut.mp4" % S["name"])
    with tempfile.TemporaryDirectory() as tmp:
        r = ST.assemble(S, files, out, tmp)
    say("cut: %s (%d frames, %.2f s, shots %s)" % (out, r["frames"], r["seconds"], sorted(files)))


if __name__ == "__main__":
    sys.exit(main())
