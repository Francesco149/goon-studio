# Stories: longer animations from chained shots

A clip from H3 is at most 124 frames (5.2 s). A longer animation is a **story**: a list of shots,
each one keyframe and one clip (or a chain of clips), cut together with hard cuts like the
reference. Consistency across shots comes from shared text blocks and one character LoRA, not
from one long generation.

- story files: `kit/stories/*.json`
- engine: `kit/studio/story.py` (expand to jobs, cut), runner `tools/rounds/run_story.py`
- first story: `kit/stories/emilia_meadow.json` (round a101), after `gallery/refs/art-study/refs/emillia.mp4`

## The method (from a reference video)

1. **Measure the reference**, don't trust the write-up's numbers: cuts (frame difference > 25 at
   160x90), per shot the drawings per second and the hold lengths (a frame equal to the previous one
   is a held drawing). The Gemini write-ups get frame counts wrong (a95, a101 below).
2. **Write the shared blocks once**: `style` (keyframe style tags), `character` (LoRA trigger +
   identity tags), `outfit`, `partner`, `setting`; and the prose versions for the H3 scripts
   (`script_style`, `script_character`, `script_partner`, `script_setting`). Every shot uses them as
   `{name}` placeholders, so a change to the outfit or the light reaches every shot.
3. **One shot = one entry**: `seconds` (from the measurement), the keyframe tags (`still`), the
   H3 script (`script`), a video `template` for the act LoRA settings (its prompt is replaced by
   the script), `timing` (the measured cadence), `hold` (measured freezes), optional `still_job` /
   `clip_job` overrides and `seed`.
4. **Keyframes first** (`--keys-only`), look at them next to the reference's contact sheet, fix the
   shots that drift (`--only s1 --redo`), then render the clips.
5. **Cut**: each shot trimmed to `seconds`, re-timed, joined; the clips' own audio stays in sync.

```
python_embeded\python.exe tools/rounds/run_story.py kit/stories/<story>.json <round> --engine <url> --keys-only
python_embeded\python.exe tools/rounds/run_story.py kit/stories/<story>.json <round> --engine <url> --only s1 --redo --keys-only
python_embeded\python.exe tools/rounds/run_story.py kit/stories/<story>.json <round> --engine <url>
python_embeded\python.exe tools/rounds/run_story.py kit/stories/<story>.json <round> --cut-only
```

Output: `<data_dir>/<round>/<story>_cut.mp4`; every keyframe and clip stays next to it; the job
record is `jobs/<round>_story.jsonl` (a rerun skips what is already made).

### Timing per shot

| `timing` | what the cut does |
|---|---|
| `off` | as H3 drew it |
| `on2` / `on3` / `on4` | hold each drawing 2/3/4 frames (the sharper of each pair) - `anime_timing.py` |
| `smooth` | drop H3's copies and interpolate (RIFE) - `anime_smooth.py`; for on-1s action |

`hold: [{"at": 1.3, "frames": 28}]` freezes the drawing at 1.3 s into the shot for 28 frames (the
stopper), keeping the shot's length.

### Long shots (chaining)

A shot longer than one clip continues: the next clip starts from the **last frame** of the one
before (`seg_len`, 49 frames by default) with the same script, and the cut drops the repeated
frame. Clip lengths snap to the page's 49 / 81 / 124. The same mechanism makes a shot of any
length; how long it stays coherent is open (a101 tests one 49-frame continuation per long shot).

### What keeps the shots consistent

- one character LoRA at a fixed strength and the same identity + outfit tags in every shot;
- the same style block and setting/light in every shot, keyframe and script;
- the partner described the same way everywhere (here: the open red track jacket);
- watch for **tag bleed**: an outfit tag lands on the other person (a101: her red jacket on s1, his
  purple trousers on s2/s4). Drop the partner tags from shots where he is barely in frame and put
  the bleeding item in that shot's negative.

## The reference: `emillia.mp4` (measured, a101)

1280x720, 60 fps container, 25.35 s; the write-up is
`gallery/refs/art-study/EMILIA_2D_ANIMATION_ART_STUDY.md`, sheets and key stills in
`gallery/refs/art-study/analysis/emillia_study/` (local, never committed).

| shot | time | what | drawings/s | holds |
|---|---|---|---|---|
| 1 | 0.00-6.05 | extreme low angle from behind, straddle bounce in purple leggings | 7.9 | on 3s (7-8 ticks of 60) |
| 2 | 6.05-11.50 | three-quarter blowjob, kneeling in the meadow, his red jacket at the left | 24.0 | on 1s |
| 3 | 11.50-17.13 | POV from his chest, she lies between his legs, his hand strokes her head | 18.3 | 1s/2s mix |
| 4 | 17.13-20.38 | profile close-up, oral climax, overflow, his hand on her head | 8.9 | on 2s, then **one 1.17 s freeze** (70 ticks = 28 frames at 24 fps; not 16 frames as written; not a black screen) |
| 5 | 20.38-25.35 | low angle against the sky, dazed, tongue out with cum strings | 7.4 | on 3s, one ~0.4 s hold |

## Round a101: `emilia_meadow` (2026-11-22)

Keyframes on ampere in ~17 s each, clips 60-155 s each (13 jobs, ~20 min), the cut in ~20 s:
`gallery/a101/emilia_meadow_cut.mp4` (25.33 s; the ref is 25.35 s). Sheets: `analysis/a101_keys.jpg`
(keyframes next to the ref's contact sheet), `a101_cut.jpg`, `a101_seams.jpg`.

| shot | drawings/s (ref) | holds | read |
|---|---|---|---|
| s1 | 7.9 (7.9) | on 3s | owner: the first version was cowgirl - the ref is a **blowjob seen from low behind, her hips hide the action** (the write-up called it a straddle bounce). Rewritten: she kneels bent forward, the man in red stands in front. Her head stays turned sideways, so the act is only implied and the bob is small |
| s2 | 23.6 (24.0) | smooth (RIFE) | steady three-quarter bob, eyes up, jacket at the left; his trousers came out purple (tag bleed from her leggings) |
| s3 | 11.0 (18.3) | on 2s | the closest to the ref: POV past his chest, his hand strokes her head and her eyes close with it |
| s4 | 6.8 (8.9) | on 2s + 29-frame freeze (28) | eyes squeezed shut, tear, overflow dripping from the lips; purple trousers again |
| s5 | 7.3 (7.4) | on 3s + 10-frame hold | dazed upward eyes, tongue out with cum, strings; almost no motion; her collar drifts toward the canon dress |

- **Continuation seams are invisible**: the 49-frame clip that starts from the last frame of the first
  one keeps pose, light and identity (s1/s2/s3 frames 121-124).
- **Identity holds across all five shots** (crown braid, flower, X clip, ribbon, ears) with one LoRA
  and the shared blocks; the TV cel look too.
- Open: tag bleed between the two people (outfit colours); s1's head should be buried in his lap;
  shot 3's mixed 1s/2s cadence (on 2s is close; `off` would keep H3's own); s5 needs a little motion.
