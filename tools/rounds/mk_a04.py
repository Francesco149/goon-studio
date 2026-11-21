#!/usr/bin/env python3
"""mk_a04.py - Love Live signature-style keyframes for the anime recreations.

Uses the signature trick from ../lovelive-studio (show name only in the last 30% of the steps,
eye colour weighted up in the late prompt), the designer tag, an optional second artist tag from
the tested blends, and face features so the face is not the generic AI anime face.
"""
import json

CHAR = ("1girl, 1boy, hetero, pov, from above, looking up at viewer, "
        "short silver hair, single braid, purple eyes, jitome, mole under eye, fang, ahoge, hair intakes")
BODY = "(curvy:1.6), (wide hips:1.4), thick thighs, large breasts, mature female, half-closed eyes, blush, saliva"
SCENE = ("cock out, (penis:1.2), (erection:1.1), detailed penis shaft, veins, defined glans, corona rim, uncensored, "
         "(penis focus:1.2), she holds his cock upright with one hand, the tip an inch below her open mouth, "
         "(mouth open:1.2), tongue out, bedroom, soft light")

NEG = ("extra hands, extra fingers, third hand, bad anatomy, fused limbs, extra limbs, male body, censored, "
       "mosaic censoring, bar censor, cum, worst quality, low quality, score_1, score_2, score_3, blurry, "
       "jpeg artifacts, watermark, text, 3d, realistic")

EARLY = "masterpiece, best quality, year 2016, anime screenshot, {char}, @murota yuuhei{artist}, {body}, {scene}"
LATE = ("masterpiece, best quality, year 2016, anime screenshot, love live! sunshine!!, {char}, @murota yuuhei{artist}, "
        "{body}, {scene}")

styles = [
    ("sig", "", "ll_signature: designer tag only, signature trick"),
    ("kantoku", ", @kantoku", "ll_soft: @kantoku blend (softer, more detail)"),
    ("fuzichoco", ", @fuzichoco", "ll_watercolor: @fuzichoco blend (pale, painted)"),
    ("ikeda", ", @ikeda kazumi", "KyoAni-like blend (untested by the guide)"),
    ("mignon", ", @mignon", "thick-soft blend (untested by the guide)"),
]
jobs = []
for i, (name, artist, why) in enumerate(styles):
    jobs.append({
        "name": "e1_" + name + "_cockout",
        "wf": "wf_anima2_sig.json",
        "unet": "ramthrustsNSFWPINK_v29.safetensors",
        "width": 832, "height": 1248, "steps": 30, "cfg": 4.0,
        "sampler": "er_sde", "sched": "simple", "seed": 85001 + i,
        "prompt": EARLY.format(char=CHAR, artist=artist, body=BODY, scene=SCENE),
        "late": LATE.format(char=CHAR.replace("purple eyes", "(purple eyes:1.3)"), artist=artist, body=BODY, scene=SCENE),
        "negative": NEG,
        "_why": why,
    })

jobs.append({
    "name": "e1_90s_cockout",
    "wf": "wf_anima2.json",
    "unet": "ramthrustsNSFWPINK_v29.safetensors",
    "width": 832, "height": 1248, "steps": 30, "cfg": 4.0,
    "sampler": "er_sde", "sched": "simple", "seed": 85010,
    "prompt": ("masterpiece, best quality, year 1995, (retro artstyle:1.4), (1990s (style):1.5), "
               + CHAR + ", (@murota yuuhei:0.6), " + BODY + ", " + SCENE),
    "negative": NEG,
    "_why": "ll_90s: 90s TV anime",
})

with open("jobs/a04_sig.jsonl", "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote jobs/a04_sig.jsonl:", len(jobs), "jobs")
