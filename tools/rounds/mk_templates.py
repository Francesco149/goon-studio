#!/usr/bin/env python3
"""mk_templates.py - add the approved Love Live signature-style templates to kit/presets.json.

The styles come from ../lovelive-studio's guide (the designer tag plus a tested second artist tag,
and the signature trick: the show's name only for the last 30% of the steps), and the faces carry
the anti-generic marks (jitome, mole, fang, ahoge, hair intakes). The poses are the 2026-11-21
anime recreation round: POV cock-out, paizuri, wide gap, cum landed.
"""
import json
import os

P = json.load(open("kit/presets.json", encoding="utf-8"))

CHAR = ("1girl, 1boy, hetero, pov, from above, looking up at viewer, short silver hair, single braid, "
        "purple eyes, jitome, mole under eye, fang, ahoge, hair intakes, (curvy:1.6), (wide hips:1.4), "
        "thick thighs, large breasts, mature female, half-closed eyes, blush, saliva")
SOFT = ("1girl, 1boy, hetero, pov, from above, looking up at viewer, short silver hair, single braid, "
        "purple eyes, tareme, thick eyebrows, freckles, mole under eye, ahoge, hair intakes, (curvy:1.6), "
        "(wide hips:1.4), thick thighs, large breasts, mature female, half-closed eyes, blush, saliva")

NEG = ("extra hands, extra fingers, third hand, bad anatomy, fused limbs, extra limbs, male body, censored, "
       "mosaic censoring, bar censor, cum, worst quality, low quality, score_1, score_2, score_3, blurry, "
       "jpeg artifacts, watermark, text, 3d, realistic")
NEG_CUM = ("extra hands, extra fingers, third hand, bad anatomy, fused limbs, extra limbs, male body, censored, "
           "mosaic censoring, bar censor, cum on face, cum on nose, cum string, strand across face, web, tears, "
           "long strand from mouth to cock, worst quality, low quality, score_1, score_2, score_3, blurry, "
           "jpeg artifacts, watermark, text, 3d, realistic")

POV = ("cock out, (penis:1.2), (erection:1.1), detailed penis shaft, veins, defined glans, corona rim, uncensored, "
       "(penis focus:1.2), she holds his cock upright with one hand, the tip an inch below her open mouth, "
       "(mouth open:1.2), tongue out, bedroom, soft light")
PAZ = ("paizuri, titjob, (breasts around penis:1.3), (penis between breasts:1.3), (glans above cleavage:1.2), "
       "detailed penis shaft, veins, uncensored, (penis focus:1.2), she presses her large breasts together with "
       "both hands, (tongue out:1.2) touching the glans, bedroom, soft light")
WIDE = ("cock out, (penis:1.2), detailed penis shaft, veins, defined glans, corona rim, uncensored, "
        "(penis focus:1.2), she holds his cock low between his thighs at the bottom of the frame, the tip a hand's "
        "width below her chin, head tilted down, (mouth wide open:1.2), tongue out, (eyes rolled up to viewer:1.15), "
        "bedroom, soft light")
SIDE = ("cock out, (penis:1.2), detailed penis shaft, veins, defined glans, corona rim, uncensored, "
        "(penis focus:1.2), his cock is upright an inch in front of her open mouth, a clear gap between the tip and "
        "her lips, she leans toward it, tongue out, (mouth open:1.2), eyes on the cock, bedroom, soft light")
SIDE_CHAR = ("1girl, 1boy, hetero, side view, profile, kneeling, leaning forward, short silver hair, single braid, "
             "purple eyes, jitome, mole under eye, fang, ahoge, hair intakes, (curvy:1.6), (wide hips:1.4), "
             "thick thighs, large breasts, mature female, half-closed eyes, blush, saliva")
SIDE_NEG = ("extra hands, extra fingers, third hand, bad anatomy, fused limbs, extra limbs, censored, mosaic censoring, "
            "bar censor, penis in mouth, lips touching the tip, worst quality, low quality, score_1, score_2, score_3, "
            "blurry, jpeg artifacts, watermark, text, 3d, realistic")
CUM = ("cock out, (penis:1.1), detailed penis shaft, veins, uncensored, (penis focus:1.1), (cum on cheek:1.2), "
       "(cum on tongue:1.2), (cum on lips:1.2), thick white semen, glossy, milky, (cum drip:1.2), "
       "(mouth open:1.2), tongue out, semen pooling on her tongue, a heavy drip from her chin, bedroom, soft light")
SUCTION = ("(penis in mouth:1.2), (lips sealed around penis:1.35), mouth stretched, no tongue, cheeks hollowed, "
           "(cheeks sucked in:1.25), (sunken cheeks:1.2), sucking hard, his cock deep in her mouth, her lips around "
           "the middle of his shaft, her nose close to his body, uncensored, eyes on viewer, bedroom, soft light")
DEEP = ("(penis in mouth:1.3), (lips sealed around penis:1.35), (cheeks hollow:1.4), (sunken cheeks:1.3), "
        "(cheek sucking:1.2), sucking, deepthroat, her lips around the middle of his shaft, her nose close to his "
        "body, no cheek bulge, uncensored, eyes on viewer, bedroom, soft light")

PROMPT = "masterpiece, best quality, year 2016, anime screenshot, {character}, @murota yuuhei{artist}, {scene}"

styles = [
    ("fz", ", @fuzichoco", "fuzichoco (pale, painted)"),
    ("kt", ", @kantoku", "kantoku (soft, detailed)"),
    ("sig", "", "signature (clean Love Live)"),
    ("ikeda", ", @ikeda kazumi", "ikeda kazumi (KyoAni-like)"),
]
specs = []
for key, artist, label in styles:
    specs.append(("anime_ll_%s_pov" % key, artist, "Anime - LL %s, POV cock out" % label, POV, NEG, True))
for key, artist, label in (("fz", ", @fuzichoco", "fuzichoco"), ("kt", ", @kantoku", "kantoku"),
                           ("sig", "", "signature")):
    specs.append(("anime_ll_%s_paizuri" % key, artist,
                  "Anime - LL %s, paizuri%s" % (label, " (best)" if key == "sig" else ""), PAZ, NEG, True))
specs.append(("anime_ll_fz_wide", ", @fuzichoco", "Anime - LL fuzichoco, wide gap", WIDE, NEG, True))
specs.append(("anime_ll_fz_side", ", @fuzichoco", "Anime - LL fuzichoco, side view cock out (visible gap)",
              SIDE, SIDE_NEG, True))
specs.append(("anime_ll_fz_suction", ", @fuzichoco", "Anime - LL fuzichoco, suction deepthroat (hollow cheeks)",
              SUCTION, NEG, True))
specs.append(("anime_ll_fz_deepthroat", ", @fuzichoco", "Anime - LL fuzichoco, deepthroat (puffed cheeks)",
              DEEP, NEG, True))
specs.append(("anime_ll_fz_cum", ", @fuzichoco", "Anime - LL fuzichoco, cum landed", CUM, NEG_CUM, False))

new = {}
for key, artist, label, scene, neg, _clean in specs:
    side = key == "anime_ll_fz_side"
    new[key] = {
        "label": label,
        "workflow": "wf_anima2_sig.json",
        "width": 1248 if side else 832,
        "height": 832 if side else 1248,
        "steps": 30,
        "cfg": 4.0,
        "prompt": PROMPT.format(artist=artist, character="{character}", scene="{scene}"),
        "late": "signature",
        "character": SIDE_CHAR if side else CHAR,
        "scene": scene,
        "negative": neg,
    }

tpl = P["templates"]
if "anime_ll_fz_pov" in tpl:
    print("templates already present; nothing to do")
else:
    out = {}
    for k, v in tpl.items():
        out[k] = v
        if k == "anime_cum":
            out.update(new)
    P["templates"] = out

chars = P.setdefault("characters", {})
chars.setdefault("ll_sig", CHAR)
chars.setdefault("ll_soft", SOFT)

with open("kit/presets.json", "w", encoding="utf-8") as f:
    json.dump(P, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("added %d templates, characters: %s" % (len(new), ",".join(sorted(chars))))
