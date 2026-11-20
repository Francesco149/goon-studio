"""Generate jobs/k06.jsonl - round 3, impact behaviour at the winning combination.

Owner feedback, in order (2026-11-20):

  k01_control_rope08  "close, but the volume per rope is exaggerated (that fat version could be an
                       option for those into it); I'd prefer more ropes, less volume; the way it
                       pools on the glans is completely unrealistic - almost none is left there."
  k05_ropes08         "closer to the dynamics we want for exaggerated cumshots - the cadence and
                       the rope-shoot dynamic are there. But the way it sticks to her face is not
                       entirely realistic. Some shots splash like they're less viscous and then
                       drip down slowly. And not all shots produce a visible extra rope on her
                       face."
  k05_ropes_wide /05   "closest, especially wide - but there is an excessive amount of splash
                       that simply doesn't make sense. The way it drips onto his legs is good and
                       realistic."

So the recipe is close to settled: wide-gap keyframe, epic_cumshots 0.5, "four or five thin ropes
about a second apart", glans stays bare. What round 3 changes is only the IMPACT:

  * on landing each rope flattens and spreads instead of sitting as a lump (the owner's
    "splash like they're less viscous, then drip down slowly" is exactly the Gemini study's
    impact paragraph: the leading bolus pancakes outward, the viscous tail collapses into raised
    beads that run slowly under gravity);
  * only two or three drops flick off and reach his thighs - "only a little splashes", against
    the wide clip's excessive scatter;
  * not every pulse has to leave a visible new rope - "some pulses only add to what is already
    there";
  * the deposits gather into heavy beads and start to run slowly, which is the drip the owner
    liked on his legs.

Three clips: the recipe at 0.5 and 0.4 (is thinner still a rope, or does it mist like v14a?), and
the 0.5 recipe on a second seed to see whether it survives a reseed before it becomes a template.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k06.jsonl"))

HEAD = ("integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed "
        "camera. A young adult Asian woman in her mid-twenties with long black hair in pink-streaked "
        "twin tails and a silver choker kneels between the viewer's legs. She holds his erect adult "
        "cock in her hand low between his thighs, the tip a hand's width below her chin and a little "
        "to one side, her head tilted down, her mouth wide open with her tongue out, her eyes rolled "
        "up to the lens, half-lidded, a light blush. ")

IMPACT = ("His cock pulses again and again. With each pulse a short thin rope of milky semen shoots "
          "from the tip and lands on her tongue and her lower lip. On impact each rope flattens and "
          "spreads into a thin glossy patch instead of staying a lump, and two or three small drops "
          "flick off beside it and fall onto his thighs. Four or five ropes in a row, about a second "
          "apart, each one narrow and translucent milky; some pulses only add to what is already on "
          "her tongue. Most of it stays on her tongue and lower lip, only a little splashes. The ropes "
          "do not cross her nose or her cheek. His glans stays bare and clean between pulses, no semen "
          "sits on the tip; the tip is only wet and glossy. After the last rope the thin patches gather "
          "into small heavy beads and begin to run slowly down her chin. She flinches at each spurt, "
          "then looks into the lens with half-lidded eyes and a light blush, flushed. The camera does "
          "not move.")

SOUND = ("\n\noverall_soundscape: four or five soft wet spurts about a second apart, one low male groan, "
         "her breath catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

LORA = "h3nsfw/epic_cumshots.safetensors"
WIDE = os.path.abspath(os.path.join(HERE, "..", "..", "gens", "k04", "k4_wide_clean_00001_.png"))


def job(name, seed, strength):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": WIDE,
            "width": 768, "height": 1152, "length": 124, "seed": seed,
            "nsfw_lora": LORA, "nsfw_strength": strength,
            "prompt": HEAD + IMPACT + SOUND}


rows = [
    job("k06_wide05", 903, 0.5),
    job("k06_wide04", 903, 0.4),
    job("k06_wide05b", 904, 0.5),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
