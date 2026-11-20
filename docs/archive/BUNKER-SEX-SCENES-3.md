# Explicit scenes, session 3 - 2026-11-20 (owner verdicts and the facial recipe)

This session took the owner's verdicts on the first two sessions and closed the gaps they named:
the facial/cum-shot scene type, the anime motion recipe, and the model limits.

## 1. Owner verdicts that define the current canon

- **Anime stills (`gens/pb`)**: zero anatomical issues. Both cock styles are good. Preferred
  presentation: the light mosaic (`pb5_pov_mosaic`, or `pov_mosaic` in the old gen), or the
  half-foreskin cock; the fully retracted/cut one is also correct. **Keep all three styles.**
  The anime cum still (`pb7`) is on point - that recipe stands.
- **Photoreal BJ video**: `v3d_astro` (Astro NSFW 0.8) is the best BJ video so far - multiple
  strokes, no unrealistic deformation. `v3a` is close but slightly unnatural.
- **Paizuri**: `v3e` close to good, but the tongue reads split; fix the tongue or crop it.
- **Side view**: `v3g` would be natural if the saliva string did not look unnatural (same
  problem in the cum clip).
- **Anime video**: `v10b_pov_bob` is the best anime clip so far (motion decent, still slightly
  stiff, generic AI-render feel); `v10a_side_body` is rejected (cheek puffing does not match the
  action).
- **Frame-by-frame restyle**: rejected - unstable and not a good anime style. Closed.
- **Cum**: the old cum is "glue", too opaque and too explosive. The new direction below is
  approved as an improvement and the base of a recipe.

## 2. The facial / cum-shot recipe (approved pose)

Base pose: `gens/p3/p1_cock_out_cheek` and `p2_cock_out_face` (Krea 2 Turbo NSFW v10, 8 steps,
cfg 1.0, 896x1344). Cock pulled out and held an inch below/at her open mouth, tongue out, eyes
on the lens. Owner: good facial expressions, use this as the recipe for the scene type.

Cum landed still (`gens/p4/p4_cum_landed`, `p5_cum_landed_2`): add

```
Thick translucent milky semen is splattered across her open mouth, her lips and one cheek,
glossy and see-through so the skin shows through, a heavy strand hanging from her chin.
```

Placement rule: lips, tongue, chin, jaw. Cum high on the cheek or near the eye reads as tears
and kills the shot (three separate attempts: `v8b`, `v8c`, Qwen-edited targets).

Cum-shot clip (`gens/v13/v13a_p1`, `v13b_p2`): H3 i2v from the p1/p2 still, Pika Flex 6-step +
**`h3nsfw/epic_cumshots` at 0.8**, 768x1152, 124 f. Prompt: one slow pulse, one short
translucent milky rope across her lips and cheek, nothing foams, no spray; she flinches then
smiles. The cum arrives as a heavy translucent mass on the open mouth and hangs to the chin -
the best cum-shot look so far. It reads as landing/landed, not as a visible projectile: H3 does
not simulate the flight.

## 3. What failed on cum (do not repeat)

| attempt | result |
|---|---|
| start with cock in mouth (`v3d_last`), prompt emission | drool string from tip to lip (`v8a`) |
| first+last with a cum target edited from the start frame | cum appears near the eyes as tears (`v8b`, `v8c`) |
| Qwen-Image-2.1 edit to add cum | identity perfect, placement high on cheeks -> tears (`q1`) |
| HMCumshot V1/V2, CUMOUF, MH3_Cum | static strand or glass-clear cock artifact (`v11`) |
| `thick white ropes` / `a lot of cum` | opaque glue or a swinging cord |

## 3b. Material vs dynamics, and the twitch spec (owner-tested)

| attempt | material | dynamics |
|---|---|---|
| `v13` epic 0.8, "one short rope, no spray" | glue, too opaque | **good**: a rope, right timing, stable anatomy |
| `v14a` epic 0.5, "thin strands, droplets" | **more real** | nebulizer/mist, no rope |
| `v16a` epic 0.6, "single rope holds together" | still glue | still nebulizer |
| `v15a` first+last p1 -> p4, no LoRA | okay (p4 material) | cum fades in, no event |
| `v15b` Ref2VA p1 + p4 | okay, still stringy | cum appears, no event |
| `v14b` no LoRA | almost no cum | - |

The LoRA carries the event/rope but its learned material is glue; the prompt can thin the
material only by turning the event into mist. The still model has the approved material but no
motion.

Owner's twitch specification (for the next attempt): rhythmic **distinct** twitches, not a
vibration; a few twitches with no cum, then one spurt on almost every twitch; each spurt
synchronized to a twitch about a beat apart; the glans keeps its shape, the veins swell on each
pulse. Write it as a timeline, not as "pulses".

Next routes: (1) post-composite an AI-generated cum plate with a matte over a clean reaction
clip; (2) dense Krea2 keyframe sequence + interpolation; (3) 24 GB card + Wan 2.2 with a
cum-shot LoRA (does not fit 16 GB).

## 4. Anime video recipe (current best)

`gens/v10/v10b_pov_bob`: H3 i2v from the `pb3_pov_seal` keyframe, 768x1152, 124 f, no LoRA.
The lever is **whole-body motion in the prompt**, not just the mouth:

```
... She bobs her head up and down the shaft in a steady rhythm, her breasts bouncing with the
motion, her braid swinging, her eyes lifting to the camera between strokes. ... The camera
shakes very slightly with her motion.
```

Side view with the same idea (`v10a`) was rejected. The restyle route is closed.

## 5. Hardware

Wan 2.2/2.1 (the obvious next step for dynamic anime and better fluids) does not fit the 16 GB
7800 XT: OOM at model load with the Q5 GGUF high/low pair, and still OOM with `--lowvram`
(16.8/17.2 GB VRAM). It needs a 24 GB card, or a much smaller quant + a different loader path.
The box was returned to its normal `lame-comfyui` service state after the test.

## 6. Files

- `gens/p3` - approved facial pose stills; `gens/p4` - cum-landed stills
- `gens/v13` - cum-shot clips; `gens/v10` - anime motion tests
- `gens/pb` - anime stills (all three cock styles); `gens/v3`/`v3b` - photoreal motion canon
- recipes: `goonlab/notes/RECIPE-FACIAL.md`, `RECIPE-ANIME.md`, `RECIPE-E-GIRL.md`
