"""mk_a115.py - round a115: Gemma design lock, pass 2 (Illustrious only, owner pick after a114).

a114 result: WAI-illustrious holds the outfit on every seed; Anima drifted (halter, plain wings).
Earrings: gold hoops 4/4 stable, pink gem drops 4/4 but size varies, studs turned into dangles.
Horns were the main drift (seed 114002 drew upward crescents) -> "ram horns" here.
Face: the same girl, but sweeter or colder by seed (owner) -> two expression locks:
  cold  - tsurime, smug, half-closed eyes, closed-mouth smile
  sweet - tareme, gentle smile, light blush
Earrings: hoop / drop. Seeds: the four a114 seeds + two new. Adult OC.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ID = ("1girl, solo, succubus, mature female, very long hair, light purple hair, straight hair, hair between eyes, "
      "sidelocks, pink eyes, glowing eyes, demon horns, black horns, ram horns, curled horns, pointy ears, "
      "butterfly wings, pink wings, black wing veins, demon tail, black tail, large breasts")
FACES = {
    "cold": "tsurime, smug, half-closed eyes, closed mouth, smile",
    "sweet": "tareme, gentle smile, light blush",
}
EARRINGS = {"hoop": "gold hoop earrings", "drop": "pink gem drop earrings"}
OUTFIT = ("black bodysuit, latex bodysuit, shiny clothes, high collar, gold trim, glowing yellow neon trim, "
          "pink gemstone on collar, see-through cleavage, black elbow gloves, cyberpunk")
SHOT = "upper body, looking at viewer, front view, dark blue background, glowing particles"
NEG = ("lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, blurry, jpeg artifacts, watermark, "
       "text, 3d, realistic, multiple girls")


def jobs():
    out = []
    for seed in (114001, 114002, 114003, 114004, 115005, 115006):
        for fk, face in FACES.items():
            for ek, ear in EARRINGS.items():
                p = "masterpiece, best quality, amazing quality, " + ", ".join((ID, face, ear, OUTFIT, SHOT))
                out.append({"workflow": "wf_illu_lora.json", "lora": "konosuba-aqua-s2-illustriousxl-lora-nochekaiser.safetensors",
                            "strength": 0.0, "width": 832, "height": 1216, "negative": NEG,
                            "name": "gm_%s_%s_%d" % (fk, ek, seed), "seed": seed, "prompt": p})
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a115_gemma_face.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
