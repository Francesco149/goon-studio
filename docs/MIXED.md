# Mixed reality: a real cock in an anime picture (2026-11-21)

Goal: the "anime tribute" look - a photoreal real cock in an otherwise flat 2D anime picture,
with the anime girl taking it. The real-cock source is the owner's sharp still
`gallery/refs/custom-cock/p03ryyxaprvh1.jpg` (2256x3295). The cock is cut by the left frame edge,
so the cutout carries a straight edge on that side; place it toward the frame edge or let the
girl's body cover it.

**Owner verdicts on the first routes (do not repeat):**
- Qwen one-image edit of the isolated cock (a45/a47): the cock is the real one, but the model
  draws the girl *around* it and her lips end up on the tip - she is not sucking it.
- Hand-compositing the BiRefNet cutout over the drawn cock: rejected. It reads as a cock PNG
  slapped on top of the anime, whatever the grading (`analysis/mixed/s1_mix_v1..v7` are the dead
  end; do not continue them).
- Qwen two-image swap: rejected, it regenerates the cock.
- Editing the real photo itself ("keep the penis, replace the screen"): keeps the screen girl;
  proof of method only.

## Isolation: BiRefNet, cropped to the cock

ComfyUI's core background-removal nodes work:

- model: `Comfy-Org/BiRefNet` -> `background_removal/birefnet.safetensors` (424 MB,
  https://huggingface.co/Comfy-Org/BiRefNet), into `ComfyUI/models/background_removal/`.
- `workflows/wf_bgremove.json`: LoadImage -> LoadBackgroundRemovalModel -> RemoveBackground ->
  MaskToImage -> SaveImage. Run with
  `python tools/lab.py --wf wf_bgremove.json --jobs jobs/a43_bgremove.jsonl --box local --sub gl/mask --out gens/mask`.

**Crop first.** On the full frame BiRefNet picks the anime figure printed on the screen as the
salient object. On the crop `(0, 650, 950, 2950)` it picks the cock cleanly. The cutout on the
dark canvas is `analysis/mixed/mix_canvas2.png` (896x1344, the cock 1150 px tall).

## The complete recipe: head-out take-in (shows the real glans, no invention)

The reveal was the unsolved half because the glans is hidden at frame 0 and the video model
invents it. The fix is to put the glans **in frame 0**: start on a head-out seal, then have her
take it in. The model never has to invent the hidden part; it sees it, then hides it.

1. **Head-out seal still (Anima):** `jobs/a74_headout.jsonl` / `jobs/a77_k9_headout.jsonl`, prompt
   "(lips sealed around penis:1.5), (glans outside mouth:1.4), (penis head out of her mouth:1.3),
   the swollen glans is outside above her lips, her lips are sealed around the shaft just below
   the glans, cheeks hollow". Pick a frame that actually does it (`gens/a74/p3`, `gens/a77/q3`;
   2/2 in that round). This is a pose the anime model can draw, unlike the reveal.
2. **Fill the real cock (head-out mask).** Two mask lobes, the glans above the lip line and the
   shaft below, with the lip band black between them: `analysis/mixed/p3_headout_mask.png` /
   `analysis/mixed/q3_headout_mask.png`. H3-Image 2ref inpaint
   (`wf_h3img_2ref_inpaint`, 0.92) fills the real glans and shaft; the lips stay in front of the
   join. Results: `gens/a75/headout_fill` (dim pink), `gens/a78/q3_fill` (warm). 2/2.
3. **i2v take-in:** from that still, 124 f 768x1152, prompt "she takes it into her mouth: her lips
   stay sealed and slide over the glans, the glans goes inside and is hidden, the shaft slides in
   until deep, then she holds and sucks; the cock is the real one from the first frame; lips a
   thin seal, cheeks hollow, never puffed; camera fixed." The glans is real and visible at frame
   0, so it is anchored; then it is inside and no reveal is needed.
   Results: `gens/a83/v10_takein_dark` (dim pink, `headout_fill`) and `v10_takein_warm` (warm,
   `q3_fill`); the 49 f versions are `gens/a82`. 2/2 at 49 f and 2/2 at 124 f.

Pass criteria: frame 0 shows the real glans above the lips with the lips sealed around the shaft;
the take-in hides it; after that the mouth is a thin seal, cheeks hollow, no puff; the cock is the
same real one throughout. The face/scene are the head-out still's own roll, so there is no morph
and no identity blend. This is the recipe to use when the glans must be seen.



## The deep-seal variant: golden k9 base + fill + i2v

The still base matters more than the wording. A fresh Anima "seal" still (j2_b, h1, h2, s1) is
not the best BJ mouth, and whatever it gets wrong the video carries. Use a frame from the
**golden k9 clip** instead - the best non-mixed BJ, fixed camera, thin seal, hollow cheeks:

1. **Base frame:** `analysis/mixed/golden_k9_f00.png` (the deep-stroke frame of
   `gens/a21/k9_anime_suction_perf`). The camera and the cock are fixed in that clip, so one mask
   fits its frames.
2. **Mask:** `analysis/mixed/k9_cock_mask.png` - the drawn cock only, under the lip line.
3. **Fill:** `jobs/a70_k9_fill.jsonl` -> `gens/a70/k9_fill_00001_.png`. H3-Image 2ref inpaint
   (`wf_h3img_2ref_inpaint`, 0.92) puts the real cock in the mask; the golden k9 mouth, cheeks
   and face are untouched. This is the best still so far: the mouth is the best BJ gen, and the
   cock is real.
4. **Suction clip:** i2v from the fill (`jobs/a73`, `v7_seal`, 124 f 768x1152): "she sucks hard
   and slow, cheeks hollow and pull in, lips grip and drag, the glans stays inside". The golden
   mouth holds, the cheeks hollow, the glans never comes out, so there is nothing to invent.
   This is the **proven** half of the recipe (`v6_seal` is the 49 f version).
5. **Reveal via Ref2VA (optional; the take-in above is the way to show the glans):** Ref2VA from
   the fill + the same real cock (`v7_reveal`) shows a real glans, but at the reveal her lips
   close *behind* the head - the cock sits on her lips rather than staying sealed around the
   shaft. The golden k9 does not contain a head-out seal, so the model has no pose to copy; the
   head-out take-in recipe above is why we no longer need this route.

The k9 base is why `v7_seal` reads like the non-mixed BJs and the j2_b/h1/h2 bases did not: the
mouth and cheeks are already the approved ones before the real cock is filled in.



### How the fill works

The mixed-gen model is **H3-Image** (the Love Live research: H3 edits keep a 2D girl and draw a
photoreal element around her). The trick is to start from an anime frame whose mouth is already
the approved golden seal, and let H3 fill *only the cock* with the real photo, so the lips cannot
be redrawn into a pucker or puff.

1. **Golden base.** The k9 frame (above) is the best. The earlier base was Anima's
   `gens/a11/j2_suction_seal_b_00001_.png`; it works but its mouth is not k9 level.
2. **Mask the drawn cock only.** White over the drawn cock from just under the lip line down to
   the pubic hair; black everywhere else (lips included). The k9 mask is
   `analysis/mixed/k9_cock_mask.png`; the j2_b one is `analysis/mixed/j2b_cock_mask.png`. The lips
   are outside the mask, so the sampler keeps them exactly; only the cock is generated.
3. **H3-Image 2ref + mask** (`workflows/wf_h3img_2ref_inpaint.json`): Picture 1 = the golden
   frame, Picture 2 = the real cock on `mix_canvas2.png`, 896x1344, 6 steps, cfg 1, denoise
   **0.92** (1.0 opens the lips and shows the glans - a kiss, not a seal).
   Jobs: `jobs/a70_k9_fill.jsonl` (k9) and `jobs/a55_h3_inpaint.jsonl` (j2_b).
4. **Prompt** (see the jobs): fill the masked area with the real penis from Picture 2 exactly
   (photoreal skin texture, veins, colour, shape, warm light), and state that every pixel outside
   the mask stays: her lips a thin tight ring in front of the shaft, upper lip one clean thin
   line, cheeks hollow, no pucker/pout/puff, the glans hidden inside her mouth.

**Best still:** `gens/a70/k9_fill_00001_.png` (golden k9 mouth + real cock). The earlier
`gens/a55/inpaint_a_00001_.png` (j2_b mouth) is the same pipeline on a weaker base;
`inpaint_b` (denoise 1.0) shows the head at the lips; keep 0.92.

## Why not H3 two-reference full generation

`workflows/wf_h3img_2ref.json` (Picture 1 scene, Picture 2 real cock, no mask) also produces a
coherent mixed image (`gens/a50/h3a_swap`, `h3c_rawref`; `gens/a52/j2b_tight`, `s2_tight`,
`s4_tight`), and the raw-photo reference is the cleanest of that route. But the model redraws the
mouth around the real cock: a thick pursed lip ring (`j2b_tight`), a pout (`s2_tight`) or puffed
cheeks (`s4_tight`), and `h3c` leaves the head on the lips. Use the masked fill when the seal is
the point; the full generation is only for a scene where the mouth shape does not matter.

## Video

H3 FL2VA i2v (`workflows/wf_h3vid_i2v.json`) from the masked-fill still, 768x1152, 124 f, 24 fps,
6-step Pika. The model wants to pucker/puff the lips as it animates, so the prompt has to repeat
the shape: thin flat sealed ring, cheeks hollow, **never purse, pucker or puff**, the motion is
her head and neck, the cock stays photoreal and still. The first 49-frame tests (`gens/a54`,
`gens/a56`) pouted or opened; the 124-frame pair from `inpaint_a` is the first that holds the
golden mouth:

- **`gens/a57/v3_seal` - the dynamic one.** One slow stroke: her head rises until the shaft comes
  out to the head at her lips, holds, then sinks deep again. The lips stay a thin ring; on the
  upstroke the real glans is revealed outside her lips (no pucker, she is still sealed around the
  shaft). This is the clip that shows the real cock and the act.
- **`gens/a57/v3_slow` - the tight one.** A small slow bob, the seal held throughout, a little
  saliva and two thin strings at the corner. Almost no lip movement; the closest to the golden
  k9 mouth.
- The audio is the model's scratch track; never claim it is good (`docs/SOUND.md`).
- `wf_h3vid_i2v_fl.json` (first+last pair with the thin seal at both ends) is the next route if
  the deepest point of a longer stroke still puffs.

### Video: reanchor what frame 0 does not show

The i2v clips only know what is visible in the first frame. In `v3_seal` the glans is hidden in
her mouth at frame 0 and appears on the upstroke - the video model **invented** that glans, and it
is the wrong shape. The same will happen to any hand, prop, second person or cum that is not on
screen at frame 0. This is now a general rule in `AGENTS.md` section 4.

Tests (2026-11-21, session 6):

- **Ref2VA** (`wf_h3vid_ref2va6.json`, ref0 = the `inpaint_a` seal still, ref1 = the real cock,
  or a glans close-up): the scene is preserved and the glans that appears is a real photographed
  glans (a60/r1, r3), but the mouth opens into a pout at the pull-back and the suction still does
  not read. It reanchors the cock; it does not fix the mouth.
- **First+last** (`wf_h3vid_i2v_fl.json`, first = `inpaint_a` deep, last = `inpaint_b` at the
  head): at 49 f / 6 steps the model did not follow the last frame; it invented a gold-toned cock
  and puffed the cheeks (a61). The workflow's own note says one stroke that returns to the same
  pose - deep-to-head may be too large a transition for it. Do not trust the last frame to
  anchor the object at this length.
- **The practical rule for this act:** if the glans stays hidden inside her mouth for the whole
  clip (the `v3_slow` tight-seal stroke), there is nothing for the video model to invent. If it
  is going to be revealed, reanchor it with Ref2VA - or keep it hidden. The suction expression
  must also be in the first frame: the video model does not invent hollow cheeks.

The next still round (`jobs/a62_suction_seal.jsonl`) is a dark deep-seal base with the cheek tags
pushed (cheeks hollowed/sucked in/sunken 1.5-1.6) so the first frame reads as suction before any
video is made.

### Suction motion

The mouth shape was only half the problem; the other half is that the first frame's expression
was neutral. The fix is to make the *suction itself* the motion, with the glans kept inside:

- `gens/a68/s1_hollow` and `s2_drag` (49 f) and the 124 f finals `gens/a69/v5_suction` and
  **`gens/a69/v5_pull`**. The prompt: "she sucks hard and slow, her cheeks hollow and pull in
  sharply, the skin under her cheekbones dents inward, her lips grip the shaft and drag it, the
  seal holds; the glans stays inside her mouth and never comes out." `v5_pull` is two long
  pulls with the cheeks hollowing then relaxing - the best "applying suction" read so far.
  `v5_suction` is a held suck; stronger, but the cheeks end gaunt.
- Because the glans never comes out, there is nothing for the video model to invent. This is the
  cheap side of the reanchor rule: keep the unseen thing unseen.
- Strong-cheek Anima stills (`a62`, `a67`) put the drawn head *at* the lips, so the masked fill
  shows the real head outside the mouth; they are not deep-seal bases. The `j2_b` still remains
  the only base that fills as a shaft-only seal. A cheek-only H3 mask (`a66`) did not hollow the
  cheeks; H3 ignored the expression inside the small mask.

## Open

- The deep-seal fill hides the glans. A "head out" piece needs a shallow still + its own mask
  (or a mouth-level seal) - do not reuse the deep mask.
- The dark `s1_dark` base has her lips at the tip of the drawn head, so the fill puts the real
  glans outside the mouth (`gens/a58`, `gens/a59`) and the mask edge shows. It needs a dark base
  generated with the j2_b deep prompt ("his cock deep in her mouth, her lips around the middle of
  his shaft"), not the s1 prompt; then the same masked fill.
- The i2v still puffs at the deepest point of a long stroke. Next: a first+last frame pair with
  the thin seal at both ends (`wf_h3vid_i2v_fl.json`), or a shorter stroke.
- The mask is traced for the base still. A SAM point mask on the drawn cock would automate it;
  a mask is a generation constraint, not a composite - the output is one H3 image.
- The real cock on the dark canvas keeps its own warm screen light; H3 grades it toward the
  scene. If it comes out too dark, lift the reference canvas before H3.
