# Sex scenes on the lab's local models

How to get a consistent, well-formed explicit scene out of H3-Image + H3 video (FL2VA) on ampere
or cutestation, without the usual failure shapes. Written 2026-11-20 from the rounds in
`~/goonlab` (cutestation) - owner-sourced references, 6 clips, ~30 renders.

Everything here is for the owner's personal use on the lab's own boxes. Nothing in this file is
for a deployed or shared surface; see `docs/OPERATIONS.md` for where renders may live.

## 1. The three failures, and what actually fixes each

### A. The cock comes out as a stick

**Not a model limit.** H3 video draws a correct erect penis - thick shaft, a glans with a visible
rim, a retracted foreskin ridge, veins, scrotum - when the prompt names those parts and says the
shape holds. Asked for `blowjob, penis` it produces a tapered stick with no rim: that is the shape
in the owner's paizuri clip, and it is what the model does when the anatomy is left implied.

The frame matters as much as the words. An i2v clip at 512x768 from an 896x1344 keyframe loses the
rim (the detail is downsampled away); the same keyframe at 768x1152 keeps it. A pure **t2v** take
of the same text is sharper still, because nothing anchors the model to a low-res frame.

**Do, in this order:**
1. Name the anatomy, verbatim, in every video prompt:
   `thick shaft, a defined glans with a clear rim, a retracted foreskin ridge, visible veins and a
   scrotum below, with her fingers wrapped around the base`, then `the penis keeps exactly that
   shape` / `stays thick and clearly shaped for the whole shot`.
2. Make the keyframe with **H3-Image**, not Anima (see the model table).
3. Run the clip at the keyframe's aspect and as close to its resolution as the box allows:
   2:3 keyframe -> 768x1152. 512x768 only for a first look.
4. If the clip still softens the head, redo it as t2v with the same text.

### A1. If the anatomy still comes out wrong: anchor it, or mosaic it

The glans is the weakest part of every photoreal render so far - in the 768-wide clips the head is
often a smooth cap with no corona, or a balloon. Two answers were tested on 2026-11-20; both work,
neither is free.

**Anchor it with a prop.** Make the anatomy alone, clean, large and in the target look, then insert
it (this is the object-anchor method from `research/object-anchor`, applied to a body part):

1. `a01/prop_photo_side` - H3-Image, 1152x1152, "photorealistic studio photograph of one adult erect
   penis, side-on, filling the frame from the base to the tip, against a plain seamless white
   background ... the glans is clearly defined with a pronounced corona rim ... foreskin retracted
   ... scrotum at the base", 28 s on cutestation. That gives a **correct** reference on white.
2. Insert it into the keyframe with **Qwen-Image-2.1 edit** (two references: Picture 1 = the scene,
   Picture 2 = the prop), prompt: *keep Picture 1 exactly ... change only the penis: it must have
   exactly the anatomy of the penis in Picture 2 - the same defined glans with the pronounced corona
   rim, the same retracted foreskin collar, the same ridge under the glans ... at the same angle and
   position as in Picture 1*.
   - `a03/q1_qwen_insert`: the anatomy transfers (glans with a rim and a collar, not a stick), the
     woman, skin, light and pose survive intact. It reads slightly prosthetic - the collar looks like
     a ring - but it is unambiguously a cock.
   - **H3-Image edit is the wrong tool for this**: `a02/ins1_photo` and `a02/ins2_anime` do transfer
     the anatomy but repaint the whole frame with an over-sharpened, crusty texture (cracked skin,
     wiry hair, black line noise in the anime one). Use H3-Image for *making* the picture, not for
     editing one.

**Or mosaic it.** If the goal is the flim13 look anyway, a mosaic hides the weakest 100 px of the
frame and costs one ffmpeg pass (section 7). For photoreal output where the head has to hold up, the
mosaic is the cheaper, more reliable answer than another round of keyframe roulette.

**What not to do:** do not ask the video model to fix the head. It preserves what the keyframe has,
good or bad (`w1_side_photo` keeps a muddled mouth/shaft junction for the whole clip) - check the
keyframe's junction *before* you spend the clip.

### A2. The balls come out on the wrong side

Seen in `v02/v5_t2v_photo_768`: a two-lobed sac with a raphe sits **in front of** the shaft base,
so the cock appears to grow out of the top of the balls - and her fingers are *behind* the sac
instead of in front of it. The words that caused it are `...a scrotum below her hand`: in a
top-down POV "below" means "lower in the picture", which is *towards the camera*, so the model
puts the whole sac nearest the viewer and stacks the shaft behind it.

Round `b01` (same seed, three prompts, 512x768, t2v):
- `b1_baseline` (`a scrotum below her hand`): the wrong-side shelf of balls, in front of the shaft.
- `b2_no_scrotum` (delete the word, keep `pubic hair at the base`): no sac drawn at all; the base
  resolves into pubic hair. **This is the right look for a POV** - from his own eyes the scrotum is
  behind the shaft and barely in frame, so a solution that merely moves it lower is still wrong.
- `b3_depth_order` (sac "behind her fingers", fingers nearest the camera): better than b1 and still
  wrong - the user's verdict, 2026-11-20: *"we're looking from the man's perspective so the scrotum
  shouldn't be in front, it should be behind the cock"*. b3 keeps a big two-lobed sac in frame under
  the shaft. Do not use it.

**So for a POV: leave the scrotum out of the prompt and let the base dissolve into pubic hair.**
If it must appear, it belongs *behind the shaft* - hidden by the shaft from his viewpoint - not
below it in the picture:

```
his scrotum sits behind the base of the shaft, below it and away from the camera, so the shaft
hides most of it; nothing of it is in front of the shaft.
```

That wording is untested; test it before trusting it. For a side or three-quarter view the balls are
legitimately visible and the plain `a scrotum at the base` wording is fine - the artifact is specific
to looking down the shaft from the man's own eyes.

### B. Cum behaves like expanding foam

The still models know cum: ropes hanging off a lip, a strand down a shaft, blobs that sag. The
video model does not - left to emit, it grows a symmetric foam over the skin.

**Do:** put the cum in the *first frame* and animate only the continuation (one twitch, the last
spurts, a drip). When the clip must emit, describe matter with a direction, an arrival point and a
beat after it:

```
the shaft jerks up once, and a thick white rope leaves the tip in one short arc, crossing her cheek
from jaw to cheekbone; the rope stays unbroken for a moment, then sags. Nothing expands.
At 1.2 s a second, smaller rope follows the same path and lands on her chin.
```

The load-bearing words are the *path*, the *count*, the *beat*, and `nothing expands`. Never "a lot
of cum" - it answers that with growth.

**It still reads as glue** (owner, 2026-11-20 - better than before, but glue). The strands in
`w02/w2_cum_pov` are opaque, high-contrast white ropes that hang rigidly and do not move at all in
5 s. What is missing is the material: semen is slightly translucent, picks up the skin colour at its
edges, sags, thins in the middle and beads at the bottom. Say that:

```
The semen is off-white and slightly translucent, so the skin tone shows at the edges of every
strand; the thick strand from her lip sags under its own weight, thins in the middle and beads into
a heavier drop at the bottom, which slides a millimetre and drips onto her chin.
```

Fewer, longer strands read better than many short ones, and one strand that *moves* beats a dozen
that hang. That wording is the next thing to test; the anchors that work for anatomy (A1) should work
here too - a real frame of the same moment is a better reference than any adjective.

### C. The stroke rushes and the men moan wrong

"Bobbing" reads as one continuous action; the model has no clock. Give the stroke a shape and a
duration:

```
She slides her mouth down until her lips are halfway along the shaft, holds there for a beat with
a small swallow, then draws back up until only the head stays between her lips. One stroke takes
about two seconds.
```

Sound is a script, not an emotion. In `overall_soundscape`, name the register, the pitch, the
length and where it lands in the shot:

```
At about three seconds the man lets out one low, short grunt from the chest, air pushed out, no
word, ending quickly; after it a slower exhale that trails off.
```

The failed version is `the men moan` - the model then invents a voice, and the voice is wrong.

## 2. Style: a specific anime look holds, and it is the fix for AI-slop faces

Owner, 2026-11-20: the anime renders are "all competent but generic AI slop" - so the next test was
whether a *specific* look survives an explicit scene. It does, two ways.

**With H3-Image (plain English, no tags).** Put the look in the first sentence, concretely, and keep
it out of the scene description (`s02/ll_h3img_style`, 19 s on ampere):

```
A screenshot from a 2016 Japanese TV anime in the art style of Love Live! Sunshine!!, character
design by Murota Yuuhei: clean uniform line work, flat cel shading with soft gradient highlights,
large expressive eyes with crisp highlights and a coloured iris, light pink blush, a pastel palette
with slightly warm desaturated colours, no 3D shading and no photorealistic texture.
The scene: <the POV description>
```

The result reads as a TV-anime still: sailor uniform with the right collar and neckerchief, glossy
purple eyes with the show's highlight pattern, small nose, cel shading - and no glossy generic AI
face. The anatomy suffers (the glans becomes a cherry on a flat tan slab), which is the A1 problem,
not a style problem.

**With Anima (booru tags).** The studio's own `ll_signature` recipe - designer tag + `year 2016,
anime screenshot` + the series tag - holds in an explicit side view too (`s01/ll_anima_side_bj`):
clean uniform linework, flat cel shading, the soft pastel light, the show's face. What fails there
is the cock (it is not drawn at all, just a shape at her lips), so an Anima-style scene needs the
prop insert or an anatomy LoRA, not more prompt words.

Rule of thumb that came out of this: **any style you can name precisely survives; "anime" alone
gives the generic face.** For this lab the cheap path is H3-Image with the style in the opening
sentence, because the same model then gives you the composition as well.

## 3. Which model draws what (round p01, one prompt, four models)

| model | explicit anatomy | speed on ampere | use it for |
|---|---|---|---|
| **H3-Image** int8, 6 steps | correct and detailed, in photo **and** 2D anime | 17-27 s a picture | **the keyframe workhorse** |
| Qwen-Image-2.1 int8 | the most detailed anatomy of the four | 45-63 s | a second opinion; messy body layout |
| Anima Aesthetic v1.1 | yes but stylised: soft head, no clear rim | 36-40 s on cutestation | a specific TV-anime look (booru tags + `@artist`) |
| Krea 2 Turbo | **refused** - dropped the genitals, made a softcore pose | 45 s | not for this |
| H3 video FL2VA + Pika 6-step | correct anatomy **only** with the prompt rule in 1A | 55 s / 5 s clip | the clip itself |

Anima cannot arrange a POV: `1boy` + `pov, from above` gives a giant unexplained ass filling the
frame in every variant tried. Use Anima for the look and H3-Image for the arrangement, or (for the
Love Live look specifically) H3-Image with `2D anime illustration, clean line art with cel
shading` in front.

## 4. The two shots that work

Both are one keyframe + one clip. The composition names below are measured from the owner's
references.

### 4.1 POV blowjob, camera at his chest looking down (ref1, ref2, ref4, ref6)

Keyframe (H3-Image, 896x1344, 6 steps, cfg 1.0):

```
Photorealistic first-person POV photo, taken by a man lying on his back looking down his own body
at a young adult woman with long black hair kneeling between his legs. Her lips are stretched
around the shaft of an erect adult penis rising from the bottom centre of the frame; the shaft is
thick with a clearly defined glans, a retracted foreskin ridge, visible veins and a scrotum below,
and a thin string of saliva runs from her lower lip to the shaft. She looks up into the camera with
half-closed eyes and flushed cheeks, one hand wrapped around the base. Soft bedroom window light
from the left, shallow depth of field, natural skin texture, slight phone-camera grain.
```

Anime variant: same text with `A 2D anime illustration, clean line art with cel shading, soft
pastel palette, of ...` in front, and drop the photo-only tail.

Clip (H3 FL2VA + Pika 6-step, i2v from that frame, 768x1152, 124 frames = 5 s):

```
integrated_multimodal_description: [Shot 1] Photorealistic first-person video, the same scene and
the same woman as <Picture 1>: a man lies on his back, the camera looks down his own body at her
kneeling between his legs, her lips sealed around the shaft of the erect penis rising from the
bottom centre of the frame. The penis keeps exactly the anatomy it has in <Picture 1>: a thick
shaft, a defined glans with a clear rim, a retracted foreskin ridge, visible veins and a scrotum
below, with her fingers wrapped around the base. The stroke is slow and deep: she slides her mouth
down until her lips are halfway along the shaft, holds for a beat with a small swallow, then draws
back up until only the head stays between her lips, the lips sealed all the way so the shaft comes
out shining wet. One stroke takes about two seconds. A thin string of saliva connects her lower lip
to the skin and stretches until it breaks. Her eyes lift to the lens each time she comes up; her
cheeks are flushed, she breathes through her nose. The camera does not move.

overall_soundscape: soft wet suction on the way down, a small wet pop as her lips pass the rim, a
slow breath out through her nose at the bottom of each stroke, and one low, short male grunt near
the end. Quiet bedroom room tone. No music.

non_diegetic_music: N/A
```

### 4.2 Side view, her on all fours over his lap (ref3, ref4)

Keyframe (H3-Image, 1152x896):

```
Photorealistic side view photograph of a young adult woman with long black hair kneeling on all
fours on a bed beside a man lying on his back; her hips are high and her chest is low over his lap,
her full breasts hanging down and resting on his thigh. Her lips are sealed around the shaft of his
erect penis; the shaft is thick with a clearly defined glans, a retracted foreskin ridge and visible
veins, her upper lip rides over the shaft and her lower lip under it, one hand around the base. His
hand rests flat on her back. Profile view, hip to knees in frame, soft window light, natural skin
texture, shallow depth of field.
```

Clip: same video template as 3.1 with the camera line replaced by `Profile view from the side, both
of them waist-up in frame, the camera does not move.` and one extra beat for the breasts:
`her breasts sway a little behind each stroke, lagging the head by a moment`.

Notes from the rounds: in profile the mouth/shaft junction is where the image model is weakest - its
own fingers and the glans can merge into a pink blob. Check the keyframe before you spend the clip;
if it is muddled, regenerate rather than hoping the video fixes it.

### 4.3 Cumshot, as a second shot

1. Keyframe the **after** state: `Thick white semen is already on her: a rope across her cheek from
   her jaw to below her eye, a smear over her upper lip and chin, one thick blob hanging from her
   lower lip. The glans is still wet and the opening of the tip is visible; a strand of semen still
   connects the tip to her lip.`
2. Clip: i2v, and ask for the continuation only - `the shaft twitches once, the strand from the tip
   to her lip thickens and breaks, one drip runs down from her lip to her chin, her tongue comes out
   and licks the corner of her mouth`. That shape is safe.
3. If you want the emission itself, use the rope/path/count/beat wording from 1B in a clip whose
   first frame has the tip out of her mouth and her face in the splash zone.

## 5. Prompt words that backfire

| word | what comes back | use instead |
|---|---|---|
| `flushed cheeks`, `cheeks flushed` | hard red bands or blotches painted on the cheeks, in stills and clips alike (`v01`, `v05`, `q01/c1`, `q01/c2`) | `a light natural blush`, or nothing |
| `a scrotum below her hand` | the sac in front of the shaft, on the wrong side (`v02/v5`) | the depth-order list in 1A2 |
| `censored, mosaic censoring` | nothing; the picture comes back uncensored (`g01/e`) | post-process, section 5 |
| `a scrotum below her hand` | a sac in front of the shaft (`v02/v5`) | leave the scrotum out of a POV prompt; keep `pubic hair at the base` |
| `a lot of cum`, `excessive cum` | foam that grows over the skin | count the ropes, name where each lands, ask for translucency and sag |
| `bobbing` | one continuous slide, far too fast | down-hold-up with a duration in seconds |
| `the men moan` | an invented voice, usually the wrong register | one low short grunt, air pushed out, no word, at time T |
| `pov, from above` + `1boy` on Anima | a giant unexplained ass filling the frame | H3-Image for the arrangement, or the side view |

## 6. Censorship

The tags do not work: `censored, mosaic censoring` in an Anima prompt returns a clean uncensored
picture. Mosaic is a post-process. Fixed region, keeps the audio:

```
ffmpeg -i in.mp4 -filter_complex \
 "[0:v]split=2[a][b];[b]crop=140:230:195:495,pixelize=10:10[c];[a][c]overlay=195:495" \
 -c:a copy out.mp4
```

`crop` is `w:h:x:y` in output pixels; `pixelize` is the block size. Cover the *base and scrotum*
as well as the shaft - a mosaic that stops at the shaft reads as a mistake. For a softer look than
mosaic use a heavy gaussian blur on the same region (`boxblur=12:2`).

## 7. Shot grammar (what the references actually do)

The owner's six references share one structure; prompts that follow it read as real, prompts that
skip the seal read as a kiss.

1. **Reveal** - tongue out, mouth open, eyes up, before anything enters.
2. **Seal** - lips form a ring *behind* the glans. This is the single most important thing to say.
3. **Stroke** - down to take, up to release, 1.2 s (rough) to 2.2 s (slow); the seal holds on the
   way up so the shaft emerges wet.
4. **Held bottom** - a beat, a swallow, a breath out through the nose.
5. **Saliva** - a strand from the lower lip to the shaft, thinning, swinging, breaking.
6. **Eyes** - down at the cock while working, up at the viewer on the pull-off.
7. **Hands** - hers at the base, his on her head when he drives the pace.
8. **Sound** - wet suction, a small pop at the top, a nasal breath, one low male grunt.

## 8. Operational

- **Never let the clip introduce the penis.** A clip that must make one appear mid-shot produces
  the stick regardless of the prompt. Start with it already in her mouth (or already out, for a
  cumshot).
- **One camera, stated** - `The camera does not move`. Otherwise T2V cuts between angles by itself.
- **ComfyUI can leave a finished prompt in `queue_running`**, blocking everything after it. Its
  history entry is already written, so `POST /interrupt` clears it. Do it automatically.
- **Resolution** must be multiples of 32; 2:3 = 768x1152 for a clip, 896x1344 for the keyframe.
- **Hygiene**: renders go to `output/gl/<round>`, are pulled off, and the folder is deleted. PNGs
  keep the prompt in their metadata and both boxes serve `/view` and `/history` to the whole LAN
  with no auth. Uploads land in `input/gl_up` and are deleted with the round.
- Model files, workflows and the drivers are on cutestation at `~/goonlab/tools` (`lab.py` runs a
  JSONL batch, pulls the renders, cleans the box; `clean.py` deletes a round and only that round's
  history entries).

## 9. The LoRA route - what the field actually does

Survey (Civitai API, 2026-11-20) in `NSFW-RESEARCH.md`. Short version: no serious realistic NSFW
result is prompt-only. They run a **purpose-trained anatomy LoRA on the exact base** plus a
**second regional pass** over the genitals. For this lab that maps to four concrete moves, none of
which need a new pipeline:

| move | what to add | state |
|---|---|---|
| photoreal keyframe | **`krea2 sex 淫模`** on Krea 2, sub-LoRA `BJ` / `SBJ` (trigger `kreablowjob`, `krea2blow`), and `cum` / `FC` for the money shot | not downloaded |
| video | **`DR34ML4Y_H3_P1`** - a MiniMax H3 LoRA (`bl0wj0b`, `m15510n4ry`, `d0gg1e`, `d0wg1rl`), one more `LoraLoaderModelOnly` in our graph | not downloaded |
| photoreal edit / anchor | Qwen-Image-2.1 NSFW LoRAs (`NSFW LORA | Qwen Image 2.1`, `NSFW Qwen Image Edit Rapid AIO`) on the a03 insert step | not downloaded |
| anime (Anima) | nothing exists - train one with `research/style-lock/scripts/train_anima_lora.sh` (40 min on lame) or keep the prop insert | proposal |

Until one of those is in place, the prompt-level workarounds in section 1 are what we have, and they
do work - just expensively.

## 10. Not tested yet

- **First *and* last frame anchoring** to force one slow stroke at an exact duration
  (`MiniMaxH3ImageToVideo` accepts `last_frame`). The cleanest way to control pace; untried.
- **Ref2VA two-reference anchoring** (the girl + the prop, straight into the video model) - the
  prop route works for the still (A1) but has not been tried through the clip.
- **RelayVSR x2** on a finished clip (keeps the audio) to get the rim back after a 512-wide take.
  The workflow is on ampere; the first attempt died on an input path, not on the model.
- **The cum material wording** in B (translucency, sag, beading) - written, not yet rendered.
- **Multi-shot scenes**: the same girl in a 3-shot sequence (reveal / stroke / cumshot) with the
  keyframe of shot N+1 made by Qwen-Image-2.1 edit from the last frame of shot N.
- **Anima as the look, H3-Image as the layout**: animating an Anima Love Live frame with the prop
  inserted first, to get the anime-series look with correct anatomy.

