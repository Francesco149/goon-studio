# Cum-shot video: what works, what does not (as of 2026-11-20)

The still side has the approved pose and material (`docs/FACIAL.md`), but the landed shape still
reads as a string; the video side is the bigger open problem: the event and the material have not
been achieved in the same clip.

## The tradeoff (owner-tested)

| clip | material | dynamics |
|---|---|---|
| `v13` (p1 pose, epic_cumshots 0.8, "one short rope, no spray") | glue, too opaque | **good**: a rope, right timing, stable anatomy |
| `v14a` (epic 0.5, "thin strands, droplets") | **more real** | nebulizer mist, no rope |
| `v16a` (epic 0.6, "single rope holds together") | still glue | still nebulizer |
| `v15a` (first+last p1 -> p4, no LoRA) | okay (p4 material) | cum fades in, no event |
| `v15b` (Ref2VA p1 + p4) | okay, stringy | cum appears, no event |
| `v14b` (no LoRA) | almost no cum | - |
| `v17a` (twitch timeline prompt, epic 0.65) | thin drool | no twitches, no spurts |
| `v18`/`v19` (dual render + mask composite) | marginal | keeps v13's rope |

On cutestation the recipe costs **111 s** for 512x768 / 85 f at 6 steps and **82 s** at 4;
768x1152 / 124 f is **372 s** at 6 and **267 s** at 4. The LoRA adds about 3%. Preview at 4
steps with the final seed, then refine at 6. Full numbers: `docs/PERFORMANCE-8GB.md`.

The LoRA carries the event/rope but its learned cum is glue. Thinning the material in the prompt
turns the event into mist. The still model (Krea2) has the approved material but no motion.
Compositing the two was rejected by the owner: the cum would not land and drip organically.

## Landed vs in-flight (owner note, 2026-11-20)

Long thin strings are an **in-flight / impact** look: cum only looks like a string while it is
shooting out of the cock. Once it lands it should pool or blob on the lips/chin and drip down
organically in short heavy runs. The current stills and clips often keep the string hanging from
the tip after it has "landed", which reads as a fake cum string. For landed shots prompt for
`thick milky droplets pooling on her lower lip, a slow heavy drip from the chin, no strand from
the tip` and keep `translucent milky, glossy` for the material. This is an open prompt/material
problem, not a hardware one.

## Keyframe inheritance (benchmark note, 2026-11-20)

The 8 GB H3 video benchmark used a keyframe whose cock had a pointed/deformed glans, and every
clip made from that picture inherited the bad anatomy - the video model preserves the keyframe.
The prompt's `detailed penis shaft, veins, erection` did not fix it. This is not a performance
finding, but it is a reminder that the still is the recipe: check the keyframe anatomy before
spending 2-6 minutes on the clip.

## Owner's twitch specification (the build-up)

- rhythmic, **distinct** twitches, not a vibration;
- a few twitches with no cum first, then one spurt on almost every twitch;
- each spurt synchronized to a twitch, about a beat apart;
- the glans keeps its shape (no stretching when sucked), the veins swell on each pulse;
- the cum must actually leave the tip and drip off, not stretch as an endless blob.

A prompt written as a timeline ("twitch, twitch, then twitch+rope, pause, twitch+rope") did not
produce this in `v17a`.

## What has been ruled out

- Starting with the cock in the mouth: the emission has nowhere to go (drool string).
- Cum high on the cheeks / near the eyes: reads as tears.
- HMCumshot V1/V2, CUMOUF, MH3_Cum: static strand or a glass-clear cock artifact.
- "thick white ropes", "a lot of cum": opaque glue or a cord.
- Wan 2.2/2.1 on the 16 GB RX 7800 XT: OOM at model load, even with `--lowvram` (16.8/17.2 GB
  VRAM). Needs a 24 GB card or a much smaller quant.

## Next routes

1. A video model with a cum-shot LoRA that fits 10-16 GB (Wan 2.2 at a smaller quant on a 24 GB
   card is the obvious candidate). This is the only route that can generate the event natively.
2. A different H3 cum LoRA, if one appears that is trained on projected ropes rather than
   creampies.
3. Do not use a frame-by-frame or composited cum layer: owner verdict.

Until then, the best honest pair is: `v13` for the event (dynamics), `p4` for the material
(still), and `docs/FACIAL.md` records why they are separate.
