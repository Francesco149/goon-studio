# Scenes: a recipe index for multi-shot animations

An index to remix from, not a manual: sequences, shot types, looks and dynamics that worked, each
pointing at the measured reference and the known-good gen to copy. How to run a story:
`docs/STORY.md`. Add a line here whenever a new shot, look or arc works (owner verdict); keep the
details where they already live.

Gens are under `<data_dir>/<round>/` (the agent's gallery, `gallery/<round>/` here); stories in
`kit/stories/`.

## Sequences (arcs)

| arc | shots | story | status |
|---|---|---|---|
| **Meadow arc** - tease, act, intimacy, climax freeze, afterglow | back tease -> 3/4 BJ close-up (gaze him -> camera) -> POV headpat -> profile oral climax + freeze -> low-angle afterglow | `emilia_meadow` (a103 flatter cut) | owner: good |
| **Sweet paizuri arc** - same opening, paizuri build to a smiling climax | back tease -> 3/4 BJ (gaze shift) -> paizuri slow -> paizuri fast -> paizuri climax + freeze -> smiling afterglow | `lanzhu_hotel` (a104) | testing |

Pacing that works (from `emillia.mp4`, measured in `docs/STORY.md`): 5-6 shots in ~25 s, 3-6 s each;
alternate slow (on 3s, ~8 drawings/s) and fast (on 1s, 24/s) shots; a long freeze (~1.2 s) on the
climax; the last shot slow and quiet.

## Shot types

| shot | camera / staging | cadence | reference | known-good gen | notes |
|---|---|---|---|---|---|
| **Back tease** | extreme low angle, centred, directly behind her kneeling; her head buried in his lap/crotch, hips cover the act; his legs/jacket frame her | on 3s | emillia shot 1 | `a103/s1_c0_00002_.mp4`; `a104` s1 | lock it: `(back view)`, `(from directly behind)`, `(centered)`, negative side view + penis; owner prefers centred over a 3/4 view |
| **3/4 BJ close-up** | face fills the frame from slightly above, plain background (grass/sheets), his jacket at one edge | smooth (24/s) | emillia shot 2 | `a103s2/s2_c0_00002_.mp4` | gaze shift in one clip (him -> camera) works; clear saliva wording |
| **POV headpat** | from his chest straight down; he stands, she kneels bent forward, feet up; his hand strokes her head | H3's own (`off`) | emillia shot 3 | `a103/s3_c0_00003_.mp4` | her eyes close with each stroke; the hair flower jumps under the hand (open) |
| **Profile climax** | side close-up, his hand on her head, overflow at the lips | on 2s + 28-frame freeze | emillia shot 4 | `a103/s4_c0_00001_.mp4` | `anime_ll_cumshot` LoRA at 0.5 |
| **Low-angle afterglow** | from below her chin against the sky, head back, tongue out with strings | on 3s + short hold | emillia shot 5 | `a103/s5_c0_00003_.mp4` | `solo` + no penis/male in the negative |
| **Profile BJ** | side, his hand on her head | on 2s | 7-min ref s15 (`docs/ANIME-TIMING.md`) | `a96/v_bj_profile_00001_.mp4`; `a97/lz_f_bj_profile_00001_.mp4` | no cheek words in the script (a97f) |
| **Paizuri POV, wide** | from above, she presses her breasts, glans at the top of the cleavage | slow: `off`; fast: smooth | 7-min ref s20 | `a97/lz_e_pz_wide_96101_00001_.mp4`; h-game `a99/tpl_hgame_paizuri_hg_99002_s99101_00001_.mp4` | squeeze words draw folds: Breasts "smooth" wording |
| **Paizuri close** | on the cleavage, glans below her chin | on 2s | 7-min ref s21 | `a97/lz_e_pz_close_97102_00001_.mp4` | keyframe decides tongue/no tongue |
| **Paizuri climax** | continues from the fast paizuri shot (`start_from`); three thin ropes out of the cleavage landing unevenly on one side; she smiles at the camera | on 2s, **no freeze** | - | `a104/s5_c0_00003_.mp4` | owner: good continuity and dynamics; ropes still a little thick |
| **Cum shot (face)** | close on her face, ropes landing unevenly on one side | on 2s | BlobCG refs (`docs/archive/REFS.md`) | templates `anime_ll_cumshot`, `anime_ll_cumshot_hard` (a93b/d) | three pulses, never thicker ropes (`docs/CUM-VIDEO.md`) |
| **Golden BJ POV** | from above, head grab / two hands / tip tease | on 2s | - | templates `anime_ll_headgrab_push` ... (a26) | the dynamics gold standard |

## Looks

| look | where the blocks live | reads as |
|---|---|---|
| **flatter** (owner's pick for h-anime) | `emilia_meadow` `variants.flatter`; `lanzhu_hotel` `blocks.style` | flat TV h-anime, matte, a thick veiny but flat-coloured penis |
| flat | `emilia_meadow` `blocks.style` | flat TV anime with a little shading |
| tv | `docs/ANIME-TIMING.md` (a96 `tv`) | cel-shaded TV with gloss - closer to h-game, reads "AI" for flat refs |
| h-game (smooth motion) | templates `anime_lz_hgame_*` (a99) | soft gradient CG; H3 animates on 1s by itself |

The series tag of the character's show (`re:zero ...`, `love live! nijigasaki ...`) in the style block
pulls that show's own look.

## Dynamics and direction that work

- Cadence per shot: `timing` on2/on3/off/smooth (`docs/STORY.md`); smooth = RIFE.
- **Freeze frames (`hold`) only for shots designed around one** (the meadow's oral climax, an impact
  stopper) - owner: not a good fit for the sweet paizuri climax. Put `at` on the event (the frame-difference peak).
- Bigger climaxes: never more pulses (faster twitching, a93c/a104); three pulses, vary where they land.
- Micro-motion (jiggle, follow-through, breathing): Video tab **Dynamics** (`dynamics_video`).
- A gaze shift inside one clip works when it is slow ("looks up into his eyes ..., then slowly turns
  her gaze to the camera"); sweet vibe: "looks into the camera with a soft, sweet smile, lips closed".
- Fluids: describe one continuous result, never a repeated action (a looped "each time ..." swings
  back and forth); saliva "thin, clear, see-through, colourless like water, a small white glint".
- In H3 scripts describe the result, never the thing to avoid (a97).
- Consistency: one character LoRA, shared blocks, one seed per shot; watch tag bleed between the two
  people (give him his own colours: black trousers, black hair).
