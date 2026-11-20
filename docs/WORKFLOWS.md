# Workflows: what each graph is for

All graphs are ComfyUI API JSON with `{{placeholders}}`. `tools/lab.py` (batch) and the Studio
page (`kit/studio/core.py`) fill them the same way. Model files live on the boxes, not in this
repo.

| workflow | model | size / steps | use |
|---|---|---|---|
| `wf_krea2_nsfw.json` | Krea 2 Turbo NSFW v10 (nvfp4) | 896x1344, 8, cfg 1 | photoreal e-girl, facial, cum stills |
| `wf_krea2_verite.json` | Krea 2 Turbo + Verite realism LoRA | 896x1344, 8 | older photoreal chain, plastic skin - superseded |
| `wf_anima2.json` | Pink Alchemy Anima v2.9 (or anima-base) | 1248x832 / 832x1248, 30, cfg 4 | anime stills; seal prompt |
| `wf_anima_hires.json` | same, img2img | 1.38x, 20, denoise 0.30 | anime second pass |
| `wf_anima_i2i.json` | same, img2img | 24 steps, denoise 0.45 | frame restyle (closed by owner verdict) |
| `wf_h3img.json` | H3-Image | 896x1344, 6, cfg 1 | keyframes, cum material stills |
| `wf_h3vid_i2v.json` | H3 FL2VA + Pika 6-step | 768x1152, 124 f | POV blowjob motion |
| `wf_h3vid_i2v_lora.json` | same + a second LoRA (node 21) | same | side deepthroat, titjob, cum LoRA |
| `wf_h3vid_i2v_fl.json` | same, first+last frame | same | state transitions (endpoint must be an edit of the first) |
| `wf_h3vid_ref2va6.json` | H3 Ref2VA + Pika ref LoRA | same | two references (pose + cock, or pose + cum) |
| `wf_h3vid_t2v.json` / `_lora` | H3 FL2VA t2v | 576x1024, 124 f | text-only motion |
| `wf_qwen21_edit1.json` | Qwen-Image-2.1 edit | source size | identity-preserving edits ("same girl, add X") |
| `wf_qwen21_t2i.json` | Qwen-Image-2.1 | 1024 | detailed anatomy stills |
| `wf_wan21_i2v.json`, `wf_wan22_i2v.json` | Wan 2.1/2.2 14B GGUF | 480x832 | not viable on 16 GB (OOM); kept for a 24 GB card |

## Placeholders

The app and `tools/lab.py` substitute `{{name}}` with the job field of that name; values missing
from the job come from the workflow's `_params`, then from the template. The standard set:
`prompt`, `negative`, `seed`, `width`, `height`, `steps`, `cfg`, `length`, `image`, `image1`,
`last`, `lora`, `strength`, `denoise`, `unet`, `prefix`.

## Node names that matter

- H3 LoRAs under `models/loras/h3nsfw/` are addressed as `h3nsfw/<file>`.
- H3 needs `qwen3vl_32b_minimax_h3_nvfp4_awq` (or the 4B for small cards) and the miniMax VAEs.
- Anima/Pink uses `qwen_3_06b_base` + `qwen_image_vae`.
- Krea 2 uses `qwen3vl_4b_int8_convrot` + `qwen_image_vae`.
- Qwen-Image-2.1 uses `qwen3vl_8b_w4a8` + `qwen_image_2.1_vae_bf16`.
