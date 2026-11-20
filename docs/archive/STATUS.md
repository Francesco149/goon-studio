# Status, 2026-11-20 - staged, not approved, not published

Owner verdict is the source of truth: **the only thing right so far is the prompting for blowjob
motion and the still-level detail.** Everything else is staged as not solved. Nothing here has been
written to nix-lab or bunker; the two doc commits I made earlier were reverted (`nix-lab` back to
`bf38355`, `bunker` back to `db6ef53`), so neither repo carries any trace of this session.

## Right (owner-approved)

| # | claim | evidence |
|---|---|---|
| 1 | **Blowjob motion in a clip**: slow stroke with a held bottom, camera stays put if you say so | `gens/v02/v4_i2v_photo_768` - owner: motion "doesn't look terrible"; `gens/pv01/pvid_ve1` |
| 2 | **Still-level detail**: naming the parts (glans, rim, foreskin ridge, veins) and asserting the shape holds gets them drawn | `gens/v01/v1_t2v_photo`, `gens/p01/p1` |

## Not solved (staged, awaiting a real solution)

| # | problem | state / evidence |
|---|---|---|
| A | **Realistic stills still have issues.** The LoRA the owner downloaded is a real improvement - correct glans, rim, foreskin collar, scrotum behind the hand (`gens/ve01/ve1`,`ve2`,`ve3`) - but the owner has not accepted it and the mask/pose/face are still AI-ish. | promising, **not accepted** |
| B | **Realistic video anatomy.** `pvid_ve1` holds the head and rim most of the 5 s but flattens on some frames and merges the forearm; `pvid_ve3` (flash, seed 2) drifts and softens. | not solved |
| C | **Anime anatomy in a named style.** `s02/ll_h3img_style` has the Love Live look right but a slab with a cherry head; `s01/ll_anima_side_bj` (owner: "side one ... is decent") does not draw the cock at all. | not solved; round `lf01` tries to fix it by borrowing the real anatomy into the drawing |
| D | **Cum still reads as glue** in motion - opaque, rigid, motionless strands (`gens/w02/w2_cum_pov`). Material wording is written, not rendered. The author's `Verite-overcooked` file, which he says is strong for fluids, is not downloaded. | not solved |
| E | Balls on the wrong side in a POV: mostly an artifact of the words `a scrotum below`; leaving the scrotum out resolves the base into pubic hair (`gens/b01/b2_no_scrotum`). Works, but it works by omission. | workaround only |
| F | Mosaic as a post step (`gens/v01/v1_t2v_mosaic.mp4`) - a fallback that hides an unsolved anatomy, not a solution. | fallback |

## The current best chain (unapproved, just the least bad)

```
Krea 2 Turbo + Verite_realism (strength 1.0-1.3, 8 steps, cfg 1.0)   -> still
H3 FL2VA + Pika 6-step, i2v from that still, 768x1152, 124 frames    -> clip
prompt shape: act first, then her, then him, then his cock, then where her hands are,
              then the anatomy sentence, then the stroke with a duration, camera tag last
```

The LoRA author's own rule, which is what made the stills work:
*"don't just write a thick cock between or somewhere, write like a man then his cock."*

## Open questions for the owner

1. Is `gens/ve01/ve1` or `ve2` good enough as a realistic still, or still not?
2. Cum: is the next test `Verite-overcooked` (needs the second file from the same Civitai version)?
3. Anime anatomy: prefer borrowing the real shape into the drawing (`lf01`), or training a small
   anatomy LoRA on Anima (~40 min on lame), or a Pony/Illustrious anatomy LoRA then restyle?
4. Civitai access: an API key in `~/goonlab/.civitai-token` unlocks `tools/civitai.py download`
   (search, metadata and example images already work without it; downloads return 401).

## Files

- `notes/REFS.md` - what the six references do (shot grammar).
- `notes/SEX-SCENES.md`, `notes/NSFW-RESEARCH.md` - drafts, **not pushed anywhere**.
- `notes/LOG.md` - per-round log, through `ve01`/`pv01`.
- `gens/`, `jobs/`, `tools/` - renders, the exact prompts and seeds, the drivers.

## Update 2026-11-20 (late): approved pose/face recipes + the censor experiment

- `notes/WINS.md` now holds the two owner-approved prompts verbatim (`ha01` side and POV). Rule:
  keep that pose+face half fixed forever, vary only the cock half.
- Censor round `cen01` (same seeds, same prompts, `uncensored` swapped for `censored` + `bar censor`
  / `mosaic censoring`): **poses and faces survive all four**, and the POV pair comes out with a
  better-defined head than the uncensored `ha01` POV did. `pov_bar` is thin but the glans and rim
  read; `side_mosaic` keeps the pink head and hides the shaft, which is the flim13 look the owner
  likes. So bar/mosaic is not a fix for the anatomy, but it is a usable, on-reference presentation
  that hides the weakest part - and the four are the best anime stills so far.
- Still open for anime: a proper head/shaft *uncensored*, which needs a hentai-native Anima
  checkpoint (Illustrij A1/TINKER) or a trained anatomy LoRA - both need a download decision.
- Realistic: next test is the owner's two-clip idea - clip 1 takes it in, clip 2 is the pull-off
  seeded with a reference of what that cock must look like coming out. On this box that is H3
  Ref2VA (`minimax_h3_ref2va` + the `pika_h3_flex_ref2va` LoRA), Picture 1 = last frame of clip 1,
  Picture 2 = the cock crop from the keyframe.

## Update: the two-clip pull-off (round `rc01`, ampere)

The owner's idea - do the pull-off as a second clip that is told what the cock must look like coming
out - works, two ways:

- `rc01/r1_ref2va_pulloff` - **H3 Ref2VA** (`minimax_h3_ref2va` + `pika_h3_flex_ref2va` 6-step),
  ref 1 = an in-mouth frame from `pvid_ve1`, ref 2 = the Verite keyframe. The mouth comes off over
  the clip and the cock that emerges keeps a defined glans with a rim and the foreskin collar.
  Softer, more "home video" texture; the shaft goes a little flat near the end.
- `rc01/r2_i2v_return_to_key` - plain H3 i2v with **first frame = in-mouth, last frame = the Verite
  keyframe with the cock out**. Same result with better anatomy consistency: the head stays
  ridged as it leaves her lips and the clip must land on the known-correct cock. This is the one to
  keep.

Both beat `gl01/g2_no_collapse` (prompt-only attempt at stopping the collapse), where the head still
came out different from how it went in. Conclusion: **the exit state has to be an image constraint,
not a sentence.** Two workflows added: `tools/wf_h3vid_ref2va6.json` and
`tools/wf_h3vid_i2v_fl.json` (first+last).

## Update 2026-11-20 (session 2, overnight): e-girl stack, Pink Alchemy, act LoRAs

Everything here is **staged, not owner-rated**. The session-1 approvals still stand.

### New right (candidate)

| # | claim | evidence |
|---|---|---|
| 1 | **Krea 2 Turbo NSFW v10 (nvfp4) runs on the 3080** and is the new photoreal e-girl model: real skin, natural bust, no LoRA needed for explicit anatomy | `gens/k1`, `gens/e3` |
| 2 | **The e-girl character block** (fixed prose) gives a consistent face and the requested curvy proportions; `full natural breasts` is the size control | `gens/e3/p1`,`p3`,`p4`; `notes/RECIPE-E-GIRL.md` |
| 3 | **Pink Alchemy Anima v2.9** is the anime checkpoint: base style + correct anatomy + curvy body in one model | `gens/pa`, `notes/RECIPE-ANIME.md` |
| 4 | **The anime mouth seal is a prompt fix**: `penis in mouth`, `lips sealed around penis`, `cheeks hollowed`, `no tongue`, and `tongue out, open mouth` in the negative | `gens/pb/pb1`,`pb2`,`pb3` |
| 5 | **Act LoRAs help only the act they were trained for**: Titjob holds the breast-around-cock pose (`v3e`), sideview-deepthroat gives a real profile stroke (`v3g`); the POV Blowjob LoRAs reduce the stroke to licking (`v3b`, `v3c`, `v4a`, `v4b`, `v4c`) | `gens/v3`, `gens/v4` |
| 6 | **Cum stills work in anime** (strands, blobs, drips) while the photoreal still/video produce a rigid cord | `gens/pb/pb7` vs `gens/e1h`, `gens/v3f` |

### Not solved

- **Photoreal cum**: the model draws one long rope that behaves like a cord. Prompting
  "short splatters/blobs, glossy" helps the still (`e67/c3`,`c4`,`o4`) but the video transition
  still materialises the cum rather than emitting it.
- **Anime video with H3**: the style holds but the shaft stays rigid and the act degrades to
  licking (`v6a`/`v6b`/`v6c`). The tested workaround is the frame restyle
  (`RECIPE-RESTYLE.md`, run `gens/r2`).
- **Two-clip chain endpoints**: `v7a`/`v7b` prove the first+last technique but the target still
  must be an *edit of the start frame*. Independent generations morph her face on the way there.
- **Bar censor** is unusable; mosaic is luck. Post is still the answer.

### Current best chains

```
photoreal still   Krea 2 Turbo NSFW v10 nvfp4, 8 steps, cfg 1, euler/simple        ampere, 12-20 s
anime still       Pink Alchemy Anima v2.9, 30 steps, cfg 4, er_sde/simple          ampere/cutestation
video             H3 FL2VA + Pika 6-step, i2v from the still, 768x1152, 124 f
                  - POV blowjob: no act LoRA, detailed stroke prompt (v3a)
                  - side deepthroat: + h3-sideview-deepthroat 0.75 (v3g)
                  - paizuri: + Titjob 0.85 (v3e)
anime video       photoreal H3 clip -> per-frame Pink img2img (denoise 0.45) -> reassemble + audio
```

### Open questions for the owner

1. Is `gens/e3/p1` / `p3` the right e-girl look and bust size, or should the character block move?
2. `gens/v3a` is the new best photoreal stroke; is it good enough to replace `v4_i2v_photo_768`?
3. Does the restyled anime clip (`gens/r2`) hold up, or is the per-frame flicker too much?
4. Is `pb3` the anime POV keyframe to build a longer scene from?

### Update (end of session 2): the restyle clip

`gens/r2_anime.mp4` is the full 124-frame restyle of `gens/v3/v3a_ctrl` (768x1152, 24 fps,
source audio). It holds the dark semi-real anime look, the pink streaks, the choker and the
mouth seal for the whole 5.2 s, and it carries the photoreal stroke. Artifacts: two frames
invent a thin vapour wisp at her mouth, and the eyes/eyeliner shift a little; no frame breaks
the pose. Cost: 124 frames in 22 min on the 3080 (~10.9 s/frame), plus the source clip.

That makes the current anime-video recipe: **H3 photoreal clip -> Pink Alchemy per-frame
img2img at denoise 0.45, fixed seed -> reassemble with the source audio** (`RECIPE-RESTYLE.md`).
