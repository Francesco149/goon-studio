# Session summary - 2026-11-20 (overnight run 2)

What changed tonight, what the owner needs to rate, and what to try next. Everything lives
under `~/goonlab` (refs, gens, jobs, tools, notes). Copies for the author's other machines are in `docs/archive.local/` (author sessions only).

## The three big results

1. **Photoreal e-girl is solved.** Krea 2 Turbo NSFW v10 (the owner's 7.15 GB nvfp4 download)
   runs on the 3080 through the plain `UNETLoader` and produces a consistent, natural, curvy
   Asian e-girl at 12-20 s per still. Character block and size wording: `RECIPE-E-GIRL.md`.
   Best: `analysis/BEST_photoreal.jpg`.
2. **Anime has a new checkpoint and the mouth problem is a prompt fix.** Pink Alchemy Anima
   v2.9 gives the anime look + correct anatomy + curvy body; `penis in mouth` + `lips sealed
   around penis` + `cheeks hollowed` + `no tongue` + negative `tongue out, open mouth` produces
   a real seal. Best: `analysis/BEST_anime.jpg`; hires pass: `analysis/HIRES_compare.jpg`.
3. **Anime video via restyle works (day-one).** H3 cannot animate fellatio from a 2D keyframe,
   so the motion is generated photoreal (`v3a`) and each frame is repainted with Pink at
   denoise 0.45. 124 frames in ~20 min; `gens/r2_anime.mp4`. Still: `analysis/RESTYLE_compare.jpg`.

## The act-LoRA verdict (H3, same keyframe/seed)

- POV blowjob: **no LoRA is best**. MM-H3 Blowjob v3, HMNSFW AIO V2 (0.5 and 0.85) all reduce
  the stroke to licking the tip; AIO also costs +136 s per clip.
- Titjob: `Titjob-Titfuck-H3` (0.85) holds the breasts around the shaft (`v3e`).
- Side deepthroat: `h3-sideview-deepthroat` (0.75) gives a real profile stroke (`v3g`).
- Cumshot: `HMCumshot_V2` makes cum worse (a swinging white cord).
- Motion booster: no effect on the stroke.

## Cum

- Photoreal still: "short splatters / blobs / drips, glossy", never "rope". `e67/o4_cum_out`
  is the best photoreal cum frame (`analysis/BEST_photoreal.jpg` last but one).
- Photoreal video: still materialises the cum between frames; the chain test shows it but the
  endpoint identity drifts.
- Anime still: correct (`pb7`), no work needed.

## Chains (first+last frame)

Works, with one hard rule: the last frame must be an **edit of the first frame** (same face and
framing), not an independent generation. `v7a`/`v7b` show what happens otherwise.

## Files the owner should open first

- `analysis/BEST_photoreal.jpg` - 10 e-girl stills, labelled.
- `analysis/BEST_anime.jpg` - 10 Pink stills, labelled.
- `gens/v3/v3a_ctrl_00001_.mp4` - best photoreal blowjob motion (no LoRA).
- `gens/v3b/v3g_side_00001_.mp4` - best side deepthroat (LoRA).
- `gens/r2_anime.mp4` - the restyled 2D version of v3a.
- `notes/RECIPE-E-GIRL.md`, `notes/RECIPE-ANIME.md`, `notes/RECIPE-RESTYLE.md`.

## Next, if the owner likes these directions

1. Longer scenes: stitch `v3a` -> an edit of its last frame -> a cum edit, all first+last i2v.
2. Anime: replace the frame restyle with a native 2D video model if one appears; until then the
   restyle is the route. A 16 GB card can run Pink at 1536 for cleaner restyle frames.
3. Photoreal: try the `krea2 sex` per-act LoRA set on Krea 2 for the acts that still drift
   (needs a Civitai token or an owner-side download).
4. Train an Anima anatomy LoRA only if the owner wants a specific drawing style; Pink + the
   seal prompt covers the general case.

## Session 3 (owner verdict round)

Owner-approved after review: the `gens/p3` facial pose (`p1_cock_out_cheek`, `p2_cock_out_face`)
and the cum-landed stills `gens/p4`; `v13a`/`v13b` as the cum-shot clips; `v10b_pov_bob` as the
best anime clip so far (`v10a` rejected); `v3d_astro` as the best photoreal BJ clip.

New recipes written this round:

- `notes/RECIPE-FACIAL.md` - the approved cock-out pose, the cum-landed still, the
  `epic_cumshots` 0.8 video recipe, the placement rule (lips/chin only; cheeks read as tears),
  and the list of cum attempts that failed.
- `notes/RECIPE-ANIME.md` - the anime video section is now `v10b` (whole-body motion prompt from
  the `pb3` POV keyframe). The restyle route is marked closed by owner verdict.
- `notes/RECIPE-E-GIRL.md` - cum section points at the facial recipe.

Hardware note: Wan 2.2/2.1 cannot load on the 16 GB 7800 XT (OOM even with `--lowvram`,
16.8/17.2 GB); it is the obvious route for a real projected spurt and for more dynamic anime,
but it needs a 24 GB card or a much smaller quant.
