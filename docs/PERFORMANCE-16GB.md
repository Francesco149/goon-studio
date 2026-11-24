# 16 GB pass (2026-11-24)

Measured on a **16 GB AMD RX 7800 XT** (ROCm 10.1, PyTorch 2.14, Linux, 125 GB RAM, ComfyUI 0.45.0),
the Studio's own templates run through the page's engine layer (`tools/experiments/bench_templates.py`;
raw rows in `jobs/b16_bench.jsonl`). Times are server-side execution seconds; "warm" is the second run
(next seed) with the models loaded. The 8 GB numbers are the RTX 5060 pass (`PERFORMANCE-8GB.md`).

## The short answer

**16 GB is not faster, it is roomier.** This card runs the Studio's jobs at about the speed of the
8 GB RTX 5060 (H3 video slower: ROCm compute, not memory, is its limit). So the **16 GB profile keeps the
same headroom as an 8 GB card** - the engine uses about 8 GB and the rest stays free for the desktop,
games or a second app - and only the jobs that measurably gain from the whole card are worth giving it:

| job (896x1344 unless noted) | whole card | 8 GB headroom | 8 GB RTX 5060 |
|---|---:|---:|---:|
| Krea NSFW v10, 6 steps | 21.7 s | 21.8 s | 16.1 s |
| Krea 2 INT8 + Verite, 8 steps (`egirl_bj_pov` and the pose templates) | **25.3 s** | 32.7 s | ~40 s |
| Krea 2 + Verite at 1024x1536 | 33.3 s | - | - |
| Anima / Pink, 30 steps (832x1248) | 28.0 s | 28.1 s | 36.3 s |
| Illustrious (WAI), 28 steps (1216x832) | 11.4 s | 11.5 s | - |
| H3-Image, 32B encoder | 7.2 s | 7.3 s | ~10 s (4B encoder) |
| H3 video 512x768, 85 f, w4a8 | **93.8 s** | 103.3 s | 111.4 s |
| H3 video 512x768, 85 f, INT8 | 99.7 s | - | - |
| H3 video 768x1152, 124 f, INT8 | 468.5 s cold / 408.6 s warm | 474.7 s cold | 372.3 s |

Peak VRAM with the whole card is ~15.3 GB on every job: ComfyUI's dynamic VRAM fills what it is
given, which is not the same as needing it - the 8 GB-headroom column ran at ~8.3 GB peak.

**Gains from the whole card:** the Krea 2 + Verite chain (-23%: its 13 GB INT8 model plus LoRA
patches no longer stream) and H3 video (-9%). Everything else is the same. Use the whole card for a
batch of photoreal keyframes or a long video session when nothing else needs the GPU.

## Flags (all on top of `--use-ck-attention`)

| flag | result |
|---|---|
| `--use-ck-attention` | keep: Anima 28.0 s vs 50.7 s without it; Krea/H3 graphs pick their attention in the workflow |
| `--reserve-vram 1.5` | keep on AMD: this card corrupts output when VRAM runs nearly full |
| `--reserve-vram <VRAM - 7.5>` | **the 16 GB profile's headroom**: the engine behaves like an 8 GB card |
| `--highvram` | **never**: out of memory on Krea + Verite, H3-Image and H3 video |
| `--fast fp16_accumulation` | no change on ROCm (it is the measured win on NVIDIA, keep it there) |
| `--disable-dynamic-vram` | hung in the first VAE decode (5+ min); never |

**INT8 vs w4a8 transformers:** on 16 GB the w4a8 H3 files (12.5 GB) fit and are slightly faster than
INT8 (21 GB, streamed): 93.8 vs 99.7 s. The profile keeps the 8 GB variants; INT8 brings nothing here.
(NVIDIA cards with INT8 tensor cores may differ: unmeasured.)

## The profile

- Windows: `kit\setup.ps1 -Profile16` (only on a 16 GB+ card and on the user's yes; `-Profile8` undoes
  it); Linux: `kit/linux/setup.sh --profile16`. It writes `"perf_profile": "16gb"` and the headroom
  reserve into `extra_flags`. To give a session the whole card, drop the `--reserve-vram` value from
  `extra_flags` and restart the engine; put it back afterwards.
- Offer it at setup in one line with the caveat: using the whole card leaves less for other apps
  during a job, and on most jobs it is not faster.
- A headless box with nothing else on its GPU (the author's) runs the whole card all the time.
