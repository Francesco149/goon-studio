# Round 2026-11-20 (overnight): checkpoint swaps, act-LoRA A/B, and a per-frame style pass

Follow-on to `ROUND-2026-11-20-detail-and-order.md`. This round is about *which model* to use
for a given job, what a second video LoRA actually buys, and one new technique: using a
photoreal clip as the motion source and restyling it frame by frame. Numbers are from ampere
(RTX 3080 10 GB, ComfyUI 0.45.0) unless stated otherwise.

## 1. nvfp4 checkpoints load on Ampere through the normal loader

A 7.15 GB `nvfp4` text-to-image checkpoint (a Krea 2 Turbo fine-tune) loaded with the stock
`UNETLoader` and ran at 12-20 s per 896x1344 still at 8 steps, cfg 1.0, `euler`/`simple`.
No Blackwell-only node, no conversion step. The file stores `U8` weights with `F32`/`F8_E4M3`
scales per layer, and ComfyUI's safetensors path dequantizes it on the fly.

## 2. A second video LoRA: sometimes free, sometimes +136 s, and usually not an upgrade

Model: MiniMax H3 FL2VA + Pika Flex 6-step, i2v, 768x1152, 124 frames. A second
`LoraLoaderModelOnly` was inserted after Pika Flex and the same keyframe/seed/prompt was rerun.

| second LoRA | clip time | effect |
|---|---|---|
| none | 145 s | reference |
| Blowjob act LoRA, rank 32, 0.5-0.85 | 147 s | motion collapses to licking the tip |
| general NSFW LoRA, larger rank, 0.5-0.7 | 281 s | same motion problem, +136 s |
| character/style LoRA | 145 s | drifts hair and face away from the keyframe |
| act-specific LoRA (titjob / side deepthroat) | 145 s | **does** help the matching act |

The compute cost tracks the LoRA's rank/patch count, not its file size alone (a 0.3 GB LoRA
added 136 s because it patched ~208 weights). Validation is by name including the subfolder:
files under `models/loras/h3nsfw/` are addressed as `h3nsfw/<file>`.

## 3. First+last frame i2v: the endpoint rule

`MiniMaxH3ImageToVideo` with both `first_frame` and `last_frame` works, but if the last frame is
an independently generated image the model interpolates *toward that image's identity*, not
toward the same character in a new state. Two 5 s clips were made: one where the last frame was
a separate generation (face morphs over the clip) and one where it was an edit of the first
frame's own scene (stable). Rule: **the last frame must be an edit of the first frame**, not a
new roll.

## 4. Per-frame restyle: photoreal motion -> 2D look

The 2D video model does not animate a stroke on a 2D keyframe (shaft stays rigid, the mouth
licks). Working around it with the image model:

```
1  generate the clip photoreal (the recipe that already gives a real stroke)
2  ffmpeg -fps_mode passthrough -start_number 0 frames/f%03d.png
3  img2img every frame: anime checkpoint, denoise 0.40-0.45, 24 steps, cfg 4,
   fixed seed, "2D anime screenshot, cel shading" + character tags
4  ffmpeg -framerate 24 -i frames_out/f%03d.png -i source.mp4 -map 0:v -map 1:a
```

- 9.3 s per frame at 768x1152 on the 3080 (24-step img2img), so 124 frames ~ 19 min.
- Denoise 0.40 keeps hair colour, accessories and identity; 0.55 stylises more but drops them.
- Fixed seed across frames keeps the palette stable; four consecutive restyled frames were
  visually consistent in the 24-frame test.
- The audio comes from the photoreal source untouched.

This is the first route tried here that gives a 2D clip with real blowjob motion. It is a
day-one experiment; the full-length output is being reviewed.

## 5. Model notes

- **Krea 2 Turbo NSFW v10** (7.15 GB nvfp4): photoreal, explicit-capable without a LoRA,
  natural bodies, 8 steps. Best photoreal stills of the round.
- **Pink Alchemy Anima v2.9** (4.18 GB unet, Anima base): anime, explicit-capable, correct
  anatomy and a real anime face at 30 steps / cfg 4 / er_sde. Replaces base+aesthetic for
  explicit work.
- **H3 act LoRAs** (`h3nsfw/*`): useful only for their trained act; the POV blowjob set is not
  an upgrade over a detailed prompt.
- **PinkCherry / 10Eros H3 merges**: 20-66 GB fine-tunes seen on the hub; not attempted here
  (they fit 16 GB with offload, not a 10 GB card).
