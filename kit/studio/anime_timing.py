#!/usr/bin/env python3
"""anime_timing.py - re-time a generated clip to hand-drawn TV-anime timing.

H3 draws a new, slightly motion-blurred frame every 1/24 s, which reads as live2d / h-game
motion. Limited TV animation shows fewer, crisp drawings, each held for 2 (or 3) frames with hard
cuts between them, and may freeze on the end of a stroke (the "stopper"). Measured reference and
round a95: docs/ANIME-TIMING.md.

Only picks which source frame is shown at each output frame; every drawing is shown at (or one
frame after) its own time, so the clip keeps its length and the audio stays in sync.

The page applies it after a video finishes (job/template key "anime_timing", see MODES); the
untouched clip is kept next to it as <name>-raw.mp4. By hand:

  python_embeded\\python.exe -I kit/studio/anime_timing.py in.mp4 out.mp4 [--mode on2]
         [--on 2] [--stop 4] [--no-sharp] [--sheet sheet.jpg]

Needs PyAV + numpy (the engine's python_embeded has both).
"""
import argparse, os, sys

# id -> (label, frames per drawing, stopper hold in frames; 0 = none)
MODES = {
    "off": ("off (smooth, as generated)", 1, 0),
    "on2": ("anime: on 2s", 2, 0),
    "on2_stop": ("anime: on 2s + holds at stroke ends", 2, 4),
    "on3_stop": ("anime: on 3s + holds (most limited)", 3, 5),
}


def load(src):
    import av
    with av.open(src) as c:
        s = c.streams.video[0]
        rate = s.average_rate
        frames = [f.to_ndarray(format="rgb24") for f in c.decode(s)]
    return frames, rate


def sharpness(rgb):
    import numpy as np
    g = rgb.mean(2)
    return float(np.abs(4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]).mean())


def motion(frames):
    """per-frame motion energy (mean abs diff to the previous frame, downscaled grey), smoothed."""
    import numpy as np
    small = [f[::8, ::8].mean(2) for f in frames]
    d = np.array([0.0] + [float(np.abs(small[i] - small[i - 1]).mean()) for i in range(1, len(small))])
    k = np.array([1, 2, 3, 2, 1], float)
    k /= k.sum()
    return np.convolve(np.pad(d, 2, mode="edge"), k, mode="valid")


def extremes(m, min_gap=6):
    """frames where the motion slows to a local minimum = the ends of a stroke."""
    out = []
    for i in range(2, len(m) - 2):
        if m[i] <= m[i - 1] and m[i] <= m[i + 1] and m[i] < 0.8 * max(m[max(0, i - 6):i + 7]):
            if not out or i - out[-1] >= min_gap:
                out.append(i)
            elif m[i] < m[out[-1]]:
                out[-1] = i
    return out


def schedule(n, on, stop, ext):
    """drawing start frames, and the source frame index for each output frame."""
    ext = sorted(ext)
    keys, i = [], 0
    while i < n:
        hit = [e for e in ext if i <= e < i + on]
        if stop and hit:
            e = hit[0]
            if e > i:
                keys.append(i)
            keys.append(e)
            i = e + stop
        else:
            keys.append(i)
            i += on
    shown, k = [], 0
    for o in range(n):
        while k + 1 < len(keys) and keys[k + 1] <= o:
            k += 1
        shown.append(keys[k])
    return keys, shown


def pick_sharp(frames, keys, shown):
    """for each drawing, show the sharper of its own frame and the next one (still in its slot)."""
    sharp = {}

    def sh(i):
        if i not in sharp:
            sharp[i] = sharpness(frames[i][::2, ::2])
        return sharp[i]
    best = {}
    for k, k2 in zip(keys, keys[1:] + [len(frames)]):
        cands = [c for c in (k, k + 1) if c < k2 and c < len(frames)]
        best[k] = max(cands, key=sh)
    return [best[s] for s in shown]


def write(frames, idx, rate, src, dst):
    """encode the chosen frames (h264) and copy the source's audio packets unchanged."""
    import av
    h, w = frames[0].shape[:2]
    with av.open(src) as cin, av.open(dst, "w") as out:
        vs = out.add_stream("libx264", rate=rate)
        vs.width, vs.height, vs.pix_fmt = w, h, "yuv420p"
        vs.options = {"crf": "16", "preset": "medium"}
        ain = cin.streams.audio[0] if cin.streams.audio else None
        aout = out.add_stream_from_template(ain) if ain is not None else None
        for i in idx:
            for p in vs.encode(av.VideoFrame.from_ndarray(frames[i], format="rgb24")):
                out.mux(p)
        for p in vs.encode():
            out.mux(p)
        if ain is not None:
            for p in cin.demux(ain):
                if p.dts is None:
                    continue
                p.stream = aout
                out.mux(p)


def retime(src, dst, on=2, stop=0, sharp=True):
    """re-time src into dst; returns a short summary dict."""
    frames, rate = load(src)
    ext = extremes(motion(frames)) if stop else []
    keys, shown = schedule(len(frames), max(1, on), stop, ext)
    if sharp and on > 1:
        shown = pick_sharp(frames, keys, shown)
    write(frames, shown, rate, src, dst)
    return {"frames": len(frames), "drawings": len(set(shown)), "fps": float(rate), "stoppers": ext, "shown": shown,
            "_frames": frames}


def apply_mode(path, mode):
    """page hook: re-time path in place for a MODES id; the untouched clip is kept as <stem>-raw<ext>.
    Returns the raw path, or None when nothing was done."""
    if not mode or mode == "off" or mode not in MODES or not path.lower().endswith((".mp4", ".webm", ".mov")):
        return None
    _, on, stop = MODES[mode]
    stem, ext = os.path.splitext(path)
    raw = stem + "-raw" + ext
    os.replace(path, raw)
    try:
        retime(raw, path, on=on, stop=stop)
    except Exception:
        if os.path.exists(path):
            os.remove(path)
        os.replace(raw, path)
        raise
    return raw


def sheet(frames, idx, path, count=32, cols=8, width=240):
    from PIL import Image, ImageDraw
    h, w = frames[0].shape[:2]
    th = width * h // w
    n = min(count, len(idx))
    out = Image.new("RGB", (width * cols, th * ((n + cols - 1) // cols)))
    for o in range(n):
        im = Image.fromarray(frames[idx[o]]).resize((width, th))
        ImageDraw.Draw(im).text((4, 4), "o%d<-s%d" % (o, idx[o]), fill=(255, 255, 0))
        out.paste(im, ((o % cols) * width, (o // cols) * th))
    out.save(path, quality=85)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--mode", choices=sorted(MODES), help="a page preset (overrides --on/--stop)")
    ap.add_argument("--on", type=int, default=2, help="frames each drawing is held (2 = on twos)")
    ap.add_argument("--stop", type=int, default=0, help="frames a stroke end is held (0 = none)")
    ap.add_argument("--no-sharp", action="store_true")
    ap.add_argument("--sheet")
    a = ap.parse_args()
    on, stop = (MODES[a.mode][1], MODES[a.mode][2]) if a.mode else (a.on, a.stop)
    r = retime(a.src, a.dst, on=on, stop=stop, sharp=not a.no_sharp)
    if a.sheet:
        sheet(r["_frames"], r["shown"], a.sheet)
    print("%s: %d frames, %d drawings (%.1f/s), %d stoppers %s" % (
        os.path.basename(a.dst), r["frames"], r["drawings"], r["drawings"] / (r["frames"] / r["fps"]),
        len(r["stoppers"]), r["stoppers"]))


if __name__ == "__main__":
    sys.exit(main())
