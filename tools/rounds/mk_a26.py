#!/usr/bin/env python3
"""mk_a26.py - motion variants on the k9 blowjob base + the cum-switch recipe.

k9 (jobs/a19_suction_perf.jsonl) is the owner-approved blowjob base. Each job changes only the
stroke/motion sentence and the sound line; the face, suction, saliva and eye contact stay.
"""
import json

K9 = next(json.loads(l) for l in open("jobs/a19_suction_perf.jsonl", encoding="utf-8") if l.strip())
BASE = K9["prompt"]
OLD = ("She slides her mouth up until only the head stays between her lips, purses her lips tight around it "
       "and sucks with a small wet pop, then slides down again until her nose is close to his body, a steady "
       "deep rhythm.")
assert OLD in BASE

IMG_DEEP = "C:\\Users\\headpats\\Documents\\goon-studio\\gens\\a11\\j2_suction_seal_a_00001_.png"
IMG_COCK = "C:\\Users\\headpats\\Documents\\goon-studio\\gens\\a04\\e1_fuzichoco_cockout_00001_.png"


def mk(name, img, seed, prompt, lora="h3nsfw/MM-H3-Blwjob-v3.safetensors", strength=0.65):
    return {"name": name, "wf": "wf_h3vid_i2v_lora2.json",
            "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors", "image": img,
            "width": 768, "height": 1152, "length": 124, "seed": seed,
            "nsfw_lora": lora, "nsfw_strength": strength,
            "motion_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "motion_strength": 0.5,
            "prompt": prompt}


PUSH = ("His hand grabs the back of her head and pushes her down; she takes him deeper until her nose presses "
        "against his body and holds it, her throat working. He pushes once more, holds her there for a beat, "
        "then releases and she pulls back up until only the head stays between her lips. He pushes her down "
        "again, harder, and holds her deep.")
TWO = ("Both of his hands come into frame, one on each side of her head, his fingers in her hair; he guides her "
       "up and down with both hands, then holds her deep with both hands, his thumbs on her temples, and lets "
       "her suck.")

jobs = [mk("k11_headgrab_push", IMG_DEEP, 93007, BASE.replace(OLD, PUSH)
           .replace("a soft suction hush as her mouth slides down the shaft, a wet mouth-purse and a small pop as she pulls up",
                    "a wet suction hush as her mouth is pushed down the shaft, a muffled gag and a swallow when she is held deep, a small pop as she pulls up, his hand in her hair")),
        mk("k12_two_hands", IMG_DEEP, 93008, BASE.replace(OLD, TWO)
           .replace("a soft suction hush as her mouth slides down the shaft, a wet mouth-purse and a small pop as she pulls up",
                    "a wet suction hush as her mouth slides down the shaft, both hands in her hair, a small pop as she pulls up"))]

TEASE = BASE.replace(
    "kneels between the viewer's legs with his cock deep in her mouth, her lips sealed around the shaft and her cheeks hollow and sucked in.",
    "kneels between the viewer's legs and holds his cock upright with one hand, the tip an inch below her open mouth, her tongue out, her eyes on the camera.").replace(
    OLD, "She licks the tip, kisses the glans, takes just the head between her lips and pulls off with a wet pop, "
         "teasing the slit with her tongue; then she opens wide and slides her mouth all the way down until her "
         "nose presses against his body, holds it deep, and looks up into the camera.")
jobs.append(mk("k13_tip_tease", IMG_COCK, 93009, TEASE))

SWITCH = ("integrated_multimodal_description: [Shot 1] A 2D anime clip in a clean cel-shaded TV-anime style, one fixed "
          "camera. POV from above: a young adult woman with short silver hair in a single braid, a mole under her "
          "eye and a small fang, kneels between the viewer's legs and strokes his erect cock with her hand, slow "
          "and tight, her eyes on the camera, her mouth open. He starts to cum: the shaft jerks and the first "
          "spurt starts, and the moment it starts she takes the head into her mouth and holds it there, her lips "
          "sealed around the glans, as the cock twitches and pulses in her mouth. She keeps it in her mouth, her "
          "cheeks hollow, swallowing, her eyes locked on the camera; a little semen escapes at the corner of her "
          "lips and runs down her chin. She holds him in her mouth until the twitching stops, then slowly pulls "
          "off with a milky thread. Her breasts press against his thighs, her shoulders work, her braid swings. "
          "The camera shakes very slightly with her motion.\n\n"
          "overall_soundscape: close-miked Foley, loud and present, clearly audible over a bedroom room tone, no "
          "music and no speech: a wet hand sliding on skin, a wet spurt and a muffled swallow as she takes him in "
          "her mouth, the soft wet pulses of the cock in her mouth, her breath through her nose, one low male "
          "groan. No chewing, no crunch, no slurp.\n\nnon_diegetic_music: N/A")
jobs.append(mk("k14_cum_switch", IMG_COCK, 93010, SWITCH,
               lora="h3nsfw/epic_cumshots.safetensors", strength=0.55))

with open("jobs/a26_motions.jsonl", "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote", [j["name"] for j in jobs])
