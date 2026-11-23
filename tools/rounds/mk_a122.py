"""mk_a122.py - round a122: Gemma under Xu Er 0.6 - wings, earrings, horns.

a121 (docs/OC.md): style holds 24/24; wings vanish unless weighted, (butterfly wings:1.3) bleeds butterflies
into the earrings and brooch; horns small/spiky or big/jagged. Owner: no spiky horns; the horn to aim for is
gallery/a121/gm_xu_A_114001 (analysis/a121_A114001_horns.jpg): a glossy segmented coil beside the head
with a smooth tapered point rising from it, pink glow in the grooves. The canon negative bans curls, which
fights that shape -> lifted here.
  H1 - curved, large, segmented, smooth, glossy horns
  H2 - ram/curled (the coil) + segmented, smooth, glossy
Both: wings at 1.15 + earring/brooch butterfly negative, spiked/jagged horns in the negative.
Cat-mouth smirk kept (the style's face). Eight seeds. Adult OC.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a117 import GEMMA, SHOT

LORA = "style" + chr(92) + "xuer_thickpaint_il_v3.safetensors"
TRIG = "XUER guangying"
OLD_HORNS = "(curved horns:1.3), large horns, thick horns"
HORNS = {
    "H1": "(curved horns:1.2), large horns, thick horns, segmented horns, smooth horns, glossy horns",
    "H2": "ram horns, curled horns, large horns, segmented horns, smooth horns, glossy horns",
}
WINGS = ("butterfly wings, pink wings", "(butterfly wings:1.15), pink wings")
NEG = ("lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, blurry, jpeg artifacts, watermark, "
       "text, 3d, realistic, signature, multiple girls, spiked horns, jagged horns, spikes, "
       "butterfly earrings, butterfly brooch, butterfly hair ornament")
SEEDS = (114001, 115006, 121001, 121002, 121003, 121004, 121005, 121006)


def jobs():
    assert OLD_HORNS in GEMMA and WINGS[0] in GEMMA
    out = []
    for seed in SEEDS:
        for hk, horns in HORNS.items():
            block = GEMMA.replace(OLD_HORNS, horns).replace(*WINGS)
            out.append({"workflow": "wf_illu_lora.json", "lora": LORA, "strength": 0.6, "width": 832, "height": 1216,
                        "negative": NEG, "seed": seed, "name": "gm_xh_%s_%d" % (hk, seed),
                        "prompt": "masterpiece, best quality, amazing quality, " + TRIG + ", " + block + ", " + SHOT})
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a122_gemma_xuer_horns.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
