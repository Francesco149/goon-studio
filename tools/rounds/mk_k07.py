"""Generate jobs/k07.jsonl - round 4, the material (owner: too gluey, needs to be heterogeneous).

Owner feedback:
  k05_ropes05  "could probably be passable if the cum didn't have that glue look - needs to be a bit
                more translucent. The texture of cum is like a clear liquid with a pearl opaque
                texture part suspended within, while this is more like a uniformly opaque liquid."

That is a material statement, not a dynamics one, so round 4 holds the dynamics (thin ropes, ~1 s
apart, glans bare, impact flattens, drip runs slowly) and moves ONLY the material wording.

Three wordings, one per clip, plus one repeat on the wide keyframe:

  pearl   the material described as the owner described it: a mostly clear glossy carrier with
          pearl-white opaque clumps suspended in it.
  clear   pushed further towards translucent, with pearly swirls, for the upper bound on
          transparency (docs warn that too far reads as water, so this is the probe).
  pearl06 the pearl wording at 0.6 instead of 0.5, in case the LoRA's opacity follows strength and
          the thinner ropes want a touch more LoRA to keep their body.

The LoRA's learned material is what makes the glue look, so this is a fight between the prompt and
the LoRA. If none of the three moves it, the material has to come from a keyframe or a different
LoRA, and that is a different session - hence the explicit "uniform opaque white" negative-ish
phrasing in each prompt.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k07.jsonl"))

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

DYNAMICS = ("His cock pulses again and again. With each pulse a short thin rope of semen shoots from the "
            "tip and lands on her tongue and her lower lip. On impact each rope flattens and spreads into "
            "a thin patch instead of staying a lump, and two or three small drops flick off beside it and "
            "fall onto his thighs. Four or five ropes in a row, about a second apart, each one narrow; some "
            "pulses only add to what is already on her tongue. Most of it stays on her tongue and lower lip, "
            "only a little splashes. The ropes do not cross her nose or her cheek. {MATERIAL} His glans "
            "stays bare and clean between pulses, no semen sits on the tip; the tip is only wet and glossy. "
            "After the last rope the patches gather into small heavy beads and begin to run slowly down her "
            "chin. She flinches at each spurt, then looks into the lens with half-lidded eyes and a light "
            "blush, flushed. The camera does not move.")

SOUND = ("\n\noverall_soundscape: four or five soft wet spurts about a second apart, one low male groan, "
         "her breath catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

PEARL = ("The semen is not a uniform milky white: it is a mostly clear, glossy liquid with pearl-white "
         "opaque clumps suspended inside it, so the milky parts float as separate pearly streaks and the "
         "wetter parts are see-through with her skin faintly visible through them.")

CLEAR = ("The semen is thin and translucent, closer to clear than to white, with pearly white swirls "
         "suspended in it: her skin shows through the thin parts and only the small clumps are opaque "
         "milk-white. It is glossy and wet, not a uniform opaque liquid.")

LORA = "h3nsfw/epic_cumshots.safetensors"


def job(name, head, material, strength, seed=905, image=P1):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": image,
            "width": 768, "height": 1152, "length": 124, "seed": seed,
            "nsfw_lora": LORA, "nsfw_strength": strength,
            "prompt": head + DYNAMICS.replace("{MATERIAL}", material) + SOUND}


rows = [
    job("k07_mat_pearl", HEAD_P1, PEARL, 0.5),
    job("k07_mat_clear", HEAD_P1, CLEAR, 0.5),
    job("k07_mat_pearl06", HEAD_P1, PEARL, 0.6),
    job("k07_mat_pearl_wide", HEAD_WIDE, PEARL, 0.5, image=WIDE),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
