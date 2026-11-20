# Anime recipe: Pink Alchemy Anima (2026-11-20)

The anime side moved from `anima-base-v1.0` + `anima-aesthetic-v1.1` to a single hentai-native
Anima merge, and the mouth-seal problem was solved with prompt wording. This supersedes the
anime halves of `WINS.md` / `SEX-SCENES.md` for anything explicit.

## The checkpoint

| | |
|---|---|
| name | RAMTHRUST'S NSFW Pink Alchemy Anima v2.9 |
| file | `ramthrustsNSFWPINK_v29.safetensors` (4.18 GB unet) |
| base | Anima-Base v1.0 (same VAE `qwen_image_vae`, same TE `qwen_3_06b_base`) |
| loaded as | `UNETLoader` in the normal Anima graph (`tools/wf_anima2.json`) |
| source | Civitai model 2578175, v2.9-Anima1.0Base; a copy was fetched from the RunningHub HF mirror |
| where | ampere `unet/` and cutestation `F:\LLStudioTest\models\diffusion_models\` |

Why it wins: `pa1`-`pa3` (same prompts and seeds as the base-model `a2a`-`a2c`) have the anime
screenshot style, a real anime face, curvy proportions and a thick, veined cock with a defined
head. The base model could not do all four at once; adding anatomy weights to base pulled the
mouth off the cock (`a2b`). Pink keeps both.

## Settings

```
30 steps, cfg 4.0, er_sde / simple, 1248x832 (side) or 832x1248 (POV), denoise 1.0
```

The model card recommends `euler_ancestral`/`beta`, 26 steps, cfg 4.7. `pa5`/`pa6` with those
settings are close but not better; stick with the lab's existing Anima numbers.

**8 GB tuning (cutestation, 2026-11-20).** With `--use-ck-attention --fast fp16_accumulation`:
30 steps = **36 s**, 20 steps = **26 s**, 12 steps = **23 s**. 20 steps is almost identical to 30
and is the better everyday default; keep 30 for a final and 12 for a quick preview. For composition
drafts, `anima-turbo-v1.1` at 6-8 steps, cfg 1, euler runs in **4-10 s** but has a weaker style -
never use it for the finished anime look. The hires pass (1152x1728, 20 steps, denoise 0.30) is
**60 s** and peaks at ~7.6 GB VRAM. Full method and numbers: `PERFORMANCE-8GB.md`.

## Prompt - side view (mouth sealed)

```
masterpiece, best quality, year 2016, anime screenshot, 1girl, 1boy, hetero, blowjob, fellatio,
(penis in mouth:1.2), (lips sealed around penis:1.35), mouth stretched, no tongue,
cheeks hollowed, sucking, detailed penis shaft, veins, erection, uncensored,
(penis focus:1.2), side view, profile, kneeling, leaning forward, short silver hair, single braid,
purple eyes, @murota yuuhei, (curvy:1.6), (wide hips:1.4), thick thighs, large breasts,
mature female, half-closed eyes, blush, saliva, bedroom, soft light, love live! sunshine!!
```

negative:

```
extra hands, extra fingers, third hand, bad anatomy, fused limbs, censored, mosaic censoring,
bar censor, tongue out, open mouth, glans outside mouth, worst quality, low quality, score_1,
score_2, score_3, blurry, jpeg artifacts, watermark, text, 3d, realistic
```

## Prompt - POV (mouth sealed)

Same, with the side block replaced by:

```
pov, from above, looking up at viewer, short silver hair, single braid, purple eyes,
(curvy:1.6), thick thighs, large breasts, mature female, half-closed eyes, blush, saliva
```

and `male body` added to the negative.

## What makes the seal work

- `penis in mouth` + `lips sealed around penis` + `cheeks hollowed` in the positive.
- `no tongue`, and `tongue out, open mouth` in the **negative**. Without these the model's
  default is an open mouth with the tongue on the glans.
- Do **not** weight `glans` high for an in-mouth shot: the tags draw what they name, so a weighted
  glans ends up outside her mouth. Keep `detailed penis shaft, veins` and let the head go in.
- The seal is still seed-sensitive; reroll before rewriting.

## Results that define the look

- `pb2_side_seal_w` - side, sealed, thick veined shaft, curvy body.
- `pb3_pov_seal` - best anime POV: face, breasts, head in her mouth.
- `pb1_side_seal` - lighter/pastel variant.
- `pb6_side_big` - the "bigger" variant. `huge thick penis` really is comical; use it only on purpose.
- `pb7_cum_face` - anime cum is correct (strands, drips, gloss). The photoreal model is not.

## Censorship

- `bar censor` draws a free-floating striped sticker (`pb4`) - unusable.
- `mosaic censoring` draws one large block over the shaft with the head visible (`pb5`) - the
  flim13 look, and usable, but its placement is luck.
- For a controlled result, censor in post (ffmpeg crop + pixelize + overlay) as before.

## Second pass (hires detail)

The still is good at 832x1248; a low-denoise hires pass makes it deliverable:

```
upscale to 1.38x (832x1248 -> 1152x1728), 20 steps, cfg 4.0, er_sde/simple, denoise 0.30
```

`h1_d30` (Pink on `pb3`) sharpens the face, the shaft shading and the chest, and keeps the
mouth seal. `denoise 0.45` is punchier but loosens the seal and starts changing the braid;
keep 0.30 for the final. 90 s on the 5060. This is the anime equivalent of the detailer pass
the community runs after the first render.

## Anime video (owner verdict, 2026-11-20)

Best anime clip so far: `gens/v10/v10b_pov_bob` - H3 i2v from the `pb3_pov_seal` keyframe,
768x1152, 124 f, no LoRA, with the prompt asking for **whole-body motion**, not just the mouth:
```
A 2D anime clip in a clean cel-shaded TV-anime style. POV from above: a young adult woman with
short silver hair and purple eyes kneels between the viewer's legs, her large breasts on either
side of an erect penis, her lips sealed around the head. She bobs her head up and down the
shaft in a steady rhythm, her breasts bouncing with the motion, her braid swinging, her eyes
lifting to the camera between strokes. Saliva gathers at the corner of her mouth. The camera
shakes very slightly with her motion.

overall_soundscape: wet suction, soft pops, her breath, a low male grunt, quiet room tone. No music.
```

Owner: "nicer ... the motion is decent ... still feels a bit stiff but probably the best anime
one we got so far." The look still has a generic AI-render feel (Pink's shading), which is a
model property, not a prompt one.

On cutestation the same 768x1152 / 124 f clip is **372 s** at the standard 6 steps and **267 s**
at 4 steps; 512x768 / 85 f is **111 s** at 6 and **82 s** at 4. Use 4 steps with the same seed as
a preview, then re-run at 6 for the final. Full numbers: `PERFORMANCE-8GB.md`.

The side-view version of the same idea (`v10a_side_body`) was rejected: the cheek puffing reads
wrong and does not match the action. Do not use it.

The frame-by-frame restyle (`RECIPE-RESTYLE.md`) was rejected outright: owner called it
unstable and not a good anime style. Treat that route as closed unless the style model changes.

## What is still open

- The man is a featureless slab at the left edge. Add `his hip, his thigh, his hand on the back
  of her head` to the prompt or accept it as a crop.
- Extra hands still appear occasionally; inpaint the hand region or reroll.
- **Anime video**: best current recipe is `v10b` above (POV bob, whole-body motion prompt).
  It is still slightly stiff and the shaft does not travel as far as in the photoreal clips;
  the restyle route is closed by owner verdict.

## Sound

The model audio is a scratch track: the strokes crunch, the slurp sounds like noodles, and the
events are not synced to the action. Do not present a clip as finished on the strength of its
sound; the findings and the next routes are in docs/SOUND.md.
