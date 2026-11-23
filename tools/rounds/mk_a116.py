"""mk_a116.py - round a116: Gemma horn lock (Illustrious).

Owner: the canon horn is a114 seed 114002 (analysis/a114_horns_114002.jpg): thick, ribbed, glossy
black, rising from the sides of the head, sweeping outward then up, tips pointing up and slightly in
(an upward crescent) - not a ram curl. a115's "ram horns" goes the wrong way.
Variants (all with a negative against the ram/spiral curl):
  curved - curved horns, large horns
  up     - (curved horns:1.2), large horns, horns pointing up
  ribbed - (curved horns:1.2), large horns, horns pointing up, ribbed horns
Face/earrings held at the a114 wording (smug, light smile) + gold hoops. Six seeds. Adult OC.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PRE = ("1girl, solo, succubus, mature female, very long hair, light purple hair, straight hair, hair between eyes, "
       "sidelocks, pink eyes, glowing eyes, demon horns, black horns, {horns}, pointy ears, "
       "butterfly wings, pink wings, black wing veins, demon tail, black tail, large breasts, smug, light smile, "
       "gold hoop earrings, black bodysuit, latex bodysuit, shiny clothes, high collar, gold trim, glowing yellow neon trim, "
       "pink gemstone on collar, see-through cleavage, black elbow gloves, cyberpunk, "
       "upper body, looking at viewer, front view, dark blue background, glowing particles")
HORNS = {
    "curved": "curved horns, large horns",
    "up": "(curved horns:1.2), large horns, horns pointing up",
    "ribbed": "(curved horns:1.2), large horns, horns pointing up, ribbed horns",
}
NEG = ("lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, blurry, jpeg artifacts, watermark, "
       "text, 3d, realistic, multiple girls, ram horns, curled horns, spiral horns, horns curling down")


def jobs():
    out = []
    for seed in (114001, 114002, 114003, 114004, 115005, 115006):
        for hk, h in HORNS.items():
            out.append({"workflow": "wf_illu_lora.json", "lora": "konosuba-aqua-s2-illustriousxl-lora-nochekaiser.safetensors",
                        "strength": 0.0, "width": 832, "height": 1216, "negative": NEG,
                        "name": "gm_h_%s_%d" % (hk, seed), "seed": seed,
                        "prompt": "masterpiece, best quality, amazing quality, " + PRE.format(horns=h)})
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a116_gemma_horns.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
