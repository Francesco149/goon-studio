"""Generate jobs/k08.jsonl - round 5, the combined recipe (splash fix + material push).

Two owner notes drive it:

  k05_ropes_wide   "closest, but there is an excessive amount of splash that doesn't make sense;
                    the way it drips onto his legs is good and realistic."
  k05_ropes05      "passable if the cum didn't have the glue look - a clear liquid with a pearl
                    opaque part suspended in it, not a uniformly opaque liquid."

Round 4 (k07) showed the material barely moves on prompt wording alone: pearl/clear/0.6 all still
render a uniform white string, because the material is in the epic_cumshots weights. So this round
does two things at once:

  * kills the SPLASH and keeps the DRIP: "there is no spray and nothing splatters across her face,
    only a few drops run off her chin and fall onto his thighs". The owner likes the run-off that
    reaches his thighs; they do not like the impact scatter.
  * pushes the material harder, including the negative form ("does not look like glue or paint",
    "not a uniform opaque white"), which the earlier rounds did not use.

Strength probe on the combined wording: 0.35 (does the LoRA loosen its material at low strength
while the wording keeps the ropes?), 0.5 (the k05/k06 winner) and 0.6 (in case the extra wording
strips the body out of the ropes). Plus the same at p1, because the owner called k05_ropes05
"passable" and it is the tighter framing.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k08.jsonl"))

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

MATERIAL = ("The semen is not a uniform opaque white and does not look like glue or paint: it is a mostly "
            "clear, glossy liquid with pearl-white clumps suspended in it, so the thin parts are see-through "
            "and wet and only the small clumps are opaque milk-white. ")

DYNAMICS = ("His cock pulses again and again. With each pulse a short thin rope of semen shoots from the tip "
            "and lands on her tongue and her lower lip. There is no spray and nothing splatters across her "
            "face; most of it stays on her tongue and lower lip, and only a few drops run off her chin and "
            "fall slowly onto his thighs. Four or five ropes in a row, about a second apart, each one narrow; "
            "some pulses only add to what is already there. The ropes do not cross her nose or her cheek. His "
            "glans stays bare and clean between pulses, no semen sits on the tip; the tip is only wet. After "
            "the last rope the patches gather into small heavy beads and begin to run slowly down her chin. "
            "She flinches at each spurt, then looks into the lens with half-lidded eyes and a light blush, "
            "flushed. The camera does not move.")

SOUND = ("\n\noverall_soundscape: four or five soft wet spurts about a second apart, one low male groan, her "
         "breath catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

LORA = "h3nsfw/epic_cumshots.safetensors"


def job(name, head, strength, seed=906, image=None):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": image or P1,
            "width": 768, "height": 1152, "length": 124, "seed": seed,
            "nsfw_lora": LORA, "nsfw_strength": strength,
            "prompt": head + MATERIAL + DYNAMICS + SOUND}


rows = [
    job("k08_wide05", HEAD_WIDE, 0.5, image=WIDE),
    job("k08_wide035", HEAD_WIDE, 0.35, image=WIDE),
    job("k08_wide06", HEAD_WIDE, 0.6, image=WIDE),
    job("k08_p1_05", HEAD_P1, 0.5),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
