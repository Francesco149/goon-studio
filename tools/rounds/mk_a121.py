"""mk_a121.py - round a121: Gemma in the Xu Er thick-paint style (owner pick from a119).

Owner: gallery/a119/gm_sl_xuer_60_114001 has the art style to keep (heavy outlines, punchy cel with
gloss, ornate gold filigree). It also drifted the design: no wings, horns curled into buns with a spike,
cat-mouth fang smirk. a120 (base-look dataset) stopped at 27/72.
  A - xuer 0.6, the a117 block (does the style hold on other seeds?)
  B - xuer 0.6, wings and horns weighted back toward canon
  C - xuer 0.5, the a117 block (style with less drift?)
Eight seeds, upper body. Adult OC.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a117 import GEMMA, SHOT, NEG

LORA = "style" + chr(92) + "xuer_thickpaint_il_v3.safetensors"
TRIG = "XUER guangying"
GEMMA_B = (GEMMA.replace("(curved horns:1.3), large horns, thick horns", "(curved horns:1.3), (large horns:1.2), (thick horns:1.2)")
                .replace("butterfly wings, pink wings", "(butterfly wings:1.3), (pink wings:1.2), wings"))
VARIANTS = {"A": (0.6, GEMMA), "B": (0.6, GEMMA_B), "C": (0.5, GEMMA)}
SEEDS = (114001, 115006, 121001, 121002, 121003, 121004, 121005, 121006)


def jobs():
    out = []
    for seed in SEEDS:
        for vk, (s, block) in VARIANTS.items():
            out.append({"workflow": "wf_illu_lora.json", "lora": LORA, "strength": s, "width": 832, "height": 1216,
                        "negative": NEG + ", signature, watermark", "seed": seed, "name": "gm_xu_%s_%d" % (vk, seed),
                        "prompt": "masterpiece, best quality, amazing quality, " + TRIG + ", " + block + ", " + SHOT})
    return out


if __name__ == "__main__":
    assert GEMMA_B != GEMMA
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a121_gemma_xuer.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
