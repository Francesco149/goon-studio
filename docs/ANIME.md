# Anime recipe: Pink Alchemy Anima (2026-11-20)

The anime side moved from `anima-base-v1.0` + `anima-aesthetic-v1.1` to a single hentai-native
Anima merge, and the mouth-seal problem was solved with prompt wording. This supersedes the
anime halves of `WINS.md` / `SEX-SCENES.md` for anything explicit.

## The checkpoint

| | |
|---|---|
| name | RAMTHRUST'S NSFW Pink Alchemy Anima v2.9 |
| file | `ramthrustsNSFWPINK_v29.safetensors` (4.18 GB unet) |
| base | Anima-Base v1.0 (same VAE `qwen_image_vae`, same TE `qwen_3_06b_base`) |
| loaded as | `UNETLoader` in the normal Anima graph (`tools/wf_anima2.json`) |
| source | Civitai model 2578175, v2.9-Anima1.0Base; a copy was fetched from the RunningHub HF mirror |
| where | `<engine_dir>\ComfyUI\models\diffusion_models\` (local) |

Why it wins: `pa1`-`pa3` (same prompts and seeds as the base-model `a2a`-`a2c`) have the anime
screenshot style, a real anime face, curvy proportions and a thick, veined cock with a defined
head. The base model could not do all four at once; adding anatomy weights to base pulled the
mouth off the cock (`a2b`). Pink keeps both.

## Settings

```
30 steps, cfg 4.0, er_sde / simple, 1248x832 (side) or 832x1248 (POV), denoise 1.0
```

The model card recommends `euler_ancestral`/`beta`, 26 steps, cfg 4.7. `pa5`/`pa6` with those
settings are close but not better; stick with the lab's existing Anima numbers.

**8 GB tuning (cutestation, 2026-11-20).** With `--use-ck-attention --fast fp16_accumulation`:
30 steps = **36 s**, 20 steps = **26 s**, 12 steps = **23 s**. 20 steps is almost identical to 30
and is the better everyday default; keep 30 for a final and 12 for a quick preview. For composition
drafts, `anima-turbo-v1.1` at 6-8 steps, cfg 1, euler runs in **4-10 s** but has a weaker style -
never use it for the finished anime look. The hires pass (1152x1728, 20 steps, denoise 0.30) is
**60 s** and peaks at ~7.6 GB VRAM. Full method and numbers: `PERFORMANCE-8GB.md`.

## Prompt - side view (mouth sealed)

```
masterpiece, best quality, year 2016, anime screenshot, 1girl, 1boy, hetero, blowjob, fellatio,
(penis in mouth:1.2), (lips sealed around penis:1.35), mouth stretched, no tongue,
cheeks hollowed, sucking, detailed penis shaft, veins, erection, uncensored,
(penis focus:1.2), side view, profile, kneeling, leaning forward, short silver hair, single braid,
purple eyes, @murota yuuhei, (curvy:1.6), (wide hips:1.4), thick thighs, large breasts,
mature female, half-closed eyes, blush, saliva, bedroom, soft light, love live! sunshine!!
```

negative:

```
extra hands, extra fingers, third hand, bad anatomy, fused limbs, censored, mosaic censoring,
bar censor, tongue out, open mouth, glans outside mouth, worst quality, low quality, score_1,
score_2, score_3, blurry, jpeg artifacts, watermark, text, 3d, realistic
```

## Prompt - POV (mouth sealed)

Same, with the side block replaced by:

```
pov, from above, looking up at viewer, short silver hair, single braid, purple eyes,
(curvy:1.6), thick thighs, large breasts, mature female, half-closed eyes, blush, saliva
```

and `male body` added to the negative.

## What makes the seal work

- `penis in mouth` + `lips sealed around penis` + `cheeks hollowed` in the positive.
- `no tongue`, and `tongue out, open mouth` in the **negative**. Without these the model's
  default is an open mouth with the tongue on the glans.
- Do **not** weight `glans` high for an in-mouth shot: the tags draw what they name, so a weighted
  glans ends up outside her mouth. Keep `detailed penis shaft, veins` and let the head go in.
- The seal is still seed-sensitive; reroll before rewriting.

## Results that define the look

- `pb2_side_seal_w` - side, sealed, thick veined shaft, curvy body.
- `pb3_pov_seal` - best anime POV: face, breasts, head in her mouth.
- `pb1_side_seal` - lighter/pastel variant.
- `pb6_side_big` - the "bigger" variant. `huge thick penis` really is comical; use it only on purpose.
- `pb7_cum_face` - anime cum is correct (strands, drips, gloss). The photoreal model is not.

## Censorship

- `bar censor` draws a free-floating striped sticker (`pb4`) - unusable.
- `mosaic censoring` draws one large block over the shaft with the head visible (`pb5`) - the
  flim13 look, and usable, but its placement is luck.
- For a controlled result, censor in post (ffmpeg crop + pixelize + overlay) as before.

## Second pass (hires detail)

The still is good at 832x1248; a low-denoise hires pass makes it deliverable:

```
upscale to 1.38x (832x1248 -> 1152x1728), 20 steps, cfg 4.0, er_sde/simple, denoise 0.30
```

`h1_d30` (Pink on `pb3`) sharpens the face, the shaft shading and the chest, and keeps the
mouth seal. `denoise 0.45` is punchier but loosens the seal and starts changing the braid;
keep 0.30 for the final. 90 s on the 5060. This is the anime equivalent of the detailer pass
the community runs after the first render.

## Anime video (owner verdict, 2026-11-20)

Best anime clip so far: `gens/v10/v10b_pov_bob` - H3 i2v from the `pb3_pov_seal` keyframe,
768x1152, 124 f, no LoRA, with the prompt asking for **whole-body motion**, not just the mouth:
```
A 2D anime clip in a clean cel-shaded TV-anime style. POV from above: a young adult woman with
short silver hair and purple eyes kneels between the viewer's legs, her large breasts on either
side of an erect penis, her lips sealed around the head. She bobs her head up and down the
shaft in a steady rhythm, her breasts bouncing with the motion, her braid swinging, her eyes
lifting to the camera between strokes. Saliva gathers at the corner of her mouth. The camera
shakes very slightly with her motion.

overall_soundscape: wet suction, soft pops, her breath, a low male grunt, quiet room tone. No music.
```

Owner: "nicer ... the motion is decent ... still feels a bit stiff but probably the best anime
one we got so far." The look still has a generic AI-render feel (Pink's shading), which is a
model property, not a prompt one.

On cutestation the same 768x1152 / 124 f clip is **372 s** at the standard 6 steps and **267 s**
at 4 steps; 512x768 / 85 f is **111 s** at 6 and **82 s** at 4. Use 4 steps with the same seed as
a preview, then re-run at 6 for the final. Full numbers: `PERFORMANCE-8GB.md`.

The side-view version of the same idea (`v10a_side_body`) was rejected: the cheek puffing reads
wrong and does not match the action. Do not use it.

The frame-by-frame restyle (`RECIPE-RESTYLE.md`) was rejected outright: owner called it
unstable and not a good anime style. Treat that route as closed unless the style model changes.

## What is still open

- The man is a featureless slab at the left edge. Add `his hip, his thigh, his hand on the back
  of her head` to the prompt or accept it as a crop.
- Extra hands still appear occasionally; inpaint the hand region or reroll.
- **Anime video**: best current recipe is `v10b` above (POV bob, whole-body motion prompt).
  It is still slightly stiff and the shaft does not travel as far as in the photoreal clips;
  the restyle route is closed by owner verdict.

## Sound

The model audio is a scratch track: the strokes crunch, the slurp sounds like noodles, and the
events are not synced to the action. Do not present a clip as finished on the strength of its
sound; the findings and the next routes are in docs/SOUND.md.

## Anime recreations of the photoreal shots (2026-11-21 session 6)

Goal: the three photoreal signatures, re-drawn in anime - the owner's `seed 824704499` cum-first
POV blowjob, the `seed 2042927734` paizuri, and the `k14` cum-shot poses - with the public anime
still (`gallery/studio/img_00006_.png`) as the face/cock/pose baseline and the Gemini art study
(`ART-STUDY.md`) as the proportion source.

**The generic face was a prompt problem, not a model problem.** The first anime pass (`a01`) used
`year 2016, anime screenshot, @murota yuuhei` but no face details; the owner called it generic.
The fix came from the Love Live Studio research (`../lovelive-studio/docs/guide/index.html` and
`kit/presets.json`):

- the designer tag `@murota yuuhei` + `year 2016` + `anime screenshot` carries the look;
- the **signature trick**: the show name `love live! sunshine!!` is in the prompt only for the
  last 30% of the steps (`ConditioningSetTimestepRange` 0.0-0.7 early, 0.7-1.0 late,
  `ConditioningCombine`). Without it the name turns her into a canon character; with it she gets
  the round eyes and blush while staying ours. `workflows/wf_anima2_sig.json` does this, and
  `kit/studio/core.py` builds the late prompt from the filled prompt for templates that set
  `"late": "signature"` (eye colour gets `:1.3`);
- **face features** that a character designer would use: `jitome, mole under eye, fang, ahoge,
  hair intakes`. Two or three of them are what stop the generic AI face;
- a **second artist tag** blends a new look: `@fuzichoco` (pale, painted) and `@kantoku` (soft,
  detailed) were the owner's picks, `@ikeda kazumi` decent; `@as109` and `@mizuryu kei` did
  nothing useful. The 90s blend (`year 1995`, retro tags) was rejected: "too slop today because
  it's been over-saturated by AI gens".

The e-girl translated to anime read as generic and was dropped; the Love Live girl won. The best
paizuri still so far is `gens/a05/e2_sig_paizuri_00001_.png` (signature style); `e2_fz` and
`e2_kt` are close.

**Poses that work as stills** (all 832x1248, 30 steps, cfg 4, er_sde/simple):
POV cock-out (`a04`), paizuri (`a05`), wide gap (`a05`), suction deepthroat (`a09`),
cum-on-tongue (`a09`). The owner wants the deepthroat **suction/hollow-cheek** look, not puffed
cheeks: `(cheeks hollow:1.4), (sunken cheeks:1.3), (cheek sucking:1.2)` with `puffed cheeks,
bulging cheeks, cheek bulge, throat bulge` in the negative.

**Templates**: `kit/presets.json` now has `anime_ll_{fz,kt,sig,ikeda}_pov`,
`anime_ll_{fz,kt,sig}_paizuri`, `anime_ll_fz_wide` and `anime_ll_fz_cum`, all on
`wf_anima2_sig.json`; characters `ll_sig` and `ll_soft` carry two face sets. The page must be
restarted once to load the `late` support in `core.py`.

### End-frame route (failed - do not repeat)

To force a deep stroke or a landed cum state we tried to author the last frame, then run H3
first+last:

- Qwen-Image-2.1 single-image edit: the deepthroat became a mouth artifact with the cock still at
  her lips; the cum became a web of strands across her nose. Owner: "it just degrades the image
  and makes it less clean without giving a good edit."
- Pink img2img with the signature workflow (`wf_anima_i2i_sig.json`, denoise 0.5-0.65): the
  deepthroat kept the cock outside the mouth; the cum became drool down the shaft.
- Pink t2i end frames: the deepthroat still was decent but puffed-cheeked; the cum still drew
  strands across the face from the `cum on face`/`cum on nose` wording.

Reword a landed still with `cum on cheek, cum on tongue, cum on lips, thick white semen, cum
drip, semen pooling on her tongue` and put `cum on face, cum on nose, cum string, strand across
face, web` in the negative; that removed the face web but a mouth-to-chest drip string remains.
For the video, the only route left is the model's own emission with a trajectory prompt.

### The clip defects to beat (owner, 2026-11-21)

- The first anime clips are **rigid** and unnaturally smooth next to the photoreal ones; the
  face barely moves.
- Paizuri at `Titjob-Titfuck-H3` 0.85: the motion idea is right, but it goes **dark and grainy**
  after the first frames and the cock/tongue overlap badly. Try 0.6 and the motion booster.
- `k14`: better, but the ropes are too thick and the cum pools **around** the mouth. The owner
  wants thinner ropes that travel **across her face** or **into her mouth**, plus some **below
  and dripping**.
- Sound: see SOUND.md; the new wordings were tested this session.

### New video route under test (a10)

`workflows/wf_h3vid_i2v_lora2.json` chains an act LoRA and `H3_Motion_BoosterV2` (node 22), so the
clip can get both the act and more motion. Jobs `jobs/a10_clips.jsonl`:

- `k1_anime_k14_ropes`: epic_cumshots 0.5 + motion 0.5, thin-rope trajectory prompt (first rope
  across the cheek/nose, second into the mouth, third below the lip and dripping), strong flinch
  and camera shake; the negative idea "the ropes travel, they do not pool" is written positively.
- `k2_anime_paizuri`: Titjob 0.6 + motion 0.4, bright even light, "the breasts drag and catch on
  the shaft, the flesh squashes, a small hitch at the top of each stroke".
- `k3_anime_deepthroat`: first+last (`wf_h3vid_i2v_fl.json`) from the cock-out still to the
  suction deepthroat still, so the insertion is forced; hollow cheeks in both still and prompt.

Judge at 1:1 for the cum and with `tools/vsheet.py --frames 8` for the motion.

### Results of the a10-a17 clips (owner, live review)

- **Best blowjob POV: `gens/a21/k9_anime_suction_perf_00001_.mp4`** (the k4 base plus eye lock,
  a slight expression change, a mouth-pursing suction pop and more saliva). Owner: "best blowjob
  so far - make that the recipe for blowjobs for now." **This is the base recipe**; other angles
  and motions change only the stroke sentence (`anime_ll_slow`, `anime_ll_deepthroat`,
  `anime_ll_headgrab`). The earlier `k4` is kept as `anime_ll_suction_orig`.
- **Paizuri: `gens/a11/k2_anime_paizuri_00001_.mp4`** is "better than anything we did before"
  (Titjob 0.6 + motion 0.4, bright prompt fixed the dark/grainy drift of the 0.85 pass). The one
  defect is the tongue drawn in front of the glans; `k7` changes it to "her tongue stays under
  the shaft and never covers the glans". Video template `anime_ll_paizuri`.
- **k14 cum: dynamics are getting lifelike** with the motion booster, and the first rope lands
  and stays. Two recurring defects: the shaft barely twitches and the veins barely swell, and the
  rope reads as a line **over her face** that lands lower. `k6` adds a springy sideways kick,
  throbbing veins, a hip jerk and "the rope ends where it hits, it does not lie across her face".
- **The FL deepthroat (`k3`) failed**: the first still and the t2i end frame had different
  framing and identity, so the clip morphed into a washed-out face instead of a clean insertion.
  Do not combine two independently rolled stills as first+last; the pair must share the framing.
- **Side-gap route (`a16`)**: a side-view keyframe with the cock upright an **inch in front of
  her face and a visible gap** renders reliably (`m1_side_gap_a/b`). `k8` is the side-view cum
  shot at 1152x768, where the ropes have a real gap to cross and can land on the cheek, the
  tongue and the chin without a rope lying over the face.
- Audio levels: `k1` -27.4 dBFS, `k2` -30.9, `k4` -42.7; no clipping on those. The k4 clip is
  quiet by ear too. The "loud and present" wording helps sometimes, not monotonically.

Templates added or updated after this round: 12 image templates (`anime_ll_*`, plus the side
view), 3 video templates (`anime_ll_cumshot`, `anime_ll_paizuri`, `anime_ll_suction`), and the
characters `ll_sig` / `ll_soft`. The page also keeps a template's own workflow now (`VWF` in
`kit/studio/index.html`), so the `lora2` motion-booster workflow is not silently replaced by the
plain LoRA one.

### Twitch and tongue: what was tried after that verdict

- `k6` (twitch wording, epic 0.6, motion 0.5): owner - "the dick now looks like a spring and
  constantly bounces". The words `springy`, `dampened bounce`, `jerk` over-corrected; motion
  dropped from 4.8 to 3.2. A continuously bouncing shaft is worse than a still one.
- `t1_kick_once` and `t2_veins_only` (81 f) are the controlled recipes: t1 = one sharp ~10 degree
  kick per pulse and *perfectly still between pulses*; t2 = the shaft does not move at all, only
  the veins swell and the glans twitches. Owner on t1: "way better but a bit too extreme
  expansion when twitching ... a slight side bob instead of too much expansion". t2 did not
  remove the rope-from-above; it stayed static.
- `t3_gemini_timing` (the Gemini cadence: 0.8 s then 1.0 s then 1.2 s between spurts, 10 degree
  snap in two frames, hold, dampened bob, still between) **failed badly**: the "slit flares open"
  wording turned the urethra into a hole. Never prompt the meatus/slit opening in anime - the
  model draws it as a hole. The rope-from-above also stayed.
- `t4` (prompted as a small sideways bob, but the model rendered another **front POV** cum shot)
  and `t1` (one upward kick, still between) are both **acceptable**; the owner wants the motion
  dialled down a tiny bit. `t4` is the best cum shot so far. Do not call t4 a side bob in notes -
  it is a front POV.
- `t5_dialed_down` is `t4` with a very small sideways sway, faint vein swell and motion 0.35.
- **The blowjob base is now `k9_anime_suction_perf`** (owner: "best blowjob so far - make that the
  recipe for blowjobs for now"). Video templates built from it: `anime_ll_suction` (the base),
  `anime_ll_slow`, `anime_ll_deepthroat`, `anime_ll_headgrab` (his hand on the back of her head),
  plus `anime_ll_suction_orig` (the k4 still-shaft version). Use the base prompt and change only
  the stroke/motion sentence.
- Paizuri tongue: the k7 wording ("her tongue stays under the shaft and never covers the glans")
  changed nothing. The tongue is baked into the keyframe (`tongue out touching the glans`), so the
  fix is structural - a keyframe with the tongue away from the tip, or no licking action - not
  more prompt words.
- Side-view cum (`k8`, 1152x768 from `m1_side_gap_b`): the gap renders, but the epic LoRA did
  **not** emit at all and motion was 1.9, so the clip is static. The side keyframe is solid for a
  blowjob; it is not a cum-shot keyframe on this recipe. Keep it for the side-view pose template.
- `k9_anime_suction_perf` is the k4 performance pass: locking eyes with the camera, a slight
  expression change (eyebrows, lashes, blush), a mouth-pursing suction pop, and more saliva.
  Video template `anime_ll_suction_perf`.
- Video templates now carry the cum flavours: `anime_ll_cumshot` (t4: the best so far, small
  sway, no expansion), `anime_ll_cumshot_soft` (t5: t4 dialled down) and `anime_ll_cumshot_twitch`
  (t1: one kick and still between, but the shaft expands). None is finished.
- `t5_dialed_down` is t4 with the sway/vein swell dialled down; `anime_ll_cumshot_soft` preserves
  it. `anime_ll_cumshot` stays on t4 until t5 is judged.
- `k10_headgrab` proves the base takes a new motion: his hand enters from the side at about 0.7 s
  and stays on the back of her head. The hand is large and slightly stiff, but it reads; template
  `anime_ll_headgrab`. The slow and deepthroat variants are written as templates but not rendered
  yet.

### Motion variants (owner review, 2026-11-21 late)

The owner asked for a push, a two-hand, a tip tease, and a stroke-then-take-it cum shot. All are
built from the k9 base by changing only the stroke sentence:

- **Head-grab push, held: `k16_headgrab_hold` is the recipe** ("very good that's the recipe"). He
  pushes her down until her nose is against his body, holds her perfectly still while she sucks,
  she braces her hands on his thighs and briefly tries to push back up against his hand, then he
  releases. The earlier `k11` was close but ended with the smile; remove the k9 base's
  `the corner of her mouth curls` on any clip where the cock stays in the mouth - it opens the
  mouth and shows the fangs.
- Two hands: `k12` is good but fangs pop at the end (same smile); `k18` removes the smile and
  keeps the lips sealed. Template `anime_ll_two_hands`.
- Tip tease: `k13` (licks the tip, kisses the glans, takes just the head, pops off, then goes
  deep) reads; template `anime_ll_tip_tease`.
- **Cum switch:** the front version `k17` is **good** (owner), template
  `anime_ll_cum_switch_front`; it uses the front handjob keyframe `n1_handjob_a`. The side version
  `k19` has a **good pose** but the rope shoots sideways and the mouth goes static after; `k21`
  (side) fixes the rope direction and adds suction - owner: "everything else is solid" except
  **she does not take it into her mouth correctly: the dick goes behind the mouth, not inside**.
  `k22` (closer keyframe `n2_a`, "the head goes past her lips, lips seal in front of the shaft")
  went static altogether (motion 1.1) and did not solve the placement. `k23` is the clean side
  take-in: no cum, no drip, no cheek puff (the shot does not exist, so nothing is faked), motion
  1.6; it is the cleanest side take-in so far. The side keyframes (`n2_side_handjob_a/b`) are good
  for blowjobs; for the side cum switch the next route is a side keyframe with the **lips already
  around the head** (a side sealed still) and then suction, or an FL pair with matching framing -
  not another wording pass on the handjob keyframe.

**Mixed reality (real cock in an anime picture): unfinished - needs more research.** The still
pipeline is now **golden anime seal + H3-Image masked fill** (k9 deep seal, and a head-out seal so
the real glans can be shown in frame 0), not the Qwen one-image edit and not a hand composite. But
the owner's verdict (2026-11-21) is that the video dynamics are still below the pure-anime BJs -
one take-in clip puffs the cheeks, the other reads as chewing - and the audio is unusable. Do not
call the video recipe proven. See `docs/MIXED.md` for the stills, the pipeline and the rejected
routes.
- The mouth-purse/suction base is unchanged; the `k9` prompt plus the `anime_ll_*` video templates
  are the current library (headgrab, two hands, tip tease, slow, deepthroat, cum switch).

## Character LoRAs on Anima: Lanzhu Zhong, Kasumi Nakasu (owner-approved 2026-11-21)

Two character LoRAs from the same author, same training recipe (base Anima `anima_baseV10`, 1000
images, dim 32, text encoder not trained), both on the Pink Alchemy checkpoint we already use:
`lanzhu-zhong-s2-anima-lora-nochekaiser.safetensors` (Civitai 2708274) and
`kasumi-nakasu-s2-anima-lora-nochekaiser.safetensors` (Civitai 2708250). They run through a new
graph with one `LoraLoaderModelOnly` node: `workflows/wf_anima2_lora.json` (a copy of the
signature graph, node 48 between the unet and the KSampler). Model-only is right because the text
encoder was not trained.

Settings: the normal Anima numbers - 30 steps, cfg 4.0, er_sde/simple, 832x1248 (POV) or
1248x832 (side), **LoRA strength 1.0**. Measured on the local 5060 (8 GB): **36-41 s** per still,
peak about 7.0 GB used, no new flags. Nothing about this needs the lab boxes.

**Identity is the LoRA's job, style is ours.** Without an artist tag she goes generic (the same
failure as the LL girl); `@murota yuuhei` in the prompt fixes the face while the LoRA keeps her
hair, mole and outfit. Her series tag goes in the signature late pass, not Sunshine's:
`kit/studio/core.py` takes a per-template `series` for `"late": "signature"`, and both character
sets set `love live! nijigasaki high school idol club`.

Two body readings, both approved as templates (per character):

- **curvy** (`anime_lz_*`, `anime_kc_*`): body weighting in the character block - Lanzhu
  `(curvy:1.8), (wide hips:1.5), thick thighs, large breasts`; Kasumi `(curvy:1.6), (wide hips:1.4),
  thick thighs, medium breasts` (her trigger says `small breasts`, so the curvy read is a step up,
  not a big-bust one).
- **canon** (`anime_lz_canon_*`, `anime_kc_canon_*`): the trigger words without body weighting -
  Lanzhu's own petite read, Kasumi's small breasts. The owner's call (2026-11-21): it is a
  fictional character and anime girls look petite; both are kept.

Kasumi notes: both `kasumi nakasu` and `nakasu kasumi` work and the LoRA likes both; her
`red ribbon` tag renders the **yellow-gold** canonical ribbon; paizuri works even on the small-
breasts canon body.

**The POV mouth seal does not work on either LoRA** (same author, same recipe - it is the training
data's closed-mouth face) and the seal template for both is the side one (`anime_lz_seal`,
`anime_kc_seal`: her lips closed around the head, side view). What was tried and failed on the POV
framing, on Lanzhu: the LL seal wording, `(penis in mouth:1.4)` / `(lips sealed around penis:1.4)`,
strength 0.7/0.8/0.9, with and without `@murota yuuhei`, and seeds 811, 4242, 611, 9137; on Kasumi:
the same wording with and without the signature pass. Every time the model drew the shaft in front
of her closed lips. The POV **deepthroat** wording does get the shaft in, but the framing is poor -
kept as a route in `jobs/kc02.jsonl`, not shipped. Do not spend another wording pass on the POV
seal. The full recipe and the measured numbers live in `docs/LORAS.md`.

**Verdict (owner, 2026-11-21):** Lanzhu - "the gens are mostly good... the seal one is maybe a
little bit deviating from the design and going into slightly generic territory, others are solid";
Kasumi - approved with the same templates. POV cock-out, side gap and paizuri are approved for
both; the sealed shot is the side head seal.

