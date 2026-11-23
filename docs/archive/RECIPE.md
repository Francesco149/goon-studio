# The recipe: a blowjob scene that stays well formed

Status: working draft, 2026-11-20. Numbers and verdicts below are from the rounds in `gens/`;
each claim names the round it came from.

## What actually goes wrong (and what fixes it)

Three separate failures, three separate causes. Fixing one does not fix the others.

### 1. The cock comes out as a stick

**Cause: the video model is not given the anatomy, and the image it starts from is too small to
hold it.** H3 video *can* draw a correct erect penis - `v01/v1_t2v_photo` has a thick shaft, a
defined glans with a rim, veins and a scrotum for the whole 5 s - but only when the prompt names
those parts and says the shape holds. Asked for "blowjob, penis" it produces a tapered stick with
no rim, which is what the owner saw in the paizuri/hug clip.

The frame matters as much as the words: `v01b/v3_i2v_photo` (i2v, 512x768) keeps the anatomy but
softens the rim; `v01b/v2_i2v_anime` (i2v, 512x768, anime) loses it and drifts back to a sausage.
The keyframe is 896x1344 and the video is scaled down to 512x768, so the rim is only a few pixels
- the model can't preserve what it can't see.

**Fix, in order of effect:**
1. Spell out the anatomy in the video prompt, every time, in this shape:
   `thick shaft, a defined glans with a clear rim, a retracted foreskin ridge, visible veins and a
   scrotum below, with her fingers wrapped around the base`, then `the penis keeps exactly that
   shape` / `the penis is thick and stays clearly shaped for the whole shot`.
2. Generate the keyframe with **H3-Image**, not Anima, and at the video's aspect. Anima draws a
   passable cock but with a soft, blunt head (`g01/c_anatomy`, `g01b/i_nobody`); H3-Image draws a
   correct, detailed one, in photo *and* anime style (`p01/p1`, `p01/p2`).
3. Run the video at the keyframe's resolution or as close as the box allows (768x1152 for a
   2:3 keyframe), not 512x768.
4. If the video still softens it, do a **t2v** take with the same text: the pure-text path keeps
   the anatomy sharper than i2v at low resolution (`v01` vs `v01b/v2`).

### 2. Cum behaves like expanding foam

**Cause: the video model's only seen cum as an abstract effect.** In a still, the same model family
does it right: `g01b/f_cumshot` (Anima) has ropes hanging off her lip, a strand down the shaft, and
blobs that sag - discrete, gravity-shaped, correct.

**Fix:** put the cum in the first frame (`q01/c1_cum_face`, `q01/c2_cum_tits`) and let the video
animate the *continuation* (a twitch, the last spurts, a drip), never the first emission. When it
must emit, describe it as matter with a direction and a time budget:

```
the shaft jerks up once, and a thick white rope leaves the tip in one short arc, crossing her
cheek from jaw to cheekbone; the rope stays unbroken for a moment, then sags. Nothing expands.
At 1.2 s a second, smaller rope follows the same path and lands on her chin.
```

`nothing expands`, the arrival path, and the beat after the spurt are the load-bearing parts. Do not
say "a lot of cum" (broad, and the model answers with growth), say how many ropes and where they land.

### 3. Strokes are too fast, moans are wrong

**Cause:** "bobbing" reads as one continuous action; the model has no idea what 2 seconds is.
**Fix:** give the stroke a shape and a duration, and describe sound as a script, not as an emotion.

```
The stroke is slow and deep: she slides her mouth down until her lips are halfway along the shaft,
holds there for a beat with a small swallow, then draws back up until only the head stays between
her lips. One stroke takes about two seconds.
```

Sound goes in `overall_soundscape` as events with a place in time - a wet suction on the way down, a
small wet pop as her lips pass the rim, a breath out through the nose, and *one low, short male
grunt, air pushed out, not a word*. Male moaning that came out wrong before was asked for as
"the men moan"; the model then invents a voice. Naming the register (low, short, no word) and the
timing is the lever.

## The pipeline

```
1  keyframe   H3-Image, plain English, explicit anatomy, at the video's aspect      3080, 17-27 s
2  video      H3 FL2VA + Pika 6-step, i2v from that keyframe (or t2v)               3080, 55 s / 5 s
3  check      tools/strip.py on the clip: rim, seal, stroke count, strand, sound
4  censor     optional, post: ffmpeg crop + pixelize + overlay, -c:a copy
5  upscale    optional: RelayVSR x2 keeps the audio
```

Two boxes: **the 3080** is the main one (2.5-3x faster, every model). **cutestation** does the same
work at about a third of the speed and only one clip at a time, which is fine for the final take.

## The keyframe prompt (H3-Image)

Photo, POV, mid-blowjob - `p01/p1_h3img_photo`, 896x1344, 6 steps, cfg 1.0, 17 s on a 3080:

```
Photorealistic first-person POV photo, taken by a man lying on his back looking down his own body
at a young adult woman with long black hair kneeling between his legs. Her lips are stretched
around the shaft of an erect adult penis rising from the bottom centre of the frame; the shaft is
thick with a clearly defined glans, a retracted foreskin ridge, visible veins and a scrotum below,
and a thin string of saliva runs from her lower lip to the shaft. She looks up into the camera with
half-closed eyes and flushed cheeks, one hand wrapped around the base. Soft bedroom window light
from the left, shallow depth of field, natural skin texture, slight phone-camera grain.
```

Same prompt with `A 2D anime illustration, clean line art with cel shading, soft pastel palette,`
in front gives the anime version (`p01/p2`). Both hold the anatomy; the whole trick is naming the
parts and saying where they are relative to the frame.

## The video prompt (H3 FL2VA)

MiniMax structure, three sections, plain sentences inside them. `v01/v1_t2v_photo`:

```
integrated_multimodal_description: [Shot 1] Photorealistic first-person video: a man lies on his
back and the camera looks down his own body to a young adult woman with long black hair kneeling
between his legs on a bed. Her lips are sealed around the shaft of an erect penis that rises from
the bottom centre of the frame. The penis stays thick and clearly shaped for the whole shot, with a
defined glans, a retracted foreskin ridge, visible veins and a scrotum below her hand. She slides
her mouth slowly down the shaft until her lips are past the middle, then pulls back up until only
the head is still between her lips; her lips stay sealed the whole way, so the shaft comes back out
glistening. A thin string of saliva stretches from her lower lip to the skin and thins out. She
looks up into the lens with half-closed eyes and flushed cheeks, breathing through her nose. The
camera does not move.

overall_soundscape: soft wet suction and a quiet pop as her lips pass the head; her breathing
through her nose; one low, short male grunt about halfway through; quiet bedroom room tone. No music.

non_diegetic_music: N/A
```

Rules that came out of the rounds:
- **One camera, stated.** `The camera does not move` / `The camera holds still`. Without it the clip
  will cut to another angle by itself (a known T2V habit), which breaks continuity.
- **The seal is the thing to describe**, not the mouth: "lips sealed around the shaft", "the lips
  stay sealed the whole way". A mouth near a cock reads as a kiss; a sealed ring reads as a blowjob.
- **State the duration of a stroke** and give the bottom of the stroke a beat.
- **Never let the clip introduce a new object.** A penis that has to appear mid-clip arrives wrong;
  start the clip with it already in the mouth (`v01`, `v01b/v3`).
- **Say what the camera sees of the man**: `his own body along the bottom of the frame` keeps it a
  POV instead of inventing a third person.

## Style: anime vs photo, and censorship

- H3-Image carries a style from one sentence: `2D anime illustration, clean line art with cel
  shading` for anime; `photorealistic ... natural skin texture` for photo. Same composition prompt
  otherwise. The anime one reads closer to the flim13 refs; the photo one closer to refs 5/6.
- **Anima** is the alternative when a specific TV-anime look is wanted (booru tags + `@artist`), and
  it does explicit content, but its anatomy is softer and it will not compose a POV: `1boy` +
  `pov, from above` produced a giant unexplained ass filling the frame in every variant
  (`g01/a`,`b`,`c`,`d`,`e`). Use Anima for the look, H3-Image for the arrangement.
- **Mosaic censorship is post.** `censored, mosaic censoring` in an Anima prompt produced a clean
  uncensored picture (`g01/e_censored_tags`); the tag is not honoured. The working method is
  ffmpeg: `split` the frame, `crop` the genitals, `pixelize=10:10`, `overlay` it back, `-c:a copy`
  (`gens/v01/v1_t2v_mosaic.mp4`).

## Model choice for explicit anatomy (round p01)

| model | explicit anatomy | note |
|---|---|---|
| **H3-Image** (int8, 6 steps) | yes, correct and detailed, photo and anime | the keyframe workhorse; 17-27 s on a 3080 |
| Qwen-Image-2.1 | yes, the most detailed anatomy of the four | the body arrangement is less clean |
| Anima Aesthetic | yes, stylised: soft head, no clear rim | good for the anime look, weak on arrangement |
| Krea 2 Turbo | **no** - dropped the genitals entirely, made a softcore pose | unusable for this |

## Operational notes

- Both boxes' ComfyUI can leave a **finished prompt sitting in `queue_running`**, which blocks
  every later prompt. The history entry is already written, so `POST /interrupt` clears it safely;
  `tools/lab.py` does that automatically when it sees a completed prompt still in the running list.
- A batch of images on cutestation after a video model has been resident is slow (model swap plus
  8 GB VRAM); run one clip at a time there and use the 3080 for iteration.
- ComfyUI's `/upload/image` rejects a hand-rolled urllib multipart body (HTTP 400); `curl -F`
  works.
- Sizes must be multiples of 32. A 2:3 keyframe wants 768x1152 for the clip (884 736 px, 720p-ish).
