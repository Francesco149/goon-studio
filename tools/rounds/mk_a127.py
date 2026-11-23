"""mk_a127.py - round a127: Uzaki Hana, Illustrious LoRA (uzaki_il_v2, Civitai 1410199 / 1620490), neutral look.

Owner (a124-a125): UzakiHanaXL (Pony) is trained on fanart - thick lineart stays even with the flat block.
Try this LoRA on WAI v17 with NO style block first (a forced flat look can be too flat for some shows' art).
Trigger 'uzaki' + the page's identity tags ("an anime girl" is in its captions); strength 0.8 vs 1.0.
Shots: identity in her canon outfit, the a105 lap pillow sofa and on top (a124 wording). Adult design study.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a124 import NUDE_TOP, HIM
from mk_a125 import SHOTS as LAP

PRE = "masterpiece, best quality, amazing quality"
HANA = ("uzaki, an anime girl, 1girl, uzaki hana, short hair, grey hair, hair between eyes, bangs, blue eyes, fang, "
        "large breasts, mature female")
OUTFIT = "shirt, clothes writing, romaji text, raglan sleeves, skirt, denim skirt, black pantyhose"
NEG = ("lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, blurry, jpeg artifacts, watermark, "
       "signature, text, 3d, realistic, censored, mosaic censoring, bar censor")
SHOTS = {
    "id": (832, 1216, ", ".join((HANA, OUTFIT, "solo, smile, open mouth, looking at viewer, cowboy shot, outdoors, day, city street")),
           NEG + ", multiple girls"),
    "sofa": (LAP["sofa"][0], LAP["sofa"][1], ", ".join((HANA, NUDE_TOP, HIM, LAP["sofa"][2])),
             NEG + ", his hand on his penis, male masturbation, extra arms, multiple girls, grey hair on boy"),
    "ontop": (LAP["ontop"][0], LAP["ontop"][1], ", ".join((HANA, NUDE_TOP, HIM, LAP["ontop"][2])),
              NEG + ", his hand on his penis, male masturbation, extra arms, multiple girls, grey hair on boy"),
}


def jobs():
    out = []
    for name, (w, h, body, neg) in SHOTS.items():
        for st in (0.8, 1.0):
            for seed in (127001, 127002):
                out.append({"workflow": "wf_illu_lora.json", "lora": "uzaki_il_v2.safetensors", "strength": st,
                            "width": w, "height": h, "seed": seed, "negative": neg,
                            "name": "uzi_%s_%02d_%d" % (name, round(st * 100), seed), "prompt": PRE + ", " + body})
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a127_uzaki_illu.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
