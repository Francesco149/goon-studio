# Round 2026-11-20: keeping a small, detailed part correct through H3 video

Testbed: a close-up, two-subject scene on ampere (3080) and cutestation (5060) where one part of
the frame is small, highly detailed and anatomically specific, and the rest is a face. The same
failure mode applies to any small detailed object that must stay itself while it moves: a hand
holding something, a printed label, a mechanism, a face in a crowd.

Everything below is measured; the rounds and prompts are in `~/goonlab` on cutestation
(`gens/`, `jobs/`), drivers in `tools/`.

## 1. Name the parts, and say the shape holds

Asked for the subject generically, H3 video draws a smooth, tapered, generic shape - no rim, no
seam, no attachment. Named part by part, the same prompt at the same size draws all of it:

```
...the shaft is thick with a clearly defined glans and a clear rim, a retracted foreskin ridge,
visible veins and a scrotum below..., and it keeps that shape for the whole shot.
```

That is the same lever as the baguette bite in `research/object-anchor` (2026-11-19) and the
"spell out the physics" rule: **the video model will draw fine, specific structure if the prompt
enumerates the structure and asserts that it persists.** Without the assertion it drifts back to
the generic shape mid-clip, exactly like the Yorkie drifting back to a show dog.

## 2. A clip cannot preserve detail the keyframe had at a higher resolution

- keyframe 896x1344, clip 512x768: the rim and the seam are gone in every frame; the shape drifts
  to a rounded cylinder.
- keyframe 896x1344, clip 768x1152: the rim, the seam and the veins are all still there 5 s later.
- Same prompt as t2v at 512x768: sharper than i2v at the same size.

So: **run the clip at the keyframe's aspect and as close to its resolution as the box allows**
(2:3 keyframe -> 768x1152), and prefer t2v when the small detail matters more than identity
lock. t2v costs identity: the face drifts across 5 s; i2v holds the face but softens small parts.

## 3. Depth order, spelled as a list, fixes parts landing on the wrong side

A part that should be *behind* something came out in front of it (a sack that should sit under a
shaft was drawn in front of it, with the hand behind). `below` is ambiguous: it means "lower in
the picture", which for a top-down camera is *towards the viewer*.

Fix, and it worked first try: give the model the order along the camera axis as a list.

```
Depth order, nearest to furthest: A at the bottom edge of the frame, then B, then C, then D.
E is at the very base, behind B, mostly hidden by it.
```

A/B on one seed: ambiguous wording -> wrong side; no mention -> the part is simply omitted;
depth-order list -> correct placement and correct occlusion.

Cost, worth knowing: pinning the face as the last item in that list makes her stare at the lens for
the whole clip and the face goes more generic. End the list at the face and describe the eye
behaviour in its own sentence.

## 4. A word can be painted literally

`flushed cheeks` produced hard red blotches on the cheeks in every still and clip that used it
(H3-Image and Anima alike), not a flush. `a light natural blush` is the safe wording. The same
class of problem: any word naming a *state* or a *colour* may be rendered as a literal patch
rather than as the state. Check the wording on the first render of a new prompt.

## 5. Some effects are post-process, not prompt

An effect the text encoder has no visual prior for is not fixable in the prompt - a mosaic/censor
pattern asked for in words came back as an uncensored picture, every time. Do it after the render
(`ffmpeg` crop + `pixelize` + overlay, `-c:a copy` keeps the audio). Expect the same for motion
blur, focus pulls, film burn: describe them in words only where the model has seen them a lot.

## 6. Model willingness is not uniform - probe before committing a pipeline

One prompt, four image models, same seed and size:
- **H3-Image** int8: drew the whole subject correctly and in detail (17-27 s on ampere).
- **Qwen-Image-2.1** int8: the most detailed of the four, less clean layout.
- **Anima Aesthetic v1.1**: drew it, softened (36-40 s on cutestation).
- **Krea 2 Turbo**: **dropped the part entirely** and produced a different, tamer composition.
  8 steps, 45 s, and the pipeline criterion is unusable.

So a model's speed and general quality say nothing about whether it will draw a specific hard
detail. Probe the one prompt on each candidate before building the chain; H3-Image was not the
obvious first guess and was the only clean one.

## 7. Operation notes (both boxes)

- **ComfyUI can leave a finished prompt in `queue_running`**, which blocks every later prompt
  forever while its history entry already says success. `POST /interrupt` clears it and is safe
  once history is written; `tools/lab.py` does it automatically when it sees its own completed
  prompt still listed as running.
- **`/upload/image` rejects a hand-rolled urllib multipart body** (HTTP 400, aiohttp). `curl -F
  image=@file -F subfolder=... ` works. The same endpoint accepts video for `LoadVideo`.
- **Two batches sharing one output subfolder clean each other's renders away**: cleanup deletes by
  subfolder, so a second batch's cleanup removed a first batch's renders (and its uploads, which
  made a queued `LoadImage` fail). Give every batch its own output *and* upload subfolder
  (`gl_up/<round>`) and a per-box lock.
- cutestation after a video model has been resident is slow to come back to images (model swap,
  8 GB VRAM): one clip at a time there, iterate on ampere.
