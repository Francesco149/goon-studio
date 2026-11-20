# Explicit scenes: the recipes that work, and the ones still open

Owner-approval status is marked per section. Written 2026-11-20 from rounds on **cutestation**
(RTX 5060 8 GB) and **ampere** (RTX 3080); every render, prompt and seed is in `~/goonlab` on
cutestation (`gens/`, `jobs/`, `tools/`). The six source references and the shot grammar they share
are in `~/goonlab/notes/REFS.md`.

| section | status |
|---|---|
| 1. Erotic anime faces and poses | **approved** |
| 2. Correct cocks in stills (photoreal) | **approved** |
| 3. Blowjob motion in a clip, and its variations | **approved** |
| 4. Anime cock anatomy | incomplete - hit or miss, needs more work |
| 5. Photoreal video anatomy | incomplete - the exit frame has to be an image constraint |
| 6. Cum | incomplete - still reads as glue |
| 7. Operation notes | - |

---

## 1. Erotic anime faces and poses  (approved)

Two prompts, kept **verbatim** as the base. Only the "cock half" may vary around them (section 4);
rebuilding the rest is what turned the faces into a lottery before.

Model: **Anima**, `anima-aesthetic-v1.1` for the look (section 4 explains when to use Base instead).
30-32 steps, cfg 4.0, `er_sde` / `simple`. 30-32 s a picture on cutestation, ~15 s on ampere.

### 1a. Side view - `gens/ha01/ll_anima_tags_side`, 1248x832, seed 21

```
masterpiece, best quality, year 2016, anime screenshot, 1girl, 1boy, hetero, blowjob, fellatio,
oral, penis, glans, foreskin, veins, erection, uncensored, penis focus, side view, profile,
kneeling, leaning forward, short silver hair, single braid, purple eyes, @murota yuuhei,
(curvy:1.6), (wide hips:1.4), thick thighs, large breasts, mature female, half-closed eyes, blush,
saliva, bedroom, soft light, love live! sunshine!!
```

negative:

```
extra hands, extra fingers, third hand, bad anatomy, fused limbs, censored, mosaic censoring,
bar censor, worst quality, low quality, score_1, score_2, score_3, blurry, jpeg artifacts,
watermark, text, 3d, realistic
```

Why the face works: `side view, profile` + `kneeling, leaning forward` gives a readable two-body
arrangement (Anima cannot compose a POV), and `half-closed eyes, blush` on top of the Love Live tags
carries the expression.

### 1b. POV - `gens/ha01/ll_anima_tags_pov`, 832x1248, seed 22

```
masterpiece, best quality, year 2016, anime screenshot, 1girl, 1boy, hetero, blowjob, fellatio,
oral, penis, glans, foreskin, veins, erection, uncensored, penis focus, pov, from above,
looking up at viewer, short silver hair, single braid, purple eyes, @murota yuuhei, (curvy:1.6),
thick thighs, large breasts, mature female, half-closed eyes, blush, saliva, bedroom, soft light,
love live! sunshine!!
```

negative: as 1a plus `extra limbs, male body` - `male body` in the negative is what keeps the man out
of a POV frame, `looking up at viewer` is what puts her eyes on the lens.

### 1c. Style notes

- The show's look is carried by `@murota yuuhei` + `year 2016, anime screenshot` + the series tag;
  with Anima the series tag can be left in for an original character without stealing the face
  (it did not turn this silver-haired OC into a canon girl).
- `blush` alone is safe; anything phrased as a state of the skin (`flushed cheeks`) paints hard red
  patches instead of a flush.
- Negative `3d, realistic` keeps the drawing flat.

---

## 2. Correct cocks in stills, photoreal  (approved)

The one that works is a **LoRA, not a prompt**. Krea 2 Turbo alone refused the subject entirely
(`~/goonlab/gens/p01/p3` - it drew a softcore pose with no genitals), and H3-Image drew a plausible
but generic one.

### 2a. The chain

1. **Krea 2 Turbo + `Verite_realism` LoRA** (owner's download; the Civitai page for "Verite V5" is
   the source). On ampere: `models/loras/Verite_realism.safetensors`, 436 MB.
   - `UNETLoader krea2_turbo_int8_convrot` -> `LoraLoaderModelOnly` strength **1.0-1.3**
   - `CLIPLoader qwen3vl_4b_int8_convrot` (`krea2`), `VAELoader qwen_image_vae`
   - 8 steps, cfg 1.0, `euler` / `simple`, 896x1344 (portrait) - 20-45 s a picture on ampere
2. Nothing else: no prop, no edit pass, no mosaic.

### 2b. Prompt shape (photoreal, sex act)

Act first, then her, then **him**, then his cock, then where her hands are, then the setting, camera
tag last:

```
A candid amateur photo of a blowjob. There is a man lying on his back on a bed. He is an adult man
in his thirties, lean, with a strip of dark pubic hair. His erect cock rises from his body and a
woman with long black hair kneels between his legs and takes it into her mouth, her lips sealed
around the shaft halfway down; her hand is around the base. The head of the cock is clearly defined,
with a rim where the foreskin is folded back behind it, and a visible slit at the tip. Her eyes are
up at the camera. Bedroom, afternoon window light. Amateur phone photo.
```

- The LoRA author's own rule, and it is what made the difference:
  **"don't just write a thick cock between or somewhere, write like a man then his cock."**
- Camera tags that work: `Amateur phone photo`, `Candid flash photo`, `Candid amateur photo` - last.
- Strength 1.0 for natural light, 1.3 for flash/punchier.
- The author ships a second file, `Verite-overcooked`, which he says is strong for fluids; it is not
  downloaded here and is the obvious test for section 6.

### 2c. What was tried first, and why it is worse

- `minimax_h3_image_pruned` (H3-Image) with anatomy spelled out: correct and detailed, but the
  drawing is generic and the pose/camera are less controllable -> `gens/p01/p1`, `p2`.
- `qwen_image_2.1` (int8, 25 steps): the most anatomical detail of the four, muddier body layout.
- Photo anatomy transplanted into the scene with an edit model: the shape transfers but the target
  image degrades (H3-Image edit repaints skin crustily) or flattens (`gens/a02`, `a03`). Only worth
  it when a specific anatomy must be imposed - see section 4.

---

## 3. Blowjob motion in a clip, and its variations  (approved)

Base recipe, then the variations that were tested and what each one buys.

### 3a. Base clip - `gens/v02/v4_i2v_photo_768`, `gens/pv01/pvid_ve1`

H3 video, **FL2VA int8 + Pika Flex 6-step LoRA**, i2v from a still, **768x1152** (2:3, multiples of
32), 124 frames = 5 s, `lcm` sampler with the Pika sigmas
(`1.0, 0.972973, 0.923077, 0.8, 0.571429, 0.333333, 0.0`), and **Comfy Kitchen attention**
(`ModelAttentionBackend`, "comfy kitchen attention"). 130-150 s a clip on ampere, ~140 s at
512x768 on cutestation.

```
integrated_multimodal_description: [Shot 1] Photorealistic amateur video, the same scene and the
same two people as <Picture 1>: a man lies on his back, the camera looks down his body at her
kneeling between his legs, her lips sealed around his erect cock. The cock keeps exactly the
anatomy it has in <Picture 1>: a thick shaft, a clearly defined glans with the foreskin folded back
behind the rim, the ridge under the head, her fingers around the base. The stroke is slow: she
slides her mouth down until her lips are halfway along the shaft, holds for a beat with a small
swallow, then draws back up until only the head stays between her lips, the lips sealed all the way
so the shaft comes out wet. One stroke takes about two seconds. A thin string of saliva stretches
from her lower lip to the skin and breaks. Her eyes lift to the camera, a light natural blush. The
camera does not move.

overall_soundscape: soft wet suction on the way down, a small wet pop as her lips pass the rim, her
slow breath out through her nose at the bottom of each stroke, one low short male grunt near the
end, quiet bedroom room tone. No music.

non_diegetic_music: N/A
```

The load-bearing lines, each learned the hard way:

- **`The camera does not move.`** Without it the model cuts to another angle by itself.
- **`the lips sealed the whole way`** - the seal is what reads as a blowjob; a mouth near a cock
  reads as a kiss.
- **`One stroke takes about two seconds`** - "bobbing" reads as one continuous slide, far too fast.
- **`holds for a beat with a small swallow`** - the held bottom is most of the realism.
- **`one low short male grunt ... no word`** - asking for "the men moan" makes the model invent a
  voice in the wrong register. Give the register, the length and where it lands.
- Sound goes in `overall_soundscape` as events in order, never as an emotion.

### 3b. Variations, and when to use each

| variation | how | round | what it buys |
|---|---|---|---|
| **first + last frame anchored** | `wf_h3vid_i2v_fl.json`: same still as `first_frame` and `last_frame` (or two known frames) | `gens/rc01/r2` | the clip must land on a known pose, so the anatomy cannot drift away permanently. **Best for a pull-off.** |
| **two-reference (Ref2VA)** | `wf_h3vid_ref2va6.json`: `minimax_h3_ref2va_pruned_int8_convrot` + `pika_h3_flex_ref2va` LoRA, `MiniMaxH3ReferenceToVideo`, ref_image_0 = current frame, ref_image_1 = the target anatomy | `gens/rc01/r1` | tells the model what the cock must look like when it comes out; softer, more home-video texture |
| **head-only work** | `her lips slide over the glans and back to the rim, never further down` | `gens/gl01/g1` | keeps the glans visible for more of the clip when it is collapsing |
| **explicit no-deform** | `no strong suction and no squeezing ... the glans is never pulled thin or sucked into the mouth` | `gens/gl01/g2` | helps but does not solve it on its own; pair with an image constraint |
| **t2v instead of i2v** | same text, no first frame | `gens/v01`, `gens/v05` | sharper small detail, weaker identity - the face drifts across 5 s |
| **lower resolution** | 512x768 | `gens/v01b` | **do not**: it loses the rim entirely if the keyframe was 896x1344 |
| **mosaic** | post: ffmpeg `split` + `crop` + `pixelize` + `overlay`, `-c:a copy` | `gens/v01/v1_t2v_mosaic.mp4` | hides an unresolved head; matches the reference look |

### 3c. What to check on a finished clip

`tools/strip.py <frames dir> out.jpg 1 20` gives a 20-frame filmstrip: check the rim on the way in,
the seal (lips as a ring behind the glans), the held bottom, the strand of saliva, and whether the
head is the same shape when it comes out as when it went in.

---

## 4. Anime cock anatomy  (incomplete - hit or miss)

**Working, not solved.** Two changes moved it from "bad" to "sometimes good":

1. **`anima-base-v1.0` instead of `anima-aesthetic-v1.1`** for the anatomy. Same prompts and seeds:
   Base draws a real head with a corona rim and the foreskin bunched behind it
   (`gens/cock01/b_base_pov`, `d_closeup_pov`, `gens/cock02/base_pov_seed28`); Aesthetic keeps a
   smooth tube with a cap. Base is now the default for anything explicit.
2. **Weight the parts**, in the prompt's action half and nowhere else:
   `(penis:1.2), (glans:1.5), (foreskin:1.4), (veins:1.2), erection, uncensored, penis focus,
   detailed penis`. `penis focus` is what stops the cock being drawn as background.

Censored variants work on Base too (`gens/cock02`): `censored, bar censor` gives a clean bar over a
still-readable head; `censored, mosaic censoring` reads like the reference material. Censorship is
*not* a fix for the anatomy - the model does not draw a better cock under a bar - but it is a
presentation that hides the weak part and matches the references. The side view at 1248x832 loses
the cock when mosaicked, so keep that one uncensored.

**Tried and rejected:** transplanting a real photo's anatomy into the drawing with
`qwen_image_2.1` edit (`gens/lf01`) - the shape transfers, the drawing does not; the corona becomes
a bracelet. Transplanting an *anime* prop (`gens/anp` -> `gens/anfix`) keeps the style but flattens
the head. `close-up` on a side view splits the frame into an inset panel (`gens/cock01/c`).

**Next, needs a decision:** a hentai-native Anima checkpoint. The Civitai listing "Illustrij" ships
versions whose base model is **Anima** (`A1`, `TINKER`: a 3989 MB unet + `anima_baseV10_txt` +
`qwen_image_vae`, i.e. drop-in for the Anima graph), and "Hentai Comic Random Generator" also lists
Anima. The alternative is training an anatomy LoRA on Anima with
`research/style-lock/scripts/train_anima_lora.sh` (~40 min on lame).

---

## 5. Photoreal video anatomy  (incomplete)

What works: the still (section 2) plus section 3's clip recipe. The residual failure is the **glans
deforming under suction** - it goes in with a rim and comes out as a different head
(`gens/gl01/g2_no_collapse`).

What fixed most of it: **make the exit state an image constraint**, not a sentence.

- `gens/rc01/r2_i2v_return_to_key`: first frame = an in-mouth frame, last frame = the keyframe with
  the cock out. The head stays ridged on the way out and the clip is forced to land on the correct
  cock. **This is the one to keep.**
- `gens/rc01/r1_ref2va_pulloff`: Ref2VA with the keyframe as the second reference. Same idea,
  softer texture, flatter shaft at the end.

Still weird in both: the saliva reads as an unnatural blob at the mouth (`r2`), and the shaft goes
slightly flat near the base. Both need work.

---

## 6. Cum  (incomplete)

In stills it is fine - Anima draws ropes, strands and drips that sag (`gens/g01b/f_cumshot`), and the
Krea 2 + Verite stills draw it acceptably. **In video it still reads as glue**: opaque, rigid,
motionless strands (`gens/w02/w2_cum_pov`), and left to emit it foams outward instead.

Rules that helped: put the cum in the first frame and animate only the continuation (a twitch, the
last sprout, a drip); when the clip must emit, describe matter with a path, a count, an arrival point
and a beat after it, and say `nothing expands`. Never "a lot of cum".

Not yet tried: `Verite-overcooked` (the LoRA author says it is strong for fluids); translucency
wording (`off-white and slightly translucent, the skin tone shows at the edges, the strand sags,
thins in the middle and beads`).

---

## 7. Operation notes

- **Two workflows to reuse** (copy out of `~/goonlab/tools`): `wf_h3vid_i2v.json` (i2v, Pika 6-step),
  `wf_h3vid_i2v_fl.json` (first+last frame), `wf_h3vid_ref2va6.json` (two references),
  `wf_krea2_verite.json` (Krea 2 + the LoRA), `wf_anima.json` (Anima tags).
- **Resolutions**: keyframe 896x1344 (2:3) and the clip at 768x1152 for that shape; clips need
  multiples of 32; 512x768 loses fine detail if the keyframe was larger.
- **ComfyUI can leave a finished prompt sitting in `queue_running`**, which blocks everything after
  it while its history entry already says success. `POST /interrupt` clears it safely; the batch
  driver does it automatically.
- **`/upload/image` rejects a hand-rolled urllib multipart body** (HTTP 400). `curl -F` works, and
  the same endpoint accepts video for `LoadVideo`.
- **One batch per box, one output and upload subfolder per batch.** Two batches sharing a subfolder
  delete each other's renders on cleanup.
- **Hygiene**: renders go to `output/gl/<round>`, are pulled off, and the folder is deleted
  afterwards - a PNG keeps its prompt in the metadata and both boxes serve `/view` and `/history`
  to the whole LAN with no auth.
- **cutestation** is fine for one clip at a time; after a video model has been resident, returning to
  images is slow (8 GB VRAM, model swap). Iterate on **ampere**.
