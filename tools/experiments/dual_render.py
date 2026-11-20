"""Dual-render material transfer: keep the rope/motion of clip A, take the cum texture of clip B.

A and B must be rendered with the same keyframe, prompt family, LoRA and seed, differing only in
the LoRA strength/prompt that controls the fluid. The cum mask is found in A (bright, low
saturation, inside the lower-face ROI), feathered, and B's pixels are composited through it.
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

A, B, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
TMP = os.path.join(os.path.dirname(OUT), "_dual")
fa, fb, fo = (os.path.join(TMP, d) for d in ("a", "b", "o"))
for d in (fa, fb, fo):
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))

for src, dst in ((A, fa), (B, fb)):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-fps_mode", "passthrough",
                    "-start_number", "0", os.path.join(dst, "f%03d.png")], check=True)

names = sorted(os.listdir(fa))
n = 0
for name in names:
    pa, pb = os.path.join(fa, name), os.path.join(fb, name)
    if not os.path.exists(pb):
        continue
    a = np.asarray(Image.open(pa).convert("RGB"), dtype=np.float32)
    b = np.asarray(Image.open(pb).convert("RGB"), dtype=np.float32)
    h, w, _ = a.shape
    # ROI: lower half of the face / mouth / chin
    roi = np.zeros((h, w), dtype=bool)
    roi[int(h * 0.18):int(h * 0.58), int(w * 0.20):int(w * 0.78)] = True
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    mask = (mn > 145) & ((mx - mn) < 40) & roi
    m = Image.fromarray((mask * 255).astype(np.uint8), "L")
    m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(3))
    alpha = (np.asarray(m, dtype=np.float32) / 255.0)[..., None]
    out = a * (1 - alpha) + b * alpha
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(os.path.join(fo, name))
    n += 1

subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "24", "-i", os.path.join(fo, "f%03d.png"),
                "-i", A, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-crf", "18", "-c:a", "copy", OUT], check=True)
print("frames", n, "->", OUT)
