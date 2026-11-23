# 8 GB performance pass: cutestation (2026-11-20)

Measured on the target machine: **RTX 5060 8 GB, 16 GB system RAM, Windows, ComfyUI 0.45.0,
PyTorch 2.14.1+cu130**, models on the F: NVMe. The engine was a private ComfyUI on port 8189
(`tools/experiments/bench_engine.ps1`) so the user's engine was not restarted. Times are
server-side execution seconds (`/history` timestamps), peak VRAM is the `nvidia-smi` maximum
during the job.

Two caveats about the numbers:

- **Cold vs warm.** "Cold" is the first job after the engine starts (weights read from disk and
  staged); "warm" is a following job with the weight cache still resident. On this box a cold H3
  load can add 30-50 s, and Windows file-cache warming can make a later "cold" run look faster.
  The tables say which is which; do not compare a cold number with a warm one.
- **The box was busy.** Browsers, Steam, Telegram and the harness itself were open. Free RAM
  routinely fell to 0.0-1.2 GB during H3 jobs. Closing them helps; the numbers below are what a
  normal desktop session gets, not a clean benchmark rig.

One content note that is easy to miss: the H3 video test keyframe had a pointed/deformed glans,
and every benchmark clip inherited it. The prompt did not fix it. That is a keyframe problem, not
a performance result; see `docs/CUM-VIDEO.md` for the lesson.

## The short answer

Launch ComfyUI with:

```
--use-ck-attention --fast fp16_accumulation
```

Everything else in `--fast` was slower or neutral; `--highvram` was worse and nearly filled RAM;
`--lowvram` is a no-op because DynamicVRAM is on by default. DynamicVRAM, `--fast-disk` and the
RAM-pressure cache are already the defaults in 0.45.0.

Then use **4 steps as a preview, 6 as the standard, 8 as the final** (same seed and prompt) for
Krea and H3-Image; **4/6** for H3 video (8 was 50% slower with no proven gain). This is the
owner's verdict: 4-step is visibly softer but useful, 6-step is almost identical to 8.

Quality checks: the same-seed Anima baseline and `ck + fp16_accumulation` images were visually
equivalent (the braid drifted, which is normal diffusion divergence, no new artifact). The Krea
4/6/8 and H3-Image 4/6/8 comparisons show the expected softness at 4, not a broken model. The 4B
H3 text encoder is close but not identical to the 32B; use 32B when the face/material matters.

## Measured results

### Anima / Pink Alchemy (832x1248, er_sde / simple, cfg 4)

| setting | exec | peak VRAM | note |
|---|---:|---:|---|
| 30 steps, no flags | 64.5 s cold | 7273 MB | the old default |
| 30 steps, `--use-ck-attention` | 56.8 s cold | 7017 MB | ~12% faster |
| 30 steps, ck + `--fast fp16_accumulation` | 40.5 s cold / **36.3 s warm** | 6966 MB | **use this** |
| 20 steps, ck + fp16 acc | **26.3 s warm** | 6724 MB | almost identical, 28% faster |
| 12 steps, ck + fp16 acc | 23.1 s cold | 6934 MB | preview only |
| `anima-turbo-v1.1`, 8 steps, cfg 1, euler | 10.1 s cold | 6933 MB | weak style, composition drafts |
| `anima-turbo-v1.1`, 6 steps | 4.4 s warm | 7215 MB | very rough preview |
| hires 1152x1728, 20 steps, denoise 0.30 | 59.9 s | 7567 MB | second pass; close to the VRAM ceiling |

### Krea 2 Turbo NSFW v10 (896x1344, 8 steps, cfg 1, euler / simple)

| setting | exec | peak VRAM | note |
|---|---:|---:|---|
| 8 steps, no attention override | 28.7 s cold | 7102 MB | baseline |
| 8 steps, kitchen attention | 19.6 s warm | 7506 MB | **final quality** |
| 6 steps, kitchen attention | **16.1 s** | 7602 MB | almost identical; new default |
| 4 steps, kitchen attention | **10.3 s** | 7534 MB | visibly softer; preview only |

### H3-Image (896x1344, 6 steps, cfg 1, w4a8 transformer)

| setting | exec | peak VRAM | free RAM | note |
|---|---:|---:|---:|---|
| 32B nvfp4 text encoder, 6 steps | 32.4 s cold | 7269 MB | 0.54 GB | best material/face, heaviest |
| P-H3 4B int8 text encoder, 6 steps | **21.3 s cold / ~10 s warm** | 7304 MB | 1.90 GB | comparable, much lighter |
| 4B TE, 4 steps | 17.6 s cold / ~7 s warm | 6923 MB | 1.94 GB | softer preview |
| 4B TE, 8 steps | 13.5 s warm | 6906 MB | 1.52 GB | HQ; more detail, slower |
| 4B TE + P-H3 LoRA, 8 steps | 45.8 s cold | 7362 MB | 1.06 GB | not worth it on H3-Image: ~2x slower, changes composition |

The 4B TE is the **P-H3-Image** text encoder (`p-h3-image_text_encoder_int8_convrot.safetensors`,
~5 GB) with its connector. It is a distilled 4B replacement for the 32B encoder; it works with the
normal `minimax` CLIP type. The 32B encoder still gives the most natural face and the thickest cum
material; the 4B is good enough for drafts and iteration. Per-step warm cost is about 1.3-1.5 s.

### H3 video (FL2VA w4a8 + Pika Flex 6-step, 24 fps)

| clip | steps | exec | peak VRAM | note |
|---|---:|---:|---:|---|
| 512x768, 85 f (3.5 s) | 6 | 152.9 s cold / **111.4 s warm** | 7411 MB | standard draft |
| 512x768, 85 f | 4 | 96.6 s cold / **81.7 s warm** | 7411 MB | 27% faster, preview |
| 512x768, 85 f | 8 | 167.3 s warm | 7460 MB | 50% slower than 6; no proven gain |
| 512x768, 124 f (5 s) | 6 | 211.6 s cold | 7466 MB | |
| 512x768, 124 f | 4 | 110.3 s | 7435 MB | |
| 768x1152, 124 f | 6 | **372.3 s** | 7429 MB | final |
| 768x1152, 124 f | 4 | **267.3 s** | 7669 MB | 28% faster, softer |
| 512x768, 85 f + act LoRA 0.8 | 6 | 114.9 s warm | 7412 MB | ~3% over the plain clip |
| 512x768, 85 f, pytorch attention | 6 | 196.9 s warm | 7455 MB | kitchen is 20-45% faster |

Removing the audio VAE/mux did **not** help (158.5 s vs 152.9 s cold, within noise) and the sound is
a scratch track anyway, so keep the audio node rather than special-casing it.

The first/last, Ref2VA and t2v graphs use the same transformer and attention; expect the same
range, with a second reference image adding a second VAE encode (a second or two, not a new
bottleneck). The Qwen edit graph is the same model and step cost as t2i; the reference encode adds
very little.

### Coverage of the remaining graphs

| graph | measured / status |
|---|---|
| first+last (`wf_h3vid_i2v_fl.json`), 512x768 85 f, 6 steps | **122.9 s** (about 10% over plain i2v; the second image adds a VAE encode) |
| t2v (`wf_h3vid_t2v.json`), 512x768 85 f, 6 steps | **109.3 s** (same as i2v; no keyframe encode) |
| Qwen edit (`wf_qwen21_edit1.json`), 1024x1024, 12 steps | **55.7 s** cold (reference encode + model load; a 25-step edit is ~70 s) |
| Ref2VA (`wf_h3vid_ref2va6.json`) | the Ref2VA transformer is not on cutestation; same attention class as FL2VA, so budget the i2v range and test it on a 24 GB card |
| Wan 2.1/2.2 | not installed and not viable on 16 GB (see `CUM-VIDEO.md`) |
| Anima i2i restyle | closed by owner verdict; not re-benchmarked |
| Krea Verite | superseded; its int8 UNet is not on cutestation |

The first 5-second 512x768 clip after an engine start took 211.6 s; the same clip later took ~111 s
for 85 frames and ~160-170 s extrapolated for 124 frames. Budget 3-6 minutes per final clip on this
box.

### Qwen-Image-2.1 (25 steps default)

| setting | exec | peak VRAM | note |
|---|---:|---:|---|
| 1024x1024, 25 steps | 37.2 s cold | 7107 MB | default |
| 1024x1024, 12 steps | 29.1 s | 7333 MB | moderate-quality keeper / preview |
| 896x1344, 25 steps | 34.5 s | 7108 MB | portrait |
| 1024x1024 edit, 12 steps | 55.7 s cold | 7306 MB | reference encode + model load; 25-step edit ~70 s |

The `QwenImage21Cache` node already removes much of the step cost, so cutting steps saves less
than on Krea.

### RelayVSR x2

85 frames, 512x768 -> 1024x1536: **18.0 s**, peak 7346 MB. This is the cheapest way to get a large
clip: generate 4-step 512x768, then upscale. It is a real tradeoff - VSR sharpens and invents detail,
and the skin can go slightly waxy - but the result held up against a native 768x1152 6-step clip at
1/15th of the generation time. Use it for drafts and social-size finals; use native 768x1152 when
the best anatomy matters.

### Wan 2.2

Not installed on cutestation (needs the GGUF custom node and two 14B Q5 files). The 16 GB test box
already OOMs at load; on 8 GB it is not a candidate. See `docs/CUM-VIDEO.md`.

## What to use, per workflow

| job | workflow | setting |
|---|---|---|
| photoreal still | `wf_krea2_nsfw_8gb.json` | 4 preview / 6 standard / 8 final, kitchen attention |
| anime still | `wf_anima2.json` | 12 preview / 20 standard / 30 final, ck + fp16 acc |
| anime draft | `wf_anima2.json` + `anima-turbo-v1.1` | 6-8 steps, cfg 1, euler |
| anime hires | `wf_anima_hires.json` | 1152x1728, denoise 0.30, 20 steps |
| H3 keyframe / cum still | `wf_h3img_4bte.json` (draft) / `wf_h3img_8gb.json` (final) | 4 / 6 / 8 steps |
| H3 video draft | `wf_h3vid_i2v_4step.json` | 512x768, 85 f, 4 steps |
| H3 video final | `wf_h3vid_i2v.json` | 768x1152, 124 f, 6 steps |
| H3 act LoRA | `wf_h3vid_i2v_lora.json` | 512x768, 85 f, 6 steps; use `h3nsfw\...` on Windows |
| cheap large clip | 512x768 4-step -> `relayvsr_x2.json` | 2x upscale |
| identity edit | `qwen21_edit2.json` | 25 steps; 12 for preview |
| photoreal still (H3) | `wf_h3img_4bte.json` | 4B TE, 6 steps |

## Memory rules that actually mattered

1. **Peak VRAM is 7.0-7.7 GB** on every model. There is no headroom for a browser decoding a
   4K video during an H3 job. Close it if a job OOMs.
2. **16 GB RAM is the binding constraint for H3**, not 8 GB VRAM. The 32B encoder is 14.6 GB and
   the FL2VA transformer is 11.7 GB; DynamicVRAM streams them, but free RAM hit 0.01 GB and the
   pagefile became part of the pipeline. The 4B H3-Image encoder is the single best fix (free RAM
   1.9 GB instead of 0.5 GB).
3. **One job at a time.** A still batch while a video is loaded is the reliable way to OOM.
4. **Restart between model families** if timings look wrong; the RAM-pressure cache can hold the
   old family and make the next load page from disk.

## Windows-specific gotchas found during the pass

- **LoRA paths use backslashes on Windows.** `h3nsfw/epic_cumshots.safetensors` is rejected by the
  local loader; `h3nsfw\epic_cumshots.safetensors` works. The page and `tools/lab.py --box local`
  now normalize this when they talk to a local Windows ComfyUI (`kit/studio/core.py`,
  `tools/lab.py`); the workflow JSONs keep the portable forward-slash form for the Linux boxes.
- **Model filenames differ per install.** The 8 GB card has `*_w4a8_mixed.safetensors`; a bigger
  card may have `*_int8_convrot.safetensors`. The `_8gb` workflows default to the w4a8 names; with
  the other workflows set `unet` in the job (the page does it automatically).
- The second ComfyUI instance needs `--disable-assets` (or its own `--database-url`), otherwise it
  refuses to start while the user's engine holds `ComfyUI/user/comfyui.db`.

## GTX 1070 8 GB: what probably transfers

> **This is speculation, not a measurement.** No Pascal card was available. An agent on a 1070
> must run the matrix and report real numbers; do not turn this section into assumptions.

The 1070 has the same 8 GB but a very different compute envelope:

| | GTX 1070 (GP104, 2016) | RTX 5060 (GB206, 2025) |
|---|---|---|
| compute capability | 6.1 (Pascal) | 12.0 (Blackwell) |
| CUDA cores / FP32 | 1920 / 6.45 TFLOPS | 3840 / 19.18 TFLOPS |
| memory | 8 GB GDDR5, 256-bit, 256 GB/s | 8 GB GDDR7, 128-bit, 448 GB/s |
| tensor cores | none | 5th gen |
| native BF16 / FP16 compute | no / 1:64 rate | yes / yes |
| FP8 / NVFP4 | no | yes |
| CUDA 13 support | **dropped** | yes |

Sources: [GTX 1070 specs](https://www.techpowerup.com/gpu-specs/galax-gtx-1070-ex.b3830),
[RTX 5060 specs](https://www.techpowerup.com/gpu-specs/msi-rtx-5060-gaming-oc-v1.b13273),
[CUDA 13 release notes](https://docs.nvidia.com/cuda/archive/13.0.3/cuda-toolkit-release-notes/).

Hard blockers, in order:

1. **The current engine cannot run at all on a 1070.** PyTorch 2.14.1+cu130 and CUDA 13 dropped
   Pascal; a 1070 needs an older PyTorch (cu118/cu126) and an older ComfyUI. The same `pip install`
   that works on the 5060 produces `no kernel image is available for execution` on a 1070.
2. **The quantized models are Turing+.** `w4a8`, `int8_convrot`, `nvfp4` and the Kitchen INT8
   attention kernels assume tensor cores and CUDA 13. Krea nvfp4, H3 w4a8, Qwen int8, RelayVSR int8
   and the P-H3 4B encoder are all in this group. On Pascal they either refuse to load or fall back
   to a dequantize-every-step path that is far slower than the 8 GB card can afford.
3. **No native BF16/FP16 compute.** Diffusion on Pascal is effectively FP32 (or FP16 storage with
   FP32 math), roughly 1/3 the FP32 throughput and 57% of the bandwidth of the 5060. Expect a
   **3-5x slowdown** for a model that does run, not 1.5x.
4. **The small models still fit.** Anima/Pink (3.9 GB fp16) and SD1.5-class models fit in 8 GB and
   were the standard on 1070s; Anima at 832x1248/20-30 steps is the realistic Pascal best case,
   perhaps 90-180 s per still with SDPA or split attention. GGUF Q4/Q5 of Krea or Wan may load via
   ComfyUI-GGUF and run in FP16/FP32, but the 14B video models will be minutes per second of clip.
5. **H3 and Qwen-Image-2.1 are effectively out.** Even if a GGUF/fp16 version is found, the 16 GB
   RAM + 8 GB VRAM + Pascal compute combination cannot stream a 12-20 GB transformer at a usable
   rate. H3-Image with the 4B encoder is the only plausible H3 variant, and only if a non-int8
   transformer is available.

What a 1070 agent should test, in this order: frozen cu118/cu126 PyTorch + matching ComfyUI;
Anima/Pink fp16 at 832x1248 with SDPA (and split/sub-quadratic attention); GGUF Q4 Krea if a file
exists; 512x768 H3-Image with the 4B encoder only if a dequantized transformer runs; then measure
per-step time and peak VRAM before promising anything. If the first step fails on a kernel image
error, stop: the stack is wrong, not the settings.

## Desktop headroom: generating with a browser open (2026-11-20)

Question: does a normal desktop (browser with a video tab, Discord, a launcher) push an 8 GB / 16 GB
Windows machine into OOM? Measured on cutestation with `tools/experiments/vram_pressure.py`, which
holds a fixed block of VRAM and RAM the way a browser does, optionally grabbing it in the middle
of a job. Prompts are neutral (`jobs/neutral/bench_headroom.jsonl`, renders in `sfw/bench/`); speed does not depend on the subject.
Engine: ck + fp16 accumulation on :8189.

| job | pressure | exec | peak VRAM (all apps) | min free RAM | min free commit | result |
|---|---|---:|---:|---:|---:|---|
| Krea 6 steps | none | 16.6 s warm | 7450 MB | 0.65 GB | - | ok |
| Krea 6 steps | 1.5 GB VRAM held before | 13.8-17.9 s | 7649 MB | 1.87 GB | - | ok, no slowdown |
| Krea 6 steps | 1.5 GB VRAM grabbed mid-job | 20.1 s | 7674 MB | 0.27 GB | - | ok, ~20% slower |
| H3 i2v 4 steps, 512x768 85 f | none | 78.9 s warm / 67.0 s | 7447 MB | 0.99 GB | 0.74 GB | ok |
| H3 i2v 4 steps | 1.5 GB VRAM + 3 GB RAM mid-job | 84.0 s | 7770 MB | 0.50 GB | - | ok, ~6% slower |
| H3 i2v 4 steps | 3 GB VRAM + 4 GB RAM mid-job | 85.9 s | 7784 MB | 0.01 GB | **0.05 GB** | ok, but on the edge |

What this means:

1. **VRAM is not the failure mode.** DynamicVRAM measures what other apps hold (NVML) and streams
   more of the model instead of failing. Even 3 GB taken mid-video only cost a few seconds.
   `--reserve-vram` / `--vram-headroom` are not needed on this setup; leave them unset.
2. **Commit charge is the failure mode.** Windows refuses allocations when RAM + pagefile is fully
   committed, and whichever process asks next dies: usually a browser tab ("Out of memory"), or
   ComfyUI with a `MemoryError`. Free commit fell to 0.74 GB with *no* pressure and to 0.05 GB in
   the worst case. It survived only because the system-managed pagefile grew mid-job (11.4 GB ->
   29 GB on C:). Growth is lazy and resets to the small size after a reboot, so the first H3 job
   after boot is the risky one.
3. **An idle engine keeps its commit.** After one Krea + H3 session the idle bench engine held
   19.6 GB of commit (4.3 GB resident). A second idle ComfyUI (for example the Love Live Studio
   engine) held another 5.7 GB. Two engines on a 16 GB box is the easiest way to run out.
4. **`--cache-ram` does not fix it.** `--cache-ram 2 6` gave the same timings and the engine still
   reached 16.3 GB of commit after a video. The commit is the model staging itself, not the result
   cache. Not recommended.

### Recommended Windows setup for headroom

- **A fixed pagefile, so it never has to grow mid-job.** System Properties -> Advanced ->
  Performance Settings -> Advanced -> Virtual memory -> Change: untick "Automatically manage",
  pick the fastest NVMe, Custom size **initial 32768 MB, maximum 49152 MB**, then reboot. That
  gives a commit limit of about 48 GB on 16 GB RAM. It costs disk space only; with DynamicVRAM it
  is not used as slow "swap" for active weights. This is a user step: the agent must not change
  system settings.
- **One ComfyUI engine at a time.** Stop the other studio's engine (`kit\start.ps1 -Stop` in that
  repo) before an H3 session, or point both apps at the same `comfy_url`.
- **Close or restart the engine after a video session** if you go back to browsing heavily:
  `kit\start.ps1 -RestartEngine` releases the 15-20 GB of commit an idle engine holds.
- **Browser**: hardware acceleration can stay on. VRAM is handled; a 4K video tab costs a few
  seconds per job, not a crash.

### Launcher bug fixed in the same pass

`kit\start.ps1` passed `extra_flags` to ComfyUI as **one** argument, quoted because it contains
spaces. With `"--use-ck-attention --fast fp16_accumulation"` set, argparse rejected it and the
page's own engine launch failed ("ComfyUI did not start"). The flags are now split on whitespace.
`../lovelive-studio/kit/start.ps1` has the same line and needs the same fix.

## Automatic low-memory mode (2026-11-21)

Every job from the page and every `tools/lab.py` batch is checked first (`kit/studio/headroom.py`;
`python tools/headroom.py <template>` from a terminal). Because commit is the failure mode (above),
the check is about commit, not VRAM:

- **Estimate**: the files the engine will actually load (its quantization; from
  `kit/models.json`) x 0.6 + 2 GB. The 0.6 is fitted to the two measured engine commits above
  (16.3 GB after an H3 video with 32 GB of files; 19.6 GB after Krea + H3). It is an estimate, not
  a calibration: re-fit it when `bench.py` has more `min_free_commit_gb` numbers.
- **Have**: free commit (`GlobalMemoryStatusEx`) + what our own engine already holds (it reuses it).
- **ok** with 4 GB or more to spare. **lean** below that: the engine drops its cached models
  (`/free`) before the job, so it loads slower, and H3-Image swaps the 32B encoder for the P-H3 4B
  one (`wf_h3img_4bte.json`, the measured best RAM fix) when those files are present. **critical**
  when even that does not fit: same as lean, plus a warning that the pagefile has to grow mid-job.
  The job runs in every case.
- **What to close**: the apps holding the most commit (Steam, browsers, Discord, ...), never
  Windows itself, the antivirus, the agent's app or the engine. Another ComfyUI engine (the other
  studio's) is called out on its own. Other apps holding more than 1.5 GB of VRAM get a "about 20%
  slower" note (measured), not a profile change.
- The page shows it under **Make pictures** / **Make video** when a template is picked and on the
  running job's card. `tools/lab.py` warns and unloads but never swaps the encoder in a round
  (that would change what is being compared); it suggests the light workflow instead.
- Not done on purpose: engine flags. `--lowvram` is a no-op with dynamic VRAM, `--reserve-vram`
  was not needed, and `--cache-ram` did not lower commit (measured above). The one engine-level
  fix that works, restarting the engine to release 15-20 GB of idle commit, kills the engine for
  every app using it, so it stays a suggestion.

## Re-running this pass

`tools/experiments/bench_engine.ps1` starts/stops the private engine on 8189;
`tools/experiments/bench.py` queues a JSONL job file and appends
`{name, wall_s, exec_s, peak_vram_mb, min_free_ram_gb, min_free_commit_gb}` to
`<out>/_bench.jsonl`. Pass `--seed N` when repeating a job, or ComfyUI returns the cached result in
0 s. `tools/experiments/vram_pressure.py --vram 1.5 --ram 3 --delay 20` simulates a browser. The job files are
in `jobs/bench_*.jsonl`; the renders and sheets are under `gens/bench/` (git-ignored).
