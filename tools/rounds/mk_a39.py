#!/usr/bin/env python3
"""mk_a39.py - k22 take 4: the side take-in without the cum (there is no visible shot), no cheek
puffing and no fluid drip.  Clean suction only."""
import json

P = ("integrated_multimodal_description: [Shot 1] A 2D anime clip in a clean cel-shaded TV-anime style, "
     "one fixed camera. Side view, profile: a young adult woman with short silver hair in a single braid, "
     "a mole under her eye and a small fang, kneels leaning forward and strokes his erect cock with her "
     "hand, her eyes locked on the camera. She leans in until her lips are around the head and stops "
     "there: the head goes inside her mouth past her lips, her lips seal in front of the shaft, and the "
     "cock does not slide behind her mouth or through her cheek. Her cheeks stay slim and flat - no bulge "
     "in her cheek and no puffing. She sucks with two small sucking bobs and a swallow; her mouth is only "
     "wet with saliva, with no semen and no drip. She keeps sucking, then slowly pulls off. Her breasts "
     "press against the bed, her braid swings, her shoulders work. The camera shakes very slightly with "
     "her motion.\n\n"
     "overall_soundscape: close-miked Foley, loud and present, clearly audible over a bedroom room tone, "
     "no music and no speech: a wet suction as her lips close around the head, a small pop as she pulls "
     "off, a quiet swallow, her breath through her nose, one low male groan. No spurt, no drip, no "
     "chewing, no crunch, no slurp.\n\nnon_diegetic_music: N/A")

j = {"name": "k23_side_takein_clean", "wf": "wf_h3vid_i2v_lora2.json",
     "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
     "image": "gens\\a34\\n2_side_handjob_a_00001_.png",
     "width": 1152, "height": 768, "length": 124, "seed": 93020,
     "nsfw_lora": "h3nsfw/MM-H3-Blwjob-v3.safetensors", "nsfw_strength": 0.65,
     "motion_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "motion_strength": 0.5,
     "prompt": P}
with open("jobs/a39_side_takein_clean.jsonl", "w", encoding="utf-8") as f:
    f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote k23_side_takein_clean")
