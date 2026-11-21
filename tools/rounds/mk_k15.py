"""Generate jobs/k15.jsonl - round 11, bound the LENGTH of the rope, keep the impact.

Where this stands after round 10 (k14):

  "hits her face and stops there, splashing a little where it lands" produced the splash and the
  impact streaks on her face, but the rope itself still overshoots - it goes on past her mouth to
  her nose and sometimes above her head. The owner's complaint is exactly that: "it shoots higher
  than her face then lands".

Round 9 (k13) proved that *velocity* wording shortens the rope ("does not shoot, travels only a few
inches"), but it went too far the other way: the emission became a limp drop onto her lower lip
instead of a hit.

So this round keeps k14's hard impact and splash and adds an explicit LENGTH bound - "the rope is
only an inch or two long" - instead of an endpoint instruction (which failed in k12) and instead of
lowering the velocity (which failed in k13). Two clips only: p1 at 0.6 and the wide keyframe at 0.6.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k15.jsonl"))

P1 = r"C:\Users\headpats\Documents\goon-studio\gallery\refs\cumshot\p1_pose.png"
WIDE = os.path.abspath(os.path.join(HERE, "..", "..", "gens", "k04", "k4_wide_clean_00001.png"))
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

MATERIAL = ("The semen is glossy and milky white, slightly translucent where it spreads thin, and thin "
            "enough to run: it is a normal ropy fluid, not a dense cream and not a gel. ")

BOUNDED = ("His cock pulses three times and no more. Each pulse throws one single short rope of semen "
           "straight up into her face - one stream only, it never splits into two. Each rope is only an "
           "inch or two long: it leaves the tip, crosses the small gap and hits her lips and her chin "
           "hard, splashing a little where it lands, and stops there. The rope does not reach her nose, "
           "never goes past her face and never goes over her head, and nothing lands behind her. The "
           "first pulse is the strongest and splashes the most; the next two are weaker and mostly just "
           "hit and stay. On each pulse the shaft kicks upward a little and settles back down and the "
           "veins stand out. His glans stays bare and clean, no semen sits on the tip and none pools "
           "there. Where the drops touch each other they merge into small glossy pools on her lips and "
           "chin, and a slow heavy drip runs from her chin, dragging a thin translucent trail above it. "
           "She flinches at each pulse, then looks into the lens with half-lidded eyes and a light "
           "blush, flushed. The camera does not move.")

SOUND = ("\n\noverall_soundscape: three soft wet spurts about a second apart, one low male groan, her "
         "breath catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

LORA = "h3nsfw/epic_cumshots.safetensors"


def job(name, head, image, strength=0.6, seed=960):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": image,
            "width": 768, "height": 1152, "length": 124, "seed": seed,
            "nsfw_lora": LORA, "nsfw_strength": strength,
            "prompt": head + MATERIAL + BOUNDED + SOUND}


rows = [
    job("k15_bounded_p1", HEAD_P1, P1),
    job("k15_bounded_wide", HEAD_WIDE, WIDE),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
