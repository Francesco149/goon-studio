"""Generate jobs/k04.jsonl (local stills/edits) - round 2, keyframes for the composition fix.

What round 1 taught (k01, 8 clips, one seed, 768x1152/81f):

  * "bead / blob / lands / spreads" wording kills the face-thread that "rope" produced: every
    clip now has a dense milky mass ON her tongue and lips instead of a hair-thin line across
    her nose. Shape: fixed.
  * It also kills the EVENT. The mass is simply there from the first frames; nothing visibly
    leaves the tip. In the LoRA clips the "bead" sits stuck on the glans like a pearl; with no
    LoRA the base model puts a literal white sphere on the glans and then removes it.
  * EVERY variant still joins the tip to her face with some kind of column, and the p5-keyframe
    clips grow that column thicker over the clip. This is not a material problem: the cock is
    pointing straight up into her open mouth from ~1 inch away, so a drip off her chin falls
    onto the glans by construction.

So round 2 changes the geometry (the spurt/drip must have somewhere to go that is not the tip)
and adds an in-flight keyframe so the event exists in the picture before the motion starts.

  k4_wide_landed  (Krea2)  landed material in a pose where the tip sits a hand's width below
                           her chin and off-centre, so the heavy drip falls past it to her chest.
  k4_wide_clean   (Krea2)  the same pose with no cum, for the "visible spurt" video test.
  p1_spurt_air    (Qwen)   p1 with a thick spurt actually in the air, for the FL pair: the same
                           p1 pose as p1_landed_edit, so first and last frame are two states of
                           one photo and the clip only has to carry it from flight to landed.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k04.jsonl"))
REF = r"C:\Users\headpats\Documents\goon-studio\gallery\refs\cumshot"

CHAR = ("a young adult Asian woman in her mid-twenties, e-girl with long black hair in "
        "pink-streaked twin tails, wispy bangs, winged eyeliner, glossy lips and a silver heart "
        "choker, full natural breasts")

WIDE = (CHAR + ", kneels between the viewer's legs. She holds his erect adult penis in her hand low "
        "between his thighs, so the tip of his cock is a hand's width below her chin and slightly "
        "to one side, pointing up at her mouth; her head is tilted down, her mouth is wide open "
        "with her tongue out, her lips wet, her eyes rolled up to the lens, half-lidded, a light blush.")

LIGHT = (" Dim bedroom with pink LED glow, phone flash, natural skin with pores, slight grain, "
         "amateur photo.")

LANDED = (" Thick milky semen sits pooled on her tongue and on her lower lip in glossy milky patches, "
          "the skin visible through it, and a heavy slow drip hangs from her chin and falls clear of "
          "his cock onto her chest; the tip of his cock is clean and separate, nothing hangs between "
          "them.")

rows = [
    {"name": "k4_wide_landed", "wf": "wf_krea2_nsfw_8gb.json", "width": 896, "height": 1344,
     "steps": 6, "cfg": 1.0, "seed": 711,
     "prompt": "Photorealistic first-person POV close-up: " + WIDE + LANDED + LIGHT},
    {"name": "k4_wide_clean", "wf": "wf_krea2_nsfw_8gb.json", "width": 896, "height": 1344,
     "steps": 6, "cfg": 1.0, "seed": 712,
     "prompt": ("Photorealistic first-person POV close-up: " + WIDE +
                " A thin strand of saliva hangs from her lower lip to her tongue." + LIGHT)},
    {"name": "p1_spurt_air", "wf": "wf_qwen21_edit1.json", "width": 896, "height": 1344,
     "seed": 713, "image1": os.path.join(REF, "p1_pose.png"),
     "prompt": ("Edit this photo: add sperm in mid-air. A short thick spurt of milky white semen comes "
                "out of the tip of the cock and flies up through the air between the tip and her open "
                "mouth, halfway to her tongue; it is glossy milky white, thick and rounded at the front "
                "and trailing a thin tail. Keep her face, hair, makeup, eyes, mouth, tongue, the hand and "
                "the cock exactly as they are; the rest of the picture stays exactly the same. Same "
                "lighting, same camera, same framing.")},
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
