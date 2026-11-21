"""Generate jobs/k17.jsonl - round 13, the glans rule on the two tiers that still bead.

Owner (2026-11-21): "the cum needs to not pool on the glans for cumshots like that. it would only
happen for a low strength shot that doesnt reach her face and even then it would almost never pool
like that - it would likely drip down the front of the glans facing away from the camera in a pov."

Checked at 1:1 across the tiers (analysis/cum-ref/mat/glans_dial.jpg):

  k14 (high)     the glans is coated in a thick white patch   -> must be fixed
  k15 (bounded)  a white blob sits on the glans               -> must be fixed
  k16_medium     glans clean, only a wet gloss                -> this is what all tiers need
  k16_low        a small drop pools on the visible front      -> should run down the far side

The medium tier came out clean simply because the amount is smaller, so the rule needs to be
stronger for the tiers that emit more. Two clips:

  k17_high_clean  k14's exact dynamics with the stronger glans wording
  k17_low_far     k16_low with "the little that stays runs down the far side of the glans, away from
                  the camera, so the visible top of the head stays clean" - the owner's own
                  description of where the residue goes in a POV.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k17.jsonl"))

P1 = r"gallery\refs\cumshot\p1_pose.png"

HEAD_P1 = ("integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed "
           "camera. A young adult Asian woman in her mid-twenties with long black hair in pink-streaked "
           "twin tails and a silver choker kneels between the viewer's legs, holding his erect adult "
           "cock upright an inch below her open mouth, her tongue out, her eyes on the lens. ")

MATERIAL = ("The semen is glossy and milky white, slightly translucent where it spreads thin, and thin "
            "enough to run: it is a normal ropy fluid, not a dense cream and not a gel. ")

GLANS_HIGH = ("His glans stays completely bare: not a drop of semen sits on the head of his cock, none "
              "pools on it and nothing runs back down onto it. The head is only wet and glossy with no "
              "white on it at all. Where the drops touch each other they merge into small glossy pools on "
              "her lips and chin, and a slow heavy drip runs from her chin, dragging a thin translucent "
              "trail above it. ")

GLANS_LOW = ("Almost nothing is left on his cock: the little that stays at the opening runs down the far "
             "side of the glans, away from the camera, so the visible top of the head stays clean and "
             "only wet. Where the drops touch they merge into a small glossy pool on her lip, and a slow "
             "drip runs from her chin. ")

REACTION = ("She flinches at each pulse, then looks into the lens with half-lidded eyes and a light blush, "
            "flushed. The camera does not move.")

HIGH = ("His cock pulses three times and no more. Each pulse throws one single short rope of semen straight "
        "up into her face - one stream only, it never splits into two. Each rope is only an inch or two "
        "long: it leaves the tip, crosses the small gap and hits her lips and her chin hard, splashing a "
        "little where it lands, and stops there. The rope does not reach her nose, never goes past her "
        "face and never goes over her head, and nothing lands behind her. The first pulse is the strongest "
        "and splashes the most; the next two are weaker and mostly just hit and stay. On each pulse the "
        "shaft kicks upward a little and settles back down and the veins stand out. " + GLANS_HIGH + REACTION)

LOW = ("His cock pulses twice, then the rest only oozes. A small amount of semen: the first pulse sends one "
       "short thin rope that lands on her lips and stops there, and the second a thinner one that barely "
       "reaches her lip. After that nothing more shoots and only a few drops ooze slowly from the tip. "
       "The single rope is narrow and there is no spray and no splash. The shaft does not kick: it only "
       "swells slightly and the veins stand out a little before each pulse, and the cock stays mostly "
       "still. " + GLANS_LOW + REACTION)

SOUND = ("\n\noverall_soundscape: soft wet spurts about a second apart, one low male groan, her breath "
         "catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

LORA = "h3nsfw/epic_cumshots.safetensors"


def job(name, body, seed):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": P1,
            "width": 768, "height": 1152, "length": 124, "seed": seed,
            "nsfw_lora": LORA, "nsfw_strength": 0.6,
            "prompt": HEAD_P1 + MATERIAL + body + SOUND}


rows = [
    job("k17_high_clean", HIGH, 980),
    job("k17_low_far", LOW, 981),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
