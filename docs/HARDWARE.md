# Hardware baseline: 8 GB VRAM + 16 GB RAM

The repo defaults to a **single consumer GPU with 8 GB VRAM and 16 GB system RAM**. That is the
machine the setup instructions target. Bigger cards are a bonus, not an assumption.

## What fits, what streams

| job | model on disk | fits 8 GB? | how it runs |
|---|---|---|---|
| photoreal stills | Krea 2 Turbo NSFW v10, 7.15 GB nvfp4 + 4B text encoder | not fully | ComfyUI streams the UNet from system RAM; the 4B encoder is small. Expect a slow first picture, then ~20-40 s |
| anime stills | Pink Alchemy Anima v2.9, 4.18 GB + 0.6B encoder + VAE | yes (~5.5 GB) | the comfortable case: 30 steps, 832x1248 |
| anime second pass | same, img2img at 1.38x | yes | 20 steps, denoise 0.30 |
| H3-Image keyframes | H3-Image int8, 11.7 GB + 32B encoder 14.6 GB | no | both stream; the first load is minutes, then ~30-60 s per still. On 16 GB RAM this is the tight one |
| H3 video | H3 FL2VA int8, 11.7 GB + 32B encoder + VAEs | no | same streaming; 512x768 for tests, 768x1152 for finals, one clip at a time |
| Wan 2.2 14B | 2x Q5 GGUF, ~11 GB each | no | does not fit; documented as a 24 GB job (`CUM-VIDEO.md`) |

## Levers that make it fit

1. **Quantized weights**: int8 / w4a8 / nvfp4 variants are what make the 8 GB card usable at all.
2. **Text encoder on CPU**: the H3 32B encoder is the biggest single allocation. ComfyUI's
   `CLIPLoader` accepts `device: cpu`; it costs speed, not correctness.
3. **ComfyUI's dynamic VRAM** streams weights from system RAM. Keep 16 GB free of other apps;
   close the browser and the SFW studio while a big model runs.
4. **`--lowvram` / `--reserve-vram`** in the launcher (`my/settings.json` `extra_flags`): lower
   the reserve (e.g. `--reserve-vram 0.5`) and add `--lowvram` when a model refuses to start.
5. **Smaller frames**: 512x768 for motion tests, 768x1152 for finals, fewer than 124 frames for a
   draft. Video cost scales with pixels x frames.
6. **One at a time**: the app queues jobs; do not run a still batch while a video is loaded.

## What is deferred

The **8 GB optimization pass** is a later session: measure peak VRAM per workflow, find the
largest 768p H3 settings that survive, test CPU text encoders, tiled VAE for the hires pass, and
write the exact flags per box. This note only records the baseline so nothing is designed for a
card the user does not have.
