"""Generate jobs/k02_stills.jsonl - the keyframe study for the cum shot (Krea2, local box).

Why stills first: H3 preserves its keyframe (docs/CUM-VIDEO.md), and the still model is the one
that has the approved cum material. Every failed video so far started from a keyframe with no
cum in it and asked the video model to invent the whole event. So the cheapest place to test
the *shape vocabulary* is the still model, at ~10 s a picture instead of ~2.5 min a clip.

Four keyframes, all at 896x1344 (exactly 2:3, so the video workflow's centre crop is a no-op):

  k2a  clean wide-gap cum pose   - the cock held ~6 in below her open mouth instead of 1 in.
                                    At the old gap the spurt has nowhere to travel, so all the
                                    model can draw is a connector from tip to face.
  k2b  detached mid-air blob     - tests whether the bolus shape survives on its own.
  k2c  bolus + short tail        - the ejaculate as a dense leading body with a thin tail, the
                                    shape the Gemini study describes (2.3), against the uniform
                                    "rope" H3 has been drawing.
  k2d  landed, wide gap          - the approved landed material (pool + heavy drip, clean tip)
                                    in the wider-gap pose.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k02_stills.jsonl"))

CHAR = ("a young adult Asian woman in her mid-twenties, e-girl with long black hair in "
        "pink-streaked twin tails, wispy bangs, winged eyeliner, glossy lips and a silver heart "
        "choker, full natural breasts")

POSE = (CHAR + ", kneels between the viewer's legs. She has pulled his erect adult penis out of "
        "her mouth and holds it in her hand low between his thighs, the glans pointing up at her "
        "face from about six inches below her open mouth; her head is tilted down, her mouth is "
        "wide open with her tongue out, her lips wet, her eyes rolled up to the lens, half-lidded, "
        "a light blush.")

LIGHT = (" Dim bedroom with pink LED glow, phone flash, natural skin with pores, slight grain, "
         "amateur photo.")

STILLS = [
    ("k2a_gap_clean", "Photorealistic first-person POV close-up: " + POSE + LIGHT),
    ("k2b_air_blob", "Photorealistic first-person POV close-up: " + POSE +
     " A single dense rounded blob of thick milky semen floats in the air three inches above the "
     "tip of his cock, alone and separate from the tip, glossy milky white with bright specular "
     "highlights, one tiny satellite droplet beside it. The tip of his cock is clean." + LIGHT),
    ("k2c_bolus_tail", "Photorealistic first-person POV close-up: " + POSE +
     " A dense rounded bolus of thick milky semen hangs in the air two inches above the tip, "
     "connected to the tip by one short thin milky tail; the bolus itself is round, heavy and "
     "opaque white, a few separate droplets break off ahead of it and float above her mouth. "
     "The shaft is swollen, the veins standing out." + LIGHT),
    ("k2d_landed_wide", "Photorealistic first-person POV close-up: " + POSE +
     " Thick milky semen sits pooled on her tongue and lower lip in glossy milky patches, the "
     "skin visible through it, a heavy slow drip hanging from her chin; the tip of his cock is "
     "clean and separate far below her face." + LIGHT),
]

rows = []
for i, (name, prompt) in enumerate(STILLS):
    rows.append({
        "name": name,
        "wf": "wf_krea2_nsfw_8gb.json",
        "width": 896,
        "height": 1344,
        "steps": 6,
        "cfg": 1.0,
        "seed": 610 + i,
        "prompt": prompt,
    })

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "stills")
