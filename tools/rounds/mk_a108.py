"""mk_a108.py - round a108: Aqua (KonoSuba) design-study LoRAs, which keeps the identity best.

Setups (docs/LORAS.md):
  illu  - nochekaiser "anime s2" for Illustrious (civitai 1376640 v1555410) on WAI-illustrious v17, wf_illu_lora.json
  anima - nochekaiser "anime s2" for Anima (civitai 2652645 v2978564) on Pink, wf_anima2_lora.json
  ctrl  - Anima with no character LoRA (what the base model knows), same tags
(the owner's other link, civitai 352605, is Pony-only: no Pony checkpoint here yet)
Looks: none / flat (the lanzhu_night flat TV block). Shots: canon outfit, nude upper body. Two seeds.
Adult design study: "mature female".
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SERIES = "kono subarashii sekai ni shukufuku wo!"
LOOKS = {
    "none": "",
    "flat": ("year 2020, anime screenshot, " + SERIES + ", anime coloring, (flat color:1.4), (no shading:0.8), (matte:1.2), "
             "(simple coloring:1.2), thin lineart, soft pastel colors"),
}
# nochekaiser trainedWords: identity block (+ "mature female") and the outfit block
ILLU_ID = ("aqua (konosuba), long hair, blue eyes, hair ornament, very long hair, blue hair, hair rings, single hair ring, "
           "hair bobbles, mature female, breasts")
ANIMA_ID = ("aqua (konosuba), long hair, blue eyes, hair ornament, very long hair, blue hair, hair rings, single hair ring, "
            "hair bobbles, mature female, medium breasts")
OUTFIT = "skirt, shirt, thighhighs, bare shoulders, detached sleeves, white thighhighs, blue skirt, blue shirt, green bow"
SHOTS = {
    "outfit": "1girl, solo, {id}, " + OUTFIT + ", upper body, looking at viewer, smile, town, sunlight",
    "nude": "1girl, solo, {id}, (completely nude:1.2), upper body, looking at viewer, blush, smile, bedroom, warm light",
}
NEG_A = ("worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, watermark, text, 3d, realistic, "
         "bad anatomy, extra fingers, extra hands")
NEG_I = "lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, blurry, jpeg artifacts, watermark, text, 3d, realistic"


def jobs():
    out = []
    for seed in (108001, 108002):
        for setup in ("illu", "anima", "ctrl"):
            for lk, look in LOOKS.items():
                for shot, tpl in SHOTS.items():
                    if setup == "illu":
                        p = "masterpiece, best quality, amazing quality" + (", " + look if look else "") + ", " + tpl.format(id=ILLU_ID) + ", anime screencap"
                        j = {"workflow": "wf_illu_lora.json", "lora": "konosuba-aqua-s2-illustriousxl-lora-nochekaiser.safetensors",
                             "strength": 1.0, "width": 1216, "height": 832, "negative": NEG_I}
                    else:
                        p = "masterpiece, best quality" + (", " + look if look else "") + ", " + tpl.format(id=ANIMA_ID)
                        j = {"workflow": "wf_anima2_lora.json", "late": p, "width": 1248, "height": 832, "negative": NEG_A,
                             "lora": "konosuba-aqua-s2-anima-lora-nochekaiser.safetensors", "strength": 1.0 if setup == "anima" else 0.0}
                    j.update(name="aq_%s_%s_%s_%d" % (setup, lk, shot, seed), seed=seed, prompt=p)
                    out.append(j)
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a108_aqua_lora.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
