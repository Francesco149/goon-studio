"""mk_a114.py - round a114: Gemma (original cyber-succubus OC), design lock, pass 1.

Goal: a tag block that draws the same Gemma on every seed, before any LoRA exists.
Owner's reference: lavender very long hair, black curled demon horns, pointy ears, glowing pink
eyes, pink/black butterfly wings, demon tail, black latex bodysuit with gold trim and glowing
yellow neon lines, a pink gem at the collar, see-through cleavage panel. Her earrings were the
unstable part in the owner's earlier tests -> four earring designs side by side.

Stacks (no character LoRA; a zero-strength LoRA keeps the graph):
  illu  - WAI-illustrious v17, wf_illu_lora.json
  anima - Pink Alchemy v2.9, wf_anima2_lora.json
Earrings: none / gold hoops / pink gem drops (match the collar gem) / pink gem studs.
Shot: upper body, front, plain dark background (earrings and horns readable). Four seeds.
Adult OC ("mature female").
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ID = ("1girl, solo, succubus, mature female, very long hair, light purple hair, straight hair, hair between eyes, "
      "sidelocks, pink eyes, glowing eyes, demon horns, black horns, curled horns, pointy ears, "
      "butterfly wings, pink wings, black wing veins, demon tail, black tail, large breasts, smug, light smile")
OUTFIT = ("black bodysuit, latex bodysuit, shiny clothes, high collar, gold trim, glowing yellow neon trim, "
          "pink gemstone on collar, see-through cleavage, black elbow gloves, cyberpunk")
EARRINGS = {
    "none": ("", "earrings, jewelry on ears"),
    "hoop": ("gold hoop earrings", ""),
    "drop": ("pink gem drop earrings", ""),
    "stud": ("pink gem stud earrings", ""),
}
SHOT = "upper body, looking at viewer, front view, dark blue background, glowing particles"
NEG_A = ("worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, watermark, text, 3d, realistic, "
         "bad anatomy, extra fingers, extra hands, multiple girls")
NEG_I = ("lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, blurry, jpeg artifacts, watermark, "
         "text, 3d, realistic, multiple girls")
ZERO_ILLU = "konosuba-aqua-s2-illustriousxl-lora-nochekaiser.safetensors"
ZERO_ANIMA = "konosuba-aqua-s2-anima-lora-nochekaiser.safetensors"


def jobs():
    out = []
    for seed in (114001, 114002, 114003, 114004):
        for setup in ("illu", "anima"):
            for ek, (ear, eneg) in EARRINGS.items():
                body = ", ".join(x for x in (ID, ear, OUTFIT, SHOT) if x)
                if setup == "illu":
                    p = "masterpiece, best quality, amazing quality, " + body
                    j = {"workflow": "wf_illu_lora.json", "lora": ZERO_ILLU, "strength": 0.0,
                         "width": 832, "height": 1216, "negative": NEG_I + (", " + eneg if eneg else "")}
                else:
                    p = "masterpiece, best quality, " + body
                    j = {"workflow": "wf_anima2_lora.json", "late": p, "lora": ZERO_ANIMA, "strength": 0.0,
                         "width": 832, "height": 1248, "negative": NEG_A + (", " + eneg if eneg else "")}
                j.update(name="gm_%s_%s_%d" % (setup, ek, seed), seed=seed, prompt=p)
                out.append(j)
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a114_gemma_lock.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
