"""mk_a100.py - round a100: Emilia (Re:Zero) design-study LoRAs, identity across our style blocks.

Setups (docs/LORAS.md):
  illu  - nochekaiser "anime s4" (Illustrious only, civitai 1336055) on WAI-illustrious v17,
          workflows/wf_illu_lora.json, its own trigger words
  anima - duongve13112002's Anima LoRA (civitai 2790541), wf_anima2_lora.json, trigger "emilia (re:zero)"
  ctrl  - Anima with no character LoRA (what the base model knows), same tags
Styles: none / base / tv / hg / hgf (the a96 and a99 blocks). Shots: canon outfit portrait, and a
nude bedroom upper body (identity without the outfit). Adult design study: "mature female".
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STYLES = {
    "none": "",
    "base": "year 2016, anime screenshot, @murota yuuhei",
    "tv": ("year 2018, anime screenshot, anime coloring, cel shading, flat color, hard shadows, (shiny skin:1.2), glossy skin, "
           "(large white specular highlights:1.1), soft bloom, glow, pastel colors, thin lineart"),
    "hg": ("newest, game cg, eroge, (soft shading:1.2), (gradient shading:1.1), (shiny skin:1.2), oily skin, glossy skin, detailed skin, "
           "(skin shine:1.1), rim lighting, soft lighting, bloom, depth of field"),
    "hgf": ("newest, game cg, eroge, @fuzichoco, (soft shading:1.2), gradient shading, (shiny skin:1.2), oily skin, glossy skin, "
            "detailed skin, rim lighting, soft lighting, bloom"),
}
# nochekaiser s4 trainedWords (identity block + the s4 outfit block)
ILLU_ID = ("rezero emilia, emilia (re:zero), long hair, hair ornament, braid, flower, hair flower, french braid, crown braid, pointy ears, "
           "white flower, grey hair, purple eyes, x hair ornament, white hair, hair ribbon, elf, breasts, blunt bangs, mature female, medium breasts")
ANIMA_ID = ("emilia (re:zero), long hair, hair ornament, braid, crown braid, hair flower, white flower, pointy ears, grey hair, purple eyes, "
            "x hair ornament, hair ribbon, blunt bangs, mature female, medium breasts")
OUTFIT = "cape, dress, ribbon, purple ribbon, white cape, purple dress, long sleeves, covered navel, purple bodysuit"
SHOTS = {
    "outfit": "1girl, solo, {id}, " + OUTFIT + ", upper body, looking at viewer, gentle smile, forest, sunlight",
    "nude": "1girl, solo, {id}, (completely nude:1.2), upper body, looking at viewer, blush, smile, bedroom, warm light",
}
NEG_A = ("worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, watermark, text, 3d, realistic, "
         "bad anatomy, extra fingers, extra hands")
NEG_I = "lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, blurry, jpeg artifacts, watermark, text, 3d, realistic"


def jobs():
    out = []
    for setup in ("illu", "anima", "ctrl"):
        for sk, style in STYLES.items():
            for shot, tpl in SHOTS.items():
                if setup == "illu":
                    st = style.replace("@", "").replace("newest, ", "")
                    head = "masterpiece, best quality, amazing quality" + (", " + st if st else "")
                    p = head + ", " + tpl.format(id=ILLU_ID) + ", anime screencap"
                    j = {"workflow": "wf_illu_lora.json", "lora": "rezero-emilia-s4-illustriousxl-lora-nochekaiser.safetensors",
                         "strength": 1.0, "width": 1216, "height": 832, "negative": NEG_I}
                else:
                    head = "masterpiece, best quality" + (", " + style if style else "")
                    p = head + ", " + tpl.format(id=ANIMA_ID)
                    j = {"workflow": "wf_anima2_lora.json", "late": p, "width": 1248, "height": 832, "negative": NEG_A,
                         "lora": "anima_Emilia_2-30.safetensors", "strength": 1.0 if setup == "anima" else 0.0}
                j.update(name="em_%s_%s_%s" % (setup, sk, shot), seed=100001, prompt=p)
                out.append(j)
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a100_emilia_styles.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
