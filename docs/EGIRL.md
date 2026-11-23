# Photoreal e-girl recipe (Krea 2 Turbo NSFW v10, 2026-11-20)

> **Blowjob keyframe: Krea 2 Turbo + Verite (owner, 2026-11-21: "excellent ... the recipe working
> correctly").** Template `egirl_bj_pov`: plain `krea2_turbo_int8_convrot` + `Verite_realism` 1.0
> (`wf_krea2_lora_8gb.json`, 8 steps, 896x1344, ~40 s on 8 GB), prompted the Verite way - the act
> first, then her (the character block), then him ("a man ... his cock has a defined glans with a
> rim, the foreskin folded back behind it ... his balls at the base behind her hand"), hands,
> setting, `Candid amateur phone photo.` last. Round a86: 4/4 seeds a sealed POV blowjob with the
> e-girl look, LED room and natural bust; weak spots are slightly vine-like veins and one seed
> where his hand replaced hers. **Krea NSFW v10 alone draws a handjob for the same scene (4/4)**,
> and Verite on NSFW v10 seals but drifts to a side angle with a tongue-like glans. H3-Image as
> the keyframe (round a85) was the regression the owner saw. The portrait/facial stills below
> stay on NSFW v10.

The owner's target for the photoreal side: an Asian e-girl with a curvy body and large
breasts, proportions comparable to the anime curvy type, not a caricature. This is the first
stack that hit it, and it is a different model from the earlier photoreal chain
(Krea 2 Turbo + `Verite_realism`).

## The model

| | |
|---|---|
| file | `KREA 2TurboNSFW_v10-nvfp4.safetensors` (7.15 GB, "Star Ultimate Model Converter" nvfp4) |
| where | `<engine_dir>\ComfyUI\models\diffusion_models\` (local), loaded by the plain `UNETLoader` (no special node) |
| comfy | 0.45.0; runs on a 3080 and on the 8 GB RTX 5060 (nvfp4 is dequantized at load) |
| speed | cutestation 8 GB: 4 steps 10 s, 6 steps 16 s, 8 steps 20 s at 896x1344 |
| settings | **6 steps standard** (4 preview / 8 final), cfg 1.0, euler / simple, denoise 1.0, no negative (ConditioningZeroOut) |
| workflow | `workflows/wf_krea2_nsfw_8gb.json` on cutestation (kitchen attention), `wf_krea2_nsfw.json` otherwise |

It is willing to draw explicit acts without any LoRA, which the plain Krea 2 + Verite chain
needed the LoRA for. Skin and faces are much more photographic than the Verite stills: pores,
soft body, real-light falloff, no plastic sheen.

**Preview/refine.** 4 steps is visibly softer but useful for checking pose, framing and the mouth
seal; 6 is almost identical to 8 and is the default; 8 is the final. Keep the seed and prompt and
change only the step count. The measured numbers are in `docs/PERFORMANCE-8GB.md`.

## The character block (keep fixed)

Prose, one sentence, reused verbatim in every shot:

```
a young adult Asian woman in her mid-twenties, e-girl: long black hair in twin tails with
pink streaks, wispy bangs, winged eyeliner, glossy lips, a silver heart choker. She has full
natural breasts that sit heavy with a soft slope, a narrow waist, wide hips and thick thighs.
```

Notes from the rounds:
- `p1_bust_natural` / `p3_mirror` are the reference proportions. `p2_bust_large` is the upper
  bound that still reads natural.
- "very large" / "huge" pushes the model into caricature (`e3/p8_paizuri`, `e1b_mirror`):
  keep the word `natural` in the same clause as the size.
- The face is stable across seeds when the character block is verbatim; the seed then mainly
  changes pose and framing, not identity (`e3` p1-p4).

## Prompt shape

**Portrait / body stills: tag-style is best.** `e5/g7_egirl`:

```
1girl, asian, egirl, long black hair, twintails, pink streaks, winged eyeliner, choker,
large breasts, curvy, oversized black tshirt, sitting on bed, looking at viewer,
half-closed eyes, realistic, photorealistic, led lights, bedroom, phone photo
```

**Scenes: prose, not tags.** The tag prompt with the author's own trigger words is what the
`krea2 sex` LoRA family was trained on, but in this merged checkpoint those tags produced a
two-panel collage and wrong acts (`e5/g3_bj_side` inset panel, `e5/g4_deepthroat` a
straddle that is not a blowjob). Prose held the composition (`e5/g8_prose_control`).

**Mouth seal.** The model's default is an open mouth with the tongue on the glans. What
worked (`e3/p5`, `e5/g8`, and on the anime side `pb1`/`pb2`):

```
Her lips are stretched in a tight wet ring around the shaft just behind the glans, her cheeks
hollowed, her head bowed forward as she takes it into her mouth. Her hand wraps the base. Her
eyes lift to the camera, half-lidded, light blush, saliva at the corner of her mouth.
```

Avoid `tongue out` / `open mouth` in the positive; they are followed literally. The seal is
seed-sensitive: re-roll before rewriting.

**Bust size.** "full natural breasts that sit heavy" -> reference. "large full breasts" ->
one step up. "huge" -> caricature. The owner is fine with some bigger-cock variants; the same
applies to chest.

## What is still wrong

- **Cum** was a cord in the first tries (`e1h`, `e3/p9`): one long rigid rope that travels
  off-frame. The fix is wording: `short thick splatters, blobs, drips, glossy` and no "rope"
  (`e67/c3`, `c4`, `o4`), or for the best material `translucent milky, watery, nearly clear with
  a milky tint, the skin visible through it` on H3-Image (`c1/h2_watery`). The facial pose and
  cum-shot video recipe are in `RECIPE-FACIAL.md`.
- **Bar/mosaic censorship cannot be prompted.** Bar censor draws a striped sticker in a random
  place (`pb4`); mosaic draws one large block that does cover the shaft (`pb5`) but its
  placement is luck. Post-process with ffmpeg is the reliable route.
- **Video** starts from these stills well (see the `v3`-`v6` rounds): the e1e keyframe gives a
  clean 5 s stroke at 768x1152 in 145 s on a 3080. That clip is the new best photoreal
  blowjob motion.

## The e-girl stills that define the look

- face + natural body: `gens/e3/p1_bust_natural`, `gens/e3/p3_mirror`
- lingerie / full body: `gens/e3/p4_standing`
- act: `gens/e3/p5_bj_seal`, `gens/e3/p7_bj_side`, `gens/e3/p8_paizuri`
- cum-landed: `gens/p4/p4_cum_landed`, `p5_cum_landed_2`
- best video keyframe: `gens/e1/e1e_bj_pov` (mouth sealed, hands right, O-ring lips)
- facial scene base: `gens/p3/p1_cock_out_cheek`, `p2_cock_out_face` (owner-approved pose/face)
