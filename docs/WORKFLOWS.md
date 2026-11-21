# Workflows: what each graph is for

All graphs are ComfyUI API JSON with `{{placeholders}}`. `tools/lab.py` (batch) and the Studio
page (`kit/studio/core.py`) fill them the same way. Model files live on the boxes, not in this
repo.

| workflow | model | size / steps | use |
|---|---|---|---|
| `wf_krea2_nsfw.json` | Krea 2 Turbo NSFW v10 (nvfp4) | 896x1344, 8, cfg 1 | photoreal e-girl, facial, cum stills |
| `wf_krea2_nsfw_8gb.json` | same, kitchen INT8 attention | 896x1344, 4/6/8 | **cutestation default**; 6 standard |
| `wf_krea2_nsfw_4step.json` | same, parameterised `steps` | 896x1344 | preview/refine test graph |
| `wf_krea2_verite.json` | Krea 2 Turbo + Verite realism LoRA | 896x1344, 8 | older photoreal chain, plastic skin - superseded |
| `wf_anima2.json` | Pink Alchemy Anima v2.9 (or anima-base) | 1248x832 / 832x1248, 30, cfg 4 | anime stills; seal prompt |
| `wf_anima_hires.json` | same, img2img | 1152x1728, 20, denoise 0.30 | anime second pass |
| `wf_anima_i2i.json` | same, img2img | 24 steps, denoise 0.45 | frame restyle (closed by owner verdict) |
| `wf_h3img.json` | H3-Image | 896x1344, 6, cfg 1 | keyframes, cum material stills |
| `wf_h3img_2ref.json` | H3-Image with Picture 1 + Picture 2 | 896x1344, 6 | mixed gens: scene + real object (mouth redrawn) |
| `wf_h3img_2ref_inpaint.json` | H3-Image 2ref + `SetLatentNoiseMask` | 896x1344, 6, denoise 0.92 | mixed gens with the lips pinned: fill only the cock mask |
| `wf_h3img_8gb.json` | H3-Image w4a8 + 32B encoder, kitchen attention | 896x1344, 6 | cutestation final; 32B material |
| `wf_h3img_4bte.json` | H3-Image w4a8 + P-H3 4B encoder, kitchen attention | 896x1344, 4/6/8 | cutestation draft; ~5 GB encoder |
| `wf_h3img_4bte_lora.json` | 4B encoder + `p-h3-image_lora_bf16` | 896x1344, 8 | slower, changes composition; not recommended |
| `wf_h3vid_i2v.json` | H3 FL2VA + Pika 6-step | 768x1152, 124 f | POV blowjob motion |
| `wf_h3vid_i2v_4step.json` | same, 4 sigmas | 512x768 / 768x1152 | preview clip, same seed |
| `wf_h3vid_i2v_8step.json` | same, 8 sigmas | same | HQ test; 50% slower than 6, no proven gain |
| `wf_h3vid_i2v_lora.json` | same + a second LoRA (node 21) | same | side deepthroat, titjob, cum LoRA |
| `wf_h3vid_i2v_fl.json` | same, first+last frame | same | state transitions (endpoint must be an edit of the first) |
| `wf_h3vid_ref2va6.json` | H3 Ref2VA + Pika ref LoRA | same | two references (pose + cock, or pose + cum); **use it whenever something that appears in the clip is not in the first frame** |
| `wf_h3vid_t2v.json` / `_lora` | H3 FL2VA t2v | 576x1024, 124 f | text-only motion |
| `wf_h3vid_i2v_noaudio.json` | i2v without audio VAE | same | measured no gain; kept for testing |
| `wf_h3vid_i2v_pytorch.json` | i2v with pytorch attention | same | fallback for cards without Kitchen INT8 |
| `qwen21_edit2.json` / `wf_qwen21_edit1.json` | Qwen-Image-2.1 edit | source size | identity-preserving edits ("same girl, add X") |
| `qwen21_t2i.json` / `wf_qwen21_t2i.json` | Qwen-Image-2.1 | 1024, 25 | detailed anatomy stills; 12 steps for a preview |
| `relayvsr_x2.json` | RelayVSR x2 int8 | 2x source | 18 s for an 85-frame 512x768 clip; cheap large clip |
| `wf_wan21_i2v.json`, `wf_wan22_i2v.json` | Wan 2.1/2.2 14B GGUF | 480x832 | not viable on 16 GB (OOM); kept for a 24 GB card |

## Model names per box

The graph files are portable, but the model filenames are not. cutestation has
`minimax_h3_*_w4a8*.safetensors`; ampere has `*_int8_convrot.safetensors`. The `_8gb` H3 workflows
default to the cutestation names. On ampere, override `unet` in the job or use the original
workflow. LoRA names on Windows use `h3nsfw\name.safetensors`; the page and `tools/lab.py
--box local` normalize them for a local Windows ComfyUI, but a hand-written ComfyUI API call
must use the backslash form.

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
