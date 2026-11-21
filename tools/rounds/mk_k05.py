"""Generate jobs/k05.jsonl - round 2, the rope sweep.

Owner feedback on k01_control_rope08 (2026-11-20), read at full resolution:

  * the rope geometry is right - this clip is "close";
  * the VOLUME per rope is exaggerated, and a fat two-cord version could be an option for people
    into that, but the preference is MORE ropes with LESS volume each;
  * the way it pools on the glans is completely unrealistic - almost nothing is left on the glans
    after a cum shot like that;
  * (from the frame: the two fat cords also run up across her nose, which is placement, not
    volume.)

So this round keeps the working base (p1 keyframe, epic_cumshots, "rope ... shoots from the tip")
and only moves the three things the owner named:

  1. COUNT / VOLUME: "four or five thin ropes in a row, about a second apart, each one narrow",
     in a 124-frame clip so five beats actually fit (81 frames only leaves room for three).
  2. GLANS: "his glans stays bare and clean between pulses, no semen sits on the tip" + "left wet
     with glossy wetness only".
  3. PLACEMENT: "the ropes do not cross her nose or her cheek" - they land on her tongue and
     lower lip.

The strength sweep (0.8 / 0.6 / 0.5) is the other half: 0.8 is what made the fat cord, but v14a
showed that lowering the strength with "thin, breaks into droplets" wording gave mist instead of
a rope. Dense wording at a lower strength has not been tried, so 0.5 and 0.6 may thin the ropes
without misting them.

Two extra keyframes:
  * k4_wide_clean - the tip sits a hand's width below her chin, off-centre, so the ropes and the
    chin drip have somewhere to go that is not the glans.
  * p1_spurt_air - a keyframe with semen already in the air and touching the glans; the clip only
    has to lift it off the glans and resolve it. Tests the "glans left clean" rule directly.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k05.jsonl"))
REF = r"gallery\refs\cumshot"

HEAD = ("integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed "
        "camera. A young adult Asian woman in her mid-twenties with long black hair in pink-streaked "
        "twin tails and a silver choker kneels between the viewer's legs, holding his erect adult "
        "cock upright an inch below her open mouth, her tongue out, her eyes on the lens. ")

OUTCOME = (" After the last one the semen sits in a few small glossy milky pools on her tongue and her "
           "lower lip and a slow heavy drip runs from her chin. She flinches at each spurt, then looks "
           "into the lens with half-lidded eyes and a light blush, flushed. The camera does not move.")

SOUND = ("\n\noverall_soundscape: four or five soft wet spurts about a second apart, one low male groan, "
         "her breath catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

ROPES = (HEAD +
         "His cock pulses again and again. With each pulse a short thin rope of milky semen shoots from "
         "the tip and lands on her tongue and her lower lip, where it stays: four or five thin ropes in "
         "a row about a second apart, each one narrow and glossy and translucent milky, none of them "
         "thick. The ropes do not cross her nose or her cheek. His glans stays bare and clean between "
         "pulses, no semen sits on the tip, the tip is only wet and glossy."
         + OUTCOME + SOUND)

AIR = ("integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed camera. "
       "A young adult Asian woman in her mid-twenties with long black hair in pink-streaked twin tails "
       "kneels between the viewer's legs with her mouth open and her tongue out; a thick rope of milky "
       "semen hangs from her tongue down to the tip of his cock. ")
AIR_MOTION = ("It detaches from the tip and slides up onto her tongue as one narrow string, and his glans "
              "is left bare and clean, only wet. His cock pulses twice more and each pulse sends one "
              "thin short rope of milky semen from the tip onto her tongue, where it stays. The semen sits "
              "in small glossy milky pools on her tongue and lower lip and a slow heavy drip runs from her "
              "chin. She winces, then looks into the lens with half-lidded eyes, flushed. The camera does "
              "not move. No semen is left on the glans.")
AIR_SOUND = ("\n\noverall_soundscape: a soft wet slide, two soft wet spurts, one low male grunt, her breath, "
             "quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

LORA = "h3nsfw/epic_cumshots.safetensors"


def job(name, prompt, image, length, strength=None, wf="wf_h3vid_i2v_lora.json", why=""):
    j = {"name": name, "wf": wf, "image": image, "width": 768, "height": 1152,
         "length": length, "seed": 902, "prompt": prompt, "_why": why}
    if strength is not None:
        j["nsfw_lora"] = LORA
        j["nsfw_strength"] = strength
    return j


rows = [
    job("k05_ropes08", ROPES, os.path.join(REF, "p1_pose.png"), 124, 0.8,
        why="count/volume/glans wording at the strength that made the fat cord"),
    job("k05_ropes06", ROPES, os.path.join(REF, "p1_pose.png"), 124, 0.6,
        why="same wording, thinner via strength"),
    job("k05_ropes05", ROPES, os.path.join(REF, "p1_pose.png"), 124, 0.5,
        why="same wording, thinner via strength (tests whether 0.5 still misting was the wording)"),
    job("k05_ropes_wide", ROPES, os.path.abspath(os.path.join(HERE, "..", "..", "gens", "k04", "k4_wide_clean_00001_.png")),
        124, 0.8, why="wider gap so ropes and the chin drip do not fall back onto the glans"),
    job("k05_air08", AIR + AIR_MOTION + AIR_SOUND,
        os.path.abspath(os.path.join(HERE, "..", "..", "gens", "k04", "p1_spurt_air_00001_.png")), 124, 0.8,
        why="starts with semen touching the glans; must leave the glans clean"),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
for r in rows:
    print(" ", r["name"], r.get("nsfw_strength"), r["length"], "f")
