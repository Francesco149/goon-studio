"""mk_a117.py - round a117: Gemma, the full locked block (Illustrious), hit-rate check on 8 seeds.

Owner picks: Illustrious (a114), cold face + pink gem drop earrings (a115), horns = a114 seed 114002
(upward crescent). a116: "curved horns, large horns" 4/6; "horns pointing up" bled into a pointing
finger; seed 114004 sweeps sideways on every wording -> weight 1.3 + thick + a weighted negative.
Adult OC.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GEMMA = ("1girl, solo, succubus, mature female, very long hair, light purple hair, straight hair, hair between eyes, "
         "sidelocks, pink eyes, glowing eyes, demon horns, black horns, (curved horns:1.3), large horns, thick horns, "
         "pointy ears, butterfly wings, pink wings, black wing veins, demon tail, black tail, large breasts, "
         "tsurime, smug, half-closed eyes, closed mouth, smile, pink gem drop earrings, "
         "black bodysuit, latex bodysuit, shiny clothes, high collar, gold trim, glowing yellow neon trim, "
         "pink gemstone on collar, see-through cleavage, black elbow gloves, cyberpunk")
GEMMA_NEG = "(ram horns:1.3), (goat horns:1.2), curled horns, spiral horns, horizontal horns, multiple girls"
SHOT = "upper body, looking at viewer, front view, dark blue background, glowing particles"
NEG = ("lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, blurry, jpeg artifacts, watermark, "
       "text, 3d, realistic, " + GEMMA_NEG)


def jobs():
    return [{"workflow": "wf_illu_lora.json", "lora": "konosuba-aqua-s2-illustriousxl-lora-nochekaiser.safetensors",
             "strength": 0.0, "width": 832, "height": 1216, "negative": NEG, "name": "gm_lock_%d" % s, "seed": s,
             "prompt": "masterpiece, best quality, amazing quality, " + GEMMA + ", " + SHOT}
            for s in (114001, 114002, 114003, 114004, 115005, 115006, 117007, 117008)]


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a117_gemma_lock.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
