"""mk_a99.py - round a99: smooth / jiggly (live2d, h-game) motion from flat TV-style keyframes.

H3 renders the TV-style clips on 2s by itself (every odd frame a duplicate); the painted a88 k2_phys
is on 1s with soft-body jiggle. Same keyframes + seeds as known on-2s clips, script variants:
  base  - the a97 prompt (control, already rendered as lz_e_pz_wide_96101 / lz_v_bj_profile)
  phys  - + a micro-motion paragraph (squash, wobble, settle, follow-through, breathing)
  l2d   - phys + the opener says smooth, fluid h-game animation instead of TV anime
Anime timing off: the raw cadence is what is measured (docs/ANIME-TIMING.md, "Smooth motion").
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TV = "A 2D anime clip in a clean cel-shaded TV-anime style, flat colours, hard-edged shadows and glossy white highlights on the skin, one fixed camera."
L2D = ("A smooth, fluid 2D animation in the style of a high-frame-rate h-game scene, cel-shaded art with flat colours, "
       "hard-edged shadows and glossy white highlights on the skin, every movement soft and continuous, one fixed camera.")
SND_PZ = ("overall_soundscape: close-miked Foley, loud and present, clearly audible over a quiet bedroom room tone, no music and no speech: "
          "soft skin friction, a muffled wet squish at the bottom of each stroke, her breath, one low male grunt at about two seconds. "
          "No mouth sounds, no chewing, no crunch, no slurping.\n\nnon_diegetic_music: N/A")
SND_BJ = ("overall_soundscape: close-miked Foley, loud and present, clearly audible over a quiet bedroom room tone, no music and no speech: "
          "a wet suction hush on each stroke, a small pop at the top, her nose breathing, one low male grunt. "
          "No chewing, no crunch, no slurp.\n\nnon_diegetic_music: N/A")
PZ_LZ = ("Warm orange sunset light. POV from above: a young adult woman with long pink hair tied in two small side loops, blue eyes and a mole "
         "under her eye presses her large breasts together around his erect cock with both hands and slides them up and down the shaft in "
         "slow heavy strokes, about one stroke a second. On each up stroke the glans pushes out of the top of her cleavage; her fingers sink "
         "into her breasts, the flesh squashes and jiggles. She looks up into the camera with a smug, closed-mouth smile; her tongue stays in "
         "her mouth.")
PZ_SV = PZ_LZ.replace("long pink hair tied in two small side loops, blue eyes", "short silver hair in a single braid")
PZ_PHYS = ("Her breasts are soft and heavy: they bounce on every stroke, wobble and keep rippling for a moment after each one before they "
           "settle, the near breast lagging a beat behind her hands. Her shoulders and upper body rock with the rhythm, her hair bounces and "
           "sways behind the motion, her chest rises and falls with her breath, and a sweat sheen glides over her skin.")
BJ_LZ = ("Side profile, close on her head: a young adult woman with long pink hair tied in two small side loops, blue eyes and a mole under "
         "her eye has his cock in her mouth; his hand rests on the back of her head and guides her. She bobs her head along the shaft in long, "
         "clearly visible strokes, about one stroke a second: her head travels all the way down until her lips reach the middle of the shaft, "
         "then all the way back up until only the head stays between her lips. Her lips stay sealed around the shaft, her cheeks hollow as "
         "she sucks, her blush deepens, and saliva gathers at the corner of her mouth. Her hair sways with each stroke. At the bottom of a "
         "stroke he presses her head down for a moment, then lets her pull back.")
BJ_PHYS = ("Her whole body moves with each stroke: her shoulders and back rock forward and back, her hair loops swing, bounce and settle a "
           "beat after her head stops, her breasts sway softly below her, and her throat and jaw shift as she swallows and breathes.")
COMMON = {"width": 1152, "height": 768, "length": 124, "motion_lora": "h3nsfw/H3_Motion_BoosterV2.safetensors",
          "unet": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors", "anime_timing": "off"}

def p(opener, body, snd, extra=""):
    t = f"integrated_multimodal_description: [Shot 1] {opener} {body}"
    if extra: t += " " + extra
    if "POV" in body: t += " The camera does not move."
    return t + "\n\n" + snd

jobs = []
for v, op, ex in (("phys", TV, PZ_PHYS), ("l2d", L2D, PZ_PHYS)):
    jobs.append(dict(COMMON, name=f"lz_pz_wide_{v}", template="anime_ll_paizuri", image="gallery/a97/lz_pz_wide_2_00001_.png",
                     seed=96101, prompt=p(op, PZ_LZ, SND_PZ, ex)))
for v, op, ex in (("phys", TV, BJ_PHYS), ("l2d", L2D, BJ_PHYS)):
    jobs.append(dict(COMMON, name=f"lz_bj_profile_{v}", template="anime_ll_headgrab_push", image="gallery/a97/lz_bj_profile_3_00001_.png",
                     seed=97101, prompt=p(op, BJ_LZ, SND_BJ, ex)))
jobs.append(dict(COMMON, name="sv_pz_wide_l2d", template="anime_ll_paizuri", image="gallery/a96/pz_wide_tv_2_00001_.png",
                 seed=96101, prompt=p(L2D, PZ_SV, SND_PZ, PZ_PHYS)))
with open(os.path.join(ROOT, "jobs", "a99_smooth.jsonl"), "w", encoding="utf-8") as f:
    for j in jobs: f.write(json.dumps(j) + "\n")
print(len(jobs), "jobs")

# a99b: the Lanzhu keyframes stayed on 2s with l2d; seed or wording?
L2D2 = ("A smooth, fluid 60 fps 2D animation like a Live2D h-game scene, soft-body physics, clean anime art, "
        "every movement soft and continuous with gentle follow-through, one fixed camera.")
b = []
for s in (97102, 99101):
    b.append(dict(COMMON, name=f"lz_pz_wide_l2d_{s}", template="anime_ll_paizuri", image="gallery/a97/lz_pz_wide_2_00001_.png",
                  seed=s, prompt=p(L2D, PZ_LZ, SND_PZ, PZ_PHYS)))
b.append(dict(COMMON, name="lz_pz_wide_l2d2", template="anime_ll_paizuri", image="gallery/a97/lz_pz_wide_2_00001_.png",
              seed=96101, prompt=p(L2D2, PZ_LZ, SND_PZ, PZ_PHYS)))
b.append(dict(COMMON, name="lz_bj_profile_l2d2", template="anime_ll_headgrab_push", image="gallery/a97/lz_bj_profile_3_00001_.png",
              seed=97101, prompt=p(L2D2, BJ_LZ, SND_BJ, BJ_PHYS)))
with open(os.path.join(ROOT, "jobs", "a99b_smooth.jsonl"), "w", encoding="utf-8") as f:
    for j in b: f.write(json.dumps(j) + "\n")
print(len(b), "a99b jobs")

# a99d: h-game art style keyframes, Lanzhu LoRA + identity (anime_lz_side graph), two angles
def stills():
    src = {}
    with open(os.path.join(ROOT, "jobs", "a97_lanzhu_tv.jsonl"), encoding="utf-8") as f:
        for l in f:
            j = json.loads(l)
            src[j["name"]] = j
    TVB = ("year 2018, anime screenshot, anime coloring, cel shading, flat color, hard shadows, (shiny skin:1.2), glossy skin, "
           "(large white specular highlights:1.1), soft bloom, glow, pastel colors, thin lineart, sweat drops")
    HG = {
        "hgf": "newest, game cg, eroge, @fuzichoco, (soft shading:1.2), gradient shading, (shiny skin:1.2), oily skin, glossy skin, "
               "detailed skin, rim lighting, soft lighting, bloom, sweat drops",
        "hg": "newest, game cg, eroge, (soft shading:1.2), (gradient shading:1.1), (shiny skin:1.2), oily skin, glossy skin, detailed skin, "
              "(skin shine:1.1), rim lighting, soft lighting, bloom, depth of field, sweat drops",
    }
    out = []
    for ang in ("lz_pz_wide_2", "lz_bj_profile_3"):
        base = src[ang]
        assert TVB in base["prompt"], ang
        for k, blk in HG.items():
            for s in (99001, 99002):
                neg = base["negative"].replace(", painterly, thick painting", "") + ", flat color, cel shading, anime screenshot"
                out.append({"name": "hgk_%s_%s_%d" % (ang.split("_", 1)[1].rsplit("_", 1)[0], k, s), "template": base["template"],
                            "width": base["width"], "height": base["height"], "seed": s,
                            "prompt": base["prompt"].replace(TVB, blk), "negative": neg})
    with open(os.path.join(ROOT, "jobs", "a99d_hgame_keys.jsonl"), "w", encoding="utf-8") as f:
        for j in out: f.write(json.dumps(j) + "\n")
    print(len(out), "a99d stills")
stills()

# a99e: animate the h-game keyframes; dynamics option from kit/presets.json, timing off (measure H3's own mode)
def clips():
    with open(os.path.join(ROOT, "jobs", "a97f_lanzhu_nocheek.jsonl"), encoding="utf-8") as f:
        bjf = [json.loads(l) for l in f if l.strip()]
    bj = next(j for j in bjf if j["name"] == "lz_f_bj_profile")
    with open(os.path.join(ROOT, "jobs", "a97e_lanzhu_seeds.jsonl"), encoding="utf-8") as f:
        pz = json.loads(f.readline())
    out = []
    for k in ("hg_99002", "hgf_99001"):
        out.append(dict(COMMON, name="hgv_pz_wide_" + k, template=pz["template"], seed=96101, prompt=pz["prompt"],
                        image="gallery/a99/hgk_pz_wide_%s_00001_.png" % k, dynamics="hgame_pz"))
    for k in ("hg_99001", "hgf_99001"):
        out.append(dict(COMMON, name="hgv_bj_profile_" + k, template=bj["template"], seed=97101, prompt=bj["prompt"],
                        image="gallery/a99/hgk_bj_profile_%s_00001_.png" % k, dynamics="jiggle_bj"))
    with open(os.path.join(ROOT, "jobs", "a99e_hgame_clips.jsonl"), "w", encoding="utf-8") as f:
        for j in out: f.write(json.dumps(j) + "\n")
    print(len(out), "a99e clips")
clips()
