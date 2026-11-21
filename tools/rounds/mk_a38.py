#!/usr/bin/env python3
"""mk_a38.py - side cum switch, take 3: the mouth must close around the head (the glans goes past
her lips), not slide behind the mouth.  Uses the closer side handjob keyframe (n2_a)."""
import json

P = ("integrated_multimodal_description: [Shot 1] A 2D anime clip in a clean cel-shaded TV-anime style, "
     "one fixed camera. Side view, profile: a young adult woman with short silver hair in a single braid, "
     "a mole under her eye and a small fang, kneels leaning forward and strokes his erect cock with her "
     "hand, her eyes locked on the camera. The cock pulses once and one short thick rope of semen shoots "
     "straight forward out of the tip, into her open mouth and onto her lips. She leans in until her lips "
     "are around the head and stops there: the head goes inside her mouth past her lips, her lips seal in "
     "front of the shaft, and the cock does not slide behind her mouth or through her cheek. She sucks: "
     "her cheeks hollow and pull in, her head gives two small sucking bobs, a swallow, and a little semen "
     "escapes at the corner of her lips. She keeps sucking until the twitching stops, then slowly pulls "
     "off with a milky thread. Her breasts press against the bed, her braid swings, her shoulders work. "
     "The camera shakes very slightly with her motion.\n\n"
     "overall_soundscape: close-miked Foley, loud and present, clearly audible over a bedroom room tone, "
     "no music and no speech: a wet hand sliding on skin, a soft wet spurt, a wet suction as her lips "
     "close around the head, a muffled swallow, her breath through her nose, one low male groan. No "
     "chewing, no crunch, no slurp, no clicks.\n\nnon_diegetic_music: N/A")

j = {"name": "k22_cum_switch_side_v3", "wf": "wf_h3vid_i2v_lora2.json",
     "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
     "image": "C:\\Users\\headpats\\Documents\\goon-studio\\gens\\a34\\n2_side_handjob_a_00001_.png",
     "width": 1152, "height": 768, "length": 124, "seed": 93018,
     "nsfw_lora": "h3nsfw/epic_cumshots.safetensors", "nsfw_strength": 0.55,
     "motion_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "motion_strength": 0.45,
     "prompt": P}
with open("jobs/a38_cum_switch_side3.jsonl", "w", encoding="utf-8") as f:
    f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote k22_cum_switch_side_v3")
