#!/usr/bin/env python3
"""reanchor.py - re-anchor an H3 clip on what an object should look like (round a98).

Pass 1 is the normal clip. Its own frames at fixed spacing become anchors, so pass 2 keeps the
same motion; each anchor can first be repaired by an H3-Image edit against the keyframe
(Picture 1 = the frame, Picture 2 = the keyframe). Pass 2 is the same job (seed, script, LoRAs)
with the anchors pinned at their own frame indices (MiniMaxH3AddGuide, wf_h3vid_i2v_lora2_g5).

  python_embeded\\python.exe tools/rounds/reanchor.py jobs/x.jsonl NAME ROUND --mode MODE
         [--pass1 gallery/.../clip-raw.mp4] [--dense] [--engine URL]

MODE: selfguide (pass-1 frames pinned as they are), repair (pass-1 frames repaired first),
      ref2va (one pass: the keyframe as reference on every step + first frame),
      refrepair (ComfyUI's multiframe pattern: Ref2VA with the keyframe as <Picture 1>, named in the
      script, + the repaired anchors pinned; repaired anchors from an earlier run are reused).
A job key "ref" (path under data_dir) gives the picture the object is repaired toward, instead of the
keyframe; the start frame is then repaired too (round a104: a better penis from another seed).
"repair_prompt" replaces REPAIR (a104: a stricter one when the reference shows another pose).
PICTURE is appended to the description for the Ref2VA modes: only reference slots reach the text
encoder, AddGuide images do not (docs.comfy.org multiframe tutorial).
Needs the engine's python (PyAV) for the frame extraction.
"""
import json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "kit", "studio"))

PICTURE = (" His cock looks exactly like the one in <Picture 1> - the same size, thickness, shape and skin tone -"
           " in every frame.")
ANCHORS = [24, 48, 72, 96, -1]      # g1..g5; -1 = the last frame
DENSE = [12, 24, 36, 48, 60, 72, 84, 96, 108, 120, -1]   # --dense: g1..g11 (wf_h3vid_i2v_lora2_g11)
REPAIR = ("Edit <Picture 1>. Keep <Picture 1> exactly as it is: the same pose, framing, face, expression, hands, "
          "body, lighting, colours, line art and anime art style; change nothing else. Only redraw his penis so it "
          "looks exactly like the penis in <Picture 2> - the same size, thickness, shape, skin tone and glans - in "
          "the position and angle it has in <Picture 1>.")


def frames_at(path, idxs, out_dir, stem):
    import av
    with av.open(path) as c:
        fr = [f.to_image() for f in c.decode(video=0)]
    out = []
    for i in idxs:
        k = i if i >= 0 else len(fr) + i
        p = os.path.join(out_dir, "%s_f%03d.png" % (stem, k))
        fr[k].save(p)
        out.append(p)
    return out


def main():
    a = sys.argv[1:]
    eng = None
    if "--engine" in a:
        i = a.index("--engine"); eng = a[i + 1]; del a[i:i + 2]
    if eng:
        os.environ["GOON_COMFY_URL"] = eng
    mode = a[a.index("--mode") + 1]; del a[a.index("--mode"):a.index("--mode") + 2]
    pass1 = None
    if "--pass1" in a:
        i = a.index("--pass1"); pass1 = a[i + 1]; del a[i:i + 2]
    dense = "--dense" in a
    if dense:
        a.remove("--dense")
    anchors_at = DENSE if dense else ANCHORS
    jobs_path, name, rnd = a
    import core
    s = core.settings()
    data = s.get("data_dir", core.GALLERY)
    job = next(json.loads(l) for l in open(jobs_path, encoding="utf-8-sig") if l.strip() and json.loads(l)["name"] == name)
    job = {k: v for k, v in job.items() if not k.startswith("_")}
    job["round"] = rnd
    log = open(os.path.join(ROOT, "jobs", "%s_reanchor.log" % rnd), "a", encoding="utf-8")

    def say(m):
        line = "%s %s %s: %s" % (time.strftime("%H:%M:%S"), name, mode, m)
        print(line, flush=True); log.write(line + "\n"); log.flush()

    def run(j):
        t0 = time.time()
        r = core.run(j, by="agent")
        say("ok %.0fs %s" % (time.time() - t0, r["files"]))
        return os.path.join(data, r["files"][0])

    def with_picture(j):
        p = j["prompt"]
        cut = p.find("\n\noverall_soundscape")
        return dict(j, prompt=(p[:cut] + PICTURE + p[cut:]) if cut > 0 else p + PICTURE)

    if mode == "ref2va":
        run(dict(with_picture(job), workflow="wf_h3vid_ref2va_first.json", name=name + "_ref2va_pic"))
        return
    if not pass1:
        pass1 = run(dict(job, name=name + "_p1"))
    raw = pass1.replace(".mp4", "-raw.mp4") if not pass1.endswith("-raw.mp4") and os.path.exists(pass1.replace(".mp4", "-raw.mp4")) else pass1
    adir = os.path.join(data, rnd, "anchors")
    os.makedirs(adir, exist_ok=True)
    anchors = frames_at(raw, anchors_at, adir, name)
    say("anchors %s" % [os.path.basename(p) for p in anchors])
    if mode in ("repair", "refrepair"):
        # Picture 2 = what the object should look like: the job's "ref" picture (e.g. a better keyframe
        # from another seed), else the clip's own keyframe; core.run uploads it
        ref = job.pop("ref", None)
        prompt = job.pop("repair_prompt", None) or REPAIR
        key = os.path.join(data, ref) if ref else job["image"]
        w, h = job.get("width", 768), job.get("height", 1152)
        fixed = []
        if ref:  # the clip must also start from the repaired object
            job["image"] = run({"workflow": "wf_h3img_2ref.json", "image1": job["image"], "image2": key, "prompt": prompt,
                                "width": w, "height": h, "seed": 98001, "round": rnd + "/anchors",
                                "name": name + "_start_fix", "anime_timing": "off"})
        for p in anchors:
            stem = os.path.splitext(os.path.basename(p))[0]
            done = os.path.join(adir, stem + "_fix_00001_.png")
            if mode == "refrepair" and os.path.exists(done):
                fixed.append(done)
                continue
            fixed.append(run({"workflow": "wf_h3img_2ref.json", "image1": p, "image2": key, "prompt": prompt,
                              "width": w, "height": h, "seed": 98001, "round": rnd + "/anchors",
                              "name": stem + "_fix", "anime_timing": "off"}))
        anchors = fixed
    g = {}
    for n, (p, idx) in enumerate(zip(anchors, anchors_at), 1):
        g["g%d" % n] = core.upload_input(p, s)
        g["g%d_idx" % n] = idx
    if mode == "refrepair":
        run(dict(with_picture(job), workflow="wf_h3vid_ref2va_g5.json", name="%s_refrepair" % name, **g))
        return
    run(dict(job, workflow="wf_h3vid_i2v_lora2_g11.json" if dense else "wf_h3vid_i2v_lora2_g5.json",
             name="%s_%s%s" % (name, mode, "_dense" if dense else ""), **g))


if __name__ == "__main__":
    main()
