#!/usr/bin/env python3
"""story.py - a longer animation as a list of shots: one keyframe and one clip (or a chain of clips)
per shot, the same character/partner/setting/style blocks in every shot, each shot re-timed to
its own cadence, then cut together with the audio. docs/STORY.md.

A story file (kit/stories/*.json):
  name, about, ref           - what it is and the reference it follows
  still {...}                - keyframe job defaults (workflow, lora, strength, size, negative)
  clip {...}                 - clip job defaults (size, unet, motion LoRA, fps)
  blocks {...}               - shared text: style, character, partner, setting (keyframe tags) and
                               script_style, script_character, script_partner, script_setting
                               (H3 script prose); used as {name} placeholders in the shots
  seed                       - base seed; shot i uses seed + i unless the shot sets one
  shots [{id, seconds, still, script, template, still_job {...}, clip_job {...}, key_image, start_from, extend, restore, restore_image, restore_prompt, clip_file, clip_range, continues, cut,
          timing: "off"|"on2"|"on3"|"smooth", hold: [{"at": s, "frames": n}], seed}]

Long shots: a clip is at most `max_len` frames; a longer shot continues with more clips, each
starting from the last frame of the one before (`seg_len` frames), the same script.

extend: N (17k+5, use 22) - a `start_from` shot and a long shot's later clips continue the previous clip
as an extension instead of from its last frame: its last N frames are anchored at frame 0 (core.extend_graph),
the clip is N-5 frames longer and the cut drops the N repeated frames. Half the line-art drift of a
single-frame chain; owner (a107): unnoticeable for 2-3 hops, so keep a chain to 3 and hard-cut after.

  expand(story)          -> the round's jobs, in order (keyframes before their clips)
  assemble(story, files, out) -> the cut: shots trimmed to `seconds`, re-timed, joined with hard
                            cuts, the clips' own audio kept in sync
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


RESTORE = ("Edit <Picture 1>. Keep <Picture 1> exactly as it is: the same pose, framing, expression, hands, bodies, "
           "fluids, room and composition. Only redraw it in the exact art style of <Picture 2>: the same thin clean line "
           "art and line weight, the same flat colours and shading, the same crispness.")


def load(path, variant=None):
    """the story, with a named variant applied: story["variants"][name] is an overlay - its
    blocks/still/clip keys replace the story's, `append` adds text to them (e.g. a negative), and
    `shots` {id: {...}} replaces keys of those shots."""
    with open(path, encoding="utf-8-sig") as f:
        S = json.load(f)
    if variant:
        V = S.get("variants", {})[variant]
        for part in ("blocks", "still", "clip"):
            S.setdefault(part, {}).update(V.get(part, {}))
        for part, adds in V.get("append", {}).items():
            for k, txt in adds.items():
                S[part][k] = S[part].get(k, "") + txt
                if part == "still" and k == "negative":
                    for sh in S["shots"]:
                        if "negative" in sh.get("still_job", {}):
                            sh["still_job"]["negative"] += txt
        for sh in S["shots"]:
            sh.update(V.get("shots", {}).get(sh["id"], {}))
        S["name"] = "%s_%s" % (S["name"], variant)
    return S


def fill(text, blocks):
    return re.sub(r"\{(\w+)\}", lambda m: blocks.get(m.group(1), m.group(0)), text or "")


def tidy(tags):
    parts = [p.strip() for p in tags.split(",")]
    return ", ".join(p for p in parts if p)


def segments(story, shot):
    """clip lengths for a shot: the first clip, then continuation clips (each repeats one frame)."""
    c = story.get("clip", {})
    fps, first, more = c.get("fps", 24), c.get("max_len", 124), c.get("seg_len", 49)
    sizes = c.get("lengths", [49, 81, 124])  # the clip lengths the page offers
    need = int(round(shot["seconds"] * fps))
    out = [min([s for s in sizes if s >= need] or [first])]
    out[0] = min(out[0], first)
    have = out[0]
    while have < need:
        out.append(more)
        have += more - 1
    return out


def expand(story):
    B = dict(story.get("blocks", {}))
    jobs = []
    for i, sh in enumerate(story["shots"]):
        seed = sh.get("seed", story.get("seed", 1) + i)
        sid = sh["id"]
        if sh.get("clip_file"):  # an existing clip (path under data_dir), used as it is: nothing to render
            continue
        still = dict(story.get("still", {}))
        still.update(sh.get("still_job", {}))
        prompt = tidy(fill(sh["still"], B))
        still.update(name="%s_key" % sid, seed=seed, prompt=prompt)
        if "late" in still or still.get("workflow", "").startswith("wf_anima2"):
            still["late"] = prompt  # no signature split: the character LoRA carries the identity
        # key_image: a fixed keyframe (e.g. hand-edited, path under data_dir); start_from: "<shot id>" -
        # the shot continues from the last frame of that shot's last clip (no keyframe of its own)
        if not sh.get("key_image") and not sh.get("start_from"):
            jobs.append(still)
        prev = None
        if sh.get("start_from"):
            ref = next(s for s in story["shots"] if s["id"] == sh["start_from"])
            prev = "%s_c%d" % (ref["id"], len(segments(story, ref)) - 1)
        script = fill(sh["script"], B)
        for k, n in enumerate(segments(story, sh)):
            clip = dict(story.get("clip", {}))
            for x in ("fps", "max_len", "seg_len", "extend"):
                clip.pop(x, None)
            clip.update(sh.get("clip_job", {}))
            clip.update(name="%s_c%d" % (sid, k), template=sh.get("template", clip.get("template")), seed=seed,
                        prompt=script, length=n, anime_timing="off")
            ext = sh.get("extend")
            if ext and (prev if k == 0 else True):
                clip.update(video_from=prev if k == 0 else "%s_c%d" % (sid, k - 1), ctx_len=ext, length=n + ext - 5)
            elif k == 0 and prev:
                clip["image_last_from"] = prev
                if sh.get("restore_image"):  # or redraw it toward a given picture with a given instruction
                    clip["restore_path"] = sh["restore_image"]
                    if sh.get("restore_prompt"):
                        clip["restore_prompt"] = sh["restore_prompt"]
                if sh.get("restore"):  # redraw the start frame with that shot's keyframe line art first
                    ref = next(s for s in story["shots"] if s["id"] == sh["restore"])
                    if ref.get("key_image"):
                        clip["restore_path"] = ref["key_image"]
                    else:
                        clip["restore_from"] = "%s_key" % ref["id"]
            elif k == 0 and sh.get("key_image"):
                clip["image_path"] = sh["key_image"]
            elif k == 0:
                clip["image_from"] = "%s_key" % sid
            else:
                clip["image_last_from"] = "%s_c%d" % (sid, k - 1)
            jobs.append(clip)
    return jobs


# ---- the cut ----------------------------------------------------------------------------------
def _read(path):
    import av
    import numpy as np
    with av.open(path) as c:
        vs = c.streams.video[0]
        rate = vs.average_rate
        frames = [f.to_ndarray(format="rgb24") for f in c.decode(vs)]
    audio, arate, layout = None, None, None
    with av.open(path) as c:
        if c.streams.audio:
            a = c.streams.audio[0]
            arate, layout = a.rate, a.layout.name
            rs = av.AudioResampler(format="fltp", layout=layout, rate=arate)
            chunks = []
            for f in c.decode(a):
                for g in rs.resample(f):
                    chunks.append(g.to_ndarray())  # planar float: (channels, samples)
            for g in rs.resample(None):
                chunks.append(g.to_ndarray())
            if chunks:
                audio = np.concatenate(chunks, axis=1).astype("float32")
    return frames, float(rate), audio, arate, layout


def last_frame(path, png):
    import av
    from PIL import Image
    last = None
    with av.open(path) as c:
        for f in c.decode(video=0):
            last = f
    last.to_image().save(png)
    return png


def _shot(story, sh, files, tmpdir):
    """one shot's frames and audio: segments joined (the repeated first frame of a continuation
    dropped), trimmed to `seconds`, re-timed, with its holds."""
    import numpy as np
    import anime_timing as AT
    fps = story.get("clip", {}).get("fps", 24)
    timing = sh.get("timing", "off")
    frames, audio, arate, layout = [], [], None, None
    for k, f in enumerate(files):
        src = f
        if timing == "smooth":
            import anime_smooth
            src = os.path.join(tmpdir, "smooth_%s_%d.mp4" % (sh["id"], k))
            anime_smooth.smooth(f, src)
        fr, rate, au, ar, lay = _read(src)
        if k == 0 and sh.get("clip_range"):  # [first, last] frame of an existing clip
            a, b = sh["clip_range"]
            fr = fr[a:b + 1]
            if au is not None:
                au = au[:, int(round(a * ar / rate)):int(round((b + 1) * ar / rate))]
        # a continuation repeats the frame it starts from: start_from, or "continues" (key_image = the
        # previous shot's last frame)
        drop = 1 if (k or sh.get("start_from") or sh.get("continues")) else 0
        if sh.get("extend") and (k or sh.get("start_from")):
            drop = sh["extend"]  # an extension repeats the previous clip's last `extend` frames
        frames += fr[drop:]
        if au is not None:
            arate, layout = ar, lay
            audio.append(au[:, int(round(drop * ar / rate)):])
    n = min(len(frames), int(round(sh["seconds"] * fps)))
    frames = frames[:n]
    au = np.concatenate(audio, axis=1)[:, :int(round(n * arate / fps))] if audio else None
    on = {"on2": 2, "on3": 3, "on4": 4}.get(timing, 1)
    shown = list(range(n))
    if on > 1:
        keys, shown = AT.schedule(n, on, 0, [])
        shown = AT.pick_sharp(frames, keys, shown)
    for h in sh.get("hold", []):
        a = int(round(h["at"] * fps))
        for o in range(a, min(n, a + h["frames"])):
            shown[o] = shown[a] if a < n else shown[-1]
    return [frames[i] for i in shown], au, arate, layout


def assemble(story, files_by_shot, out, tmpdir):
    """files_by_shot: {shot id: [clip files in order]} -> one mp4 with hard cuts and the audio."""
    import av
    import numpy as np
    fps = story.get("clip", {}).get("fps", 24)
    V, A, arate, layout = [], [], None, None
    for sh in story["shots"]:
        fs = files_by_shot.get(sh["id"])
        if not fs or sh.get("cut") is False:  # cut: false keeps a shot in the story but out of the edit
            continue
        fr, au, ar, lay = _shot(story, sh, fs, tmpdir)
        if V and fr[0].shape != V[0].shape:
            from PIL import Image
            h, w = V[0].shape[:2]
            fr = [np.asarray(Image.fromarray(x).resize((w, h))) for x in fr]
        V += fr
        if au is not None:
            arate, layout = ar, lay
            want = int(round(len(fr) * ar / fps))
            au = au[:, :want] if au.shape[1] >= want else np.pad(au, ((0, 0), (0, want - au.shape[1])))
            A.append(au)
        elif A or arate:
            A.append(np.zeros((A[0].shape[0], int(round(len(fr) * arate / fps))), "float32"))
    h, w = V[0].shape[:2]
    with av.open(out, "w") as o:
        vs = o.add_stream("libx264", rate=fps)
        vs.width, vs.height, vs.pix_fmt = w, h, "yuv420p"
        vs.options = {"crf": "16", "preset": "medium"}
        as_ = o.add_stream("aac", rate=arate) if A else None
        if as_ is not None:
            as_.layout = layout
        for x in V:
            for p in vs.encode(av.VideoFrame.from_ndarray(x, format="rgb24")):
                o.mux(p)
        for p in vs.encode():
            o.mux(p)
        if as_ is not None:
            pcm = np.concatenate(A, axis=1).astype("float32")
            step = 1024
            for i in range(0, pcm.shape[1], step):
                fr = av.AudioFrame.from_ndarray(np.ascontiguousarray(pcm[:, i:i + step]), format="fltp", layout=layout)
                fr.sample_rate = arate
                for p in as_.encode(fr):
                    o.mux(p)
            for p in as_.encode():
                o.mux(p)
    return {"frames": len(V), "seconds": len(V) / fps}
