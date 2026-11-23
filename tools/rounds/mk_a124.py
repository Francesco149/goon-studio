"""mk_a124.py - round a124: Uzaki Hana design study (UzakiHanaXL, Pony V6 XL) - samples + lap pillow.

Owner's files (adopted into the store, kit/models.json): loras/UzakiHanaXL.safetensors (Civitai 589043 /
657667, Pony, trigger 'uzaki hana'; trained words in the owner's txt and on the page) and
checkpoints/ponyDiffusionV6XL_v6.safetensors (Civitai 257749 / 290640). Graph: wf_illu_lora.json with the
checkpoint swapped (LoRA on model + CLIP, clip skip 2 - Pony needs it). Pony prompt format: score_9 ...
prefix, source_anime; score_4-6 in the negative.
Shots: identity (default outfit), the bunny outfit, and the three a105 lap pillow stagings (docs/SCENES.md
"Lap pillow + nursing handjob"): sofa, bed, on top. Adult design study ("mature female"), not canon-cast.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PRE = "score_9, score_8_up, score_7_up, score_6_up, source_anime"
HANA = ("1girl, uzaki hana, grey hair, short hair, hair between eyes, bangs, blue eyes, skin fang, large breasts, "
        "mature female")
DEFAULT = "black pantyhose, boots, bracelet, clothes writing, denim skirt, long sleeves, raglan sleeves"
BUNNY = ("fake rabbit ears, bare shoulders, black leotard, red bowtie, brown pantyhose, cleavage, collarbone, "
         "detached collar, playboy bunny, rabbit tail, wrist cuffs, high heels")
HIM = "1boy, hetero, tan skin, (black hair:1.1)"
NUDE_TOP = "(open bathrobe:1.1), (bare breasts:1.2)"
P, L = (832, 1216), (1216, 832)
SHOTS = {
    "id": (P, ", ".join((HANA, DEFAULT, "solo, smile, open mouth, :d, looking at viewer, cowboy shot, outdoors, day, city street"))),
    "bunny": (P, ", ".join((HANA, BUNNY, "solo, smug, blush, looking at viewer, cowboy shot, hand on own hip, indoors, casino, night"))),
    "lap_sofa": (L, ", ".join((HANA, NUDE_TOP, HIM,
        "(lap pillow:1.3), (nursing handjob:1.3), she sits on the couch, he lies on his back along the couch with his head "
        "in her lap, she leans over him, breast on his face, (breast sucking:1.2), handjob, her hand on his penis, other hand "
        "on his head, looking down at him, (gentle smile:1.2), blush, from side, wide shot, full body, indoors, living room, "
        "couch, night, warm lamp light"))),
    "lap_bed": (P, ", ".join((HANA, NUDE_TOP, HIM,
        "(lap pillow:1.3), (nursing handjob:1.3), sitting on bed, he lies across her lap, breast sucking, her breast resting "
        "on his face, handjob, her hand on his penis, (looking at viewer:1.2), (smile:1.2), blush, from front, upper body, "
        "indoors, bedroom, bed, white bed sheet, night, warm lamp light"))),
    "lap_ontop": (L, ", ".join((HANA, NUDE_TOP, HIM,
        "(nursing handjob:1.3), lying on top of him, on bed, (breasts on his face:1.2), breast sucking, she reaches down and "
        "strokes his penis, handjob, (looking at viewer:1.2), (smile:1.2), blush, from side, close-up, indoors, bedroom, "
        "bed, white bed sheet, night, warm lamp light"))),
}
NEG = ("score_4, score_5, score_6, lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, "
       "blurry, jpeg artifacts, watermark, signature, text, 3d, realistic, censored, mosaic censoring, bar censor")
NEG_SOLO = ", multiple girls"
NEG_LAP = ", his hand on his penis, male masturbation, extra arms, multiple girls"


def jobs():
    out = []
    for name, ((w, h), body) in SHOTS.items():
        for seed in (124001, 124002):
            out.append({"workflow": "wf_illu_lora.json", "ckpt": "ponyDiffusionV6XL_v6.safetensors",
                        "lora": "UzakiHanaXL.safetensors", "strength": 0.9, "steps": 25, "cfg": 7.0,
                        "sampler": "euler_ancestral", "sched": "normal", "width": w, "height": h, "seed": seed,
                        "negative": NEG + (NEG_LAP if name.startswith("lap") else NEG_SOLO),
                        "name": "uz_%s_%d" % (name, seed), "prompt": PRE + ", " + body})
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a124_uzaki_samples.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
