#!/usr/bin/env python3
"""mk_a93c.py - round a93c: bigger anime loads from the organic a93b seed.

Owner on a93b: fz_s93102 (anime_ll_cumshot, fuzichoco keyframe, seed 93102) has a more organic
pattern - use it as the base for bigger loads: more ropes and more strength. The ropes are
already borderline too thick, so do not make them thicker. hb_s93001 (gap keyframe n1_handjob_b)
has the nicer POV and expression but draws symmetrical arches.

Same keyframe + seed 93102 throughout; the load grows by the number of ropes and how hard they
fire, with the thickness pinned to "as thin as before". Changing the prompt reshuffles the
noise, so the organic pattern is not guaranteed to survive - that is what this round checks.
  big5        five pulses, wording only
  big5_lora65 five pulses + epic LoRA 0.65 (more strength from the LoRA side)
  big4_hard   four pulses, the first two fire hard, wording only
  hb_lora45   the gap keyframe at epic 0.45, template wording: does a weaker LoRA drop the arches?
Writes jobs/a93c_anime_bigload.jsonl.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = json.load(open(os.path.join(ROOT, "kit", "presets.json"), encoding="utf-8"))["video_templates"]
t4 = P["anime_ll_cumshot"]["prompt"]
FZ = "gens/a04/e1_fuzichoco_cockout_00001_.png"
HB = "gens/a30/n1_handjob_b_00001_.png"


def sub(text, old, new):
    assert old in text, old[:60]
    return text.replace(old, new)


LAND = ("The first rope lands high on her cheek and stays; the second lands on her tongue and lower lip "
        "and stays; the third lands on her chin and drips down her jaw. The ropes are thin and short; "
        "each one ends where it hits and does not lie across her face.")
THIN = " Every rope is as thin as before; the load is bigger only because there are more ropes."


def n_pulses(text, n_word, count_word, land):
    text = sub(text, "His cock pulses three times and no more.", "His cock pulses %s times and no more." % n_word)
    text = sub(text, "Three small bobs, one per spurt,", "%s small bobs, one per spurt," % count_word)
    return sub(text, LAND, land + THIN)


big5 = n_pulses(t4, "five", "Five",
    "The first rope lands high on her cheek and stays; the second lands across the side of her nose; "
    "the third lands on her tongue and lower lip; the fourth lands on her chin and drips down her jaw; "
    "the fifth is weak and only dribbles onto her lower lip. Each one ends where it hits and stays, "
    "and they pile up unevenly instead of lying across her face.")
big4_hard = n_pulses(t4, "four", "Four",
    "The first two pulses fire hard: the first rope lands high on her cheek and the second across the "
    "side of her nose, and both stay; the third lands on her tongue and lower lip; the fourth is weak "
    "and lands on her chin and drips down her jaw. Each one ends where it hits and stays, and they "
    "pile up unevenly instead of lying across her face.")

T = "anime_ll_cumshot"
jobs = [
    dict(name="big5", template=T, seed=93102, image=FZ, prompt=big5, _note="five pulses, thin"),
    dict(name="big5_lora65", template=T, seed=93102, image=FZ, prompt=big5, nsfw_strength=0.65, _note="five pulses, epic 0.65"),
    dict(name="big4_hard", template=T, seed=93102, image=FZ, prompt=big4_hard, _note="four pulses, first two hard"),
    dict(name="hb_lora45", template=T, seed=93001, image=HB, nsfw_strength=0.45, _note="gap keyframe, epic 0.45, template wording"),
]
out = os.path.join(ROOT, "jobs", "a93c_anime_bigload.jsonl")
with open(out, "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote", out, len(jobs))
