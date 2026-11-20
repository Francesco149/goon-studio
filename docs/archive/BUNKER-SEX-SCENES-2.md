# Explicit scenes, session 2 - 2026-11-20 (overnight)

Additions from the second session: the photoreal e-girl stack, a hentai-native Anima
checkpoint, a measured survey of H3 act LoRAs, the cum findings, and the anime video workaround.
Everything here is **not yet owner-rated**; the session-1 approved recipes still stand.

## 1. Photoreal e-girl - Krea 2 Turbo NSFW v10

The owner's target: an Asian e-girl, curvy with large natural breasts, comparable to the anime
curvy type. This checkpoint (7.15 GB, `KREA 2TurboNSFW_v10-nvfp4.safetensors`) is the first
stack that hits it, and it runs on the 3080 through the plain `UNETLoader` in ComfyUI 0.45.

```
model      krea2_turbo_nsfw_v10_nvfp4.safetensors (unet)
settings   8 steps, cfg 1.0, euler / simple, denoise 1.0, no negative
sizes      896x1344 portrait, 832x1248 full body, 1216x832 side
speed      12-20 s per still on ampere
workflow   tools/wf_krea2_nsfw.json
```

Character block (keep verbatim; it fixes the face and the proportions):

```
a young adult Asian woman in her mid-twenties, e-girl: long black hair in twin tails with
pink streaks, wispy bangs, winged eyeliner, glossy lips, a silver heart choker. She has full
natural breasts that sit heavy with a soft slope, a narrow waist, wide hips and thick thighs.
```

- `full natural breasts` = reference proportions (`e3/p1`, `p3`, `p4`). `large` is one step up
  (`e3/p2`). `huge`/`very large` is caricature and should be a deliberate variant.
- Portraits: a danbooru-style tag prompt is excellent (`e5/g7`):
  `1girl, asian, egirl, long black hair, twintails, pink streaks, winged eyeliner, choker,
  large breasts, curvy, oversized black tshirt, sitting on bed, looking at viewer,
  half-closed eyes, realistic, photorealistic, led lights, bedroom, phone photo`
- Scenes: **prose, not tags**. The `krea2blow`-family triggers belong to the author's per-act
  LoRAs; in this merged checkpoint they produced a two-panel collage (`e5/g3`) and a straddle
  that is not a blowjob (`e5/g4`). Prose held the scene (`e5/g8`).
- Mouth seal: `Her lips are stretched in a tight wet ring around the shaft just behind the
  glans, her cheeks hollowed ...` and avoid `tongue out`/`open mouth` in the positive. The seal
  is still seed-sensitive.

Best stills: `gens/e3/p1_bust_natural`, `p3_mirror`, `p4_standing`, `p5_bj_seal`,
`p7_bj_side`, `p8_paizuri`; video keyframe `gens/e1/e1e_bj_pov`.

## 2. Anime - Pink Alchemy Anima v2.9

`ramthrustsNSFWPINK_v29.safetensors` (4.18 GB unet, Anima base) replaces base+aesthetic for
explicit anime. Same VAE/TE as Anima. Settings stay 30 steps, cfg 4.0, er_sde/simple; the
model card's 26/4.7/euler_ancestral/beta is close but not better (`pa5`, `pa6`).

The seal prompt (side view; swap the pose block for POV `pov, from above, looking up at viewer`):

```
masterpiece, best quality, year 2016, anime screenshot, 1girl, 1boy, hetero, blowjob, fellatio,
(penis in mouth:1.2), (lips sealed around penis:1.35), mouth stretched, no tongue,
cheeks hollowed, sucking, detailed penis shaft, veins, erection, uncensored,
(penis focus:1.2), side view, profile, kneeling, leaning forward, short silver hair, single braid,
purple eyes, @murota yuuhei, (curvy:1.6), (wide hips:1.4), thick thighs, large breasts,
mature female, half-closed eyes, blush, saliva, bedroom, soft light, love live! sunshine!!
```

negative: `extra hands, extra fingers, third hand, bad anatomy, fused limbs, censored,
mosaic censoring, bar censor, tongue out, open mouth, glans outside mouth, worst quality,
low quality, score_1, score_2, score_3, blurry, jpeg artifacts, watermark, text, 3d, realistic`

Rules:
- `penis in mouth` + `lips sealed around penis` + `cheeks hollowed`; `no tongue` in the positive
  and `tongue out, open mouth` in the negative. Without them the default is tongue-on-glans.
- Do not weight `glans` for an in-mouth shot; it draws the head outside the mouth.
- Results: `pb2_side_seal_w`, `pb3_pov_seal` (best POV), `pb1_side_seal`, `pb6_side_big`
  (deliberate bigger variant), `pb7_cum_face` (cum correct).
- Censorship: model-drawn bar is a floating striped sticker (`pb4`) - unusable; model mosaic is
  one block over the shaft (`pb5`) - usable but random placement. Post-process for control.

## 3. H3 act LoRAs - measured (ampere, 768x1152, 124 f, same keyframe/seed)

The LoRA set from `kimjob/h3_NSFW_lora` + RunningHub mirrors, loaded as a second
`LoraLoaderModelOnly` after Pika Flex (`tools/wf_h3vid_i2v_lora.json`, node 21). Names are
`h3nsfw/...` in ComfyUI.

| LoRA (strength) | clip | verdict |
|---|---|---|
| none | `v3a_ctrl` | **best POV stroke**: full down-up, held bottom, seal holds; anatomy holds |
| MM-H3 Blowjob v3 (0.85 / 0.5) | `v3b`, `v4a` | mouth stays on the glans, small licking, no stroke; weight 0.5 does not fix it |
| HMNSFW AIO V2 (0.7 / 0.5) | `v3c`, `v4b` | same as above, and +136 s compute |
| Astro NSFW (0.8) | `v3d` | drifts the character (straight hair), licking |
| Titjob (0.85) | `v3e` | **works**: breasts hold around the shaft, subtle stroke, face stable |
| HMCumshot V2 (0.7) | `v3f` | worsens cum into a swinging white cord |
| sideview-deepthroat (0.75) | `v3g` | **works**: real profile stroke, cheek bulge, takes it deeper |
| H3 Motion Booster (0.5) | `v4c` | no effect on the stroke |

Rule: an act LoRA only helps the act whose training clips match the framing. For the POV
blowjob the plain prompt + a good keyframe beat every LoRA tried.

## 4. Cum

- Photoreal still: one long rigid rope that behaves like a cord (`e1h`, `e3/p9`). The best
  photoreal stills come from "short thick splatters / blobs / drips, glossy" with no `rope`
  wording: `e67/c3_splatter`, `c4_drips`, `o4_cum_out`.
- Photoreal video: the cum materialises between frames; the HMCumshot LoRA makes it worse.
- Anime still: correct (strands, blobs, drips, gloss) - `pb7_cum_face`.
- Anime video: not tested with a real emission yet.

## 5. Two-clip chains: the endpoint rule

First+last frame i2v works (`tools/wf_h3vid_i2v_fl.json`), but `v7a`/`v7b` show the catch: if
the last frame is an independently generated still, the model morphs her face/framing on the way
there. The last frame must be an **edit of the first frame** (same image, cum added / cock
removed), otherwise identity drifts. The earlier `rc01` pair worked because the last frame was
the source image of the clip.

## 6. Anime video: H3 fails, restyle route

H3 i2v from a Pink still holds the 2D style but keeps the shaft rigid and degrades the act to
licking (`v6a`), with the Blowjob LoRA at 0.6 (`v6b`) it is the same, and the side view
(`v6c`) also licks. The workaround tested here:

```
1  photoreal clip   H3 i2v at 768x1152, the recipe in section 3       (v3a, 145 s)
2  frames           ffmpeg -fps_mode passthrough -> PNG sequence
3  restyle          Pink Alchemy img2img per frame, denoise 0.45, 24 steps, cfg 4,
                    fixed seed, "2D anime screenshot, cel shading" + the character tags
4  reassemble       ffmpeg -framerate 24 -i f%03d.png -i source.mp4 -map 0:v -map 1:a
```

A 24-frame test (`gens/r1`) held style and hair across consecutive frames; the full 124-frame
run is `gens/r2`. Denoise 0.40 keeps identity/hair/pink streaks; 0.55 is prettier but loses the
streaks. This is a day-one experiment, not yet owner-rated.

## 7. Files and paths

- workflows: `goonlab/tools/wf_krea2_nsfw.json`, `wf_anima2.json`, `wf_anima_i2i.json`,
  `wf_h3vid_i2v_lora.json`, `wf_h3vid_i2v_fl.json`
- models on ampere: `unet/krea2_turbo_nsfw_v10_nvfp4.safetensors`,
  `unet/ramthrustsNSFWPINK_v29.safetensors`, `loras/h3nsfw/*`
- models on cutestation: `F:\LLStudioTest\models\diffusion_models\ramthrustsNSFWPINK_v29.safetensors`
- prompts/seeds: `goonlab/jobs/*.jsonl`; contact sheets `goonlab/analysis/*.jpg`
- the e-girl and anime recipes as standalone notes: `goonlab/notes/RECIPE-E-GIRL.md`,
  `RECIPE-ANIME.md`, `RECIPE-RESTYLE.md`
