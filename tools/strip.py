"""Filmstrip: consecutive frames in rows, with the frame index, to read motion.

usage: python strip.py <dir> <out.jpg> <start> <count> [cols] [thumb_w]
"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

d, out_path, start, count = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 6
tw = int(sys.argv[6]) if len(sys.argv) > 6 else 400

frames = sorted(glob.glob(os.path.join(d, "*.jpg")))[start - 1:start - 1 + count]
if not frames:
    sys.exit("no frames")
try:
    font = ImageFont.truetype("arialbd.ttf", 22)
except OSError:
    font = ImageFont.load_default()

thumbs = []
for f in frames:
    im = Image.open(f).convert("RGB")
    im = im.resize((tw, int(round(im.height * tw / im.width))), Image.Resampling.LANCZOS)
    thumbs.append((im, os.path.basename(f).replace(".jpg", "").replace("d_", "")))
tw_, th = thumbs[0][0].size
lab = 26
rows = (len(thumbs) + cols - 1) // cols
img = Image.new("RGB", (cols * tw_, rows * (th + lab)), (14, 14, 14))
dr = ImageDraw.Draw(img)
for i, (im, name) in enumerate(thumbs):
    x, y = (i % cols) * tw_, (i // cols) * (th + lab)
    img.paste(im, (x, y))
    dr.text((x + 4, y + th + 2), name, fill=(235, 235, 235), font=font)
img.save(out_path, quality=90)
print(out_path, img.size, len(thumbs))
