"""mk_a128.py - round a128: Uzaki Hana lap pillow, two single-shot clips, stock art style.

Owner picks (a127, uzaki_il_v2 on WAI v17, no style block): uzi_ontop_80_127001 and uzi_sofa_80_127001.
Owner: keep the LoRA's stock look -> the script's style line names no flat/no-shading/matte words, it asks
H3 to keep the keyframe's look. Clip recipe = a105 / a126 (H3 i2v w4a8, motion booster 0.4, no act LoRA,
1152x768, 124 frames); scripts from a126 with the white robes and the a127 rooms. Adult design study.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a126 import SOUND, HANA

STYLE = ("A 2D anime clip in the style of a TV anime that keeps the look of the first frame: clean lines, soft cel "
         "shading, warm lamp light, one fixed camera.")
SCRIPTS = {
    "sofa": ("uzi_sofa_80_127001",
        "A wide side view of a living room at night, city lights in the window: " + HANA + ", in an open white bathrobe, "
        "sits on the sofa; a man with black hair lies on his back along the sofa with his head in her lap. She leans over "
        "him so her large breast rests on his face and he sucks gently on her nipple. With one hand she strokes his erect "
        "cock in slow, steady strokes, about one a second; with the other she softly strokes his hair. She looks down at "
        "him with a gentle, loving smile, her blush warm; her breasts sway softly with her strokes and her chest rises and "
        "falls with her breath. Only now and then a tiny, thin, clear thread of saliva, colourless like water, glints at "
        "his lips. His cock twitches now and then in her hand. The camera does not move."),
    "ontop": ("uzi_ontop_80_127001",
        "A close side view on a bed at night, a lamp glowing behind them: " + HANA + ", in an open white bathrobe, lies "
        "half on top of a man with black hair, her large breast resting on his face; he sucks gently on her nipple. She "
        "reaches down his body and strokes his erect cock in slow, steady strokes, about one a second. She looks into the "
        "camera with a sweet, teasing smile, her blush warm; her breasts sway softly with each stroke. Only now and then a "
        "tiny, thin, clear thread of saliva, colourless like water, glints at his lips. His cock twitches now and then in "
        "her hand. The camera does not move."),
}


def key(name):
    d = os.path.join(ROOT, "gallery", "a127")
    return next(os.path.join(d, f) for f in sorted(os.listdir(d)) if f.startswith(name + "_"))


def jobs():
    return [{"workflow": "wf_h3vid_i2v_lora.json", "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
             "nsfw_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "nsfw_strength": 0.4,
             "width": 1152, "height": 768, "length": 124, "seed": 128001, "anime_timing": "off",
             "image": key(k), "name": "uzc_%s_128001" % n,
             "prompt": "integrated_multimodal_description: [Shot 1] " + STYLE + " " + s + SOUND}
            for n, (k, s) in SCRIPTS.items()]


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a128_uzaki_lap_clips.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs", [os.path.basename(j["image"]) for j in js])
