#!/usr/bin/env python3
"""mk_a93d.py - round a93d: bigger loads on the a93b winner.

Owner on a93b: hb_oneside (gap keyframe n1_handjob_b, seed 93001, the ropes land unevenly in one
place, no side-to-side sweep) is "the most natural one yet" - it is now the anime_ll_cumshot
template. Earlier: fz_s93102 is a more organic base for bigger loads (more ropes, more strength),
and the rope thickness is already borderline too thick - do not increase it.

a93c builds bigger loads on the OLD landing plan (cheek/tongue/chin, which drew the symmetric
mask). This round builds them on the new wording instead:
  os5          hb + seed 93001, five pulses landing unevenly in one place, thin
  os5_lora65   the same + epic 0.65
  fz_os        the new template wording on the organic fuzichoco seed 93102 (does the wording
               carry to the other keyframe?)
Writes jobs/a93d_oneside_bigload.jsonl.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = json.load(open(os.path.join(ROOT, "kit", "presets.json"), encoding="utf-8"))["video_templates"]
os1 = P["anime_ll_cumshot"]["prompt"]
FZ = "gens/a04/e1_fuzichoco_cockout_00001_.png"
HB = "gens/a30/n1_handjob_b_00001_.png"


def sub(text, old, new):
    assert old in text, old[:60]
    return text.replace(old, new)


OLD = ("The ropes land one after another in roughly the same place, a little to one side of her "
       "mouth, unevenly: the first across her lips and up onto one cheek, the second shorter onto "
       "her tongue, the third only a small dribble onto her lower lip.")
NEW = ("The ropes land one after another in roughly the same place, a little to one side of her "
       "mouth, unevenly: the first two fire hard, across her lips and up onto one cheek, the third "
       "and fourth shorter onto her tongue and the corner of her lips, the fifth only a small "
       "dribble onto her lower lip. Every rope is as thin as before; the load is bigger only "
       "because there are more ropes.")
os5 = sub(os1, OLD, NEW)
os5 = sub(os5, "His cock pulses three times and no more.", "His cock pulses five times and no more.")
os5 = sub(os5, "Three small bobs, one per spurt,", "Five small bobs, one per spurt,")

T = "anime_ll_cumshot"
jobs = [
    dict(name="os5", template=T, seed=93001, image=HB, prompt=os5, _note="five pulses, uneven one-side landing, thin"),
    dict(name="os5_lora65", template=T, seed=93001, image=HB, prompt=os5, nsfw_strength=0.65, _note="the same + epic 0.65"),
    dict(name="fz_os", template=T, seed=93102, image=FZ, _note="the new template on the organic fuzichoco seed"),
]
out = os.path.join(ROOT, "jobs", "a93d_oneside_bigload.jsonl")
with open(out, "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote", out, len(jobs))
