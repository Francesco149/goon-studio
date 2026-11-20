# Anime video: photoreal motion -> per-frame restyle (2026-11-20)

H3 i2v from a 2D keyframe holds the style but not the act: the shaft stays rigid and the mouth
degenerates into licking (`v6a`, `v6b` with an act LoRA at 0.6, `v6c` side). The 2D keyframe is
out of distribution for a video model trained on live action.

The workaround that works: get the motion in photoreal (where H3 is strong), then repaint every
frame with the anime checkpoint.

## Pipeline

```
1  photoreal clip        H3 FL2VA + Pika 6-step, i2v, 768x1152, 124 f        (~145 s on ampere)
                         use the no-LoRA POV blowjob recipe (v3a)
2  frames                ffmpeg -i clip.mp4 -fps_mode passthrough -start_number 0 f%03d.png
3  restyle each frame    Pink Alchemy Anima v2.9, img2img, denoise 0.40-0.45,
                         24 steps, cfg 4.0, er_sde/simple, seed fixed for the whole sequence
                         prompt: "2D anime screenshot, cel shading" + the character tags
4  reassemble            ffmpeg -framerate 24 -i out/f%03d.png -i clip.mp4 \
                               -map 0:v -map 1:a -c:v libx264 -crf 18 -c:a copy anime.mp4
```

## Numbers

- 9-11 s per frame at 768x1152, 24 steps (RTX 3080): 124 frames in 22 min (measured: 1353 s including uploads).
- 40-45 s per frame on the 5060 (cutestation): usable only for a proof.
- `denoise 0.40` keeps hair colour, the pink streaks, the choker and the face shape.
  `0.55` stylises harder, gives a darker painted look, but drops the streaks and drifts identity.
- A fixed seed across the sequence keeps the palette and rendering stable. Four consecutive
  restyled frames (`analysis/R1_consecutive.jpg`) are visually consistent; the 24-frame test
  clip (`gens/r1`) is the flicker check.

## Why not just t2v in anime style

Tried: `v6a` (anime prompt, no LoRA) - style holds, motion does not. The model will not slide a
mouth along a shaft it cannot reason about in 2D. The restyle route inherits the photoreal
model's motion priors and only asks the image model for a look.

## Limits

- The restyled frame inherits the photoreal anatomy, so the cock reads semi-real painted rather
  than flat cel. For a flatter look raise the denoise, at the cost of identity drift.
- Per-frame independent sampling can still flicker on fast motion; check a 1 s strip before
  committing to a full sequence.
- Audio is the photoreal clip's, untouched.

## Files

- test: `gens/r1` (24 frames of v3a, denoise 0.45), `analysis/R1_consecutive.jpg`
- full: `gens/r2` (124 frames), `gens/r2_anime.mp4`
- jobs: `jobs/r1.jsonl`, `jobs/r2.jsonl`; workflow `tools/wf_anima_i2i.json`
- frame source: `gens/restyle_full/` (extracted from `gens/v3/v3a_ctrl_00001_.mp4`)
