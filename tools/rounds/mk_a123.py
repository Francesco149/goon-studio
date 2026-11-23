"""mk_a123.py - round a123: Gemma under Xu Er 0.6 - H2 horns + wings back at 1.3.

a122: H2 horns (ram/curled + segmented, smooth, glossy) = smooth glossy coils 8/8, no spikes, the point
rising from the coil on 2/8 (the owner's A_114001 horn); earrings clean 16/16 with the butterfly
negatives. But wings at 1.15 became jagged bat wings, and Xu Er drew star marks under her eyes.
-> wings (butterfly wings:1.3), negatives + bat/demon wings + facial mark. Eight seeds. Adult OC.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a117 import GEMMA, SHOT
from mk_a122 import LORA, TRIG, OLD_HORNS, HORNS, NEG as NEG122, SEEDS

WINGS = ("butterfly wings, pink wings", "(butterfly wings:1.3), (pink wings:1.2)")
NEG = NEG122 + ", bat wings, demon wings, dragon wings, facial mark, facial tattoo, star (symbol)"
BLOCK = GEMMA.replace(OLD_HORNS, HORNS["H2"]).replace(*WINGS)


def jobs():
    assert BLOCK.count("(butterfly wings:1.3)") == 1 and HORNS["H2"] in BLOCK
    return [{"workflow": "wf_illu_lora.json", "lora": LORA, "strength": 0.6, "width": 832, "height": 1216,
             "negative": NEG, "seed": s, "name": "gm_x3_%d" % s,
             "prompt": "masterpiece, best quality, amazing quality, " + TRIG + ", " + BLOCK + ", " + SHOT} for s in SEEDS]


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a123_gemma_xuer_lock.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
