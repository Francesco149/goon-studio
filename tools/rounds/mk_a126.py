"""mk_a126.py - round a126: Uzaki Hana lap pillow, two single-shot clips (no montage) from the a125 flat keys.

Keyframes (a125, flat TV look on Pony + UzakiHanaXL): sofa = uzf_sofa_65_125001, on top = uzf_ontop_90_125002.
Clip recipe = the approved a105 lap pillow (docs/SCENES.md): H3 i2v (8 GB w4a8), motion booster only
(H3_Motion_BoosterV2 0.4, no act LoRA), 1152x768, 124 frames. Scripts: a105 sofa v5 / on-top v3 wording with
Hana swapped in; no precum line on either (a105: a precum bead evaporates or grows steam). Adult design study.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STYLE = ("A 2D anime clip in the flat style of a TV anime: flat colours with no shading at all, matte skin and a matte "
         "penis with no shine, thin clean lines, hatched pink blush lines on her cheeks, warm lamp light, one fixed camera.")
SOUND = ("\n\noverall_soundscape: close-miked Foley, loud and present, over the quiet hum of a room at night, no music and "
         "no speech: a soft wet sucking at her breast, the slow soft rhythm of her hand, her quiet happy breathing, his "
         "muffled sigh.\n\nnon_diegetic_music: N/A")
HANA = "a young adult woman with short grey hair falling between her eyes, bright blue eyes and one small fang"
SCRIPTS = {
    "sofa": ("uzf_sofa_65_125001",
        "A wide side view of a living room at night: " + HANA + ", in an open white bathrobe, sits on the sofa; a man "
        "with black hair lies on his back along the sofa with his head in her lap. She leans over him so her large breast "
        "rests on his face and he sucks gently on her nipple. With one hand she strokes his erect cock in slow, steady "
        "strokes, about one a second; with the other she softly strokes his hair. She looks down at him with a gentle, "
        "loving smile, her blush warm; her breasts sway softly with her strokes and her chest rises and falls with her "
        "breath. Only now and then a tiny, thin, clear thread of saliva, colourless like water, glints at his lips. His "
        "cock twitches now and then in her hand. The camera does not move."),
    "ontop": ("uzf_ontop_90_125002",
        "A close side view on a bed at night: " + HANA + ", in an open lavender bathrobe, lies half on top of a man with "
        "black hair, her large breast resting on his face; he sucks gently on her nipple. She reaches down his body and "
        "strokes his erect cock in slow, steady strokes, about one a second. She looks into the camera with a sweet, "
        "teasing smile, her blush warm; her breasts sway softly with each stroke. Only now and then a tiny, thin, clear "
        "thread of saliva, colourless like water, glints at his lips. His cock twitches now and then in her hand. The "
        "camera does not move."),
}


def key(name):
    d = os.path.join(ROOT, "gallery", "a125")
    return next(os.path.join(d, f) for f in sorted(os.listdir(d)) if f.startswith(name + "_"))


def jobs():
    return [{"workflow": "wf_h3vid_i2v_lora.json", "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
             "nsfw_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "nsfw_strength": 0.4,
             "width": 1152, "height": 768, "length": 124, "seed": 126001, "anime_timing": "off",
             "image": key(k), "name": "uzc_%s_126001" % n,
             "prompt": "integrated_multimodal_description: [Shot 1] " + STYLE + " " + s + SOUND}
            for n, (k, s) in SCRIPTS.items()]


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a126_uzaki_lap_clips.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs", [j["image"] for j in js])
