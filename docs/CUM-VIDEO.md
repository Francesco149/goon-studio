# Cum-shot video: the recipe, the variants, and what is still open

Last updated 2026-11-21 (session 5 close). The cum shot is no longer "unsolved" - it is a **recipe
plus an intensity dial plus variant presets**, all in `kit/presets.json`. It is **not finished**: the
owner's end-of-session verdict and the three concrete defects left are at the bottom, under *Open
defects*. Read that section first if you are picking this up.

> `cumshot_normal` no longer exists; it was split into the `cumshot_high` / `_medium` / `_low` dial.
> Wherever an older note says `cumshot_normal`, it means `cumshot_medium`.

## The default look (owner preference)

The default is the **"normal" tribute style**: medium amount, medium viscosity, distinct ropy
pulses, short parabolic arcs, raised beads where the ropes land, a few satellite drops, and a slow
drip that drags a thin translucent trail. Not the dense goopy pile, not the max-strength spray.

```
model      minimax_h3_fl2va_pruned_int8_convrot + Pika Flex 6-step
second LoRA h3nsfw/epic_cumshots.safetensors at 0.5-0.6
size       768x1152, 124 frames, 24 fps (three decaying pulses need ~5 s)
workflow   workflows/wf_h3vid_i2v_lora.json
keyframe   gallery/refs/cumshot/p1_pose.png (approved facial pose) or
           gallery/refs/cumshot/k4_wide_clean.png (wide gap: keeps the glans clean)
```

The exact prompt is not reproduced here because it is a living thing: it lives in
`kit/presets.json` as `cumshot_normal` and in `jobs/k14.jsonl` / `jobs/k15.jsonl` as rendered. What
matters is the set of laws it encodes, all of them learned from owner review:

- **Three decaying pulses**, the first the strongest, then weaker, then ooze. Never "four or five",
  never a continuous stream.
- **One single rope per pulse, out of the slit at the tip.** "One stream only, it never splits into
  two" - the split is the most obviously CG artefact.
- **It hits her face and stops there**, splashing a little on impact; a strong pulse splashes, a
  weak one just hits and stays. It must not arc above her head - see *Trajectory* below, this is the
  hardest thing to control.
- **A short rope**: the tip is an inch or two from her face, so the rope is an inch or two long.
- **The glans stays bare** where the amount allows it - see the dial below; maximum volume
  paints the head and no wording tested prevents it.
- **A ropy fluid, not a gel.** Glossy milky white, slightly translucent where it spreads thin. Not
  "dense", not "semi-solid", not wax (that is the `cumshot_goopy` extreme, which the owner judged
  completely unrealistic as a look to aim at).
- **The impact flattens and coalesces**; drops that touch merge into a pool.
- **The drip has a bulbous head dragging a thin translucent trail**, it does not slide as a rod.
- **The shaft kicks up on each pulse** and settles back; the veins stand out.
- **One fixed camera**, stated in the prompt.

## Trajectory: where the rope is allowed to end

The single hardest property, and the one that took three rounds:

| attempt | what happened |
|---|---|
| "its far end stops on her lower lip, at a slight angle, not over her head" (`k12`) | no effect on the normal recipe - the rope still sails past her nose |
| "does not shoot and does not spray, it travels only a few inches and drops onto her lower lip" (`k13`) | the travel *is* bounded, but the emission goes limp: it drops instead of hitting |
| "hits her face and stops there, splashing a little where it lands" (`k14`) | the impact and the face-splash appear, but the rope itself still overshoots past her mouth |
| "each rope is only an inch or two long ... hits her lips and chin hard" (`k15`) | the current attempt: bound the length rather than the endpoint |

The lesson so far: **velocity wording shortens the rope, endpoint wording does not, and the model
wants to draw a line that passes through the face rather than stopping on it.** Length, as a
physical quantity ("an inch or two"), is the untested-but-promising lever. A high-viscosity
description also shortens it, at the cost of the splash.

## The amount / twitch dial

The owner wants the same scene at several intensities, with **medium as the default**. The tiers are
presets, and they scale two axes together (amount per shot + twitch):

| tier | amount | twitch | glans | source |
|---|---|---|---|---|
| `cumshot_high` | full rope each pulse, the first splashes on her face | shaft kicks up on every pulse | **not clean** - the head gets a white patch | `k14` - the owner's maximum exaggeration standard |
| `cumshot_medium` (default) | shorter, thinner ropes, only the first splashes | small twitch, the shaft barely moves | **clean**, wet gloss only | `k16_medium` |
| `cumshot_low` | one short thin rope, the rest only oozes | no kick, only the veins swell | a small drop on the visible head | `k16_low` - **caveat: mists at this amount; do not ship as-is**, see *Open defects* 2 |

**The glans rule is a volume effect, not a wording effect** (tested in k17, compared at 1:1 in
`analysis/cum-ref/mat/glans_tiers.jpg`): the strong wording - "not a drop of semen sits on the head,
none pools on it, nothing runs back down onto it, no white on it at all" - does not stop the high or
the low tier from depositing on the head, while the medium tier comes out clean without any special
wording. So:

- the owner's "the cum must not pool on the glans" is **met by the medium tier** (and by anything
  that emits less), and the high tier carries a known tradeoff: ask for maximum volume and the head
  gets painted;
- for a low-strength shot that never reaches her face the residue sits at the opening - the owner
  expects it to run down the **far** side of the glans, away from the camera, and that side is not
  promptable either;
- if maximum-drama-with-a-clean-head is wanted, the right build is a **high twitch + medium amount**
  tier, which has not been rendered yet.

## The variant matrix (the presets)

The variants are not quality tiers, they are different fluids and different acts. Each was derived
from the viscosity spectrum in `gallery/refs/art-study/ANIMATION_DRAWING_GUIDE.md` §4.1 and the
reference clip the owner pointed at.

| preset | what it is | source |
|---|---|---|
| `cumshot_high` / `_medium` / `_low` | the intensity dial above (the one the owner asked for) | `k14`, `k16` |
| `cumshot_goopy` | semi-solid, like melted wax: no spray, no arc, heavy cords tumble out and pile on themselves, zero splash, stubby drips that barely run | `...1795216155`; **the owner judged this completely unrealistic as a target** - kept as an extreme variant, and useful because it is the only wording that reliably keeps the rope short |
| `cumshot_mouth` | one rope straight into the mouth, a swallow, then a glossy tongue coating and one thread between the lips; nothing outside the mouth | `...1795215084` (clean swallow) |
| `cumshot_softening` | messy version: some lands on the lips, she takes the softening cock back in and keeps sucking, cum and saliva thin and smear, threads stretch each time it slips out | `...1795215624` (the outdoor mouth ref) |

Shared mechanics, all variants (learned the hard way across k01-k17):

- **one stream per pulse, from the meatus.** The split into two cords is the most unrealistic
  artefact; describe the exit as the slit at the tip and "one stream only".
- **the glans stays bare** where the amount allows it (see the dial above - the high tier cannot
  avoid painting the head). Only a wet gloss on the tip. Check it at 1:1.
- **three pulses, decaying.** The first is the strongest, then weaker, then ooze. The owner's
  original complaint about the fat-rope version was volume, and about k07 that the frequency was
  too high.
- **the shaft kicks up on each pulse** (~5-12°) and settles back; the veins stand out.
- **impact flattens and coalesces**; drops that touch merge into a pool. No splash across the face.
- **the drip has a bulbous head dragging a thin translucent trail**, it does not slide as a uniform
  rod.
- **one fixed camera**, stated in the prompt.

## Prompt vocabulary: what each word does

The nouns decide the geometry; the LoRA decides the material. This table is the accumulated
evidence from ~40 owner-reviewed clips.

| wording | result |
|---|---|
| "a short translucent milky rope shoots from the tip up across her lips and cheek" (`v13`, `k01_control_rope08`) | event and cadence are there, but one fat two-cord rope, up across her nose, with a blob pooling on the glans |
| "a dense bead of milky semen swells out of the tip, breaks free, flicks up and lands" (`k01_bead*`, `k01_multi*`) | **kills the event.** No flight: a pearl stuck on the glans (no LoRA) or a blob on the tongue (LoRA) |
| "thin strands ... thin enough to break into droplets" at 0.5 (`v14a`) | nebulizer mist. The mist was the *breakup wording*, not the strength |
| "four or five thin ropes in a row, about a second apart" + the glans rule (`k05`) | the owner's "closer to the dynamics we want"; 0.5 gives the thinnest ropes |
| "on impact each rope flattens and spreads instead of staying a lump" (`k06`) | the flatten-on-impact reading works; splash was still excessive |
| "no spray, nothing splatters across her face, only a few drops run off her chin" (`k08`) | splash reduced, run-off kept, **glans clean on the wide keyframe** |
| "a clear glossy liquid with pearl-white clumps suspended in it" + "milky depth, cream-white core, translucent faintly amber edges" (`k07`, `k10`) | **the owner's pick for the optics.** My earlier read that "the material did not move" was wrong: at 200 px the ropes look alike, at 1:1 the pearl/clear wording gives the fluid its depth. Judge material at full resolution |
| "three pulses and no more ... one single narrow rope out of the slit ... one stream only, it never splits into two" (`k10`) | the single-stream fix; the split into two cords is gone |
| "extremely dense and semi-solid, thick like melted wax ... no splash at all, piling up on itself" (`k11_goopy`) | the goopy extreme: it renders, and it is the only wording that reliably keeps the ropes short - but the owner judged it completely unrealistic as a look to aim at. Kept as `cumshot_goopy` |
| "shoots straight into her face ... hits her face and stops there, splashing a little" (`k14`) | the face-splash reads as impact, and the material is one notch thinner as asked; the rope itself still overshoots past her mouth |
| head tilted back, mouth and tongue presented upward (`k09`) | does not fix placement; the cord simply gets longer |

## Reference reality check (important)

The owner's photoreal references show that a **vertical rope joining the tip to her face is real**,
not a model artefact: in the goopy ref the ejaculate leaves the tip and lands on her nose/forehead
as a connected, near-vertical rope that then heaps up where it hits. Our pipeline reads a *thin*
strand in that position as tears, but a rope with volume reads as cum. So:

- do **not** treat "a cord between the tip and her face" as automatically wrong - it is how a
  close-range spurt actually looks;
- what was wrong in our early clips was the *count* (two cords), the *thinness* (a wire rather than
  a rope), and the *stickiness* (a static line instead of a heap that grows);
- the "low amount" refs deliver into the mouth instead, which avoids the face entirely, and are the
  source of the two mouth presets.

## Failed routes (do not retry)

- Starting with the cock in the mouth for a facial: nothing to emit, renders as drool (`v3d`, `v8a`).
- Cum high on the cheeks near the eyes as *thin strands*: tears (`v8b`, `v8c`, `q1/t1`, `t2`).
- HMCumshot V1/V2, CUMOUF, MH3_Cum: static strand or a glass-clear cock artifact.
- Timeline-style twitch prompts (`v17a`): no twitches. The twitch has to be described as a
  mechanical consequence (shaft kicks up, veins swell) or not at all.
- No LoRA (`v14b`, `k01_nolora_bead`): almost no cum, or a white sphere on the glans.
- Starting from a landed still with a strand in it as the i2v keyframe (`k01_p5key*`): the existing
  gob grows a thick column down onto the glans.
- Qwen edit with "a thick spurt in mid-air" (`p1_spurt_air`): overshoots into a scoop-of-cream gob.
  Qwen edit is right for the *landed* state (`p1_landed_edit`), not for in-flight volume.
- Wan 2.2/2.1 on the 16 GB RX 7800 XT: OOM at load, needs 24 GB.
- Frame-by-frame or composited cum layers: owner verdict.

## Keyframe rules

- The still is the recipe. Check the keyframe's anatomy before spending 145 s on a clip.
- `gallery/refs/cumshot/p1_pose.png` - the approved facial pose (`docs/FACIAL.md`).
- `gallery/refs/cumshot/k4_wide_clean.png` - the wide-gap pose; the only configuration so far that
  reliably keeps the glans clean, because the run-off falls past the cock onto his thighs. Landed
  variant: `k4_wide_landed.png`. Regenerate both with `jobs/k04.jsonl` (Krea2, 896x1344, 6 steps).
- **A landed last frame must be a Qwen-Image-2.1 edit of the first frame, not a new roll**
  (`p1_landed_edit`). `workflows/wf_h3vid_fl_lora.json` is the FL workflow with the cum LoRA wired
  in, for the route where a clip is forced to resolve into the landed state; not run yet.

## Cost (measured)

| job | box | time |
|---|---|---|
| 768x1152 / 124 f, 6 steps, i2v + LoRA | ampere (3080) | ~145 s |
| 768x1152 / 81 f, 6 steps, i2v + LoRA | ampere | ~95 s |
| Krea2 still 896x1344, 6 steps | cutestation (5060) | ~17 s |
| Qwen-Image-2.1 edit 896x1344 | cutestation | ~110 s |

Judging: `python tools/vsheet.py out.jpg gens/<round> --frames 8` for motion, and **full-resolution
crops for the material** - the owner's "pooling on the glans", "sticks to the face" and the whole
optics question are invisible at 200 px. That mistake cost a round.

## Open defects at the close of session 5 (owner verdict, 2026-11-21)

Verbatim shape of the verdict: *"its still not quite there - the low strength does the nebulizer
thing, there's still some unnatural splitting, and it feels like the in-flight cum is way more than
what lands. To be iterated on in future sessions."*

Three defects, in the order they are worth attacking:

1. **MASS CONSERVATION - the biggest one, and new.** The rope looks like far more fluid than ends up
   on her. The LoRA draws an impressive in-flight body and then the deposit is a thin smudge, which
   reads as fake no matter how good either half is. Nothing in k01-k17 addressed it, so there is no
   prompt evidence yet. Candidate levers: prompt the deposit as the same amount that left
   ("most of it lands on her face and stays there", "a heavy patch forms where the first rope
   hits"), or drive the volume *from the landing side* - decide the face deposit first and make the
   rope only as thick as that deposit implies. Worth measuring: compare the apparent width of the
   rope mid-flight with the area of the landed patch across a clip, and treat a ratio above ~2 as a
   fail. This is a taste-rule the owner stated and the pipeline currently violates.
2. **NEBULIZER MIST AT LOW AMOUNT.** The low tier (`cumshot_low`) reproduces the old `v14a`
   failure: at low amount/strength the emission atomises into mist instead of staying a rope. The
   low tier is therefore **not shippable as labelled** - either it needs a rope-preserving wording
   that survives low volume, or the low tier should be built as "fewer pulses at medium amount"
   rather than "less fluid per pulse". The latter is probably right, because of defect 3.
3. **UNNATURAL SPLITTING** still appears occasionally even though the prompt says "one stream only,
   it never splits into two" and k10 removed the systematic version. Look for it as a *fork near
   the tip* (two cords leaving the glans) rather than one cord breaking into droplets mid-flight -
   the second is physically fine.

And a standing note on the glans: the rule is met by `cumshot_medium` and below, but `cumshot_high`
still paints the head, and no wording tested fixes it (see the dial section). The unrendered fix is
a **high twitch + medium amount** tier.

## Next

1. **Mass conservation** (defect 1 above). This is the one that decides whether the cum shot reads
   as real, and it has had no work yet.
2. Rebuild the low tier around *fewer pulses at medium amount* instead of less fluid, which should
   also fix the mist (defect 2).
3. The **high twitch + medium amount** tier: maximum drama with a clean glans and no extra volume.
4. The ropes are still **smooth uniform rods**; the refs are lumpy, bulbous where they land and
   thinner where they stretch. "Uneven and lumpy, bulbous where it lands" is written into the
   prompts but has not produced lumpiness.
5. Then the blowjob/pose work the art study enables: §1 lip curl and cheek hollow, §1.2 the glans
   compress and coronal snap, §3 the paizuri and reverse cowgirl kinematics, §4.1 the upward gaze.
   The new study's §8 (vein turgor, meatal flare, recoil, post-ejaculatory tremor) is the source for
   the micro-movement pass.

## Round artefacts

| round | jobs | what changed | outcome |
|---|---|---|---|
| k01 | `jobs/k01.jsonl` | rope vs bead wording, 0.8/0.5, no LoRA, p5 keyframe | rope wins, bead kills the event |
| k02s | `jobs/k02_stills.jsonl` | keyframe shapes | "bolus/blob" becomes a sphere |
| k03e | `jobs/k03_edit.jsonl` | Qwen edit to the landed state | `p1_landed_edit` (the good landed last frame) |
| k04 | `jobs/k04.jsonl` | wide-gap pose, clean + landed, in-flight gob | `k4_wide_clean` (the clean-glans keyframe) |
| k05 | `jobs/k05.jsonl` | more/thinner ropes, glans rule, strength sweep | 0.5 = thinnest ropes |
| k06 | `jobs/k06.jsonl` | impact flattens, drops flick off, reseed | flatten works, splash too much |
| k07 | `jobs/k07.jsonl` | material wording: pearl, clear, 0.6 | **the owner's pick for the optics** |
| k08 | `jobs/k08.jsonl` | no splatter, run-off only, 0.35/0.5/0.6 | `k08_wide05`: clean glans, ropes |
| k09 | `jobs/k09.jsonl`, `jobs/k09v.jsonl` | head-back pose | no gain, the cord got longer |
| k10 | `jobs/k10.jsonl` | three decaying pulses, one stream, small amount | the `cumshot_normal` recipe |
| k11 | `jobs/k11.jsonl` | goopy / mouth / softening variants | the variant presets |
| k12 | `jobs/k12.jsonl` | endpoint instruction, angle, lumpy ropes | no effect on the normal recipe |
| k13 | `jobs/k13.jsonl` | "does not shoot, travels a few inches" | bounds the travel but goes limp |
| k14 | `jobs/k14.jsonl` | straight into her face + a little splash, thinner fluid | **the owner's maximum exaggeration standard** |
| k15 | `jobs/k15.jsonl` | explicit length bound ("an inch or two") | shorter, but not solved |
| k16 | `jobs/k16.jsonl` | the medium / low tiers | the default dial; medium is the one with a clean glans |
| k17 | `jobs/k17.jsonl` | stronger glans wording on high and low | no effect - the residue tracks volume, not wording |

Renders are git-ignored; the jobs are the recipe. Re-run any round with
`python tools/lab.py --wf wf_h3vid_i2v_lora.json --jobs jobs/k10.jsonl --box ampere --sub gl/k10 --out gens/k10`.
The `mk_*.py` generators in `tools/rounds/` carry the reasoning for each round and regenerate their
`jobs/*.jsonl`.
