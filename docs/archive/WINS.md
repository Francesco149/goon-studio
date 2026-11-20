# The remembered recipes (owner-approved poses and faces)

Owner, 2026-11-20: the best poses and facial expressions came from `gens/ha01/
ll_anima_tags_pov_00001.png` and `gens/ha01/ll_anima_tags_side_00001.png`. Those two prompt texts are
the base for anything anime from now on - vary the cock treatment around them, **do not rebuild them**.

## A. Side view (owner-approved pose + face)

`ha01/ll_anima_tags_side`, Anima Aesthetic v1.1, 1248x832, 30 steps, cfg 4.0, er_sde/simple, seed 21:

```
masterpiece, best quality, year 2016, anime screenshot, 1girl, 1boy, hetero, blowjob, fellatio,
oral, penis, glans, foreskin, veins, erection, uncensored, penis focus, side view, profile,
kneeling, leaning forward, short silver hair, single braid, purple eyes, @murota yuuhei,
(curvy:1.6), (wide hips:1.4), thick thighs, large breasts, mature female, half-closed eyes, blush,
saliva, bedroom, soft light, love live! sunshine!!
```

negative:

```
extra hands, extra fingers, third hand, bad anatomy, fused limbs, censored, mosaic censoring,
bar censor, worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts,
watermark, text, 3d, realistic
```

What makes it work: `side view, profile` + `kneeling, leaning forward` puts both bodies in a readable
arrangement (Anima cannot do POV), and `half-closed eyes, blush` plus the Love Live tags carry the
expression. The face is the reason to keep this one.

## B. POV (owner-approved pose + face)

`ha01/ll_anima_tags_pov`, 832x1248, same settings, seed 22:

```
masterpiece, best quality, year 2016, anime screenshot, 1girl, 1boy, hetero, blowjob, fellatio,
oral, penis, glans, foreskin, veins, erection, uncensored, penis focus, pov, from above,
looking up at viewer, short silver hair, single braid, purple eyes, @murota yuuhei, (curvy:1.6),
thick thighs, large breasts, mature female, half-closed eyes, blush, saliva, bedroom, soft light,
love live! sunshine!!
```

negative: as above plus `extra limbs, male body`.

What makes it work: `pov, from above, looking up at viewer` with `male body` in the negative keeps the
man out of frame; `looking up at viewer` is what puts the eyes on camera.

## The rule that came out of it

Keep A and B fixed as the "pose + face" half of the prompt. Only ever vary the **cock half**:
`penis, glans, foreskin, veins, erection, uncensored | censored, bar censor | censored, mosaic
censoring`, the `penis focus` tag, and their weights. Every anime round from now on should be a
variation of that half against these two fixed prompts, so pose and face stop being a lottery.

## Model choice for the cock half (round `cock01`/`cock02`, 2026-11-20)

Same prompts and seeds as A and B, only the checkpoint differs:

- `anima-base-v1.0` -> **the cock reads properly**: defined glans with a corona rim, the foreskin
  bunched in a collar behind it, a textured shaft with a vein. `cock01/b_base_pov`,
  `cock01/d_closeup_pov`, `cock02/base_pov_seed28`. This is the model to use for the anatomy half.
- `anima-aesthetic-v1.1` -> softer, prettier skin and slightly nicer faces, but the cock stays a
  smooth tube with a cap. Use it when the look matters more than the anatomy.

So the anime recipe is now three fixed slots:

```
1 pose + face   the A or B prompt above, verbatim
2 model         anima-base-v1.0 (safetensors in {{unet}}), 32 steps, cfg 4, er_sde/simple
3 cock half     (penis:1.2), (glans:1.5), (foreskin:1.4), (veins:1.2), erection, penis focus,
                detailed penis, uncensored | censored + bar censor | censored + mosaic censoring
```

Censored variants on Base (`cock02`): `base_pov_bar` (thin bar over the shaft, head and folds still
drawn) and `base_pov_mosaic` (whole shaft mosaicked, tongue on the head) both keep the pose and face
and read like the reference material. `side_mosaic` loses the cock at that framing - keep the
side view uncensored.

Avoid: `close-up` on the side view (it splits the frame into an inset panel, `cock01/c_closeup_side`).
