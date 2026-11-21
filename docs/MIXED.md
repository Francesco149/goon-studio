# Mixed reality: a real cock in an anime picture (2026-11-21)

Goal: the "anime tribute" look - a photoreal real cock in an otherwise flat 2D anime picture, with
the anime girl taking it. The real-cock references are the owner's tribute clips in
`gallery/refs/art-study/refs/` (git-ignored); never commit them.

## The source

The owner's sharp still `gallery/refs/custom-cock/p03ryyxaprvh1.jpg` (2256x3295). The cock is cut by
the left frame edge, so the cutout carries a straight edge on that side; place it toward the frame
edge or let the girl's body cover it.

## Isolation: BiRefNet, cropped to the cock

ComfyUI's core background-removal nodes work:

- model: `Comfy-Org/BiRefNet` -> `background_removal/birefnet.safetensors` (424 MB,
  https://huggingface.co/Comfy-Org/BiRefNet), into `ComfyUI/models/background_removal/`
  (the engine's own `models` dir, not the `F:/LLStudioTest/models` extra path - that extra path
  does not map `background_removal`).
- `workflows/wf_bgremove.json`: LoadImage -> LoadBackgroundRemovalModel -> RemoveBackground ->
  MaskToImage -> SaveImage. Run with
  `python tools/lab.py --wf wf_bgremove.json --jobs jobs/a43_bgremove.jsonl --box local --sub gl/mask --out gens/mask`.

**Crop first.** On the full frame BiRefNet picks the anime figure printed on the screen as the
salient object. On the crop `(0, 650, 950, 2950)` it picks the cock cleanly. `jobs/a44` /
`gens/mask2/mask_crop_00001_.png` is that mask.

`tools/mixed_prep.py <source> <mask> out_cut.png out_canvas.png` applies the mask, trims, scales the
cock to 1150 px tall and places it on a dark 896x1344 canvas (`analysis/mixed/mix_canvas.png`).

## The edit (works)

Qwen-Image-2.1 one-image edit (`wf_qwen21_edit1.json`, 896x1344, 25 steps, cfg 1):

```
Keep the real penis in the foreground exactly as it is: photoreal, the same shape, colour, veins,
glans and skin texture, in the same position, unchanged. Paint a flat 2D anime scene around it: a
young adult anime woman with short silver hair in a single braid, purple eyes, jitome half-lidded
eyes, a mole under her eye, a small fang, no glasses, topless, kneels in front of the penis with her
lips sealed around the glans, her cheeks hollow, her eyes looking up at the viewer; clean lineart,
flat cel shading, a dim bedroom behind her with pink LED glow. The penis stays photoreal and
unchanged, she is drawn around it. No screen, no monitor, no text.
```

Result: `gens/a45/mix5_isolated_00001_.png`. The cock is the real one (same pixels), the girl is the
LL signature 2D style.

## Rejected routes (do not repeat)

- Qwen **two-image** swap (anime still as Picture 1, real cock as Picture 2): the model regenerated
  the cock; wrong anatomy, does not resemble the source. Owner: "unusable".
- Editing the real photo itself ("keep the penis, replace the screen"): it keeps the screen girl and
  copies her outfit/face. Good enough to prove the method, not the target.
- Manual colour-threshold or polygon masks: ragged edges / screen fringes; the BiRefNet mask is
  clean.

## Open

- The girl's lips touch the glans rather than sealing deep around it. A variant with her mouth open
  around the head (or a side angle) is the next try.
- The cock is a still; a video version needs the real cock held static while the anime girl moves.
