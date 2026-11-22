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
