"""Generate jobs/k14.jsonl - round 10, "straight into her face, a little splash", one notch thinner.

Owner on round 8/9: "it looks a bit unnatural how it shoots higher than her face then lands. in most
cases you'd have a scene where it shoots straight into her face with a little bit of splashing for
very strong shots. i think you need to turn down the goopyness one notch - the first gens are
already goopy and the goopy one is completely unrealistic."

Two corrections, and they interact:

  1. TRAJECTORY: not a lob that sails above her head and comes down. The rope goes straight from the
     tip into her face, hits it and stops there. A strong pulse splashes a little on impact; the weak
     ones just hit and stay. So the impact is the end of the event, and the splash is the *receipt*
     of the impact - the earlier rounds had it backwards (splash in mid-air, then a long arc).
  2. VISCOSITY, one notch down: everything since k10 read as too thick. Drop "dense", "semi-solid",
     "wax". Keep it opaque enough to be white, thin enough to run and to splash on impact.

That means the k13 hypothesis (slow and heavy, travels a few inches, drops onto her lip) is wrong:
it is the opposite of what the owner wants. k13 still runs for the record, but this round replaces
it. The material here is deliberately plainer than k07's - k07 stays the "heavy matter" ceiling and
the goopy preset is demoted to an extreme variant, not a look to aim at.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k14.jsonl"))

P1 = r"C:\Users\headpats\Documents\goon-studio\gallery\refs\cumshot\p1_pose.png"
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

# one notch thinner than k10/k12: opaque enough to be white, thin enough to run and to splash
MATERIAL = ("The semen is glossy and milky white, slightly translucent where it spreads thin, and thin "
            "enough to run: it is a normal ropy fluid, not a dense cream and not a gel. ")

DIRECT = ("His cock pulses three times and no more. Each pulse throws one single narrow rope of semen "
          "straight up into her face - one stream only, it never splits into two - and the rope hits her "
          "face and stops there, splashing a little against her lips, her chin and her nose where it "
          "lands, and staying there. It does not arc above her head and nothing lands behind her. The "
          "first pulse is the strongest and splashes the most; the next two are weaker and mostly just "
          "hit and stay. On each pulse the shaft kicks upward a little and settles back down, and the "
          "veins stand out. His glans stays bare and clean, no semen sits on the tip and none pools "
          "there. The ropes keep to her mouth and her chin and do not reach her eyes. Where the drops "
          "touch each other they merge into small glossy pools, and a slow heavy drip runs from her "
          "chin, dragging a thin translucent trail above it. She flinches at each pulse, then looks into "
          "the lens with half-lidded eyes and a light blush, flushed. The camera does not move.")

SOUND = ("\n\noverall_soundscape: three soft wet spurts about a second apart, one low male groan, her "
         "breath catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

LORA = "h3nsfw/epic_cumshots.safetensors"


def job(name, head, strength, image):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": image,
            "width": 768, "height": 1152, "length": 124, "seed": 950,
            "nsfw_lora": LORA, "nsfw_strength": strength,
            "prompt": head + MATERIAL + DIRECT + SOUND}


rows = [
    job("k14_direct_p1_06", HEAD_P1, 0.6, P1),
    job("k14_direct_p1_05", HEAD_P1, 0.5, P1),
    job("k14_direct_wide_06", HEAD_WIDE, 0.6, WIDE),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
