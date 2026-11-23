"""mk_a130.py - round a130: Ilulu lap pillow, two single-shot clips, stock look (owner picks from a129).

Keyframes: il_ontop_129001, il_sofa_129001 (dragon-ilulu s2 on WAI v17). Recipe = a128 (Uzaki, owner: clean):
H3 i2v w4a8, motion booster 0.4, no act LoRA, 1152x768, 124 frames, style line keeps the first frame's look.
Reference for her scale: gallery/refs/characters/ilulu_scale_official.png (docs/LORAS.md "Ilulu"). Adult design study.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a126 import SOUND
from mk_a128 import STYLE, SCRIPTS as UZ

HANA = "a young adult woman with short grey hair falling between her eyes, bright blue eyes and one small fang"
ILULU = ("a young adult woman with long pink hair fading to purple at the curled ends, two curled golden horns and red "
         "eyes with slit pupils")
SCRIPTS = {
    "sofa": ("il_sofa_129001", UZ["sofa"][1].replace(HANA, ILULU)),
    "ontop": ("il_ontop_129001", UZ["ontop"][1].replace(HANA, ILULU)),
}


def key(name):
    d = os.path.join(ROOT, "gallery", "a129")
    return next(os.path.join(d, f) for f in sorted(os.listdir(d)) if f.startswith(name + "_"))


def jobs():
    assert all(ILULU in s for _, s in SCRIPTS.values())
    return [{"workflow": "wf_h3vid_i2v_lora.json", "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
             "nsfw_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "nsfw_strength": 0.4,
             "width": 1152, "height": 768, "length": 124, "seed": 130001, "anime_timing": "off",
             "image": key(k), "name": "ilc_%s_130001" % n,
             "prompt": "integrated_multimodal_description: [Shot 1] " + STYLE + " " + s + SOUND}
            for n, (k, s) in SCRIPTS.items()]


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a130_ilulu_lap_clips.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs", [os.path.basename(j["image"]) for j in js])
