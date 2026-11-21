#!/usr/bin/env python3
"""mixed_compose.py - put the real cock shaft into the golden anime blowjob still.

Keeps the whole j2_suction composition (face, lips, breasts, the sealed mouth); replaces only the
visible anime shaft with the real photoreal shaft, and puts the original lip ring back on top so
the joint is hidden. The glans stays inside her mouth, exactly as in the golden still.
"""
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

BASE = "gens/a11/j2_suction_seal_a_00001_.png"
CUT = "analysis/mixed/cock_birefnet.png"
OUT = "analysis/mixed/mix_j2_real.png"

base = Image.open(BASE).convert("RGB")
cut = Image.open(CUT).convert("RGBA")

# shaft only: drop the glans (top) and the hairy base (bottom); keep the middle of the shaft
shaft = cut.crop((180, 380, 740, 1850))
tw = 165
th = int(shaft.height * tw / shaft.width)
shaft = shaft.resize((tw, th), Image.LANCZOS)

# match the warm anime light a little
rgb = shaft.convert("RGB")
rgb = ImageEnhance.Brightness(rgb).enhance(1.08)
rgb = ImageEnhance.Color(rgb).enhance(1.05)
shaft = Image.merge("RGBA", (*rgb.split(), shaft.split()[-1]))

x = 360
y = 775
comp = base.copy()
comp.paste(shaft, (x, y), shaft)

# put the anime lip ring back on top so the shaft joint is under the lips
lips = base.crop((340, 720, 545, 815))
lm = Image.new("L", lips.size, 0)
d = ImageDraw.Draw(lm)
d.ellipse((10, 8, lips.width - 10, lips.height - 8), fill=255)
lm = lm.filter(ImageFilter.GaussianBlur(6))
comp.paste(lips, (340, 720), lm)
comp.save(OUT)
print("wrote", OUT)

prev = comp.copy()
prev.thumbnail((700, 1050))
prev.save("analysis/mixed/mix_j2_real_preview.jpg")
print("wrote preview")
