"""mk_a125.py - round a125: Uzaki Hana lap pillow keyframes in the flat TV-anime look (Pony + UzakiHanaXL).

Owner (a124): identity holds, but the lineart and shading read as fanart; anime is flatter with thinner lines.
-> the house "flatter" block (kit/stories/emilia_meadow.json variants.flatter) ported to Pony: series tag
+ anime screencap, flat colour / no shading / matte / thin lineart, the matte flat-coloured penis that keeps
thickness and veins; gloss words in the negative. The LoRA's training set is mostly fanart -> 0.9 vs 0.65.
Stagings: sofa and on top (a124: both read right; bed put his cock at chest height - dropped).
Sofa: both of his legs spelled out (a105 lost one). Keyframes for single-shot clips. Adult design study.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a124 import HANA, NUDE_TOP, HIM, NEG

PRE = "score_9, score_8_up, score_7_up, source_anime"
FLAT = ("anime screencap, uzaki-chan wa asobitai!, anime coloring, (flat color:1.4), (no shading:0.8), (matte:1.2), "
        "(simple coloring:1.2), thin lineart, soft pastel colors, (diagonal-lined blush:1.1), (matte penis:1.2), "
        "(thick penis:1.1), veins, flat colored penis")
SHOTS = {
    "sofa": (1216, 832,
        "(lap pillow:1.3), (nursing handjob:1.3), she sits on the couch, he lies on his back along the couch with his head "
        "in her lap, both of his legs stretched out along the couch, she leans over him, breast on his face, "
        "(breast sucking:1.2), handjob, her hand on his penis, other hand on his head, looking down at him, "
        "(gentle smile:1.2), blush, from side, wide shot, full body, indoors, living room, couch, night, warm lamp light"),
    "ontop": (1216, 832,
        "(nursing handjob:1.3), lying on top of him, on bed, (breasts on his face:1.2), breast sucking, she reaches down and "
        "strokes his penis, handjob, (looking at viewer:1.2), (smile:1.2), blush, from side, close-up, indoors, bedroom, "
        "bed, white bed sheet, night, warm lamp light"),
}
NEG_FLAT = (NEG + ", shiny skin, shiny penis, glossy penis, penis highlights, glossy lips, shine, gradient shading, "
            "heavy shading, thick lineart, his hand on his penis, male masturbation, extra arms, multiple girls")


def jobs():
    out = []
    for name, (w, h, act) in SHOTS.items():
        for st in (0.9, 0.65):
            for seed in (125001, 125002):
                out.append({"workflow": "wf_illu_lora.json", "ckpt": "ponyDiffusionV6XL_v6.safetensors",
                            "lora": "UzakiHanaXL.safetensors", "strength": st, "steps": 25, "cfg": 7.0,
                            "sampler": "euler_ancestral", "sched": "normal", "width": w, "height": h, "seed": seed,
                            "negative": NEG_FLAT, "name": "uzf_%s_%02d_%d" % (name, round(st * 100), seed),
                            "prompt": ", ".join((PRE, FLAT, HANA, NUDE_TOP, HIM, act))})
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a125_uzaki_flat_keys.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
