#!/usr/bin/env python3
"""mk_a35.py - the cum-switch on the side-view handjob keyframe: stroke, visible shot, then mouth."""
import json

P = ("integrated_multimodal_description: [Shot 1] A 2D anime clip in a clean cel-shaded TV-anime style, "
     "one fixed camera. Side view, profile: a young adult woman with short silver hair in a single braid, "
     "a mole under her eye and a small fang, kneels leaning forward and strokes his erect cock with her "
     "hand, slow and tight, her eyes locked on the camera. He starts to cum: the shaft kicks once and one "
     "short thick rope of semen shoots from the tip across the gap, onto her cheek and lips. The moment it "
     "starts she leans in and takes the head into her mouth, her lips sealed around the glans, her eyes "
     "never leaving the camera, as the cock twitches and pulses in her mouth. She keeps it in her mouth, "
     "swallowing, her cheeks hollow; a little semen escapes at the corner of her lips and runs down her "
     "chin. She holds him in her mouth until the twitching stops, then slowly pulls off with a milky "
     "thread. Her breasts press against the bed, her braid swings, her shoulders work. The camera shakes "
     "very slightly with her motion.\n\n"
     "overall_soundscape: close-miked Foley, loud and present, clearly audible over a bedroom room tone, no "
     "music and no speech: a wet hand sliding on skin, a soft wet spurt, a muffled swallow as she takes him "
     "in her mouth, the soft wet pulses of the cock in her mouth, her breath through her nose, one low male "
     "groan. No chewing, no crunch, no slurp, no clicks.\n\nnon_diegetic_music: N/A")

j = {"name": "k19_cum_switch_side", "wf": "wf_h3vid_i2v_lora2.json",
     "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
     "image": "C:\\Users\\headpats\\Documents\\goon-studio\\gens\\a34\\n2_side_handjob_b_00001_.png",
     "width": 1152, "height": 768, "length": 124, "seed": 93015,
     "nsfw_lora": "h3nsfw/epic_cumshots.safetensors", "nsfw_strength": 0.55,
     "motion_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "motion_strength": 0.5,
     "prompt": P}
with open("jobs/a35_cum_switch_side.jsonl", "w", encoding="utf-8") as f:
    f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote k19_cum_switch_side")
