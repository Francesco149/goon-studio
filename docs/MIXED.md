# Mixed reality: a real cock in an anime picture (2026-11-21)

Goal: the "anime tribute" look - a photoreal real cock in an otherwise flat 2D anime picture, with
the anime girl taking it. The real-cock references are the owner's tribute clips in
`gallery/refs/art-study/refs/` (git-ignored); never commit them.

## The source frame

The cleanest handless real cock is in
`photoreal-medium-amount-medium-strength_1795215215.mp4` at **8 s**: the anime standee (Tohsaka
maid) behind, the real cock vertical in front, no hand in frame. Crop 440x920 at (360,1000) from
the 1080x1920 frame -> `analysis/mixed/real_cock_ref.jpg` (scratch, not committed).

Other refs are usable but worse: `..._1795215197` (tablet, cock out of focus),
`..._1795215167` (tablet, cock blurred), `..._1795215155` (card + only the tip), ref5/ref6
(real girl in frame, cock partly soft). The ref11 8 s frame is the one.

## The recipe (works)

1. Anime scene: the LL signature still with the girl taking a cock in her mouth, e.g.
   `gens/a11/j2_suction_seal_a_00001_.png`.
2. Qwen-Image-2.1 edit, **two pictures** (`workflows/qwen21_edit2.json`): Picture 1 = the anime
   still, Picture 2 = the real cock crop.
3. Prompt:

```
Keep the anime girl from Picture 1 exactly: the same face, hair, eyes, body, pose, mouth, hands,
background, lighting and 2D flat anime art style. Replace only the penis with the photoreal penis
from Picture 2: real skin texture, visible veins, a defined glans, photoreal specular highlights
and natural shadows, at the same position and angle as the penis in Picture 1, scaled so her lips
are sealed around the real glans and the shaft goes into her mouth. Only the penis is photoreal;
the girl and everything else stay 2D anime. Match the scene light and colour on the real skin.
```

832x1248, 25 steps, cfg 1. Results: `gens/a40/mix1_qwen_ref_00001_.png`.

The one-image variant also works (`wf_qwen21_edit1.json`, "render only the penis
photorealistically..."), `gens/a40/mix2_qwen_paint_00001_.png`; the two-image version keeps the
real cock's actual shape and veins a little better.

## What still needs work

- The mouth is behind the shaft in this composition, so the "sucking" is implied rather than seen.
  The next pass should start from a **side** anime still with the lips clearly sealed around the
  glans, or edit the mouth open around the real tip.
- A video version would need the real cock to hold still while the anime girl moves; H3 will
  probably relight/restyle it. Test later.
- The real-cock crop keeps the anime standee behind it; it is a reference for the object, not a
  background. The prompt is explicit that only the penis changes.
