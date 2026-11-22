#!/usr/bin/env python3
"""mk_a93d.py - round a93d: bigger loads on the a93b winner.

Owner on a93b: hb_oneside (gap keyframe n1_handjob_b, seed 93001, the ropes land unevenly in one
place, no side-to-side sweep) is "the most natural one yet" - it is now the anime_ll_cumshot
template. Earlier: fz_s93102 is a more organic base for bigger loads (more ropes, more strength),
and the rope thickness is already borderline too thick - do not increase it.

Owner on a93c (five/four pulses): not good - more pulses only make the ropes shoot for longer,
which is unnatural pacing, and paint abnormally regular patterns on her face that do not match
the spurts. So no extra pulses and no thicker ropes; a bigger load can only come from force:
  os3_hard     hb + seed 93001, still three pulses, the first two fire harder and reach further
               up her cheek, thin
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
       "mouth, unevenly: the first fires hard and lands across her lips and high up onto one "
       "cheek, the second also hard and a little shorter, onto her tongue and the same cheek, the "
       "third only a small dribble onto her lower lip. The ropes stay thin; only the first two "
       "hit harder.")
os3 = sub(os1, OLD, NEW)

T = "anime_ll_cumshot"
jobs = [
    dict(name="os3_hard", template=T, seed=93001, image=HB, prompt=os3, _note="three pulses, first two harder, thin"),
    dict(name="fz_os", template=T, seed=93102, image=FZ, _note="the new template on the organic fuzichoco seed"),
]
out = os.path.join(ROOT, "jobs", "a93d_oneside_bigload.jsonl")
with open(out, "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote", out, len(jobs))
