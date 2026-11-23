"""mk_a131.py - round a131: the general (model-agnostic) Illustrious versions of the Anima scene templates.

Owner: everything tied to Anima gets a version that works with any character LoRA - better than typing by hand.
kit/presets.json illu_pov_bj (a112k wording), _mosaic, _foreskin, illu_side_bj, illu_pov_cockout, illu_side_gap,
illu_paizuri, illu_wide_gap, illu_suction, illu_cum_face, illu_side_handjob: plain WAI v17, neutral character, the
act and camera in Scene. Each is run exactly as the page runs it: neutral on two seeds, and once with Uzaki added as
a picked LoRA (extra_loras + her identity words in Character). Adult design study.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KEYS = ["illu_pov_bj", "illu_pov_bj_mosaic", "illu_pov_bj_foreskin", "illu_side_bj", "illu_pov_cockout", "illu_side_gap",
        "illu_paizuri", "illu_wide_gap", "illu_suction", "illu_cum_face", "illu_side_handjob"]
UZ = ("uzaki, an anime girl, 1girl, uzaki hana, short hair, grey hair, hair between eyes, bangs, blue eyes, fang, "
      "large breasts, mature female, half-closed eyes, blush")


def jobs():
    out = []
    for k in KEYS:
        for s in (131001, 131002):
            out.append({"template": k, "seed": s, "name": "gn_%s_%d" % (k[5:], s)})
        out.append({"template": k, "seed": 131001, "name": "gn_%s_uz_131001" % k[5:], "character": UZ,
                    "extra_loras": [{"name": "uzaki_il_v2.safetensors", "strength": 0.8}]})
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a131_general_templates.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
