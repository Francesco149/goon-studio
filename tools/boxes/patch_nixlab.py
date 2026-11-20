#!/usr/bin/env python3
"""Insert the 2026-11-20 round pointers into MODEL-NOTES.md (idempotent)."""
import io
import sys

P = "/opt/src/nix-lab/research/local-gen/MODEL-NOTES.md"
VID = """**Small detailed parts: name them, hold them, keep the resolution (round 2026-11-20, ampere + cutestation).**
A small, highly structured part of the frame is drawn as a smooth generic shape unless the prompt enumerates its parts and
says the shape persists (`a defined <part> with a clear rim, a ridge, visible lines ... and it keeps that shape for the whole
shot`) - the same lever as the baguette bite in `research/object-anchor`. A clip cannot keep detail the keyframe had at a
higher resolution: i2v from an 896x1344 keyframe at 512x768 loses it, at 768x1152 keeps it; t2v at the same size is sharper
than i2v, but the face drifts across 5 s, while i2v holds the face and softens the small parts. A part that lands on the
wrong side of another is a depth-order problem: give the order along the camera axis as a nearest-to-furthest list and say
what occludes what - ambiguous words like `below` mean "lower in the picture", which for a top-down camera is *towards the
viewer*. Details, prompts and the A/B: `ROUND-2026-11-20-detail-and-order.md`.

"""
IMG = """**Willingness is not uniform across models - probe first** (round 2026-11-20): the same detailed prompt on four image
models - H3-Image drew all of it cleanly (17-27 s on ampere), Qwen-Image-2.1 the most detail with a looser layout, Anima
Aesthetic softened it (36-40 s on cutestation), and **Krea 2 Turbo dropped the detail entirely and changed the composition**
(45 s). A model's speed and general quality say nothing about whether it will draw a specific hard detail; probe the one
prompt on each candidate before building the chain. `ROUND-2026-11-20-detail-and-order.md` section 6.

"""
MARK = "ROUND-2026-11-20-detail-and-order.md"

t = io.open(P, encoding="utf-8").read()
if MARK in t:
    print("already patched")
    sys.exit(0)

if "## Image/multiview to 3D" not in t:
    sys.exit("no anchor for the video block")
t = t.replace("## Image/multiview to 3D", VID + "## Image/multiview to 3D", 1)

anchor = "## P-H3-Image (LoRA on the H3 video DiT, 8 steps)"
if anchor not in t:
    sys.exit("no anchor for the image block")
t = t.replace(anchor, IMG + anchor, 1)

io.open(P, "w", encoding="utf-8").write(t)
print("patched", P)

