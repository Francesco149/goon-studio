# Facial / cum-shot scene recipe (approved pose, 2026-11-20 session 3)

The owner approved the two cock-out close-ups in `gens/p3` for facial expression and as the
base for this scene type: cock pulled out and held an inch below/at her open mouth, tongue out,
eye contact with the lens. The cum material is much closer but still reads a bit like water
running out of her mouth; the search for a projected spurt continues (see Limits).

## The still pose (approved)

`gens/p3/p1_cock_out_cheek` (896x1344, Krea 2 Turbo NSFW v10, 8 steps, cfg 1, seed 521):

```
Photorealistic first-person POV close-up: a young adult Asian woman in her mid-twenties,
e-girl with long black hair in pink-streaked twin tails and a silver choker, kneels between
the viewer's legs. He has just pulled his erect adult penis out of her mouth and holds it an
inch from her left cheek, the glans pointing at her face; her lips are wet and parted, a thin
strand of saliva connects her lower lip to the tip, her hand is wrapped around the base.
She looks up into the camera with half-lidded eyes, a light blush. Dim bedroom with pink LED
glow, phone flash, natural skin with pores, slight grain.
```

`gens/p3/p2_cock_out_face` is the tongue-out variant (seed 522): same block, cock upright in
front of her cheek, `her lips are parted and wet ... tongue out`, eyes on the lens.

Both were described by the owner as good facial expressions and a clear improvement for this
scene type.

## The cum-landed still

`gens/p4/p4_cum_landed` and `p5_cum_landed_2` apply the cum to the same pose:

```
... Thick translucent milky semen is splattered across her open mouth, her lips and one cheek,
glossy and see-through so the skin shows through, a heavy strand hanging from her chin.
```

The material reads as cum rather than water when the wording is `translucent milky`, `glossy`,
`see-through`, `heavy strand hanging`; it reads as water when the strands are thin and clear.
Placement rule: **lips, tongue, chin, jaw**. Anything high on the cheek or near the eye reads as
tears/mascara and ruins the shot (`v8b`, `v8c`, and Qwen-edited targets all did this).

## The cum-shot video

Start from the approved pose (`p1`/`p2`), then H3 i2v with the epic_cumshots LoRA:

```
model      minimax_h3_fl2va_pruned_int8_convrot + Pika Flex 6-step
second LoRA h3nsfw/epic_cumshots.safetensors at 0.8
size       768x1152, 124 frames, 24 fps
workflow   tools/wf_h3vid_i2v_lora.json
```

prompt:

```
Photorealistic amateur POV video. She holds his cock just below her open mouth, eyes on the
lens. The shaft pulses once and a short translucent milky rope shoots from the tip up across
her lips and cheek, glossy and see-through, then drips down her chin. It is one short arc, no
spray, nothing foams. She flinches, closes one eye, then smiles with half-lidded eyes, flushed.
The camera does not move.

overall_soundscape: a soft wet spurt, one low short male grunt, her sharp breath in, quiet
bedroom room tone. No music.
```

Result: `gens/v13/v13a_p1` (and `v13b_p2` for the tongue variant). The cum arrives as a heavy
translucent milky mass on the open mouth/lips and hangs in a strand to the chin; she flinches
and then smiles. This is the best cum-shot look of the session: no cord, no tears, no spray.

## Material vs dynamics - the tradeoff (owner-tested)

| attempt | material | dynamics |
|---|---|---|
| `v13` epic 0.8, "one short rope, no spray" | glue, too opaque | **good**: a rope, right timing, stable anatomy |
| `v14a` epic 0.5, "thin strands, droplets" | **more real** | nebulizer/mist, no rope |
| `v16a` epic 0.6, "single rope holds together" | still glue | still nebulizer |
| `v15a` first+last p1 -> p4, no LoRA | okay (p4 material) | cum fades in, no event |
| `v14b` no LoRA | almost no cum | - |

So the LoRA carries the event/rope, but its learned material is glue; the prompt can thin the
material but then the event turns into mist. The still model (Krea2, `p4`) has the approved
material but not the motion. Nothing tried so far gives both.

## Twitch specification (owner, for the next attempt)

The owner wants the build-up, not a single pulse:

- rhythmic, distinct twitches; **not** a vibration;
- a few twitches with no cum first, then **one spurt on almost every twitch**;
- each spurt synchronized to a twitch, about a beat apart;
- the glans keeps its shape (no stretching/deforming when sucked), the veins swell with each
  pulse.

The prompt should spell this out as a timeline ("twitch, twitch, then twitch+rope, pause,
twitch+rope ..."), not as "pulses". `v17` was written for this but not run before the session
ended.

## Next routes for a true cum-shot

1. **Post-composite**: keep a clean reaction clip (no cum) and composite an AI-generated cum
   plate with a matte, so material comes from Krea2 (approved) and timing is authored. Needs a
   static camera and per-frame face tracking; feasible on the existing clips.
2. **Keyframe sequence + interpolation**: generate 4-6 Krea2 cum states and interpolate. The
   material is right; the motion is authored rather than generated, so it will read as morphing
   unless the states are dense.
3. **24 GB card + Wan 2.2** with a cum-shot LoRA: the only route that might generate the whole
   event natively. Wan does not fit 16 GB (tested).


## What did not work (so it is not retried)

- Twitch timeline prompt (`v17a`, epic 0.65, "twitch, twitch, then twitch+rope ..."): the model
  still drew a thin drool string, no rhythmic twitches, glans static. The timeline wording alone
  does not produce the build-up.
- Dual-render material transfer (`v18` at seed 441 / epic 0.5 + `tools/dual_render.py` -> `v19`):
  render the same seed twice, keep the rope from the 0.8 pass, composite the 0.5 pass's texture
  through a white-pixel mask. The mask catches only part of the cum and the two passes drift, so
  the gain is marginal. The technique works mechanically, but the passes need to be closer.


- Starting with the cock in her mouth (`v3d_last`): emission has nowhere to go and renders as a
  drool string (`v8a`) or as streaks near the eyes (`v8b`, `v8c`).
- Qwen-Image-2.1 edits to add cum: identity is perfect but the cum is placed as thin strands
  high on the cheeks -> tears (`q1/t1`, `t2`).
- HMCumshot V1/V2, CUMOUF, MH3_Cum: static strand or a glass-clear cock artifact (`v11`).
- Asking for "thick white ropes" or "a lot of cum": opaque glue or cord.
- Wan 2.2/2.1 as a fallback: OOM on the 16 GB 7800 XT at model load even with `--lowvram`
  (16.8/17.2 GB VRAM); needs a 24 GB card.

## Limits / next

- The clip reads as "cum landing/landed on her open mouth", not as a visible projectile arc:
  H3 does not simulate the flight. For a true spurting shot the options are (a) a post-VFX cum
  layer composited onto a clean reaction clip, or (b) a video model with a cumshot LoRA that
  fits the hardware.
- Fluid wording is still the lever: milky + translucent + glossy, never "water" or "clear".

## Sound

The model audio is a scratch track: the strokes crunch, the slurp sounds like noodles, and the
events are not synced to the action. Do not present a clip as finished on the strength of its
sound; the findings and the next routes are in docs/SOUND.md.
