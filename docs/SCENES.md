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
| **Sweet paizuri arc** - same opening, paizuri build to a smiling climax | back tease -> 3/4 BJ (gaze shift) -> paizuri slow -> paizuri fast -> paizuri climax -> smiling afterglow | `lanzhu_hotel` (a104) | **owner: with the meadow arc, the golden standard** |
| **Sweet night** - tease, newjersey BJ arc, cowgirl, missionary | over-him tease -> tip lick -> tip suck -> suck (eyes closed -> eye contact) -> speed-up -> faster (fresh keyframe) -> cum in her mouth, pull off (cheek-puff keyframe) -> tongue show -> cowgirl (squat, his speed-up, her hands on his chest) -> missionary | `lanzhu_night` (a106) | owner: solid after fixes, less smooth than the two above; good new poses |
| **Goddess evening** - tip tease, slow suck, deep throat, oral climax, tongue show + wink | lick -> take the tip in (transition script) -> slow suck (suction face) -> deep throat (`extend`) -> climax held deep: twitch, veins, cum seeps (`extend` hop 2) -> tongue show, swallow, wink | `aqua_evening` (a109/a110, Illustrious keyframes) | a110 owner: pretty good (t1 phasing, s2 shorter); v3 a113 (P5 t1, s2-s4 extended from it, suction script) awaiting owner |
| **Photoreal night** - lick tease, golden BJ + faster, side deep throat, cum shot, afterglow | POV lick -> golden POV BJ -> faster (`extend`) -> side-profile deep throat -> `cumshot_medium` on her own keyframe -> licks her lips and smiles (`extend`) | `egirl_night` (a111) | **owner: solid** (both cuts); the own-girl cum-shot pose is a recipe |

Pacing that works (from `emillia.mp4`, measured in `docs/STORY.md`): 5-6 shots in ~25 s, 3-6 s each;
alternate slow (on 3s, ~8 drawings/s) and fast (on 1s, 24/s) shots; a long freeze (~1.2 s) on the
climax; the last shot slow and quiet.

## Shot types

| shot | camera / staging | cadence | reference | known-good gen | notes |
|---|---|---|---|---|---|
| **Back tease** | extreme low angle, centred, directly behind her kneeling; her head buried in his lap/crotch, hips cover the act; his legs/jacket frame her | on 3s | emillia shot 1 | `a103/s1_c0_00002_.mp4`; `a104` s1 | lock it: `(back view)`, `(from directly behind)`, `(centered)`, negative side view + penis; owner prefers centred over a 3/4 view |
| **Glans suck -> deep throat** | the 3/4 close-up: Ref2VA glans suck, then a deep throat from its deepest frame | off -> smooth | - | `a104` s2a+s2b (`lanzhu_hotel_cut.mp4` 6.0-11.45 s) | the fix for a glans that degrades on the pull-out |
| **3/4 BJ close-up** | face fills the frame from slightly above, plain background (grass/sheets), his jacket at one edge | smooth (24/s) | emillia shot 2 | `a103s2/s2_c0_00002_.mp4` | gaze shift in one clip (him -> camera) works; clear saliva wording |
| **POV headpat** | from his chest straight down; he stands, she kneels bent forward, feet up; his hand strokes her head | H3's own (`off`) | emillia shot 3 | `a103/s3_c0_00003_.mp4` | her eyes close with each stroke; the hair flower jumps under the hand (open) |
| **Profile climax** | side close-up, his hand on her head, overflow at the lips | on 2s + 28-frame freeze | emillia shot 4 | `a103/s4_c0_00001_.mp4` | `anime_ll_cumshot` LoRA at 0.5 |
| **Low-angle afterglow** | from below her chin against the sky, head back, tongue out with strings | on 3s + short hold | emillia shot 5 | `a103/s5_c0_00003_.mp4` | `solo` + no penis/male in the negative |
| **Lap pillow + nursing handjob** (sweet) | three stagings that make physical sense: **sofa** - she sits, he lies on his back along the sofa with his head in her lap, she leans her breast onto his face, strokes him with one hand, the other in his hair (refs `lap_pillow_sofa_pixel.png`); **bed** - she lies on her side curled over him (ref `lap_pillow_bed_ai.webp`); **on top** - she lies half on him, breasts on his face, reaching down (blob-present opening) | `off` (H3's own) | `gallery/refs/art-study/refs/lap_pillow_*`, blob-present 0-15 s | keyframes `a105/lap_sofa_105003`, `lap_bed_105001/105002`, `lap_ontop_10500*`; clips `a105/lapv2_*.mp4` (owner: on top the best, sofa and bed very good), `lapv3_ontop_105002` (clearer saliva), sofa `lapv5_sofa_105101` / `105003` - **no precum** (v2 had random smoke at the right - reseed, never name it; v3's saliva wording gave too much on the sofa; v4: "only now and then a tiny, thin, clear thread ... glints at his lips", and the precum as one continuous result: "forms at the tip and stays there, slowly growing and running a little way down" - v3's "glistens" bead appeared and evaporated, v4's growing bead dripped and both v4 seeds grew steam from the tip - precum wording dropped for this shot, which also removed the smoke) | owner: a winning recipe. Tags `(lap pillow:1.3), (nursing handjob:1.3), breast sucking, her hand on his penis`; negative his own hand (sofa 105002 had him stroke himself); spell out both of his legs on the sofa (105001 lost one). No act LoRA - motion booster only. Script details: clear saliva thread between his lips and her nipple ("colourless like water, visible only by a small white glint" - v2's plainer wording came out tinted), his cock twitching in her hand, a bead of precum (owner; also fixed a dark blob at the mouth-breast contact). Keyframe tags/scripts: `jobs/a105_lap_keys.json`, `jobs/a105_lap_scripts_v2.json`. **Also clean with an Illustrious character LoRA in its stock look** (a128, Uzaki Hana `uzaki_il_v2` on WAI v17, sofa + on top, owner: clean): style line "keeps the look of the first frame", no flat words - `tools/rounds/mk_a127.py`/`mk_a128.py` |
| **Front cowgirl** | low angle from between his legs, she rides facing the camera (blob present 24-57 s) | off / smooth | blob present part 2 | `a106/c4_c0_00001_.mp4` (owner: perfect, the most natural); `c2` (least rigid) | **the motion must have a driver**: she presses both hands on his chest and leads (c4), or squats on her feet and uses her legs (c2). A bounce with nothing propping her up reads rigid (c1); if he leads, he must visibly grip her hips and thrust her up (c3: better, still stiff, weaker face). Act LoRA `HMNSFW_AIO_V2` 0.6 + booster 0.5. Wanted next: fluid and skin movement around the penis and vagina |
| **Tip tease (lick / slow tip suck)** | the overhead stomach POV, tongue under the glans (`b1`), or a slow suck on the tip only | off | newjersey ~21 s | keyframes `gallery/a106k/b1_key_s106502_00001_.png` (owner: the cutest), `..._s106501` (solid), `..._s106503` (good slow tip-suck tease) | tags `(thick penis:1.2), the shaft as thick at the base as at the head, penis rising from between his thighs` fixed a thin, off-centre base; edits of the base left seams |
| **Tongue show** | close on her face, cum on her tongue, smiles and swallows | on 3s | newjersey ~57 s | `a106/b6_c0_00001_.mp4` | owner: good, very cute |
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

## Optional style tweaks (ideas, untested)

| tweak | where | note |
|---|---|---|
| a couple of stray pubic hairs at her lips during a blowjob | BJ shots, keyframe tags + one script sentence | some like the detail |
| she shows the load in her open mouth, a stray pubic hair in it | an afterglow / "show" shot after an oral climax | |

## Dynamics and direction that work

- Cadence per shot: `timing` on2/on3/off/smooth (`docs/STORY.md`); smooth = RIFE.
- **Freeze frames (`hold`) only for shots designed around one** (the meadow's oral climax, an impact
  stopper) - owner: not a good fit for the sweet paizuri climax. Put `at` on the event (the frame-difference peak).
- **Glans breaks on the pull-out?** Ref2VA with a penis reference (`wf_h3vid_ref2va_first2`) gives a correct
  glans but only a glans suck; use it as it is, then cut to a deep throat started from its deepest frame
  (`clip_file`/`clip_range` + `key_image`/`continues`, `lanzhu_hotel` s2a/s2b, a104). The penis never leaves her mouth.
- **Photoreal cum shot inside a scene** (a111 r5, owner: solid, as aesthetically pleasing as `p1_pose`): `cumshot_medium`
  seed 970 as is, on a Krea 2 + Verite keyframe of the scene's own girl (the BJ character block, still in
  `kit/stories/egirl_night.json` r5; seed 111503): kneeling, holding him upright under her open mouth, her tongue on the
  tip. Keeps her identity; `p1_pose` is a different woman. Then an `extend` afterglow (r6).
- **No tears** (owner, a113: "odd, doesn't look good"): never write watering or teary eyes into a BJ script, even for a
  deep throat; H3 draws heavy streaming tears.
- **Suction on an extension** (a112s): an `extend` beat has no keyframe for the lip shape - write the seal into the
  script: "stops smiling, closes her lips tight around the shaft and begins to suck", then the plain bob line and the
  a106 suction line; no smile, no saliva sentence (`aqua_evening` s2).
- **Size continuity between beats** (owner-confirmed fix: extend, a112): a fresh keyframe per beat redraws his size - s2 came out shorter than
  t1. Keyframe tags do not fix it (a112: size tags, composition tags, "sucking the tip" - 12 keyframes, none kept the
  length). **Same angle: start the next beat as an `extend` of the previous clip** (`start_from` + `"extend": 22`), not a
  fresh keyframe - a112 `C_ext_t1` held t1's length for the whole clip. A new angle is still open (reference, probe D).
- **Lick -> take it in (no cheek phasing)** (a110p, owner asked for a recipe): **the script must start from what the
  keyframe shows and describe the transition.** A lick keyframe with a script that opens "with the head of his cock in
  her mouth" makes H3 sweep the glans across her cheek/nose into her mouth in ~6 frames (a109 t1, a110p P1). Writing
  "with her tongue out, licking the underside of the head of his cock. She gives it two slow licks, then lifts her head a
  little, moves her open mouth over the tip, closes her lips around the head of his cock and bobs ..." moves her head to
  the penis instead - clean on the cheek-side keyframe (P2), the tip-at-her-lips one (P3) and an upright centred shaft
  (P4, used in `aqua_evening` t1; owner: still phases a little through her upper lip at ~f50-56 as the tip goes in).
  a112 P5 swaps the take-in for "raises her head until her mouth is above the tip, opens her mouth wide and lowers it
  down onto the tip from above, closing her lips around the head of his cock": the upper lip stays above the glans
  (`a112/P5_lower`, one seed, awaiting owner).
  The keyframe geometry matters less than the script. General rule: never let the script's
  first state contradict frame 0.
- **BJ scripts: one plain mouth line** (a106, from comparing the good Emilia/hotel BJ shots with the weaker ones):
  the good ones say only "She bobs her head slowly and steadily along the shaft, her lips sealed tight around it" -
  no mouth mechanics. Spelling the mechanics out (a wet pop at the top, lips pulled forward, the head sliding back
  out, cheeks drawing in) makes H3 animate each literally: odd lip shapes, flat open mouths, and pull-outs that expose
  the glans to a redraw. Plain wording kept the shaft in her mouth and the seal steady (`a106_b1t_simple`,
  `a106_b2_simple`). Put the look in the keyframe (`(lips sealed around penis:1.3)`, the suction tags), keep the
  script plain, and add only gaze, expression, saliva and pacing.
- **The anchoring rule (owner):** whenever the penis is pulled out (shaft or glans visible), something must tell H3
  what it looks like at that moment - otherwise it shortens, the glans warps, and the lip shape is lost. Four ways:
  1. prompt + keyframe for the lip shape (the suction face below + its script line);
  2. a reference that carries everything: Ref2VA with the keyframe as `<Picture 1>` and a penis reference as
     `<Picture 2>` (`wf_h3vid_ref2va_first2.json`; steady object, less motion - a104r2, a106 `b2_r2va`: owner "pretty good" -
     the suction keyframe as Picture 1 keeps the lips; give the man reciprocating motion to make up for the calmer
     Ref2VA motion);
  3. re-anchor what it should look like pulled out (`reanchor.py` with `ref`) - only with a reference in the
     same pose, or the anchors drag the motion (a104);
  4. chain the pull-out: a clip that shows the penis out starts from a frame where it is out and correct (a
     keyframe that shows the whole penis, or the last frame of such a clip - a106 `b2_chain`); the inverse trick
     - glans suck -> deep throat from the deepest frame - keeps it from ever coming out (a104 s2a/s2b).
- **Anime BJ keyframe recipe - use this first for every anime BJ scene** (owner, a112k: "exactly what we want for
  suction", all 12 keyframes, including the ones sucking the side of the shaft and the balls; other approaches often
  missed the mouth look). Illustrious (WAI) + the character LoRA at 1.0 (`wf_illu_lora.json`, 1216x832, 28 steps,
  cfg 6), the flat TV look, generator `tools/rounds/mk_a112.py` (`still()`), blocks from `kit/stories/aqua_evening.json`:
  - positive: `{style}` (flat look + `(matte penis:1.2), (thick penis:1.1), (veiny penis:1.2), (veins:1.1), flat colored
    penis`), `{character}`, `{outfit}`, `1boy, hetero, nude male, (long penis:1.2), (large penis:1.1)`, `pov, from above,
    lying on stomach, between legs, (ass up:1.1), her hips raised behind her, fellatio, (penis in mouth:1.2), (protruding
    lips:1.3), (lips stretched along the shaft:1.2), sealed lips, (sucking:1.2), (hollow cheeks:1.0), (looking at
    viewer:1.2), blush, uncensored, {setting}`;
  - negative: the usual list + `shiny penis, glossy penis, penis highlights, glossy lips, tongue out, open mouth, frown,
    cum, white liquid, saliva`;
  - variants that also worked: KB adds `(shaft visible:1.2), (penis between her lips and his body:1.1), upper body,
    (centered:1.1)` (closer framing); KC swaps `(lips stretched along the shaft:1.2)` for `(sucking the tip:1.2), (glans in
    mouth:1.1), (long shaft visible below her lips:1.2), (penis upright:1.1)`. The seed decides deep / side-of-shaft /
    balls (a112k seeds 110101-110104: 01/03 deep, 02/04 side and balls).
  - Size between beats is not carried by these tags: a beat at the same angle after another clip is an `extend` of it.
- **The suction face (owner-approved recipe, a106k)** - the look to aim for in every sucking shot: lips sealed and
  pushed forward along the shaft, a small visible pout around it, cheeks a little hollow, eyes up at the camera.
  Unedited keyframes on the overhead lying-on-her-stomach POV (Lanzhu, flattest look), seeds 106201/106202/106203:
  `gallery/a106k/suck_lips_10620{1,2,3}_00001_.png` (owner: "exactly the suction face I want"). The tags, added to
  the usual BJ keyframe: `fellatio, (penis in mouth:1.2), (protruding lips:1.3), (lips stretched along the shaft:1.2),
  sealed lips, (sucking:1.2), (hollow cheeks:1.0), (looking at viewer:1.2), blush, saliva, (clear saliva:1.1)`.
  `(vacuum fellatio:0.6/0.9)` gave a weaker version. **Never edit the mouth with H3-Image**: drawing the lips in on a
  keyframe (a106k) and repairing a chained start frame toward the suction keyframe (`b2_chain_lips`) both came out
  overly exaggerated (owner). The lip shape only comes from an unedited keyframe made with these tags, or Ref2VA
  referencing one.
  Script side: "Her lips stay softly sealed around the shaft and are drawn a little forward along it as she pulls
  back, her cheeks drawn in slightly by the suction." Start sucking shots from such a keyframe (`key_image`).
- **Dominant BJ keyframe** (owner): `gallery/a106/b2_key_00001_.png` - eyes closed, her hand resting on his leg; "makes it hotter".
- **Cheek puff = cum in her mouth** (idea, owner): `gallery/a106k/suck_v06_106202_00001_.png` - a slight cheek puff
  with the shaft in her mouth; a good first frame for an oral climax that fills her mouth, then she pulls out and it
  drips.
- **H3 passes can thicken the line art** (a106, measured with `tools/rounds/linemeter.py`: +0.3-0.4 px per 124-frame clip in
  the night BJ chain whatever the prompt - but not everywhere: Emilia a103's chains stay flat, see OPEN-ITEMS; a neutral style line without drawing words barely helps). Chains compound it: keep chains to one hop, start
  later beats from fresh keyframes (a cut on a change of pace or angle), and do not `restore` - the H3-Image redraw
  starts thicker than the frame it replaces (b3: 2.36 vs 2.18), so restored chains degrade faster (b5).
- **Continue a beat by extension, not one frame** (a107, owner: solid): shot key `"extend": 22` next to `start_from`
  anchors the previous clip's last 22 frames - seamless and half the line thickening of a single-frame chain (`docs/STORY.md` "Round a107").
- **Chaining from the exact last frame** (`start_from`) is the default - it is the only seamless continuation
  (`lanzhu_hotel` s5 was clean) - but check every hop for degradation (line art thickening, colours drifting,
  anatomy softening; `lanzhu_night` b3/b4 got thicker lines). `restore` was tried for this and made it worse (above).
- Bigger climaxes: never more pulses (faster twitching, a93c/a104); three pulses, vary where they land.
- Micro-motion (jiggle, follow-through, breathing): Video tab **Dynamics** (`dynamics_video`).
- A gaze shift inside one clip works when it is slow ("looks up into his eyes ..., then slowly turns
  her gaze to the camera"); sweet vibe: "looks into the camera with a soft, sweet smile, lips closed".
- Fluids: describe one continuous result, never a repeated action (a looped "each time ..." swings
  back and forth); saliva "thin, clear, see-through, colourless like water, a small white glint".
- In H3 scripts describe the result, never the thing to avoid (a97).
- **Backdrop continuity (open, a104):** describe the room the same way in every shot and match it to the
  angle - what sits behind her from this camera (window on the left from the front, the lamp behind her from
  the side ...). Rarely noticed while the focus is on the characters, but a nice extra touch; lamps and
  windows moved between shots in `lanzhu_hotel`.
- Consistency: one character LoRA, shared blocks, one seed per shot; watch tag bleed between the two
  people (give him his own colours: black trousers, black hair).
