#!/usr/bin/env python3
"""mk_a36.py - cum switch take 2 on the front handjob keyframe: the shot lands on her tongue and
lips, then she closes her mouth around it and holds, eyes on the camera."""
import json

P = ("integrated_multimodal_description: [Shot 1] A 2D anime clip in a clean cel-shaded TV-anime "
     "style, one fixed camera. POV from above: a young adult woman with short silver hair in a single "
     "braid, a mole under her eye and a small fang, kneels between the viewer's legs and strokes his "
     "erect cock with her hand, her eyes locked on the camera. The cock pulses once: one short thick "
     "rope of semen shoots out of the tip and lands on her tongue and lips, not on her nose or eyes. "
     "At that moment she closes her lips around the head and holds it in her mouth, her eyes never "
     "leaving the camera, while the cock twitches and pulses in her mouth. She keeps it in her mouth, "
     "swallowing, her cheeks hollow, until the twitching stops; then she pulls off slowly, a milky "
     "thread between her lips and the tip. Her breasts press against his thighs, her shoulders work, "
     "her braid swings. The camera shakes very slightly with her motion.\n\n"
     "overall_soundscape: close-miked Foley, loud and present, clearly audible over a bedroom room "
     "tone, no music and no speech: a wet hand sliding on skin, a soft wet spurt, a muffled swallow as "
     "she takes him in her mouth, the soft wet pulses of the cock in her mouth, her breath through her "
     "nose, one low male groan. No chewing, no crunch, no slurp, no clicks.\n\nnon_diegetic_music: N/A")

j = {"name": "k20_cum_switch_front", "wf": "wf_h3vid_i2v_lora2.json",
     "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
     "image": "C:\\Users\\headpats\\Documents\\goon-studio\\gens\\a30\\n1_handjob_a_00001_.png",
     "width": 768, "height": 1152, "length": 124, "seed": 93016,
     "nsfw_lora": "h3nsfw/epic_cumshots.safetensors", "nsfw_strength": 0.5,
     "motion_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "motion_strength": 0.5,
     "prompt": P}
with open("jobs/a36_cum_switch_front2.jsonl", "w", encoding="utf-8") as f:
    f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote k20_cum_switch_front")
