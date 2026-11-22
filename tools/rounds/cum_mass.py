#!/usr/bin/env python3
"""cum_mass.py - a crude mass-conservation meter for cum clips, plus side-by-side frame grids.

Run with the engine's Python (PyAV + PIL):
  python_embeded\\python.exe -I tools/rounds/cum_mass.py OUT_DIR a.mp4 b.mp4 [...] [--times 1,2,3]

Per clip: counts "fluid white" pixels (bright, low saturation) in every frame and subtracts the
count in frame 0 (teeth, highlights and other white things already in the keyframe). New white
that appears in flight and then vanishes is fluid the clip "lost": the meter reports
  peak  - the largest added white area (in flight + landed) in any frame,
  final - the added white area averaged over the last 12 frames (what stayed on her),
  ratio - peak / final. A conserving clip climbs in steps and keeps it (ratio near 1); a clip
          whose in-flight body is bigger than the deposit spikes and drops (ratio well above 1,
          the owner's complaint; >2 is a fail by the CUM-VIDEO.md rule of thumb).
It is a proxy - glare, teeth showing and camera motion move it too - so always look at the frames.
Writes OUT_DIR/mass.txt, a curve per clip, and full-resolution grids side by side at --times.
"""
import os, sys
import av
from PIL import Image, ImageChops, ImageDraw


def frames(path):
    with av.open(path) as c:
        s = c.streams.video[0]
        fps = float(s.average_rate or 24)
        return [f.to_image() for f in c.decode(s)], fps


def white_count(img):
    hsv = img.convert("HSV").resize((img.width // 2, img.height // 2))
    h, s, v = hsv.split()
    m = ImageChops.multiply(v.point(lambda a: 255 if a > 205 else 0), s.point(lambda a: 255 if a < 40 else 0))
    return m.histogram()[255] * 4


def main():
    args = sys.argv[1:]
    times = [1.0, 2.0, 3.0, 4.0, 5.0]
    if "--times" in args:
        i = args.index("--times")
        times = [float(t) for t in args[i + 1].split(",")]
        del args[i:i + 2]
    out, clips = args[0], args[1:]
    os.makedirs(out, exist_ok=True)
    report, grabs = [], []
    for p in clips:
        fr, fps = frames(p)
        base = white_count(fr[0])
        curve = [white_count(f) - base for f in fr]
        tail = curve[-12:]
        final = max(1, sum(tail) / len(tail))
        peak = max(curve)
        name = os.path.basename(p).rsplit("_0000", 1)[0]
        step = max(1, int(fps / 4))
        report.append("%-22s peak %7d  final %7d  ratio %.2f\n  curve/0.25s: %s" % (
            name, peak, final, peak / final, " ".join(str(c // 100) for c in curve[::step])))
        grabs.append((name, [fr[min(len(fr) - 1, int(t * fps))] for t in times]))
    open(os.path.join(out, "mass.txt"), "w").write("\n".join(report) + "\n")
    print("\n".join(report))
    # one grid per time: all clips side by side at full resolution
    for ti, t in enumerate(times):
        ims = [g[1][ti] for g in grabs]
        W = sum(i.width for i in ims)
        H = max(i.height for i in ims) + 28
        sheet = Image.new("RGB", (W, H), "black")
        d = ImageDraw.Draw(sheet)
        x = 0
        for (name, _), im in zip(grabs, ims):
            sheet.paste(im, (x, 28))
            d.text((x + 6, 6), "%s  t=%.2fs" % (name, t), fill="white")
            x += im.width
        sheet.save(os.path.join(out, "t%04.2f.jpg" % t), quality=90)


if __name__ == "__main__":
    main()
