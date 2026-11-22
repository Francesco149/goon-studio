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
