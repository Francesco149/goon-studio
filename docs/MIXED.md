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

## The method that works: golden anime seal + H3-Image two-reference masked fill

The mixed-gen model is **H3-Image** (the Love Live research: H3 edits keep a 2D girl and draw a
photoreal element around her). The trick is to start from an anime still whose mouth is already
the approved golden seal, and let H3 fill *only the cock* with the real photo, so the lips cannot
be redrawn into a pucker or puff.

1. **Golden base.** Anima's seal still `gens/a11/j2_suction_seal_b_00001_.png` (or a new
   `wf_anima2_sig` still with the same prompt). The mouth must already be the approved one: a
   thin flat ring around the shaft, cheeks hollow, no pursed lips, no puffed cheeks. The k9 clip
   (`gens/a21/k9_anime_suction_perf`) is the motion reference for that mouth.
2. **Mask the drawn cock only.** White over the drawn cock from just under the lip line down to
   the pubic hair; black everywhere else (lips included). The mask used for j2_b is
   `analysis/mixed/j2b_cock_mask.png` (896x1344). The lips are outside the mask, so the sampler
   keeps them exactly; only the cock is generated.
3. **H3-Image 2ref + mask** (`workflows/wf_h3img_2ref_inpaint.json`): Picture 1 = the golden
   still, Picture 2 = the real cock on `mix_canvas2.png`, 896x1344, 6 steps, cfg 1, denoise
   **0.92** (1.0 opens the lips and shows the glans - a kiss, not a seal).
   Job: `jobs/a55_h3_inpaint.jsonl`; run
   `python tools/lab.py --wf wf_h3img_2ref_inpaint.json --jobs jobs/a55_h3_inpaint.jsonl --box ampere --sub gl/a55 --out gens/a55`.
4. **Prompt** (see the job): fill the masked area with the real penis from Picture 2 exactly
   (photoreal skin texture, veins, colour, shape, warm light), and state that every pixel outside
   the mask stays: her lips a thin tight ring in front of the shaft, upper lip one clean thin
   line, cheeks hollow, no pucker/pout/puff, the glans hidden inside her mouth.

**Best still:** `gens/a55/inpaint_a_00001_.png` - golden mouth, real cock, the seal holds, the
glans is inside. `inpaint_b` (denoise 1.0) shows the head at the lips; keep 0.92.

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
