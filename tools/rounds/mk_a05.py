#!/usr/bin/env python3
"""mk_a05.py - the paizuri / wide / cum poses in the three signature styles the owner liked."""
import json

CHAR = ("1girl, 1boy, hetero, pov, from above, looking up at viewer, "
        "short silver hair, single braid, purple eyes, jitome, mole under eye, fang, ahoge, hair intakes")
BODY = "(curvy:1.6), (wide hips:1.4), thick thighs, large breasts, mature female, half-closed eyes, blush, saliva"

PAZ = ("paizuri, titjob, (breasts around penis:1.3), (penis between breasts:1.3), (glans above cleavage:1.2), "
       "detailed penis shaft, veins, uncensored, (penis focus:1.2), she presses her large breasts together with "
       "both hands, (tongue out:1.2) touching the glans, bedroom, soft light")
WIDE = ("cock out, (penis:1.2), detailed penis shaft, veins, defined glans, corona rim, uncensored, "
        "(penis focus:1.2), she holds his cock low between his thighs at the bottom of the frame, the tip a hand's "
        "width below her chin, head tilted down, (mouth wide open:1.2), tongue out, (eyes rolled up to viewer:1.15), "
        "bedroom, soft light")
CUM = ("cock out, (penis:1.1), detailed penis shaft, veins, uncensored, (penis focus:1.1), "
       "(cum on face:1.3), (cum on tongue:1.2), (cum on lips:1.2), thin white ropes of semen, glossy, "
       "(cum drip:1.2), (mouth open:1.2), tongue out, (cum across cheek:1.1), bedroom, soft light")

NEG = ("extra hands, extra fingers, third hand, bad anatomy, fused limbs, extra limbs, male body, censored, "
       "mosaic censoring, bar censor, long strand from mouth to cock, cum string, tears, worst quality, low quality, "
       "score_1, score_2, score_3, blurry, jpeg artifacts, watermark, text, 3d, realistic")

EARLY = "masterpiece, best quality, year 2016, anime screenshot, {char}, @murota yuuhei{artist}, {body}, {scene}"
LATE = ("masterpiece, best quality, year 2016, anime screenshot, love live! sunshine!!, {char}, @murota yuuhei{artist}, "
        "{body}, {scene}")

specs = [
    ("e2_fz_paizuri", ", @fuzichoco", PAZ),
    ("e2_kt_paizuri", ", @kantoku", PAZ),
    ("e2_sig_paizuri", "", PAZ),
    ("e2_fz_wide", ", @fuzichoco", WIDE),
    ("e2_fz_cum", ", @fuzichoco", CUM),
]
jobs = []
for i, (name, artist, pose) in enumerate(specs):
    jobs.append({
        "name": name,
        "wf": "wf_anima2_sig.json",
        "unet": "ramthrustsNSFWPINK_v29.safetensors",
        "width": 832, "height": 1248, "steps": 30, "cfg": 4.0,
        "sampler": "er_sde", "sched": "simple", "seed": 86001 + i,
        "prompt": EARLY.format(char=CHAR, artist=artist, body=BODY, scene=pose),
        "late": LATE.format(char=CHAR.replace("purple eyes", "(purple eyes:1.3)"), artist=artist, body=BODY, scene=pose),
        "negative": NEG,
    })

with open("jobs/a05_sig_poses.jsonl", "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote jobs/a05_sig_poses.jsonl:", len(jobs), "jobs")
