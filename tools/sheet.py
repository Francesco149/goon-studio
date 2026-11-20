#!/usr/bin/env python3
"""sheet.py - contact sheet of one or more round folders, labelled, for judging at a glance.

  python sheet.py out.jpg gens/g01 gens/g01b [--cols 4] [--thumb 420]

Pictures are labelled with round/name; videos are shown as three frames side by side.
"""
import argparse
import glob
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("dirs", nargs="+")
ap.add_argument("--cols", type=int, default=4)
ap.add_argument("--thumb", type=int, default=420)
a = ap.parse_args()


def font(sz):
    for n in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(n, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def frames_of(path, n=3):
    d = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-vf",
                    "select='eq(n\\,30)+eq(n\\,62)+eq(n\\,94)',scale=440:-1,tile=3x1",
                    "-vframes", "1", os.path.join(d, "s.jpg")], check=False)
    p = os.path.join(d, "s.jpg")
    return p if os.path.exists(p) else None


tiles = []
for d in a.dirs:
    round_name = os.path.basename(os.path.normpath(d))
    for f in sorted(glob.glob(os.path.join(d, "*"))):
        ext = f.lower().rsplit(".", 1)[-1]
        if ext in ("png", "jpg", "jpeg", "webp"):
            tiles.append((f, "%s/%s" % (round_name, os.path.basename(f)[:-4])))
        elif ext in ("mp4", "webm"):
            s = frames_of(f)
            if s:
                tiles.append((s, "%s/%s (3 frames)" % (round_name, os.path.basename(f)[:-4])))

if not tiles:
    sys.exit("nothing to show")

tw = a.thumb
th = int(tw * 1.5)
lab = 30
cols = a.cols
rows = (len(tiles) + cols - 1) // cols
out = Image.new("RGB", (cols * tw, rows * (th + lab)), (18, 18, 18))
dr = ImageDraw.Draw(out)
f = font(15)
for i, (path, name) in enumerate(tiles):
    im = Image.open(path).convert("RGB")
    im.thumbnail((tw - 6, th - 6), Image.Resampling.LANCZOS)
    x, y = (i % cols) * tw, (i // cols) * (th + lab)
    out.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
    dr.text((x + 4, y + th + 6), name[:52], fill=(235, 235, 235), font=f)
out.save(a.out, quality=90)
print(a.out, out.size, len(tiles), "tiles")
