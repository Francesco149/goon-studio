# Anime timing: hand-drawn cadence for H3 clips (round a95, 2026-11-22)

Open item 5: the anime clips move like an h-game / live2d avatar. H3 draws a new frame every
1/24 s with soft motion blur between poses; a hand-drawn TV anime shows fewer, crisp drawings with
hard cuts between them. This file has the measured reference timing, the post-pass that imposes
it, and the prompt experiment.

## The reference

`gallery/refs/art-study/refs/anime_anim_BJ_around_7mins_paizuri_after_doggy.mkv` (1280x720,
23.976 fps), section 07:00-08:35: a blowjob scene (07:22-08:18) and a paizuri scene (08:22-08:35).
Shot stills and the Gemini write-up: `gallery/refs/art-study/analysis/anime_7min/`,
`gallery/refs/art-study/ANIME_TRADITIONAL_2D_ANIMATION_STUDY.md` (local, never committed).

Measured with frame differences (a frame equal to the previous one = a held drawing) and the
self-similarity period (frame i vs i+k):

| shot | time | drawings/s | holds | stroke loop |
|---|---|---|---|---|
| front POV bob (s06) | 442.0-450.7 | 15.8 | mix of 1s and 2s, about even | 21 frames (0.88 s), repeats every 42 |
| high angle (s07) | 450.7-456.9 | 16.0 | 1s/2s mix | 21 frames |
| front POV, faster (s13) | 462.3-467.9 | 23 | on 1s (camera shake over the cels) | no clean loop |
| low rear (s14) | 467.9-473.6 | 24 | on 1s | **exact 14-frame cel loop** (0.58 s) |
| side profile (s15) | 473.6-478.5 | 24 | on 1s | exact 14/28-frame loop |
| cum on chest (s18) | 487.3-498.6 | 20 | mostly 1s, some holds of 4-10 frames | - |
| paizuri wide (s20) | 502.0-510.6 | 18 | 1s/2s | 21 frames |
| paizuri close (s21) | 510.6-516.0 | 15.9 | 1s/2s about even | 21 frames, repeats every 42 |

What this says, and where the Gemini write-up is wrong:

- The slow strokes (front BJ, paizuri) are drawn at about **16 drawings/s, alternating 2s and 1s**,
  with a 21-frame stroke. The pose jump between drawings is large; there is no motion blur.
- The fast pumping shots are a **short exact loop on 1s** (the same 14 drawings repeated), not
  12 fps; they read as anime because the loop repeats exactly and each drawing is crisp.
- Gemini's "hard hold of 3-6 frames at the bottom of every stroke" is **not in the BJ or paizuri
  loops**: no run of 3+ identical frames there. Long holds only appear in the cum shot and the
  stills. Its "12-frame cycle" and "8 to 6-frame loop" numbers do not match the measurement either.
  Use its shot list and descriptions, not its frame counts.

## The post-pass: `kit/studio/anime_timing.py` (page toggle "Anime timing")

Picks which source frame is shown at each output frame; nothing is generated, the length and
audio are unchanged (every drawing shows at its own time or one frame after).

```
F:\LLStudioTest\engine\ComfyUI_windows_portable\python_embeded\python.exe -I kit/studio/anime_timing.py in.mp4 out.mp4 --mode on2 [--sheet x.jpg]
```

- `--on N`: hold each drawing N frames (2 = on twos).
- `--stop N`: at each stroke end (local minimum of motion energy) hold that drawing N frames,
  then jump on. 0 turns it off. The reference BJ/paizuri loops have no such holds; it is kept as
  a stylistic option.
- The sharper of the two candidate frames is used for each drawing (less H3 motion blur).
- Audio packets are copied unchanged (PyAV only, no ffmpeg needed).

**In the page (owner verdict 2026-11-22: "on 2s is the default, the others are options").** The
Video tab has an **Anime timing** select: `off`, `on2` (anime: on 2s), `on2_stop` (on 2s + holds
at stroke ends), `on3_stop` (on 3s + holds). Every `anime_*` video template carries
`"anime_timing": "on2"`, so it is preselected for them and off for photoreal. `core.run` applies it
after the clip is pulled (job key `anime_timing` wins over the template's); the smooth original
stays next to it as `<name>-raw.mp4` (not listed in the gallery). Rounds can set it per job; the
round runner needs the engine's Python (PyAV) for it, otherwise the clip is left smooth and the
record says `skipped`. Verified in round a95b (on 2s: 28 of 55 frames held, length and audio
unchanged).

Round a95 variants on the golden clips (k11 `anime_ll_headgrab_push`, a92 `anime_ll_paizuri`):
`*_post_on2` (12 drawings/s), `*_post_on2_stop4` (~10.5/s with stoppers), `*_post_on3_stop5`
(~7.4/s, the most "limited").

## The prompt experiment

Same keyframe + seed as the golden clips, two wordings (`jobs/a95_anime_timing.jsonl`):
`_tech` (style line extended with "hand-drawn limited animation animated on twos ... no motion
blur and no smooth in-betweens") and `_desc` (an extra sentence: distinct key poses, snaps down,
freezes for a beat, snaps back, crisp). Results and the owner's verdict: below.

## Results

- **Wording does not change the cadence.** `_tech` and `_desc` are still a new frame every 1/24 s
  (0-9 held frames out of 124, same as the golden clips), with the same sharpness (motion blur
  unchanged). H3 does not do limited animation from text.
- `bj_k11_desc`: the pushes got bigger (more motion per frame), but there are no freezes. `pz_k2_desc`:
  she licks the tip for the first ~0.7 s (the template is no-tongue) and then the stroke almost stops.
  Do not use the snap/freeze sentence on paizuri.
- So the cadence has to come from the post-pass (or from a LoRA trained on limited animation). All
  four new clips also have an `_post_on2` version in `gallery/a95/`.
- Owner: on 2s is solid, especially once paired with an art style and rendering typical of that
  kind of animation (cel shading, flat colours, hard shadows). Next: the other reference shots and
  other art styles.

## Art style and angles to go with it (round a96, 2026-11-22)

Keyframes on Pink Alchemy (`anime_side` graph, 1248x832 landscape like the 16:9 reference), the
LL OC, five reference angles, three style blocks, seeds 96001/96002 (`jobs/a96_tv_style_keys.jsonl`):

- `base`: the current `year 2016, anime screenshot, @murota yuuhei`.
- `tv`: `year 2018, anime screenshot, anime coloring, cel shading, flat color, hard shadows,
  (shiny skin:1.2), glossy skin, (large white specular highlights:1.1), soft bloom, glow, pastel
  colors, thin lineart, sweat drops`, no artist tag.
- `tvm`: `tv` + `@murota yuuhei`.

Angles: `bj_front34` (close three-quarter from the side, hand on the base), `bj_high` (high angle
on her face, foreshortened), `bj_profile` (side profile, his hand on her head), `pz_wide` (POV,
sunset orange), `pz_close` (close on the cleavage, sunset).

Agent read: **`tv` is the closest to the reference** - flat two-tone cel shading, the big white
oval highlights on the skin, clean pastel colours; `base` is greyer and muddier (and seed 96001
drew a comic-panel inset on `bj_front34`); `tvm` sits between them. The angles take, except
`pz_close`: "head out of frame" is ignored and two seeds put her tongue/mouth on the glans.
Clips from the best `tv` keyframe per angle (1152x768, on 2s): `jobs/a96b_tv_style_clips.jsonl`.

**Owner verdict on the a96 stills:** solid for facial expression, lips and angles - that part of
the recipe is down. The art style varies between seeds/style blocks and some read more generic
than others; style consistency is the open part.

**a96 clips** (H3, 1152x768, seed 96101, on 2s; `gallery/a96/v_*`, smooth originals `-raw`), agent read:
the TV style holds through every clip (no drift back to the painted look).
- `v_bj_profile`: the best - clear stroke travel, sealed lips, his hand on her head; closest to the
  reference side shot.
- `v_pz_wide`: works - smug face held, glans peeks out on the up strokes; moderate breast travel.
- `v_bj_front34`, `v_bj_high`: the expression holds but the head barely travels (small bob).
- `v_pz_close`: the keyframe had the glans at her mouth, so she mouths/licks it the whole clip
  despite "tongue stays in her mouth" - needs a keyframe with the glans below the chin.

## Lanzhu in the TV style (round a97, 2026-11-22)

Stills (`jobs/a97_lanzhu_tv.jsonl`): the `tv` block + `lz_curvy` on `anime_lz_side`'s graph holds her
design and the flat TV look; the lips seal on the three-quarter, high and profile angles (the old
overhead-POV seal failure does not apply to these angles), and `pz_close` with "glans far below her
chin" + oral words in the negative keeps her mouth off the tip on all three seeds.

Clips (seed 97101): owner - animation and art style right, but the BJ clips puff the cheek instead of
sucking, and the profile cock shrinks and its glans goes red. Paizuri wide: solid, but random steam.
- Steam is seed/keyframe-specific, not the prompt: the a96 clips with the same prompt have none.
  **Never name it** - "no steam, no vapour..." (a97d) made it heavier. Same prompt on seed 96101
  (`lz_e_pz_wide_96101`): no steam (owner confirmed).
- BJ: the `anime_ll_suction` wording + "never puff/never red" (a97c) barely helped; the act LoRA at
  0.45 instead of 0.65 was worse (red flared mouth on most frames). a97f, no cheek or colour word in
  the script at all ("her lips are sealed tight ... her face drawn tight by the suction"): **profile
  fixed** - the cheek stays flat on every frame, the red flare only briefly at one pull-up; front
  three-quarter still bulges the far cheek from frame ~30 (the angle/keyframe, not the words). Rule:
  in H3 scripts describe the action and the result, never the body part or colour you want to avoid.

### The source style changes H3's own cadence (measured on the `-raw` clips)

Owner noticed the TV-style clips already step like hand-drawn animation before the post-pass. The
numbers agree - per-frame change (median / 90th percentile) and frames nearly identical to the
previous one (of 124):

| clip | style | median | p90 | near-held |
|---|---|---|---|---|
| a26 k11 (golden BJ) | painted LL | 15.0 | 24.6 | 4 |
| a92 k2 (golden paizuri) | painted LL | 10.9 | 14.4 | 2 |
| a96 v_bj_profile | `tv` | 2.6 | 19.1 | 14 |
| a96 v_pz_wide | `tv` | 2.7 | 13.5 | 16 |
| a97 lz_v_bj_profile | `tv` + Lanzhu | 1.5 | 13.5 | 29 |
| a97 lz_e_pz_wide_96101 | `tv` + Lanzhu | 2.1 | 15.9 | 18 |

On a flat cel keyframe H3 moves in bursts - small drift on most frames, big jumps on a few - which
is already close to drawings with hard boundaries; on the painted keyframes every frame changes.
**Keep the on-2s post-pass anyway** (owner): it normalizes every clip to the same pacing whatever H3
does for a given style.
- Seed variants (a97e, original prompt): no steam on any of the four (`pz_wide` 96101/97102,
  `pz_close` 96101/97102). `pz_close` still has defects on both seeds: a tongue flick at the start,
  an open grin, and blotchy reddish smudges on the breasts (worse on 96101). `pz_wide_96101` is the
  keeper.
- Paizuri close-up, glans behind her chin (owner): **`lz_e_pz_close_97102` fixes it** (original prompt,
  seed 97102). The short-stroke script (a97g: "glans pops out in the middle of her chest, she leans
  back, head held high") turns the cock into another object on both seeds - do not use. The
  lean-back stills (`lz_pzc_lean_*`: "sitting upright, leaning back, head tilted back, chin up")
  crop her face at the top, like the reference close-up; unanimated, kept as an option.
- Inner-breast fold lines while stroking (owner: a nice touch, but should be promptable away): the
  squeeze words ("fingers sink into her breasts, the flesh squashes") draw extra shading lines on the
  inner breasts (same as a88's skin-drag band). **Video tab "Breasts" dropdown** (`breasts_video`
  in `kit/presets.json`, job key `breasts`): "as the template" keeps the folds; "smooth" removes the
  squeeze phrases (regex `drop` list) and adds "Her breasts stay smooth and round, the skin taut and
  even as she squeezes them." before the soundscape. Test clip: `lz_h_pz_close_97102_smooth` (a97h,
  same seed/keyframe as `lz_e_pz_close_97102`).
- a97h result (agent read): the smooth wording works - no fold/crease lines on the inner breasts on any
  checked frame, her hands lie flat instead of digging in, a soft pink shading stays; the glans stays
  below her chin. Same open-mouth grin as the folds clip (seed/keyframe, not this option).

## Re-anchoring the object mid-clip (round a98, 2026-11-22)

Idea (owner, from r/StableDiffusion): keep showing H3 what the object should look like, with
perfect continuity and no hand tuning. Tools: `MiniMaxH3AddGuide` pins an image at any frame index;
`MiniMaxH3ReferenceToVideo` (Ref2VA) conditions every step on reference images. New graphs
`wf_h3vid_i2v_lora2_g5.json` (i2v + act LoRA + booster + five guides) and `wf_h3vid_ref2va_first.json`
(the keyframe as reference + first-frame guide + LoRAs); driver `tools/rounds/reanchor.py`.

Method (`--mode repair`): pass 1 = the normal clip; its own frames 24/48/72/96/last become the
anchors (poses the motion already passes through, so nothing is forced); each anchor gets an
H3-Image two-picture edit (Picture 1 = the frame, Picture 2 = the keyframe; fixed instruction:
"keep everything exactly, only redraw his penis like Picture 2"); pass 2 = same job and seed with
the repaired anchors pinned at their own indices. ~150 s + 5 x 35 s + 185 s on a 3080.

Tested on two known-bad clips (`jobs/a98_reanchor.jsonl`, `analysis/a98_*`):

| variant | paizuri, cock turns into a ribbed object (a97g) | profile BJ, red flare + shrink (a97b) |
|---|---|---|
| base | ribbed brown object from frame ~35 | red flare on every pull-up |
| selfguide (raw pass-1 frames pinned) | same motion and same defect - pinning keeps continuity | same as base |
| **repair** | right cock at the anchors, but it still morphs between them - owner: better than without, not usable | full shaft at the anchors; the flare still shows between anchors (36, 75) |
| ref2va (one pass) | no morph but the cock shrinks to a small tip; tongue at the start | **cleanest: no flare, full shaft, flat cheek** (different motion from pass 1) |

- The H3-Image repair edits are faithful: face, hands, light, background unchanged; only the object
  redrawn (`gallery/a98/anchors/`).
- Continuity: no new jumps at the anchors. H3's own clips already jump on frames 24/48/72/96
  (per-frame change 8-17 vs a median of ~2, base clips) - the burst grid behind the "already
  stepped" TV look; the anchors sit on it and the repaired clip's jumps are the same size.
- Persistent defects (the morph) are fixed by repair; transient ones between anchors (a flare for a
  few frames on each pull-up) are not - next: anchors every 12 frames, or repair + Ref2VA together.
- **Owner verdict (a98):** the paizuri repair "just causes weird morphing with the penis - better than
  non repair but still not very usable". The anchors hold the object at 5 frames; between them H3
  still redraws it from the (bad) script. Same failure as the profile flare.

### a98c: the documented pattern, and why the anchors morph

Research (ComfyUI multiframe tutorial, the AddGuide PR, a community ref2va gist): **AddGuide images
never reach H3's text encoder** - they pin composition at a frame, nothing else. Identity comes only
from Ref2VA's `ref_images` slots, which the script can name as `<Picture N>`. ComfyUI's multiframe
template combines both (identity picture in `ref_images` + first-frame guide + more AddGuides for
timing). a98's repair ran on the i2v model (no identity reaching the encoder) and a98's ref2va
never named `<Picture 1>`. New: `wf_h3vid_ref2va_g5.json`, `reanchor.py --mode refrepair` (Ref2VA,
keyframe as `<Picture 1>` named in the script, + the repaired anchors) and `--mode ref2va` now
names `<Picture 1>` too (`*_ref2va_pic`).

Every 3rd frame from 26 to 70, cropped on the cleavage (`analysis/a98c_pz_dense.jpg`):
- `repair` and `refrepair`: the cock **pops between two shapes** - the long angled shaft the edit
  drew at the anchors (26-32, 47-50) and a small round dome H3 draws on its own between them. The
  anchors do not fail to hold the object; they fight H3's own rendering of it. That is the morph
  the owner saw, and denser anchors cannot remove it (more pops, not fewer).
- `ref2va_pic` (Ref2VA, `<Picture 1>` named, no anchors): one steady shape on every frame, no
  morph - but the cock stays small (a dome in the cleavage), and her face got the closed smile.
- Profile BJ, `refrepair`: no red flare at 36/75, full shaft, flat cheek, same poses as pass 1.

Conclusion so far: pinning edited frames only works when the edit agrees with what H3 would draw;
consistency comes from the reference (identity every step), not from anchors. Next: Ref2VA with a
reference that carries the size (a close crop of the cock from the keyframe as `<Picture 2>`), no
anchors except the first frame.
- a98b, 11 repaired anchors (every 12 frames, `--dense`, `wf_h3vid_i2v_lora2_g11.json`): the shaft
  shows on more frames, but it still pops back to H3's small dome between anchors
  (`analysis/a98b_dense.jpg`). Denser anchors do not fix the morph - owner predicted it.

**Parked (owner, 2026-11-22):** needs more research. A cock crop as `<Picture 2>` was rejected as
the next step: how clean the crop is varies per gen (hands, lips, breasts in the way). Open leads:
how people actually keep an object consistent in H3 (the multiframe template
`video_minimax_h3_r2v_addguides_v1.json` from the AddGuide PR, not yet read), an aligned-video
ref2va LoRA (community gist, none published), or an H3 cock LoRA (open item 4).

## Smooth motion: the h-game / live2d look on purpose (round a99, 2026-11-22)

The opposite goal: the soft, continuous, jiggly motion of the painted clips (`gallery/a88/k2_phys`,
the BlobCG refs) on a flat TV-style keyframe.

**H3 has two cadence modes, and the TV clips are in the on-2s one.** Frame difference into even vs
odd frames (`r` = the smaller median over the larger; ~1 = new drawing every frame, ~0.05 = every
other frame an exact duplicate, the ~0.5 left is compression noise):

| clips | mode |
|---|---|
| a88 `k2_phys`, a91/a92 paizuri, a89 k11-k13, a95b, every photoreal clip | on 1s (`r` 0.7-1.0), median change 5-10 |
| a96 `v_*`, a97 `lz_v/c/e/g/h_*`, a88 `k9_phys`, a89 k14, a93 anime cum clips | **on 2s** (`r` 0.03-0.13): exact pairs, 12 drawings/s |
| a97 `lz_s/f_bj_*` (same keyframe+seed as `lz_v_bj_*`, a different script) | on 1s, but almost no motion (median 0.4) |

So the "already stepped" look of the a96/a97 raw clips is H3 drawing on 2s itself, not only
bursts. The mode depends on the keyframe and the script, and it is not the style words alone:
`k2_phys` and `k9_phys` have the same "2D anime ... TV-anime style" opener and land in different
modes.

Round a99 (`tools/rounds/mk_a99.py`, `jobs/a99_smooth.jsonl` + `a99b_smooth.jsonl`, 3080,
anime timing off), same keyframes + seeds as known on-2s clips:
- `phys`: the TV opener + a micro-motion paragraph ("breasts are soft and heavy: they bounce on every
  stroke, wobble and keep rippling for a moment after each one before they settle, the near breast
  lagging a beat behind her hands; shoulders and upper body rock with the rhythm, hair bounces and
  sways behind the motion, chest rises and falls with her breath, a sweat sheen glides over her
  skin"; BJ: shoulders/back rock, hair loops swing and settle a beat after her head stops, breasts
  sway, throat and jaw shift).
- `l2d`: `phys` + the opener "A smooth, fluid 2D animation in the style of a high-frame-rate h-game
  scene, cel-shaded art with flat colours, hard-edged shadows and glossy white highlights on the
  skin, every movement soft and continuous, one fixed camera."
- `l2d2`: "A smooth, fluid 60 fps 2D animation like a Live2D h-game scene, soft-body physics, clean
  anime art, every movement soft and continuous with gentle follow-through" (no cel/shadow words).

| clip | keyframe / seed | mode | notes |
|---|---|---|---|
| `sv_pz_wide_l2d` | a96 silver braid `pz_wide_tv_2` / 96101 | **on 1s**, median 7.2, 0 held | control `v_pz_wide` is on 2s: the wording flipped it. Continuous motion, longer stroke (glans up to her chin at f40), TV look holds |
| `lz_pz_wide_phys` / `_l2d` | a97 Lanzhu `pz_wide_2` / 96101 | on 2s | `l2d` doubles the motion (median 2.9 vs 1.2), breasts squash and travel more; open grin as in the control |
| `lz_pz_wide_l2d_97102` / `_99101` | same, two seeds | on 2s | the seed is not the switch |
| `lz_pz_wide_l2d2` | same / 96101 | on 2s | style holds without the cel words; the blotchy pink inner-breast band is back (f48, f72) |
| `lz_bj_profile_phys` / `_l2d` / `_l2d2` | a97 `bj_profile_3` / 97101 | on 2s | built on the a97b script, so the red lip flare returns; head travel small |

Read so far: **wording can flip a keyframe to on 1s, but the Lanzhu keyframes are locked on 2s**
(three seeds, three openers). The micro-motion paragraph adds travel and squash, but on 2s it is
still 12 drawings/s. Since the on-2s clips are exact duplicate pairs, the robust route is a
post-pass that is the mirror of `anime_timing.py`: drop each duplicate and interpolate between the
62 unique drawings (RIFE/FILM; the engine has the core `FrameInterpolate` node, but no model file in
`models/frame_interpolation` and none in `kit/models.json` yet). Keep the micro-motion paragraph for
the jiggle itself; interpolation smooths the timing, it does not add follow-through.

**Owner on a99:** reads as more physics on the anime clips, not as live2d motion; the profile cock looks
odd. So the micro-motion paragraphs are kept as an **anime option for more dynamics** (Video tab
**Dynamics**: `jiggle_pz`, `jiggle_bj`, `hgame_pz` = the h-game opener + `jiggle_pz`; `dynamics_video`
in `kit/presets.json`, job key `dynamics`; applied by `core.edit_script`, which now also runs the
Breasts option).

### The smooth post-pass: `kit/studio/anime_smooth.py` (round a99c)

The mirror of `anime_timing.py`: finds H3's copies (the frame changes split into two groups on a log
scale, Otsu; a clip that is already on 1s keeps every frame), drops them and redraws every
in-between with a frame-interpolation model, using the engine's own code
(`comfy_extras/nodes_frame_interpolation.py`), locally on the GPU. Length and audio unchanged.
Models in the store: `frame_interpolation/rife_v4.26.safetensors` (default) and
`film_net_fp16.safetensors` (Comfy-Org, `kit/models.json`; `frame_interpolation` is now a wired
folder). ~30 s per 124-frame 1152x768 clip on an 8 GB card.

```
F:\LLStudioTest\engine\ComfyUI_windows_portable\python_embeded\python.exe -I kit/studio/anime_smooth.py in.mp4 out.mp4 [--model rife|film] [--mult 2]
```

On the page it is part of **Anime timing**: `smooth` (RIFE), `smooth_film`, `smooth_x2` (48 fps); the
clip as generated stays as `-raw`. Results (`gallery/a99/*_smooth_*.mp4`, `analysis/a99c_interp_*.jpg`):
- every on-2s clip comes out on 1s (61-63 drawings in, 124 frames out, `r` 0.98-1.0);
- the in-betweens are clean at the fastest frames (paizuri f38-42, the profile head jump f26-30): no
  double image, the glans keeps its shape between drawings; RIFE and FILM look alike there.
- `lz_e_pz_wide_96101_smooth_rife` and `lz_e_pz_close_97102_smooth_rife` are the owner-approved a97 clips
  smoothed; `lz_pz_wide_l2d_smooth_rife`/`_film` the a99 dynamics clip.
- `hgv_bj_profile_*_smooth_rife`: the two h-game BJ clips below (on 2s from H3), smoothed.

### The art style is the switch: h-game keyframes (rounds a99d-g)

Lanzhu LoRA + identity tags on `anime_lz_side`'s graph, the `tv` block swapped for an h-game CG block
(`jobs/a99d_hgame_keys.jsonl`; negative: the `painterly, thick painting` ban removed, `flat color,
cel shading, anime screenshot` added):
- `hgf`: `newest, game cg, eroge, @fuzichoco, (soft shading:1.2), gradient shading, (shiny skin:1.2),
  oily skin, glossy skin, detailed skin, rim lighting, soft lighting, bloom, sweat drops` (the artist
  of the smooth a05 `k2` keyframe) - softer, more painterly;
- `hg`: the same without the artist, `(gradient shading:1.1)`, `(skin shine:1.1)`, `depth of field`.

Both keep her design (pink side buns, blue eyes, mole) with soft gradient shading and glossy skin.
Clips (`jobs/a99e_hgame_clips.jsonl`, the a97 scripts + Dynamics, timing off):

| clip | mode (H3 itself) | notes |
|---|---|---|
| `hgv_pz_wide_hg_99002` (dynamics `hgame_pz`) | **on 1s** (`r` 0.82) | same seed as the on-2s TV clip |
| `hgv_pz_wide_hgf_99001` (`hgame_pz`) | **on 1s** (`r` 0.98) | owner: good, but an odd moving fold in the front middle (a crease across the near breast, f20-40) |
| `hgv_pz_wide_hgf_99001_smooth` (+ Breasts: smooth, a99f) | on 1s (`r` 1.00) | the fold is gone, the near breast stays one round shape |
| `hgv_bj_profile_hg_99001` (a97f script + `jiggle_bj`) | on 2s | the seal opens around f20-40, glans in front of her open mouth |
| `hgv_bj_profile_hgf_99001` | on 2s | lips stay on the glans, little head travel |

**Owner (a99e): "we definitely have the recipe to force this style of animation."** The h-game
keyframe puts H3 on 1s for paizuri; the profile BJ stays on 2s whatever the style, and the smooth
post-pass covers it. Templates:
- stills `anime_lz_hgame_pz`, `anime_lz_hgame_bj` (the `hgf` block, 1248x832; reproduce the a99d
  keyframes exactly, a99g);
- clips `anime_lz_hgame_paizuri` (`hgame_pz` + Breasts smooth baked in) and `anime_lz_hgame_bj_profile`
  (a97f script + `jiggle_bj`), 1152x768, Anime timing `smooth` by default (a no-op when H3 is already
  on 1s, the RIFE pass when it is not).

**Owner on a99f:** the wide clip still has the fold with Breasts: smooth. Likely specific to this
keyframe (`hgk_pz_wide_hgf_99001` already has squeeze creases where her arms press the breasts), not the
wording. Next: animate another h-game keyframe (`hgk_pz_wide_hg_99002`, the front-on one, was on 1s and
showed no fold at the checked frames), or reseed the still for one without arm creases.
- a99h (`jobs/a99h_template_clip.jsonl`): the `anime_lz_hgame_paizuri` template on the front-on
  `hgk_pz_wide_hg_99002` keyframe, seed 96101, through the page code: **no fold** (both breasts round and
  smooth f16-f64), H3 on 1s by itself (`r` 0.78, median 5.1; the smooth pass had nothing to do). Defect:
  from ~f20 her smile opens and the tongue tip shows despite the closed-mouth line (the same open grin as
  the a97 Lanzhu paizuri - likely seed 96101), and her fingers move onto the nipples. Prefer this
  keyframe over `hgf_99001`; a reseed may close the mouth.
- a99i (`jobs/a99i_template_seeds.jsonl`), same template and keyframe, two seeds: **99101 is the keeper** -
  the closed smug smile holds to f123, no fold, H3 on 1s (`r` 0.94). 97102 opens the smile with the tongue
  tip from ~f40 and draws small crease lines at the top of the cleavage around f80-100 (`r` 0.97). On all
  three seeds her fingers move onto the nipples after the first stroke (the keyframe's hand placement).
  Sheet: `analysis/a99i_seeds.jpg`.
