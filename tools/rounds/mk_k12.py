"""Generate jobs/k12.jsonl - round 8, trajectory: the rope must STOP on her face.

Owner on k10_p1_04: "the way it flies backwards is a bit unrealistic. i'd expect it to stop on her
face. same for the other gens and the wide one is too perfectly in the middle and wouldnt expect it
to fly over her head."

Reading it precisely: the model draws the emission as a line that passes THROUGH the target and
keeps going, and on the wide keyframe it draws a perfect vertical line up the middle of the frame
that ends above her head. Both are impossible: a spurt terminates where it hits, and a real spurt
leaves at a slight angle, off the centre line.

So this round adds three things to the otherwise-settled recipes, and nothing else:

  1. TERMINATION - the far end of the rope stops on her lower lip and heaps up there, it does not
     cross her face and does not go over her head.
  2. ANGLE - the rope leaves at a slight angle and lands off-centre, not straight up the middle.
  3. SHAPE - the rope is uneven and lumpy, bulbous where it lands and thinner where it stretches,
     against the smooth uniform rod the last rounds produced (the refs are lumpy).

Rendered on the two settled bases (the normal recipe at 0.6 on p1 and 0.5 on the wide keyframe)
and on the goopy variant, because the goopy cord is the one most likely to keep its body when the
termination wording pulls it back.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k12.jsonl"))

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

TRAJECTORY = ("Each rope leaves the tip at a slight angle, off to one side rather than straight up the "
              "middle of the frame, and it is uneven and lumpy: bulbous and heavy where it lands, "
              "thinner where it stretches. The far end of each rope stops on her lower lip and heaps "
              "up there and goes no further; nothing continues past her face and nothing goes over her "
              "head. ")

NORMAL = ("His cock pulses three times and no more: once, then again about a second later, then once "
          "more. Each pulse sends one single narrow rope of semen out of the slit at the tip - one "
          "stream only, it never splits into two - and each rope is short and thin: a small amount "
          "that lands on her tongue and her lower lip and stays there. The first pulse is the strongest "
          "and the next two are weaker; after the third nothing more shoots, the last few drops only "
          "ooze slowly from the tip. On each pulse the shaft kicks upward a little and settles back "
          "down. His glans stays bare and clean, no semen sits on the tip and none pools there. The "
          "ropes do not cross her nose or her cheek. Where the drops touch each other they merge into "
          "small glossy pools on her tongue and lower lip, and a slow heavy drip runs from her chin, "
          "dragging a thin translucent trail above it. She flinches at each pulse, then looks into the "
          "lens with half-lidded eyes and a light blush, flushed. ")

GOOPY = ("His cock pulses three times and no more. The semen is extremely dense and semi-solid: creamy "
         "white, thick like melted wax or thick toothpaste, with rounded heavy edges. It does not spray "
         "and does not arc. Each pulse pushes one short heavy cord out of the slit at the tip - one "
         "stream only, never two - that tumbles slowly out and lands with no splash at all, piling up on "
         "itself in a thick mound on her lower lip. Nothing atomizes, no droplets fly off, and nothing "
         "lands outside her mouth and lips. His glans stays bare and clean. The mound clings and barely "
         "runs; a short stubby drip hangs from her chin without stretching. She flinches at each pulse, "
         "then looks into the lens with half-lidded eyes, flushed. ")

TAIL = "The camera does not move."

SOUND = ("\n\noverall_soundscape: three soft wet spurts about a second apart, one low male groan, her "
         "breath catching between them, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

LORA = "h3nsfw/epic_cumshots.safetensors"


def job(name, head, body, strength):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": None,
            "width": 768, "height": 1152, "length": 124, "seed": 930,
            "nsfw_lora": LORA, "nsfw_strength": strength,
            "prompt": head + MATERIAL + body + TRAJECTORY + TAIL + SOUND}


rows = [
    job("k12_normal_p1", HEAD_P1, NORMAL, 0.6),
    job("k12_normal_wide", HEAD_WIDE, NORMAL, 0.5),
    job("k12_goopy_p1", HEAD_P1, GOOPY, 0.6),
]
rows[0]["image"] = P1
rows[1]["image"] = WIDE
rows[2]["image"] = P1

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
