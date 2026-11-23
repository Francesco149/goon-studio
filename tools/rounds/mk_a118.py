"""mk_a118.py - round a118: Gemma art-style study (Illustrious / WAI v17), same design.

Owner: canon design = a117 gm_lock_114001 (huge segmented horns, popped collar, gold V trim); the
default WAI look reads generic -> try styles before building the dataset. The a117 block and
seeds stay fixed; only a style prefix changes.
  base     - control (a117)
  flat     - house flat TV look (docs/SCENES.md)
  hgame    - house h-game CG block (a99)
  kantoku  - soft, detailed (owner pick in docs/ANIME.md, on Anima)
  fuzichoco- pale, painted (owner pick in docs/ANIME.md, on Anima)
  pikazo   - mika pikazo: bold neon pop colour
  redjuice - clean digital, cyber
  nixeu    - dark glamour fantasy
Seeds: 114001 (canon) and 115006 (canon-like horns in a117). Adult OC.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a117 import GEMMA, SHOT, NEG

STYLES = {
    "base": "",
    "flat": "anime screenshot, anime coloring, (flat color:1.3), (matte:1.1), simple coloring, thin lineart",
    "hgame": "game cg, eroge, soft shading, gradient shading, oily skin",
    "kantoku": "kantoku",
    "fuzichoco": "fuzichoco",
    "pikazo": "mika pikazo",
    "redjuice": "redjuice",
    "nixeu": "nixeu",
}


def jobs():
    out = []
    for seed in (114001, 115006):
        for sk, st in STYLES.items():
            p = "masterpiece, best quality, amazing quality, " + (st + ", " if st else "") + GEMMA + ", " + SHOT
            out.append({"workflow": "wf_illu_lora.json", "lora": "konosuba-aqua-s2-illustriousxl-lora-nochekaiser.safetensors",
                        "strength": 0.0, "width": 832, "height": 1216, "negative": NEG,
                        "name": "gm_st_%s_%d" % (sk, seed), "seed": seed, "prompt": p})
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a118_gemma_styles.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
