#!/usr/bin/env python3
"""mixed_prep.py - crop + BiRefNet-mask + canvas for the mixed-reality still.

Inputs are the source photo and the foreground mask that ComfyUI's RemoveBackground produced
(workflows/wf_bgremove.json). The crop matters: on the full frame BiRefNet picks the anime figure
on the screen as the salient object; cropped to the cock it picks the cock.

  python tools/mixed_prep.py <source> <mask.png> out_cut.png out_canvas.png
"""
import sys

from PIL import Image

# the cock region of the supplied photo; full frame -> BiRefNet picks the screen girl instead
CROP = (0, 650, 950, 2950)
CANVAS = (896, 1344)
TARGET_H = 1150
PLACE = (180, 90)

src = Image.open(sys.argv[1]).convert("RGB").crop(CROP)
mask = Image.open(sys.argv[2]).convert("L").resize(src.size)
cut = src.convert("RGBA")
cut.putalpha(mask)
cut.save(sys.argv[3])

bb = cut.getbbox()
cock = cut.crop(bb)
th = TARGET_H
tw = max(1, int(cock.width * th / cock.height))
cock = cock.resize((tw, th), Image.LANCZOS)
canvas = Image.new("RGB", CANVAS, (24, 20, 28))
canvas.paste(cock, PLACE, cock)
canvas.save(sys.argv[4])
print("cut", bb, "->", tw, th, "canvas", CANVAS)
