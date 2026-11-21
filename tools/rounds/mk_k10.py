"""Generate jobs/k10.jsonl - round 6, k07's optics with a lower, single, slower spurt cadence.

Owner feedback on round 4 (k07):
  k07_mat_pearl06 and k07_mat_clear are "the closest in terms of the optics of the fluid" - so the
  material wording below is the one to keep. My earlier note that "the material did not move" was
  wrong: judged at 200 px the ropes look alike, but at full size the pearl/clear wording gives the
  fluid its milky depth, and the owner reads that as the win.
  Against those two clips: "the shots frequency is too high", "the way they frequently split into
  2 streams is a bit unrealistic", and "dial down the amount per shot, with this being the absolute
  exaggerated maximum for people who are into that".

So this round keeps k07's keyframe (p1), material wording and strengths, and changes exactly three
things, each with a source in the updated Gemini study (gallery/refs/art-study):

  1. FEWER SHOTS, DECAYING. §8.2: spurt 1 -> 2 is 0.8 s, then 0.9-1.0 s, then 1.2-1.5 s, and the
     late ones stop arcing and just spill. Three pulses in a 124-frame clip, the last one oozing -
     not "four or five ropes about a second apart".
  2. ONE STREAM. §8.2: the emission leaves the meatus, a single vertical slit that gapes before
     each spurt. Describing the slit as the exit ("one narrow rope from the slit at the tip, one
     stream only") gives the model one hole to draw from; "two streams" has no second hole.
  3. LESS PER SHOT. "a small amount", "short", "thin", with the first the strongest and the rest
     weaker. k07's volume becomes the `cumshot_heavy` ceiling.

Material wording kept from k07 but sharpened with §4.3's optics: a dense cream-white core, thin
edges that are translucent and faintly amber, milky depth rather than flat paint-white.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k10.jsonl"))

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

MATERIAL = ("The semen has milky depth and is not a flat paint white: a dense cream-white core with "
            "thinner translucent edges that let her skin show faintly through, faintly warm amber in "
            "the thinnest parts, glossy and wet. It is not glue and it does not look like cream. ")

# three decaying pulses, one stream each, small amount, bare glans, coalescing drops
DYNAMICS = ("His cock pulses three times and no more: once, then again about a second later, then "
            "once more. Each pulse sends one single narrow rope of semen out of the slit at the tip - "
            "one stream only, it never splits into two - and each rope is short and thin: a small "
            "amount that lands on her tongue and her lower lip and stays there. The first pulse is the "
            "strongest and the next two are weaker; after the third nothing more shoots, the last few "
            "drops only ooze slowly from the tip. On each pulse the shaft kicks upward a little and "
            "settles back down. His glans stays bare and clean, no semen sits on the tip and none pools "
            "there. The ropes do not cross her nose or her cheek. Where the drops touch each other they "
            "merge into small glossy pools on her tongue and lower lip, and a slow heavy drip runs from "
            "her chin, dragging a thin translucent trail above it. She flinches at each pulse, then "
            "looks into the lens with half-lidded eyes and a light blush, flushed. The camera does not "
            "move.")

SOUND = ("\n\noverall_soundscape: three soft wet spurts about a second apart, one low male groan, her "
         "breath catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

LORA = "h3nsfw/epic_cumshots.safetensors"


def job(name, head, strength, seed, image):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": image,
            "width": 768, "height": 1152, "length": 124, "seed": seed,
            "nsfw_lora": LORA, "nsfw_strength": strength,
            "prompt": head + MATERIAL + DYNAMICS + SOUND}


rows = [
    job("k10_p1_06", HEAD_P1, 0.6, 910, P1),
    job("k10_p1_05", HEAD_P1, 0.5, 910, P1),
    job("k10_p1_04", HEAD_P1, 0.4, 910, P1),
    job("k10_wide_06", HEAD_WIDE, 0.6, 910, WIDE),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
