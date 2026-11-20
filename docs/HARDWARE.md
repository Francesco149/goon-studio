# Hardware baseline: 8 GB VRAM + 16 GB RAM

The repo defaults to a **single consumer GPU with 8 GB VRAM and 16 GB system RAM**. That is the
machine the setup instructions target. Bigger cards are a bonus, not an assumption. The measured
8 GB pass (cutestation RTX 5060, 2026-11-20) is in [`PERFORMANCE-8GB.md`](PERFORMANCE-8GB.md);
this page is the short version.

## What fits, what streams

| job | model on disk | fits 8 GB? | how it runs |
|---|---|---|---|
| photoreal stills | Krea 2 Turbo NSFW v10, 7.15 GB nvfp4 + 4B text encoder | not fully | DynamicVRAM streams the UNet from system RAM. 4-step preview 10 s, 6-step standard 16 s, 8-step final 20 s (896x1344) |
| anime stills | Pink Alchemy Anima v2.9, 4.18 GB + 0.6B encoder + VAE | yes (~5.5 GB) | the comfortable case: 20-30 steps, 832x1248 |
| anime second pass | same, img2img at 1.38x | yes | 1152x1728, 20 steps, denoise 0.30, ~60 s |
| H3-Image keyframes | H3-Image w4a8 11.7 GB + P-H3 4B encoder 5 GB | no | both stream; 21 s cold / ~10 s warm per still at 896x1344 |
| H3-Image with the 32B encoder | 11.7 GB + 14.6 GB | no | 32 s cold, free RAM down to ~0.5 GB; use the 4B encoder for drafts |
| H3 video | H3 FL2VA w4a8 11.7 GB + 32B encoder + VAEs | no | same streaming; 512x768 85 f ~111 s warm, 768x1152 124 f ~372 s |
| Wan 2.2 14B | 2x Q5 GGUF, ~11 GB each | no | does not fit; documented as a 24 GB job (`CUM-VIDEO.md`) |

## Levers that make it fit

1. **Quantized weights**: nvfp4 / w4a8 / int8 variants are what make the 8 GB card usable at all.
2. **The right text encoder**: H3-Image runs with the P-H3 4B int8 encoder instead of the 32B
   nvfp4 one. It is 5 GB instead of 14.6 GB and roughly 35% faster cold, at a small quality cost.
3. **ComfyUI's dynamic VRAM** streams weights from system RAM. Keep 16 GB free of other apps;
   close the browser and the SFW studio while a big model runs. Free RAM, not VRAM, is the limit
   for H3.
4. **Launch flags** (`my/settings.json` `extra_flags`): `--use-ck-attention --fast fp16_accumulation`
   is the measured best pair. Do not use `--lowvram` (a no-op with dynamic VRAM), `--highvram`
   (worse and nearly fills RAM), or `--fast` with no arguments (slower than fp16 accumulation
   alone). `--fast-disk` is already on by default on the NVMe.
5. **Smaller frames / fewer frames**: 512x768 for motion tests, 768x1152 for finals, 85 frames for
   a draft, 124 for the final. Video cost scales with pixels x frames.
6. **One at a time**: the app queues jobs; do not run a still batch while a video is loaded.
7. **Preview, then refine**: 4 steps is a visibly softer but useful preview, 6 is almost identical
   to 8, and 8 is the final. Keep the seed and prompt, change only the step count.

## What is deferred

Nothing about 8 GB is deferred any more: the measured pass, per-workflow settings, lossy
tradeoffs and the GTX 1070 discussion are in [`PERFORMANCE-8GB.md`](PERFORMANCE-8GB.md).
