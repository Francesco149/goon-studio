#!/usr/bin/env python3
"""mk_a93b.py - round a93b: anime cum shot, seed luck vs keyframe vs wording.

Owner on the a93 anime t4 pair: the saliva reads well, the cum shot does not feel natural - only
two ropes visibly stay on her face and they go across in a weird circular way, as if the spray
swept from side to side, abnormally symmetrical. "Needs more attempts and maybe a couple of
different starting frames to see if it's just an unlucky seed."

So: the anime_ll_cumshot template as is, unchanged wording,
  - on the same keyframe (tongue on the tip) with two new seeds  -> is it seed luck?
  - on two gap keyframes (tip below an open mouth, like the photoreal p1 pose)  -> keyframe?
and one wording variant on the gap keyframe: the template's landing sentence assigns the three
ropes to cheek / tongue / chin, which may be what sweeps the spray across her face, so the
variant lands them unevenly in about the same place and forbids the side-to-side sweep.
No physics paragraph (a93: unnatural), no glans-rigidity paragraph (a89).
Writes jobs/a93b_anime_cum.jsonl.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = json.load(open(os.path.join(ROOT, "kit", "presets.json"), encoding="utf-8"))["video_templates"]
t4 = P["anime_ll_cumshot"]["prompt"]

FZ = "gens/a04/e1_fuzichoco_cockout_00001_.png"
HB = "gens/a30/n1_handjob_b_00001_.png"
HA = "gens/a30/n1_handjob_a_00001_.png"

OLD = ("The first rope lands high on her cheek and stays; the second lands on her tongue and lower lip "
       "and stays; the third lands on her chin and drips down her jaw. The ropes are thin and short; "
       "each one ends where it hits and does not lie across her face.")
assert OLD in t4
NEW = ("The ropes land one after another in roughly the same place, a little to one side of her "
       "mouth, unevenly: the first across her lips and up onto one cheek, the second shorter onto "
       "her tongue, the third only a small dribble onto her lower lip. They do not sweep from side "
       "to side and they do not make a symmetrical pattern; each one ends where it hits and stays, "
       "and the white on her face is uneven and lopsided.")
t4_one_side = t4.replace(OLD, NEW)

T = "anime_ll_cumshot"
jobs = [
    dict(name="fz_s93101", template=T, seed=93101, image=FZ, _note="same keyframe, new seed"),
    dict(name="fz_s93102", template=T, seed=93102, image=FZ, _note="same keyframe, new seed"),
    dict(name="hb_s93001", template=T, seed=93001, image=HB, _note="gap keyframe b, a93 seed"),
    dict(name="hb_s93101", template=T, seed=93101, image=HB, _note="gap keyframe b, new seed"),
    dict(name="ha_s93001", template=T, seed=93001, image=HA, _note="gap keyframe a, a93 seed"),
    dict(name="hb_oneside", template=T, seed=93001, image=HB, prompt=t4_one_side, _note="gap b + ropes land unevenly in one place, no side-to-side sweep"),
]
out = os.path.join(ROOT, "jobs", "a93b_anime_cum.jsonl")
with open(out, "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote", out, len(jobs))
