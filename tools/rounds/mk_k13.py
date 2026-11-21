"""Generate jobs/k13.jsonl - round 9, control the travel with VELOCITY, not with the endpoint.

Round 8 (k12) result: telling the model where the rope must stop ("its far end stops on her lower
lip, at a slight angle, not over her head") does NOT work on the normal recipe - it still draws the
rope up past her nose. But it worked on the goopy variant, whose wording is about the fluid being
slow and heavy ("it does not spray and does not arc, it tumbles slowly out"). And it worked in
k11_goopy_06 as well.

That is the physics talking: a fast, medium-viscosity rope genuinely travels far and splashes; a
short rope that lands on her lip is a *slow, heavy* emission. So the lever is velocity and travel
distance, not a description of where it should stop:

  "the semen comes out slowly and heavily; it does not shoot and does not spray, it travels only a
   few inches and drops onto her lower lip"

Three clips: the normal material at 0.6 and 0.5 on the p1 keyframe, and the same on the wide-gap
keyframe (which is the one that keeps the glans clean). Everything else is the settled k10 recipe:
three decaying pulses, one stream from the slit, bare glans, merging drops.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k13.jsonl"))

P1 = r"gallery\refs\cumshot\p1_pose.png"
WIDE = os.path.abspath(os.path.join(HERE, "..", "..", "gens", "k04", "k4_wide_clean_00001_.png"))

HEAD_P1 = ("integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed "
           "camera. A young adult Asian woman in her mid-twenties with long black hair in pink-streaked "
           "twin tails and a silver choker kneels between the viewer's legs, holding his erect adult "
           "cock upright an inch below her open mouth, her tongue out, her eyes on the lens. ")

HEAD_WIDE = ("integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed "
             "camera. A young adult Asian woman in her mid-twenties with long black hair in pink-streaked "
             "twin tails and a silver choker kneels between the viewer's legs. She holds his erect adult "
             "cock in her hand low between his thighs, the tip a hand's width below her chin and a little "
             "to one side, her head tilted down, her mouth wide open with her tongue out, her eyes rolled "
             "up to the lens, half-lidded, a light blush. ")

MATERIAL = ("The semen has milky depth and is not a flat paint white: a dense cream-white core with "
            "thinner translucent edges that let her skin show faintly through, faintly warm amber in "
            "the thinnest parts, glossy and wet. It is not glue and it does not look like cream. ")

SLOW = ("His cock pulses three times and no more: once, then again about a second later, then once more. "
        "The semen comes out slowly and heavily: it does not shoot and does not spray, it only travels a "
        "few inches and drops onto her lower lip, where it heaps up. Each pulse pushes one single heavy "
        "rope out of the slit at the tip - one stream only, it never splits into two - uneven and lumpy, "
        "bulbous where it lands and thinner where it stretches; nothing continues past her face and "
        "nothing goes over her head. The first pulse is the heaviest and the next two are weaker; after "
        "the third nothing more comes out, the last few drops only ooze slowly from the tip. On each "
        "pulse the shaft kicks upward a little and settles back down. His glans stays bare and clean, no "
        "semen sits on the tip and none pools there. The ropes do not cross her nose or her cheek. Where "
        "the drops touch each other they merge into small glossy pools on her lower lip and her chin, and "
        "a slow heavy drip runs from her chin, dragging a thin translucent trail above it. She flinches "
        "at each pulse, then looks into the lens with half-lidded eyes and a light blush, flushed. The "
        "camera does not move.")

SOUND = ("\n\noverall_soundscape: three soft wet spurts about a second apart, one low male groan, her "
         "breath catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

LORA = "h3nsfw/epic_cumshots.safetensors"


def job(name, head, strength, image):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": image,
            "width": 768, "height": 1152, "length": 124, "seed": 940,
            "nsfw_lora": LORA, "nsfw_strength": strength,
            "prompt": head + MATERIAL + SLOW + SOUND}


rows = [
    job("k13_slow_p1_06", HEAD_P1, 0.6, P1),
    job("k13_slow_p1_05", HEAD_P1, 0.5, P1),
    job("k13_slow_wide_06", HEAD_WIDE, 0.6, WIDE),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
