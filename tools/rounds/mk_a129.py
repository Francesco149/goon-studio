"""mk_a129.py - round a129: Ilulu design study (nochekaiser 'anime s2' Illustrious LoRA, Civitai 1464409 / 1656218).

Owner's files: trigger words txt + LoRA (re-fetched from Civitai, sha256 matches). Adult design study: a petite
young woman in the anime (taller than Kanna, adult proportions - owner's screenshot); 'mature female' is in the
trigger block; every render is checked and any that reads childlike is dropped. Same method as Uzaki (a127):
WAI v17, stock look (no style block), LoRA 1.0. Shots: identity in both outfits; the a105 lap pillow sofa and
on top (a124/a125 wording). Two seeds.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a124 import NUDE_TOP, HIM
from mk_a125 import SHOTS as LAP
from mk_a127 import PRE, NEG

ILULU = ("ilulu, ilulu (maidragon), curled horns, horns, long hair, multicolored hair, purple hair, red eyes, red hair, "
         "slit pupils, mature female, breasts, large breasts, anime screencap")
OUT1 = "black shirt, long shirt, black thighhighs, collarbone, shirt, short sleeves, thighhighs, wide sleeves, zettai ryouiki"
OUT2 = "shirt, short sleeves, apron, blue shirt, black apron, pants"
LAPNEG = NEG + ", his hand on his penis, male masturbation, extra arms, multiple girls, red hair on boy"
SHOTS = {
    "id1": (832, 1216, ", ".join(("1girl, solo", ILULU, OUT1, "smile, looking at viewer, cowboy shot, indoors, apartment, day")), NEG + ", multiple girls"),
    "id2": (832, 1216, ", ".join(("1girl, solo", ILULU, OUT2, "smile, looking at viewer, cowboy shot, indoors, candy shop, day")), NEG + ", multiple girls"),
    "sofa": (LAP["sofa"][0], LAP["sofa"][1], ", ".join(("1girl", ILULU, NUDE_TOP, HIM, LAP["sofa"][2])), LAPNEG),
    "ontop": (LAP["ontop"][0], LAP["ontop"][1], ", ".join(("1girl", ILULU, NUDE_TOP, HIM, LAP["ontop"][2])), LAPNEG),
}


def jobs():
    return [{"workflow": "wf_illu_lora.json", "lora": "dragon-ilulu-s2-illustriousxl-lora-nochekaiser.safetensors",
             "strength": 1.0, "width": w, "height": h, "seed": seed, "negative": neg,
             "name": "il_%s_%d" % (name, seed), "prompt": PRE + ", " + body}
            for name, (w, h, body, neg) in SHOTS.items() for seed in (129001, 129002)]


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a129_ilulu.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
