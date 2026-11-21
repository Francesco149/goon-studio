#!/usr/bin/env python3
"""mk_a37.py - side cum switch, take 2: the rope goes straight forward into her mouth, then she
sucks (hollow cheeks, small bobs, a swallow) instead of going static."""
import json

P = ("integrated_multimodal_description: [Shot 1] A 2D anime clip in a clean cel-shaded TV-anime style, "
     "one fixed camera. Side view, profile: a young adult woman with short silver hair in a single braid, "
     "a mole under her eye and a small fang, kneels leaning forward and strokes his erect cock with her "
     "hand, her eyes locked on the camera. The cock pulses once and one short thick rope of semen shoots "
     "straight forward out of the tip, across the gap, into her open mouth and onto her lips - it goes "
     "forward, not sideways. The moment it lands she closes her lips around the head and sucks: her cheeks "
     "hollow and pull in, her lips purse around the shaft, her head gives two small sucking bobs, a "
     "swallow, and a little semen escapes at the corner of her lips and runs down her chin. She keeps "
     "sucking until the twitching stops, then slowly pulls off with a milky thread. Her breasts press "
     "against the bed, her braid swings, her shoulders work. The camera shakes very slightly with her "
     "motion.\n\n"
     "overall_soundscape: close-miked Foley, loud and present, clearly audible over a bedroom room tone, "
     "no music and no speech: a wet hand sliding on skin, a soft wet spurt forward, a muffled swallow, a "
     "wet suction as she sucks the head, her breath through her nose, one low male groan. No chewing, no "
     "crunch, no slurp, no clicks.\n\nnon_diegetic_music: N/A")

j = {"name": "k21_cum_switch_side_v2", "wf": "wf_h3vid_i2v_lora2.json",
     "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
     "image": "C:\\Users\\headpats\\Documents\\goon-studio\\gens\\a34\\n2_side_handjob_b_00001_.png",
     "width": 1152, "height": 768, "length": 124, "seed": 93017,
     "nsfw_lora": "h3nsfw/epic_cumshots.safetensors", "nsfw_strength": 0.55,
     "motion_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "motion_strength": 0.5,
     "prompt": P}
with open("jobs/a37_cum_switch_side2.jsonl", "w", encoding="utf-8") as f:
    f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote k21_cum_switch_side_v2")
