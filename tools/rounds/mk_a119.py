"""mk_a119.py - round a119: Gemma, Illustrious style LoRAs on the a117 design (base = a117 control).

Owner (a118): no artist tag beat the base WAI look -> try style LoRAs; otherwise the base stays.
LoRAs (docs/LORAS.md, kit/models.json loras/style/), each at a low and a high strength, trigger first:
  xuer     - Xu Er thick paint, 'XUER guangying' (author 0.8-0.9)
  paint    - painterly impasto/chiaroscuro, 'painterly, impasto, brushstroke, chiaroscuro'
  retro    - retro sci-fi 90s, 'retro_artstyle, retro, cyberpunk' (author 0.7-1.0)
  realanim - Citron Real Anime IXL, 'bokeh, luminescent background'
Seeds 114001 (canon) and 115006. Adult OC.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a117 import GEMMA, SHOT, NEG

S = "style" + chr(92)  # ComfyUI lists subfolder LoRAs with a backslash on Windows
LORAS = {
    "xuer": (S + "xuer_thickpaint_il_v3.safetensors", "XUER guangying", (0.6, 0.85)),
    "paint": (S + "illustrious_style_painterly_v1.1.safetensors", "painterly, impasto, brushstroke, chiaroscuro", (0.6, 0.9)),
    "retro": (S + "retro_scifi_artstyle_illustriousXL-000021.safetensors", "retro_artstyle, retro, cyberpunk", (0.6, 0.85)),
    "realanim": (S + "RealisticAnimeIXL_v2.safetensors", "bokeh, luminescent background", (0.6, 0.9)),
}


def jobs():
    out = []
    for seed in (114001, 115006):
        for lk, (lora, trig, strengths) in LORAS.items():
            for s in strengths:
                out.append({"workflow": "wf_illu_lora.json", "lora": lora, "strength": s, "width": 832, "height": 1216,
                            "negative": NEG + ", signature, watermark", "seed": seed,
                            "name": "gm_sl_%s_%02d_%d" % (lk, round(s * 100), seed),
                            "prompt": "masterpiece, best quality, amazing quality, " + trig + ", " + GEMMA + ", " + SHOT})
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a119_gemma_stylelora.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
