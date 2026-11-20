# Cum-shot video: what works, what does not (2026-11-20, session 4)

**State: the dynamics are close, the material is not, and the landing point is not controllable.**
The clips that come closest are the wide-gap pose with `epic_cumshots` at 0.5 and a "four or five
thin ropes, a second apart" prompt: the ropes shoot, the cadence reads, the glans stays bare, and
the run-off drips onto his thighs. Two things still fail: the material renders as a uniform opaque
white instead of a clear carrier with pearl-white clumps suspended in it, and the ropes are
strongly drawn towards the face's centre line, so they cross her nose whatever the prompt says.
Details, the exact prompt and the failed routes are below.

## The recipe (session 4)

```
model      minimax_h3_fl2va_pruned_int8_convrot + Pika Flex 6-step
second LoRA h3nsfw/epic_cumshots.safetensors at 0.5
size       768x1152, 124 frames, 24 fps (five spurt beats need the length)
workflow   workflows/wf_h3vid_i2v_lora.json
keyframe   a still where the tip sits a hand's width below her open mouth, slightly off-centre
           (gens/k04/k4_wide_clean - "wide-gap pose"); p1 also works, but its 1-inch gap makes
           the run-off fall back onto the glans
```

prompt:

```
integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed camera. A
young adult Asian woman in her mid-twenties with long black hair in pink-streaked twin tails and a
silver choker kneels between the viewer's legs. She holds his erect adult cock in her hand low
between his thighs, the tip a hand's width below her chin and a little to one side, her head tilted
down, her mouth wide open with her tongue out, her eyes rolled up to the lens, half-lidded, a light
blush. The semen is not a uniform opaque white and does not look like glue or paint: it is a mostly
clear, glossy liquid with pearl-white clumps suspended in it, so the thin parts are see-through and
wet and only the small clumps are opaque milk-white. His cock pulses again and again. With each
pulse a short thin rope of semen shoots from the tip and lands on her tongue and her lower lip.
There is no spray and nothing splatters across her face; most of it stays on her tongue and lower
lip, and only a few drops run off her chin and fall slowly onto his thighs. Four or five ropes in a
row, about a second apart, each one narrow; some pulses only add to what is already there. The
ropes do not cross her nose or her cheek. His glans stays bare and clean between pulses, no semen
sits on the tip; the tip is only wet. After the last rope the patches gather into small heavy beads
and begin to run slowly down her chin. She flinches at each spurt, then looks into the lens with
half-lidded eyes and a light blush, flushed. The camera does not move.

overall_soundscape: four or five soft wet spurts about a second apart, one low male groan, her
breath catching between them, quiet bedroom room tone. No music.

non_diegetic_music: N/A
```

## The wording ladder (this is the useful part)

The prompt nouns decide the *geometry*, and the LoRA decides the *event* and the *material*. Every
round below changed one thing; the results are owner-judged.

| wording | what the model drew |
|---|---|
| "a short translucent milky rope shoots from the tip up across her lips and cheek" (`v13`, `k01_control_rope08`) | **the event and the rope cadence are right** - but one fat two-cord rope, up across her nose, with a blob pooling on the glans. Owner: "close, but the volume per rope is exaggerated and the pool on the glans is completely unrealistic; more ropes with less volume each" |
| "a dense bead of milky semen swells out of the tip, breaks free, flicks up and lands" (`k01_bead*`, `k01_multi*`) | **kills the event.** No flight is generated; a pearl sits stuck on the glans (no LoRA) or a blob simply appears on her tongue (LoRA). Shape fixed, motion gone |
| "thin strands ... thin enough to break into droplets" at 0.5 (`v14a`) | nebulizer mist, no rope. The mist was the *breakup wording*, not just the strength |
| "four or five thin ropes in a row, about a second apart, each one narrow" + glans rule (`k05_ropes08/06/05`) | the owner's "closer to the dynamics we want"; 0.5 gives the thinnest ropes. Still: cum sticks to the face as a lump, impact scatter everywhere, glans still holds a blob |
| + "on impact each rope flattens and spreads into a thin patch instead of staying a lump" (`k06`) | the flatten-on-impact reading works; the splash was still excessive because the prompt asked for drops to *flick off* |
| + "no spray, nothing splatters across her face, only a few drops run off her chin and fall onto his thighs" (`k08`) | splash reduced, run-off kept, **glans clean on the wide keyframe** - and the ropes still cross her nose. At 0.35 the ropes get thin and stringy, at 0.6 they get fat again; 0.5 is the setting |
| same wording on the p1 keyframe (`k08_p1_05`) | the glans **pools a blob** again - with the tip an inch under her mouth the run-off lands back on it. The wide gap is what keeps the glans clean |
| head tilted back, mouth and tongue presented upward (`k09`) | does not help: the ropes become one long vertical cord from the tip up past her nose to her forehead |
| "a clear glossy liquid with pearl-white clumps suspended in it / not a uniform opaque white / does not look like glue or paint" (`k07`, `k08`) | **barely moves the material.** pearl, clear and 0.6 all render the same uniform white string |

Consequences:

- **The LoRA carries the material, and its material is glue.** Prompt wording cannot thin it
  without also removing the rope (that is the old `v13`/`v14a` tradeoff, now confirmed at three
  strengths). If the material has to change, it has to come from a keyframe, a different LoRA or a
  video model whose weights were trained on projected ropes - not from more adjectives.
- **The LoRA draws the spurt as a cord between the tip and a point on her face, not as a
  projectile.** That is why every round has some version of "a line from the tip": the shorter the
  gap, the more it reads as a spurt, and the landing point drifts up the centre line of her face no
  matter what the prompt says. The tether character is a property of the weights
  (`epic_cumshots`), and no wording tested here changes it.
- **Never use "bead", "blob", "ball", "glob", "separate droplet"** for the emission. Those words
  make the model draw a *static sphere*: on the glans without a LoRA, on the tongue with one. The
  event has to be a **rope**.
- **The wide gap is a composition fix, not a taste fix.** With the tip an inch below her open
  mouth the run-off has nowhere to go except back onto the glans, which is exactly the unrealistic
  pool the owner called out. Moving the tip a hand's width down and off-centre sends the drip past
  the cock onto his thighs, which the owner called realistic - and it is the only configuration in
  which the glans came out clean.

## Rules established (owner-approved, 2026-11-20 session 4)

1. **The glans stays bare.** No semen pooled, sitting or beaded on the tip; only a wet gloss. This
   is the first thing to check on a cum clip.
2. **One rope per pulse, four or five pulses, about a second apart.** Not one fat rope, and not a
   steady stream. A pulse may add nothing visible - that is realistic, the prompt should say so.
3. **Thin over thick.** 0.5 LoRA strength plus "narrow" wording. A fat single rope is a *variant*
   for people who want it (`cumshot_heavy`), not the default.
4. **Impact flattens, then runs.** A landed rope spreads into a thin patch instead of sitting as a
   lump, and the patches gather into heavy beads that run slowly. Splashing across the face is
   wrong; a few drops running off the chin and falling onto his thighs is right.
5. **Placement: tongue and lower lip only.** Never the nose, cheek or above - it reads as tears.
   Stating this in the prompt is not enough to enforce it (see the tether note below); check every
   clip for a deposit on the nose before calling it done.
6. **Material target: a clear carrier with pearl-white clumps suspended in it**, not a uniform
   opaque liquid. Still unsolved; see above.

## What the Gemini study contributed

`docs/GEMINI_BLOWJOB_ANALYSIS.md` §2.3 is the paragraph that unlocked the impact wording: ejaculate
in flight is a dense leading bolus with a thin tail, it *pancakes outward into a splash corona* on
contact, and the viscous tail then *collapses into raised beads that run downward under gravity*.
That is the owner's own note ("some shots splash like they're less viscous but then drip down
slowly") and it became rules 4 and 5. §2.3 also gives the 0.8-1.0 s spurt interval, which set the
cadence and therefore the 124-frame length.

Two things from the study did **not** transfer:

- the "bolus + thin tail" shape: both models turn "bolus/blob/rounded" into a sphere, so the
  in-flight shape has to be a rope;
- the §6 reference-clip descriptions are stylized 3D-anime aspirations (ropes across the forehead
  and bangs, multi-burst arcs over the face). Our photoreal pipeline reads anything high on the
  face as tears, so those placements stay out of scope.

## Failed routes (do not retry)

Earlier sessions:

- Starting with the cock in the mouth: nothing to emit, renders as drool.
- Cum high on the cheeks / near the eyes: tears.
- HMCumshot V1/V2, CUMOUF, MH3_Cum: static strand or a glass-clear cock artifact.
- "thick white ropes", "a lot of cum": opaque glue or a cord.
- Wan 2.2/2.1 on the 16 GB RX 7800 XT: OOM at load, needs 24 GB.
- Frame-by-frame or composited cum layers: owner verdict.
- Timeline-style twitch prompts (`v17a`): no twitches.

Session 4:

- **bead/blob wording** (`k01_bead05/08`, `k01_multi05/08`): no event, pearl on the glans or blob
  on the tongue (`gens/k01`).
- **No LoRA** (`k01_nolora_bead`): the base model puts a white sphere on the glans, then removes
  it. `v14b` (no LoRA, no shape words) gave almost no cum.
- **Starting from the approved landed still** as an i2v keyframe (`k01_p5key05/08`): the material
  is right from frame 0, but the existing gob grows into a thick column down onto the glans - the
  keyframe's own strand is the defect, and it only gets worse.
- **Qwen edit with "a thick spurt in mid-air"** (`p1_spurt_air`): the edit overshoots volume into a
  scoop-of-cream gob hanging to the glans. Qwen edit *does* work for the landed state
  (`p1_landed_edit`), not for in-flight volume.

## Keyframe rules (unchanged, plus one)

- The still is the recipe. Check the keyframe's anatomy before spending 145 s on a clip.
- The approved facial pose is `gallery/refs/cumshot/p1_pose.png` (owner-approved, `docs/FACIAL.md`).
- The wide-gap pose for cum clips is `gallery/refs/cumshot/k4_wide_clean.png` (a landed variant is
  `k4_wide_landed.png`). It is git-ignored like every reference; regenerate it with the pose block
  in `jobs/k04.jsonl` (Krea2, 896x1344, 6 steps) if the local copy is lost.
- **A landed last frame must be a Qwen-Image-2.1 edit of the first frame, not a new roll**
  (`p1_landed_edit` in `gens/k03e` is the good example: identical face, pose and cock, the tip left
  clean). `workflows/wf_h3vid_fl_lora.json` is the FL workflow with the cum LoRA wired in, for the
  route where the clip is forced to resolve into the landed state; it has not been run yet.

## Cost (measured)

| job | box | time |
|---|---|---|
| 768x1152 / 124 f, 6 steps, i2v + LoRA | ampere (3080) | ~145 s |
| 768x1152 / 81 f, 6 steps, i2v + LoRA | ampere | ~95 s |
| Krea2 still 896x1344, 6 steps | cutestation (5060) | ~17 s |
| Qwen-Image-2.1 edit 896x1344 | cutestation | ~110 s |

Judging a clip: `python tools/vsheet.py out.jpg gens/<round> --frames 8` puts every clip's frames
in rows under each other, which is how these rounds were read. Full-resolution crops matter - the
owner's "pooling on the glans" and "sticks to the face" are invisible at 200 px.

## Next

1. **Material, from somewhere other than the prompt**: an H3 cum LoRA trained on projected ropes at
   low strength on top of `epic_cumshots`, or Wan 2.2 on a 24 GB card. Prompting is exhausted;
   describe the material once and stop rewriting it.
2. **The tether is the thing to attack.** Every clip draws a cord from the tip to her face. Two
   untested levers: a *very* short gap (a keyframe where the glans nearly touches her tongue, so the
   cord has nowhere to be long), or a second LoRA that favours projected ropes over creampie ooze.
   A pose where the spurting cock is beside her mouth rather than under it is the other candidate -
   the cord would then have to travel sideways into her cheek, which the prompt can describe.
3. **FL route with the edited landed frame** (`wf_h3vid_fl_lora.json`, first = `p1_pose`, last =
   `p1_landed_edit`): forces the event to resolve into the approved material. Not yet run.
4. Once the material and the tether are settled: more angles (the Gemini study's §6.3 side profile
   and §6.4 low-angle are the obvious next poses), then sounds (`docs/SOUND.md` is independent).

## Round 4 artefacts

| round | jobs | what changed | kept |
|---|---|---|---|
| k01 | `jobs/k01.jsonl` | rope vs bead wording, LoRA 0.8/0.5, no LoRA, p5 keyframe | the control (`k01_control_rope08`) is the fat-rope reference |
| k02s | `jobs/k02_stills.jsonl` | keyframe shapes: gap, detached blob, bolus+tail, landed | `k2c` proved "bolus/blob" becomes a sphere |
| k03e | `jobs/k03_edit.jsonl` | Qwen edit to the landed state | `p1_landed_edit` (the good landed last frame) |
| k04 | `jobs/k04.jsonl` | wide-gap pose, clean + landed, in-flight gob | `k4_wide_clean` (best keyframe), `k4_wide_landed` |
| k05 | `jobs/k05.jsonl` | more/thinner ropes, glans rule, strength sweep | `k05_ropes05`, `k05_ropes_wide` |
| k06 | `jobs/k06.jsonl` | impact flattens, drops flick off, reseed | `k06_wide05` |
| k07 | `jobs/k07.jsonl` | material wording: pearl, clear, 0.6 | none - material did not move |
| k08 | `jobs/k08.jsonl` | no splatter, run-off only, strength 0.35/0.5/0.6 | **`k08_wide05`** - clean glans, thin ropes, some splash |
| k09 | `jobs/k09.jsonl`, `jobs/k09v.jsonl` | head-back pose | none - the cord got longer |

Renders are git-ignored; the jobs in `jobs/` are the recipe. Re-run any round with
`python tools/lab.py --wf wf_h3vid_i2v_lora.json --jobs jobs/k08.jsonl --box ampere --sub gl/k08 --out gens/k08`.

The `mk_*.py` generators in `tools/rounds/` hold the full reasoning for each round (what was
changed and why) and regenerate their `jobs/*.jsonl` byte-for-byte, so a round can be re-derived or
extended without guessing at the intent.
