"""mk_story_emilia.py - writes kit/stories/emilia_meadow.json (round a101); run: python mk_story_emilia.py kit/stories/emilia_meadow.json"""
import json, sys
SND = "overall_soundscape: close-miked Foley, loud and present, over a quiet outdoor ambience with a light breeze, no music and no speech: %s\n\nnon_diegetic_music: N/A"
NEG = ("worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts, watermark, text, subtitles, 3d, realistic, "
       "bad anatomy, extra fingers, extra hands, third hand, fused limbs, censored, mosaic censoring, bar censor")
S = {
 "name": "emilia_meadow",
 "about": "Five-shot oral scene on a sunny meadow after gallery/refs/art-study/refs/emillia.mp4 (EMILIA_2D_ANIMATION_ART_STUDY.md): low-angle straddle bounce, three-quarter blowjob, POV headpat, profile climax with a freeze, low-angle afterglow. Adult design study (Emilia LoRA, mature female). Round a101.",
 "ref": "gallery/refs/art-study/refs/emillia.mp4",
 "seed": 101001,
 "still": {"workflow": "wf_anima2_lora.json", "lora": "anima_Emilia_2-30.safetensors", "strength": 1.0,
           "width": 1248, "height": 832, "steps": 30, "cfg": 4.0, "negative": NEG},
 "clip": {"width": 1152, "height": 768, "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
          "motion_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors", "fps": 24, "max_len": 124, "seg_len": 49},
 "blocks": {
  "style": "masterpiece, best quality, year 2018, anime screenshot, anime coloring, cel shading, flat color, hard shadows, (shiny skin:1.1), glossy skin, (large white specular highlights:1.1), thin lineart",
  "character": "1girl, emilia (re:zero), long hair, grey hair, crown braid, hair flower, white flower, x hair ornament, hair ribbon, purple ribbon, blunt bangs, pointy ears, purple eyes, mature female, medium breasts",
  "outfit": "white shirt, off-shoulder shirt, bare shoulders, (purple leggings:1.1), skin tight",
  "partner": "1boy, hetero, red jacket, open jacket, track jacket, tan skin",
  "setting": "outdoors, meadow, green grass, blue sky, white clouds, daylight, sunny",
  "script_style": "A 2D anime clip in a clean cel-shaded TV-anime style, flat colours, hard-edged shadows and glossy white highlights on the skin, bright high-key midday daylight, one fixed camera.",
  "script_character": "a young adult woman with long silver hair in a crown braid, a white flower and an X-shaped clip in her hair, a purple ribbon, pointed elf ears and purple eyes, in a white off-shoulder top and tight purple leggings",
  "script_partner": "a man in an open red track jacket",
  "script_setting": "on a sunny green meadow under a bright blue sky with small white clouds"
 },
 "shots": [
  {"id": "s1", "seconds": 6.05, "timing": "on3", "template": "anime_ll_headgrab_push",
   "still": "{style}, {character}, {outfit}, {partner}, standing, fellatio, kneeling, leaning forward, facing away, from behind, from below, (ass focus:1.2), (huge ass:1.1), wide hips, back, braid, his red jacket above her shoulders, {setting}",
   "script": "integrated_multimodal_description: [Shot 1] {script_style} An extreme low angle from behind and below her, looking up past her hips into the blue sky: {script_character} kneels {script_setting}, bent forward with her face in the lap of {script_partner}, who stands in front of her. From here her raised hips in the tight purple leggings fill the frame and hide what she is doing; only her back, her braid and his red jacket show above them. She gives him a blowjob in a slow, deep rhythm, about one bob every three quarters of a second: each time her head dips, her hips rock back toward the camera and sway, then settle as she comes up. Her braid swings with each bob. The camera does not move.\n\n" + SND % "a muffled wet suction rhythm, the soft creak of her leggings as her hips rock, her breath, one low male groan."},
  {"id": "s2", "seconds": 5.45, "timing": "smooth", "template": "anime_ll_headgrab_push",
   "still": "{style}, {character}, {outfit}, {partner}, kneeling, leaning forward, fellatio, (penis in mouth:1.2), (lips sealed around penis:1.3), three-quarter view, from side, (looking up:1.1), furrowed brow, blush, upper body, detailed penis shaft, veins, uncensored, red jacket at the left edge, {setting}",
   "still_job": {"negative": NEG + ", tongue out, open mouth"},
   "script": "integrated_multimodal_description: [Shot 1] {script_style} Three-quarter view from the side, close on her head and shoulders: {script_character} kneels {script_setting} with his cock in her mouth; the open red jacket of {script_partner} fills the left edge of the frame. She bobs her head quickly along the shaft, about two strokes a second, down to the middle of the shaft and back up until only the head stays between her lips. Her lips stay sealed tight, her face drawn by the suction; her eyes stay locked upward on his face, her brows knit, her blush deepens. Her bangs bounce with every stroke and her top slips a little on her shoulder. The camera does not move.\n\n" + SND % "a quick wet suction rhythm with a small pop at the top of each stroke, her nose breathing, one low male groan at about two seconds. No chewing, no crunch."},
  {"id": "s3", "seconds": 5.63, "timing": "on2", "template": "anime_ll_headgrab_push",
   "still": "{style}, {character}, {outfit}, white boots, {partner}, pov, male pov, from above, muscular male, abs, pectorals, lying on stomach, between legs, legs up, fellatio, (penis in mouth:1.2), (headpat:1.2), (hand on another's head:1.2), looking up, half-closed eyes, blush, uncensored, {setting}",
   "script": "integrated_multimodal_description: [Shot 1] {script_style} POV from above, looking down past the bare chest and open red jacket of {script_partner}: {script_character} lies on her stomach in the grass between his legs with his cock in her mouth, her booted feet kicked up behind her. She bobs her head slowly and steadily, her lips sealed around the shaft. His hand rests on top of her head and slowly strokes down her silver hair, pressing it softly; each time his hand strokes her, her eyes half close and her blush deepens, then she looks up at him again. The camera does not move.\n\n" + SND % "a slow wet suction hush on each stroke, his hand brushing her hair, his deep breathing, one low groan."},
  {"id": "s4", "seconds": 3.25, "timing": "on2", "hold": [{"at": 1.3, "frames": 28}], "template": "anime_ll_cumshot", "clip_job": {"nsfw_strength": 0.5},
   "still": "{style}, {character}, {outfit}, {partner}, close-up, side view, profile, fellatio, deepthroat, (penis in mouth:1.2), (closed eyes:1.1), squeezing eyes shut, tears, (cum in mouth:1.2), (cum overflow:1.1), cum on chin, hand on another's head, blush, uncensored, blue sky",
   "script": "integrated_multimodal_description: [Shot 1] {script_style} Extreme close-up from the side on her face against the blue sky: {script_character} has his cock deep in her mouth and the hand of {script_partner} holds the back of her head. He climaxes in three strong pulses: thick white cum fills her mouth and wells out past her sealed lips, running in thick ropes down her chin. Her eyes squeeze shut, a tear forms at the corner of her eye, her blush flares bright. After the last pulse everything holds still. The camera does not move.\n\n" + SND % "his long low groan of release, a thick wet overflow at her lips, her muffled breath through her nose."},
  {"id": "s5", "seconds": 4.97, "timing": "on3", "hold": [{"at": 3.0, "frames": 10}], "template": "anime_ll_cumshot", "clip_job": {"nsfw_strength": 0.4},
   "still": "{style}, {character}, {outfit}, from below, close-up, face focus, head tilted back, (ahegao:1.1), rolling eyes, half-closed eyes, open mouth, (tongue out:1.2), (cum on tongue:1.2), cum in mouth, (cum string:1.1), cum on chin, upper teeth, panting, blush, blue sky, white clouds, daylight",
   "script": "integrated_multimodal_description: [Shot 1] {script_style} A low angle from below her chin against the bright blue sky: {script_character} has her head tilted back, dazed, her eyes half closed and rolled up, her mouth hanging open with her tongue out, white cum pooled on her tongue and thin strings of it hanging from her lips down to her chin. She breathes slowly and shallowly, her chest and throat rising and falling; the strings sway and stretch, one thins out and a single drop falls. Otherwise she stays still. The camera does not move.\n\n" + SND % "her quiet shallow panting, a soft breeze, nothing else."}
 ]
}
json.dump(S, open(sys.argv[1], "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
