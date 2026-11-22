#!/usr/bin/env python3
"""mk_a93.py - round a93: cum physics in the H3 clips (open item 1).

Owner complaints, recurring: (1) far more lands/splashes than one rope can carry (mass
conservation), (2) a spurt fires on one arc and then lands much lower than that arc implies,
(3) the physics overall reads unnatural.

Method: keep every template's keyframe + seed, and replace only the emission/landing sentences
with a script that spells the physics out (docs/ART-STUDY.md 4, 5, 8.2, 8.3):
  - a fixed per-spurt volume that is the same in flight and on landing ("the patch it leaves is
    exactly as big as the rope was"), decaying spurt to spurt;
  - a short shallow arc that lands where it points (the patch appears where the rope hit, not
    below it);
  - the cadence: second spurt ~1 s after the first, third ~1.5 s after that, weaker each time,
    the last one only wells out and drops;
  - recoil: a few-degree kick per spurt and spring back (photoreal only - in anime the 10 degree
    kick read as expansion in t1, so the anime clips keep their t4 bob);
  - impact by viscosity (medium: a raised glossy bead with a rounded edge, two or three tiny
    droplets on the strongest one only).
NOT used: the glans-rigidity paragraph (removed the cum in a89) and the meatus-flare wording
(drew the slit as a hole in anime t3).

Each variant has a same-engine baseline re-render (the old renders were made on another box).
Writes jobs/a93_cum_physics.jsonl.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = json.load(open(os.path.join(ROOT, "kit", "presets.json"), encoding="utf-8"))["video_templates"]

P1 = "gallery/refs/cumshot/p1_pose.png"
FZ = "gens/a04/e1_fuzichoco_cockout_00001_.png"


def sub(text, old, new):
    assert old in text, old[:60]
    return text.replace(old, new)


# ---- photoreal medium (k16_medium: p1_pose, seed 970) ----
med = P["cumshot_medium"]["prompt"]
MED_OLD = med[med.index("His cock pulses three times"):med.index(" His glans stays bare")]
MED_PHYS = (
    "His cock pulses three times and no more, and the pulses slow down and weaken: the second "
    "comes about a second after the first, the third about a second and a half after that. "
    "Each pulse throws one single rope of semen out of the slit at the tip - one stream only, it "
    "never splits into two. The amount is small and it stays the same amount the whole way: the "
    "first rope is a short slug of about a teaspoon, the second half of that, and the third is "
    "only a bead that wells out of the tip and drops onto her tongue. Each rope keeps the same "
    "thickness from the tip to her face and does not grow on the way. The gap is only an inch or "
    "two, so each rope travels almost straight along a short shallow arc and lands exactly where "
    "it was aimed, on her lips and her chin, and the patch appears at the spot the rope hit, not "
    "below it. Everything that leaves the tip ends up on her and nothing more: each rope leaves "
    "one glossy raised patch exactly as big as the rope was, with a thick rounded edge. The first "
    "rope hits a little harder and throws two or three tiny droplets; the second and the third "
    "just land and stay. On each pulse the shaft kicks upward a few degrees as the rope fires and "
    "springs back down, then holds still until the next pulse, and the veins swell a little."
)
MED_LAND = (
    "His cock pulses three times and no more, the second about a second after the first and the "
    "third about a second and a half after that, each one weaker. By the end there is exactly "
    "this much semen on her and no more: one glossy patch the size of a small coin on her lower "
    "lip and chin from the first pulse, a smaller one on her tongue from the second, and a single "
    "bead on her lower lip from the third. Each rope in flight is only as thick and as long as "
    "the patch it leaves: a short narrow cord, then a thinner cord, then a bead that only wells "
    "out of the tip and drops. One stream only out of the slit at the tip, it never splits into "
    "two. Each rope crosses the inch-wide gap on a short shallow arc and lands exactly where it "
    "points; the patch forms at the spot it hit, not lower, and nothing lands anywhere else. The "
    "first rope throws two or three tiny droplets where it hits; the others land and stay. On "
    "each pulse the shaft kicks upward a few degrees and springs back down, then holds still, "
    "and the veins swell a little."
)
med_phys = sub(med, MED_OLD, MED_PHYS)
med_land = sub(med, MED_OLD, MED_LAND)
med_land = sub(med_land, "Where the drops touch each other they merge into small glossy pools on her lips and chin",
               "Where the patches touch each other they merge into one glossy pool on her lips and chin")
med_phys = sub(med_phys, "Where the drops touch each other they merge into small glossy pools on her lips and chin",
               "Where the patches touch each other they merge into one glossy pool on her lips and chin")

# ---- photoreal high (k14_direct_p1_06: p1_pose, seed 950) ----
hi = P["cumshot_high"]["prompt"]
HI_OLD = hi[hi.index("His cock pulses three times"):hi.index(" His glans stays bare")]
HI_PHYS = (
    "His cock pulses three times and no more, and the pulses slow down and weaken: the second "
    "comes about a second after the first, the third about a second and a half after that. "
    "Each pulse throws one single rope of semen out of the slit at the tip straight up into her "
    "face - one stream only, it never splits into two. The first rope is a full rope of about a "
    "tablespoon, the second about half of that, the third a short weak one that barely reaches "
    "her lip. Each rope keeps the same thickness from the tip to her face, and the amount that "
    "lands is the amount that flew: the first leaves one heavy glossy patch across her lips and "
    "chin as big as the rope was, the second a smaller patch, the third a bead. Each rope travels "
    "along a short shallow arc and lands exactly where it was aimed; the patch appears at the "
    "spot the rope hit, not below it, and nothing arcs above her head or lands behind her. The "
    "first rope hits hard, flattens into a raised patch with a thick rounded edge and throws a "
    "few small droplets; the next two just hit and stay. On each pulse the shaft kicks upward "
    "about ten degrees as the rope fires, holds for an instant and springs back down, then holds "
    "still until the next pulse, and the veins stand out."
)
hi_phys = sub(hi, HI_OLD, HI_PHYS)

# ---- anime t4 (anime_ll_cumshot: fuzichoco keyframe, seed 93001) ----
t4 = P["anime_ll_cumshot"]["prompt"]
T4_OLD = t4[t4.index("Each pulse sends one single thin white rope"):t4.index(" She flinches at each spurt")]
T4_PHYS = (
    "The spurts slow down and weaken: the second comes about a second after the first, the third "
    "about a second and a half after that. Each pulse sends one single thin white rope of semen "
    "out of the slit at the tip along a short arc, and it lands exactly where it points. The "
    "amount stays the same from the tip to where it lands: each rope leaves one small glossy "
    "white patch exactly as big as the rope was, and no more appears than what flew. The first "
    "rope is the biggest and lands on her upper lip and cheek; the second is half as big and "
    "lands on her tongue; the third is only a small drop that falls onto her lower lip. Each one "
    "ends where it hits and stays, it does not lie across her face, and a single slow drop runs "
    "from her chin."
)
t4_phys = sub(t4, T4_OLD, T4_PHYS)

# ---- anime a26 k14 (anime_ll_cum_switch_a26: fuzichoco keyframe, seed 93010) ----
sw = P["anime_ll_cum_switch_a26"]["prompt"]
sw_phys = sub(sw,
    "He starts to cum: the shaft jerks and the first spurt starts, and the moment it starts she takes the head into her mouth",
    "He starts to cum: the shaft jerks and one short thin rope of semen leaves the tip on a short arc and lands on her tongue - a small amount, and that same small amount sits on her tongue - and the moment it lands she takes the head into her mouth")
sw_phys = sub(sw_phys,
    "as the cock twitches and pulses in her mouth.",
    "as the cock pulses in her mouth two more times, each pulse weaker and slower than the last.")
sw_phys = sub(sw_phys,
    "a little semen escapes at the corner of her lips and runs down her chin.",
    "one small drop of semen, no more than what went in, escapes at the corner of her lips and runs slowly down her chin.")

PR = {"image": P1}
AN = {"image": FZ}
jobs = [
    dict(name="pm_base", template="cumshot_medium", seed=970, **PR, _note="cumshot_medium as is (k16_medium)"),
    dict(name="pm_phys", template="cumshot_medium", seed=970, prompt=med_phys, **PR, _note="physics script: constant volume, arc lands where aimed, cadence, recoil"),
    dict(name="pm_land", template="cumshot_medium", seed=970, prompt=med_land, **PR, _note="landing-first: the end-state deposit sets the rope size"),
    dict(name="ph_base", template="cumshot_high", seed=950, **PR, _note="cumshot_high as is (k14_direct_p1_06)"),
    dict(name="ph_phys", template="cumshot_high", seed=950, prompt=hi_phys, **PR, _note="physics script, high amount, ~10 degree recoil"),
    dict(name="at4_base", template="anime_ll_cumshot", seed=93001, **AN, _note="anime t4 as is"),
    dict(name="at4_phys", template="anime_ll_cumshot", seed=93001, prompt=t4_phys, **AN, _note="t4 + constant volume, cadence; t4 bob kept"),
    dict(name="asw_base", template="anime_ll_cum_switch_a26", seed=93010, **AN, _note="a26 k14 as is"),
    dict(name="asw_phys", template="anime_ll_cum_switch_a26", seed=93010, prompt=sw_phys, **AN, _note="k14 + small first rope that lands as itself, decaying pulses, one drop escapes"),
]
out = os.path.join(ROOT, "jobs", "a93_cum_physics.jsonl")
with open(out, "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote", out, len(jobs))
