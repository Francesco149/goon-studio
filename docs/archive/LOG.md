# Round log

Every round: what was asked, what came back, what it changed. Files under `gens/<round>/`, the
job files that produced them under `jobs/`.

## g01 - first probe, Anima on cutestation (8 jobs, 18 steps, 832x1248)

Asked: does Anima know what a blowjob looks like, does tag order matter, does `censored` work, is
a cumshot drawable.
- `a_action_early` / `b_action_late`: both put a good wet cock in her mouth with the right eyes-up
  composition. Tag order (action first vs last) changed little; the artist tag (`@murota yuuhei`)
  changed the face, not the act.
- The recurring failure: `1boy` + `pov, from above` gives a **giant unexplained ass** filling the
  top of the frame in every variant. Anima cannot place the male body.
- `c_anatomy` (+`glans`, `veins`): the best of the round; a defined head and a vein line appear.
- `d_uncensored_neg` (`censored` in the negative): no visible difference from `c`.
- `e_censored_tags` (prompt: `censored, mosaic censoring`): **no mosaic at all**. The tag is not
  honoured; censorship has to be post.
- Runtime: 36-40 s a picture.

## g01b - Anima, the three remaining ideas (cutestation)

- `f_cumshot`: best still of the day for fluids - ropes off her lip, a strand down the shaft, blobs
  sagging on the breasts. Confirms the still-image model knows cum; the video one does not.
- `g_side_view` (ref3 composition): profile works, but the male body becomes a shapeless thigh mass
  and the shaft reads as two shafts. Not the way to get the side view.
- `i_nobody` (male body in the negative): removes the ass, but the cock enters her mouth at a
  strange sideways angle and her chin is drowned in saliva. Better, still not there.

## p01 - which model actually draws it, 3080 (4 images)

One prompt, four models, photoreal except p2:
- `p1_h3img_photo`: **fully correct anatomy**, clean POV, her hands at the base, saliva strand.
- `p2_h3img_anime`: same, in clean 2D anime. Best anime keyframe of the day.
- `p3_krea2_photo`: **refused** - drew a softcore pose with no genitals at all.
- `p4_qwen21_photo`: the most detailed anatomy of the four; the body arrangement below is muddled.
- Runtime on a 3080: 17.6 s, 26.8 s, 45 s, 63 s (including model loads).

## v01 - the critical test: can H3 video draw it? (3080, 512x768, 5 s)

- `v1_t2v_photo`, text only, anatomy spelled out: **yes**. A correct, detailed cock for the whole
  clip, her lips sealing and sliding, a real stroke, a saliva string. This is the finding the
  session needed: the "stick" is a prompting failure, not a model limit.
- The face carries a harsh blush (the word `flushed cheeks` rendered as red patches); the
  background has a dark band; the audio is quiet wet suction with one short vocalisation and no
  speech (spectrogram in `analysis/v01_spec.png`).

## v01b - i2v from the two H3-Image keyframes (3080, 512x768)

- `v2_i2v_anime`: the anatomy **softens and drifts** - the rim goes, the shaft becomes a rounded
  cylinder. 512 px is too coarse for a 896x1344 keyframe.
- `v3_i2v_photo`: the anatomy holds (rim, veins, foreskin), the mouth slides and the shaft comes
  out wet; the stroke is small and the cock stays stiffly vertical.

## v02 - 768x1152, i2v and t2v from the photo prompt (3080)

- `v4_i2v_photo_768` (144 s): the rim and the veins survive, her mouth seals and slides, she comes
  off at the end with a strand. The best-motion clip of the day (owner: the motion "doesn't look
  terrible") - but the head still reads as a smooth cap in places, and her hands merge.
- `v5_t2v_photo_768` (131 s): the sharpest anatomy (rim, frenulum, scrotum, veins) and a real
  stroke with a held bottom; the face drifts across the 5 s, and this is the clip where the balls
  first came out in front of the shaft (see b01).

## b01 - the scrotum on the wrong side (3080, same seed, 512x768)

- `b1_baseline` (`a scrotum below her hand`): sac in front of the shaft.
- `b2_no_scrotum` (word removed): no sac, the base dissolves into pubic hair - the right look for a POV.
- `b3_depth_order` (sac behind her fingers): better, still wrong - owner: it should be *behind the
  cock*, not below it in the picture. Do not use.

## a01 - an anatomy prop (cutestation, H3-Image, 1152x1152)

`prop_photo_side`, 28 s: a clean, isolated, photoreal erect penis on white with a correct glans and
corona rim. Good enough to anchor from.

## a02 - inserting the prop with H3-Image edit (3080)

`ins1_photo` / `ins2_anime`: the anatomy does transfer, but the edit repaints the whole frame with a
crusty, over-sharpened skin and wiry hair. H3-Image is for making pictures, not editing them.

## a03 - inserting the prop with Qwen-Image-2.1 edit (3080)

`q1_qwen_insert` (25 steps): the right tool. The woman, skin, hair, light and pose survive; the penis
takes the prop's glans and collar. Slightly prosthetic (the collar reads as a ring), but correct.

## w02 - side view and the cum continuation (3080)

- `w1_side_photo` (1024x768): the ref3 composition works - body, hips, breasts resting on his thigh,
  his hand on her back. The mouth/shaft junction stays a blob for the whole clip because it was a
  blob in the keyframe, and the shaft reads as a flat meat slab.
- `w2_cum_pov`: the cum strands stay where they landed and drip; no emission, no foam. Owner: better,
  but still glue-like - the strands are opaque and rigid. See the material wording in the recipe.

## q01 - H3-Image keyframes for the side view and the cumshot (cutestation)

- `s1_side_anime` (1152x896, 32 s) and `s2_side_photo` (59 s): the ref3 composition, clean. The
  photoreal one is the better keyframe; in both, the mouth/shaft junction is the weak spot (fingers
  and glans merge).
- `c1_cum_face` (896x1344): cum as ropes on the cheek, a strand to the lip, a blob hanging - the
  best cum still of the day.
- `c2_cum_tits`: strands down the cleavage and drips; the body layout below is muddled.

## ve01 - the owner's Krea 2 LoRA (3080, 8 steps, 896x1344)

`Verite_realism` at strength 1.0 / 1.0 / 1.3, prompted act-first with the man described before his
cock:
- all three draw a **correct** cock: defined glans with a rim, foreskin folded back behind it,
  natural shaft, scrotum at the base behind her hand. No prop, no mosaic.
- ve3 (strength 1.3, flash) is the cleanest anatomy of the whole session.

## pv01 - i2v from those stills (3080, 768x1152)

- `pvid_ve1` (146 s): the anatomy survives the clip better than any prompt-only keyframe did - head,
  rim and foreskin hold for most of the 5 s, her mouth slides down and up with a held bottom.
  Weak spots: some frames flatten the shaft, the forearm merges, a bright band drifts in the
  background.
- `pvid_ve3` (142 s, flash, seed 2): worse - the camera drifts, the cock softens to an oval.
  Seed and lighting matter more than the prompt here.

## Session 2 - 2026-11-20, overnight: e-girl, Pink Alchemy, act LoRAs

### e1 - photoreal e-girl with Krea 2 + Verite (3080, 8 steps, 896x1344)

First e-girl set. The aesthetic and the body read (twin tails with pink streaks, choker,
oversized tee, LED bedroom), but the skin is the old plasticky Verite look and the bust runs
to caricature in half the shots. Seal is hit or miss: `e1e_bj_pov` sealed, `e1f_bj_side` licked.
`e1h_cum_face` produced the first photoreal cord-cum failure (one rigid rope across the face).
Kept only as the video keyframe: `e1e` is still the best photoreal blowjob still.

### k1 - the owner's Krea 2 Turbo NSFW v10 (nvfp4) runs on the 3080

7.15 GB nvfp4 file, plain `UNETLoader`, 8 steps cfg 1.0, 12-16 s at 896x1344. No special
node and no Blackwell requirement in practice (ComfyUI 0.45). `k1_portrait` is a step change
in realism over Verite: soft body, pores, real window light, natural bust. `k2_bj_pov` draws
the anatomy correctly unprompted but keeps the mouth off the shaft (drool strand instead).

### e3 - Krea 2 NSFW e-girl set (10 stills)

- `p1_bust_natural`, `p3_mirror`, `p4_standing` are the reference proportions: curvy, large
  natural breasts, not caricature. `p2_bust_large` is the upper bound.
- `p5_bj_seal`, `p7_bj_side`, `p8_paizuri` are usable explicit stills; the seal is still
  50/50 and the default failure is "open mouth, tongue on the glans".
- `p9_cum_face` repeats the cord: one long rigid rope, no blobs, no gravity.
- Video keyframe candidate: `p5` (POV, lips at the head, face on camera).

### e5 - tag prompt vs prose, same checkpoint

- `g7_egirl` (pure danbooru-style tags) is the best e-girl portrait of the night.
- For scenes the tags fail: `g3` came out as a two-panel collage, `g4` as a straddle that is
  not a blowjob, `g2` as a long drool string. The `krea2blow`-style triggers belong to the
  author's per-act LoRAs, not to this merged checkpoint. Prose held the scene (`g8`).
- Rule: tags for the character sheet, prose for the act.

### a2 - Anima base, anatomy weights (control for the merge)

Adding `(glans:1.5)(corona:1.35)(foreskin:1.45)` makes the cock bigger and more detailed but
pulls the mouth off it: `a2b` is a thick veined cock held next to her face. `a2a` keeps the
mouth on it but the shaft is a smooth tube. This is the tradeoff Pink Alchemy removes.

### pa - Pink Alchemy Anima v2.9 (cutestation, 1248x832, 30 steps, cfg 4, er_sde/simple)

Pink Alchemy is a different model in the same clothing. `pa1`/`pa2`/`pa3` have the anime
screenshot style, a real anime face, correct curvy proportions and a thick, veined cock with
a defined head - better than base on every axis. The model card's own settings
(`euler_ancestral`/`beta`, 26 steps, cfg 4.7) are close but not better than 30/4/er_sde
(`pa5`/`pa6`). 63 s per still on the 5060.

### pb - the anime mouth seal, censor, cum

- `pb1`/`pb2`: the seal prompt from `RECIPE-E-GIRL.md` works on Pink: lips in a ring behind
  the head, cheeks hollowed. The negative `tongue out, open mouth` is load-bearing.
- `pb3_pov_seal`: best anime POV of the night (face, breasts, head in her mouth).
- `pb6_side_big`: the "bigger" variant - comically thick, but the seal holds.
- `pb4_side_bar`: bar censor is a striped sticker, unusable. `pb5_pov_mosaic`: one large
  mosaic block that covers the shaft and leaves the head visible - the flim13 look, but its
  placement is luck. Post is still the reliable censor.
- `pb7_cum_face`: anime cum is correct (strands, drips, gloss). Confirms: cum is a still-image
  strength and a video weakness.

### v3 - H3 act-LoRA survey (3080, 768x1152, 124 f, 5.2 s)

Same keyframe (`e1e`) and seed 61 for the POV clips:

| clip | LoRA / strength | verdict |
|---|---|---|
| `v3a_ctrl` | none | **best stroke**: full down-up, held bottom, mouth stays sealed; anatomy holds |
| `v3b_bj3` | MM-H3 Blowjob v3 / 0.85 | mouth stays on the glans, small licking motion, no stroke |
| `v3c_aio` | HMNSFW AIO V2 / 0.7 | same failure as bj3, and +136 s compute |
| `v3d_astro` | Astro NSFW / 0.8 | drifts the character (straight hair), licking, no stroke |
| `v3e_paizuri` | Titjob H3 / 0.85 | works: breasts hold around the shaft, subtle stroke, face stable |
| `v3f_cum` | HMCumshot V2 / 0.7 | makes the cord worse: a thick white cord that swings and wraps her mouth |
| `v3g_side` | sideview-deepthroat / 0.75 | **works**: real profile stroke, cheek bulge, takes it deeper |

So: act LoRAs are not a blanket upgrade. They help the act that matches their training
(titjob, side deepthroat) and hurt the POV blowjob, where the plain prompt already gave the
stroke. The cum LoRA amplifies the cord problem.

### v4 - prompt-constant LoRA weight

Same prompt as `v3a`, LoRA weight dropped to 0.5: `v4a_bj05` still licks the tip, so the
weight was not the cause. The LoRA's learned motion is the cause.

### e67 - photoreal cum, take two

"Short thick splatters / blobs / drips, glossy" removed the cord: `c3_splatter` has strings down
the face and chest, `c4_drips` drips off the chin, `c5_tongue` pools on the tongue, and
`o4_cum_out` is the money frame - cum on the face with the cock still in frame and a strand from
the glans to her lip. `c6_side` came out as a collage (the side-view tag again), unusable.
So the photoreal cum still is solvable by wording, not by a LoRA.

### v6 - anime i2v from the Pink stills

- `v6a_anime_pov` (no LoRA): style and character hold, but the shaft is rigid and the act is
  licking; the cock even drifts into a floating tip in the last frames.
- `v6b_anime_lora` (Blowjob v3 at 0.6): no change. A photoreal act LoRA does not transfer to 2D.
- `v6c_anime_side` (side keyframe): the body leans in and licks; no stroke along the shaft.
Conclusion: H3 cannot animate fellatio from a 2D keyframe at this scale. Use the restyle route.

### v7 - first+last chains and the endpoint rule

- `v7a_chain_cum` (last frame of `v3a` -> `e67/o4`): the mechanics work, the cum appears and
  drips, but the target still is a different generation, so her face and framing morph on the
  way there.
- `v7b_still_chain` (o1 -> o4): same, more visible.
Rule: **the last frame must be an edit of the first frame**, not an independent roll. `rc01`
worked because its last frame was the clip's own source image.

### h1 - anime hires detail pass

`pb3` upscaled 1.38x (1152x1728), 20 steps, cfg 4, denoise 0.30 -> `h1_d30`: sharper face and
shaft, seal intact, 90 s on the 5060. denoise 0.45 (`h2_d45`) is punchier but loosens the seal
and changes the braid. Keep 0.30. This is the anime detailer pass.

### r1/r2 - photoreal motion -> anime restyle

`r1` (24 consecutive frames of `v3a`, Pink img2img denoise 0.45, fixed seed): style, hair,
streaks and choker stay consistent frame to frame; 9-11 s per frame at 768x1152 on the 3080.
`r2` is the full 124-frame run, reassembled with the source audio (`gens/r2_anime.mp4`).
This is the first route that gives a 2D clip with the photoreal stroke.
