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

## Round a102: flatter style, s1-s3 angles (2026-11-22)

Owner on a101: s1 does not read as a blowjob (she looks left, the pose is unnatural); s2/s3 have the
generic AI-art look; s3 lies in the grass while in the ref he stands; push the style flatter.
What the ref really is (key stills): almost no shading, matte skin, hatched blush lines, thin pale
lines; s1 the back of her head buried at his crotch; s2 a tight close-up against grass, eyes aside,
troubled brows; s3 he stands, she kneels bent forward with her boots up behind her.

- **Style block** `flat`: `year 2020, anime screenshot, re:zero kara hajimeru isekai seikatsu, anime
  coloring, (flat color:1.2), (minimal shading:1.1), matte skin, thin lineart, soft pastel colors,
  (diagonal-lined blush:1.1)`, negative `shiny skin, glossy skin, oily skin, specular highlights,
  gradient shading, detailed shading, rim lighting, bloom`; script style "flat colours with almost no
  shading, matte skin with no shine, thin clean lines, hatched pink blush lines". The series tag pulls
  the show's own look. `+ official style, (no shading:0.6)` (a102b) adds little.
- **The gloss words were the "generic AI" look**: `shiny skin`, `glossy`, `specular highlights` from
  the a96 `tv` block suit the h-game direction, not this ref.
- s1: `(facing away:1.3), (back of head:1.2), (face not visible:1.2), head between his legs`, negative
  `looking back, face, eyes, profile` - the act is hidden like the ref. s3: `(standing:1.1)` for him,
  `(kneeling:1.2), bent forward, feet up`, negative `lying, on stomach, sky`.
- Owner on the a102 keyframes: "a lot better in terms of style". Bleed fix: `(black pants:1.2)` in the
  partner block (his trousers were purple from her leggings).
- **a102 clips: the flat style holds in motion** (`analysis/a102_cut.jpg`). s1 now reads like the ref
  (the back of her head dips into his crotch on each bob); s3 the hand strokes and her eyes close with
  it; s4 his trousers black. Left: the hair flower jumps in s3 (f53-80); s5's collar still drifts to the
  canon dress. s3's `timing` is now `off`: on 2s over H3's own on-2s thinned it to 7.5/s; H3's own
  cadence gives 10.7/s (ref 18.3, a 1s/2s mix).
- **Variants**: a story can carry named overlays (`variants` -> `blocks`/`still`/`clip` replaced,
  `append` text added to e.g. the negative of every shot, `shots` {id: {...}}); `run_story.py
  --variant <name>`, the cut is named `<story>_<variant>_cut.mp4`. `emilia_meadow` has `flatter`
  (owner: "an even flatter look ... more like an actual h-anime; the shine on the penis gives the AI
  vibe"): `(flat color:1.4), (no shading:0.8), (matte:1.2), (simple coloring:1.2), (matte penis:1.2),
  (thick penis:1.1), veins, flat colored penis`, negative `shiny/glossy/wet penis, penis highlights,
  glossy lips, shine`. a102c tried `simple penis` + `detailed penis, veiny penis` in the negative: the
  veins went (owner: keep thick and veiny, only the colouring flat) - a102d is the fix.
- **One gaze per clip.** Owner: s2's "looks up at him, then turns to the camera" did not lock eyes
  with the camera. A change of gaze is a cut, not an instruction: s2 is now `s2a` (eyes on him) and
  `s2b` (`(looking at viewer:1.3), (eye contact:1.2)` in the keyframe, "looks straight into the camera
  the whole time" in the script), same seed so the framing matches. Same rule for any change H3 has to
  "turn to": give it its own shot with the end state in the keyframe.
- **Saliva** (owner): `(saliva:1.2), saliva trail` in the s2/s3 keyframes, and in the scripts saliva on
  the shaft, a string stretching from her lip on the pull-back and dripping from her chin. The
  `flatter` negative no longer bans `wet penis` (it fought the saliva); shiny/glossy/highlights stay.
- a103 (`--variant flatter`) after the fixes: s1 centred from directly behind (`(back view:1.2), (from
  directly behind:1.2), (centered:1.2), symmetrical`, negative side/three-quarter view and the penis -
  owner prefers the centred one, the hips cover the act like the ref), s2a/s2b gaze split works in both
  looks, s5 `solo` + negative `penis, 1boy, male, hand` (the flatter keyframe had put a penis in frame).
  Left: the hair flower jumps where his hand touches her head in s3; s5's collar drifts to the canon dress.
- **Owner, after a103:** the gaze split was not needed - the single-clip gaze shift in the earlier cut
  was fine; s2 is one shot again and both cuts use that earlier eye-contact s2 (restored with
  `--cut-only`). Saliva looked decent but **swung back and forth on the side shot instead of dripping**:
  "each time she pulls back a string stretches..." describes a repeating motion, so H3 loops it.
  Reworded as one continuous result: "a single trail of it runs slowly down from the corner of her
  mouth over her chin and falls away in drops into the grass" (a103s2, `--only s2` in its own round).
  The "one gaze per clip" note above is withdrawn as a rule: a slow gaze shift inside one clip can work.
- Saliva, owner on a103s2: right physics (it drips now), but **brown** (the shaft colour bled in) and a
  bit much. Fix (a103s2 take 2): "a thin, clear, see-through thread of saliva, colourless like water and
  visible only by a small white glint ... a few small drops"; keyframe `saliva, (clear saliva:1.1),
  transparent, saliva trail` instead of `(saliva:1.2)`. Result: a thin clear thread and small drops at
  the corner of the mouth, no brown. Side effects: the shaft reads wetter/glossier, and this keyframe's
  collar drifted to the canon dress.
- a103 final pass: s2 = a103s2 take 2 (gaze shift + clear saliva, owner-approved), s3 re-rendered with
  the clear-saliva wording, s5 collar fixed (`(off-shoulder shirt:1.3), (bare shoulders:1.3),
  collarbone`, negative `high collar, brooch, gold trim, dress`): off-shoulder top with bare shoulders
  like the other shots. Owner: "the new clips look good". Open: the hair flower still jumps in s3 where
  his hand touches her head.

## Round a104: `lanzhu_hotel` (2026-11-22)

The meadow arc with a paizuri climax (slow -> fast -> climax, sweet smile at the viewer), Lanzhu LoRA,
the flattest look with the Nijigasaki series tag, a hotel room at night. 6 shots, 28.5 s.
- Owner: the tease (s1, robe hiked to the waist over white panties, centred) and the paizuri shots
  are good; backdrop continuity between shots (lamp, window) is the next problem, after the penis.
- **New story options**: `key_image` (a shot animates from a fixed, e.g. hand-edited keyframe) and
  `start_from: "<shot id>"` (a shot continues from the last frame of that shot - no cut in the
  staging; the cut drops the repeated frame).
- s2 penis (owner: needs length and girth to match the paizuri, tip too red; the cute dynamics are
  good): the keyframe was fixed with an **H3-Image one-picture edit** (`wf_h3img_1ref.json`, "keep her
  exactly ... only change the man and his penis: his body further back at the right edge, a very
  long, very thick veiny shaft ...") - the face stays identical. Two passes: thicker (`s2_key_edit_104201`),
  then longer (`s2_key_long_104211`). In motion: length/girth right, but the veins came out as a net-like
  texture and the head still turns dark red on the pull-up (the blowjob act LoRA; "its head is the same
  tan skin tone as the shaft" did not override it). Without the act LoRA (a104s2 `bj_nolora`) there is no
  red at all, but she barely moves.
- s5 climax now `start_from: s4` and written as uneven: "the first spurt ... lands across her left cheek
  and chin; a second, smaller one splashes onto her right breast a moment later; the last only wells out
  ... The cum lands unevenly, more on one side". Result: one arc up and over to one side, uneven splashes
  - no longer the mirrored pattern of the first take.
- s5 variants (`--variant s5_more|s5_asym`, own rounds `a104_s5_*`): **`s5_more` (five very thin strands)
  failed** - owner: it just makes faster twitches with a similar shot. Same as a93c: more pulses means
  faster twitching, not more ropes. Keep three pulses; vary where and how they land instead.
- **Place a freeze on the event, not at a fixed time** (owner: an odd freeze at the climax in the cut,
  not in the clip). s5 had `hold` at 1.0 s; after `start_from` the spurts come at frames 2-15 and by
  frame 24 the shot is already settling, so the freeze landed in the calm part. Check the frame
  differences of the clip (the big changes = the event) and put `at` on the peak: s5 now
  `{"at": 0.42, "frames": 12}`.
- **s2 glans (the pull-out breaks the penis)**, a104 re-anchor tests (`tools/rounds/reanchor.py`, new job
  keys `ref` = the picture the object is repaired toward, `repair_prompt`; `core.run` now uploads `image2`):
  - `s2_old_repair` (the liked old clip, 5 anchors, ref = the 104303 keyframe): owner - the new penis made
    it into the clip but deforms oddly between anchors (the a98 morph).
  - Penis reference stills (`s2_penisref_*`: the same scene with the penis out of her mouth, fully visible,
    defined glans): owner picked `s2_penisref_104601`.
  - `s2_303_repair_dense` (11 anchors, ref = penisref): anatomy right on every frame, but the edits copied
    the reference's pose (hand on the shaft, tip at her lips) - owner: motion completely wrong, the penis
    pulled in and out unrealistically fast (pass 2 races between in-mouth frames and out-of-mouth anchors).
    **An anchor edit must not change the pose**: `s2_303s` = the same with a strict repair prompt (Picture 2
    only shows what the penis looks like; lips, depth and hands stay as in Picture 1).
  - `s2_303s` (strict prompt): the edit model **still** adds her hand and pulls the penis partly out to show
    the head, on every anchor - it reads "look like Picture 2" as the pose. Stopped before pass 2.
  - Conclusion: anchor edits fail both ways on this shot - few anchors morph between them, and a reference
    in another pose drags the anchors off the motion. Open leads: Ref2VA with the penis reference as a
    named `<Picture N>` (identity on every step, no anchors to fight; a98 saw the object shrink with a
    keyframe ref), or a masked edit (`wf_h3img_2ref_inpaint.json`) so only the penis area can change.
  - **Ref2VA with the reference** (`wf_h3vid_ref2va_first2.json`: `<Picture 1>` = the s2 keyframe, also pinned
    as frame 0; `<Picture 2>` = `s2_penisref_104601`, named in the script "His cock looks exactly like the one
    in <Picture 2> ... also when it slides out of her lips"; round `a104r2`, seeds 104002/104701): the penis
    is **consistent on every frame** (defined head, the reference's size and shape, no degrading or morph) -
    but **the motion is gone** (median frame change 0.3 vs 4.2 for the i2v clip) and the act drifts to the
    reference's pose (tip at her lips). The act/motion LoRAs are i2v (FL2VA) LoRAs and barely act on Ref2VA.
- **The fix (owner's trick): glans suck -> deep throat from its deepest frame.** The Ref2VA clip has a correct
  glans and good suction but only sucks the glans. `s2a` uses it as it is (`clip_file` + `clip_range`
  [8, 52]: frame 0 is the pinned keyframe and jumps; frame 52 = lips furthest down, past the rim); `s2b`
  starts from frame 52 (`key_image` = that frame, `continues: true` so the cut drops the repeated frame)
  with a deep-throat script on the normal i2v model + act LoRA. Result: the penis stays right (no pull-out
  ever exposes the glans to a redraw, no red), real motion again (median frame change 6.4 vs 0.4), and the
  seam is a normal motion step (7.8). New story options: `clip_file`, `clip_range`, `continues`.

## Round a106: `lanzhu_night` (2026-11-23)

Tease angles (beloved), the newjersey blowjob arc, front cowgirl with a breast grab and the switch to her
taking over, a legs-grabbed missionary - 13 shots, Lanzhu, flattest look, on ampere. Act LoRA for the sex
shots: `HMNSFW_AIO_V2` (HearmemanAI, Civitai 2834417, no trigger words; on ampere, not yet in the registry).
`Minimax3_BoobPhysics_v1` on ampere is a 15-byte "Entry not found" file (a failed download) - the real one is
Civitai version 3245935.
- **Chained clips degrade** (owner): each `start_from` hop starts from a frame H3 already redrew, and the line
  art thickens hop by hop (b3 slightly, b4 clearly). New shot key `restore: "<shot id>"`: the start frame of a
  continuation is first redrawn by a two-picture H3-Image edit in the art style of that shot's keyframe
  (`story.RESTORE`: same pose and composition, the keyframe's line weight and flat colours).
- t1 (under the breasts): her body stood still while the breasts bounced - the script now rocks her whole body.
  b1 (lick): best expression and pose, but the short laps of the tongue looked unreal and cut the penis oddly -
  one long slow lick up the shaft and a kiss on the tip instead. b2/b3 sucking dynamics were weak - the golden
  a26 wording ("slides her mouth up until only the head stays between her lips, purses ... small wet pop").
- a106 after the fixes: `restore` kept the BJ chain's line art flat (b2-b5, ink share 19-22%, no climb); b2 eyes
  closed -> eye contact works; b5 holds the first pulse then pulls off smiling. Owner: b6 (tongue show) very cute;
  cowgirl: c4 perfect (she leads, hands on his chest), c2 least rigid (squats on her legs), c1 rigid (no driver for
  the bounce) - `cut: false` keeps c1 out of the edit, the sex part opens on c2. b1 tip tease + kiss: nice; variants
  `b1_under` (tongue behind the tip) and `b1_side` (lips sliding along the side of the shaft).
