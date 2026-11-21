"""Generate jobs/k16.jsonl - round 12, the amount/twitch dial below k14.

Owner verdict (2026-11-21): k14 is "the best so far" and is now **the maximum exaggeration
standard**. They want the same scene turned down to **medium (the default)** and **low**, on two
axes at once: the amount per shot and the twitching.

k14 is copied as the high tier of `cumshot_high`. This round renders the two tiers below it by
scaling exactly the two axes the owner named, and leaving everything else (three decaying pulses,
one stream from the slit, bare glans, impact + a little splash, coalescing drops, the drip with its
translucent trail, fixed camera) untouched:

  twitch  high   the shaft kicks upward on every pulse and the veins stand out
          medium a small twitch on each pulse, the shaft barely moves
          low    no kick at all, only a swell of the veins before each pulse
  amount  high   a full rope each pulse, the first splashes on her face
          medium shorter, thinner ropes; only the first reaches her face with any splash
          low    one short thin rope, the next two only ooze to her lips

The fluid stays the k14 one (glossy, slightly translucent, ropy, not a gel) - the owner asked to
turn the goopiness down one notch at k14 and did not ask for it to move again.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k16.jsonl"))

P1 = r"gallery\refs\cumshot\p1_pose.png"

HEAD_P1 = ("integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed "
           "camera. A young adult Asian woman in her mid-twenties with long black hair in pink-streaked "
           "twin tails and a silver choker kneels between the viewer's legs, holding his erect adult "
           "cock upright an inch below her open mouth, her tongue out, her eyes on the lens. ")

MATERIAL = ("The semen is glossy and milky white, slightly translucent where it spreads thin, and thin "
            "enough to run: it is a normal ropy fluid, not a dense cream and not a gel. ")

TAIL = ("His glans stays bare and clean, no semen sits on the tip and none pools there. Where the drops "
        "touch each other they merge into small glossy pools on her lips and chin, and a slow heavy drip "
        "runs from her chin, dragging a thin translucent trail above it. She flinches at each pulse, then "
        "looks into the lens with half-lidded eyes and a light blush, flushed. The camera does not move.")

SOUND = ("\n\noverall_soundscape: soft wet spurts about a second apart, one low male groan, her breath "
         "catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

MEDIUM = ("His cock pulses three times and no more. Each pulse throws one single short thin rope of semen "
          "straight up into her face - one stream only, it never splits into two - and each rope is only "
          "an inch or two long: it leaves the tip, crosses the small gap and lands on her lips and her "
          "chin, and stops there. The first rope splashes a little where it hits; the next two are weaker "
          "and barely reach her lips. The amount is modest and the ropes are narrow. The rope never goes "
          "past her face and nothing lands behind her. The shaft gives a small twitch on each pulse and "
          "barely moves, and the veins swell a little. " + TAIL)

LOW = ("His cock pulses twice, then the rest only oozes. A small amount of semen: the first pulse sends one "
       "short thin rope that lands on her lips and stops there, and the second a thinner one that barely "
       "reaches her lip. After that nothing more shoots and only a few drops ooze slowly from the tip. "
       "The single rope is narrow and there is no spray and no splash. The shaft does not kick: it only "
       "swells slightly and the veins stand out a little before each pulse, and the cock stays mostly "
       "still. " + TAIL)

LORA = "h3nsfw/epic_cumshots.safetensors"


def job(name, body, strength=0.6, seed=970):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": P1,
            "width": 768, "height": 1152, "length": 124, "seed": seed,
            "nsfw_lora": LORA, "nsfw_strength": strength,
            "prompt": HEAD_P1 + MATERIAL + body + SOUND}


rows = [
    job("k16_medium", MEDIUM),
    job("k16_low", LOW),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
