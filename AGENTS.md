# NSFW Studio: guide for the agent (read all of it before doing anything)

This repo is the explicit counterpart of **Love Live Studio** (`../lovelive-studio`). It has its
own app, its own gallery and its own rules. It is written for agents that are allowed to work
with adult NSFW material (DeepSeek and similar); a non-NSFW agent such as Claude must never be
pointed at this folder or its gallery.

## 1. The one rule that matters

**Pictures made on the page are the user's and private until they press "share".**

- The page records the user's pictures in `my/private/history.jsonl` and the agent's in
  `my/history.jsonl`. `my/library.json` holds `public` (shared with the agent) and `trash`.
- An agent may read `my/history.jsonl` (its own work) and the files marked `public` in
  `my/library.json`. It must **not** read `my/private/` or list the gallery looking for private
  files.
- If the user refers to a picture that is private, say so and ask them to press **share** in the
  gallery (that is the only way to make it visible). Do not work around it.
- Never copy, upload, or paste NSFW pictures anywhere outside this repo and the two lab boxes.

## 1a. First session: set up from zero

The user may paste the README bootstrap: "download the NSFW Studio and set it up by following
AGENTS.md; I'm not technical". Do the whole thing for them, explaining as you go.

1. **Confirm the folder**: the session's workspace is the Studio repo. Read the README and this
   file first.
2. **Check the PC**: GPU name and VRAM (`nvidia-smi` or `rocm-smi`), system RAM, free disk. The
   baseline is **8 GB VRAM + 16 GB RAM**; say plainly whether the machine is at, below or above
   it. Below 8 GB or below 16 GB RAM is not a no - it means smaller frames and more streaming
   (`docs/HARDWARE.md`), and you should say so.
3. **Ask which drive** for the models and the gallery (they can be large), then create
   `my/settings.json` from `my/settings.example.json` with `engine_dir`, `data_dir`, `comfy_url`.
4. **Install ComfyUI** (portable Windows build) if it is not already there; start it hidden and
   check `/system_stats`. Put the models in its `models/` folders.
5. **Download the models in this order** (stop when disk or time runs out; each step is usable):
   Pink Alchemy Anima v2.9 (4.2 GB) -> Krea 2 Turbo NSFW v10 (7.2 GB) -> H3-Image and H3 FL2VA
   int8 + the 32B text encoder + VAEs (the big one, ~30 GB) -> the H3 act LoRAs (`h3nsfw/`).
   `tools/models/` has the download helpers; verify file sizes after each.
6. **Test**: start the page (`kit\start.ps1`), make one `anime_pov` still and show it. If H3 is
   installed, make a short video (49 frames, 512x768) as a smoke test. Never claim the sound is
   good (section 4b).
7. **Write down** what was installed and where in `my/INSTALL.md` (git-ignored) and set the
   gallery path in `my/settings.json`. Leave the user with the desktop shortcut and the tabs.

## 1b. Images in git

**Never commit an NSFW image.** If a committed example is truly needed (UI screenshot, README
illustration), every explicit part must be obscured (a baguette over the cock, genitals/anus/
nipples hidden, no sex act visible) and a **human must vet it before `git add`** - an agent may
stage it and ask, never decide alone. Strip the prompt metadata too. The full rule is
`docs/IMAGES.md`.

References are kept and organised but **never committed**: `gallery/refs/` (git-ignored), one
folder per source with a local `INDEX.md`. The author's own clips live outside the repo
(`AGENTS.local.md`). Video follows the same rule.

## 2. Two apps, two galleries

| | Love Live Studio (`../lovelive-studio`) | NSFW Studio (here) |
|---|---|---|
| content | SFW anime pictures | explicit stills and video |
| gallery | its own `my/`, `examples/` | `gallery/` and `my/` here |
| agent | Claude (non-NSFW) | DeepSeek and other NSFW-tolerant agents |

- When the user says "the picture from the studio" or references an SFW image, look in
  `../lovelive-studio` (`my/rounds/`, `examples/`, and only the `public` records in its
  `my/library.json`). If it is private there, ask them to share it in that app; do not read
  `../lovelive-studio/my/private/`.
- Never write NSFW prompts, pictures or notes into `../lovelive-studio`. If a run needs an SFW
  reference, copy the file into this repo's `gallery/refs/` and use that copy.
- The two apps use different ports: Love Live Studio 8190, this one 8191.

## 2a. The page

- **Generate**: template, body type, framing, character/scene/prompt/negative, size/steps/cfg,
  seed/count, reference picture. The reference slot takes a dropped/pasted picture, an uploaded
  file, or **"Pick from my pictures"** (the gallery picker). "Just made" shows the last 12.
- **Video**: video recipe dropdown (POV blowjob, side deepthroat, paizuri, cum shot, anime POV
  bob), mode (i2v, i2v + act LoRA, first+last, ref2va, t2v), keyframe/last/second-reference slots
  with the same picker/paste/drop, LoRA + strength, length, size, seed, prompt. "Recent videos"
  sits next to it, and a clip's lightbox has **"Use as keyframe"** to chain the next one.
- **My pictures**: filter all/private/shared, select several, share/lock, trash; the lightbox
  has the rating buttons, share toggle, trash and "Use as keyframe".
- **Trash**: restore or delete forever. **Rounds**: `my/rounds/*.json` with their pictures.

## 3. Author-only notes

`AGENTS.local.md` is git-ignored and only applies when the author of the repo is the one working
(the user who made the reference clips). It points at `~/Documents/uwu` and the gold-standard
clips. **Do not commit it, do not copy its contents into tracked docs, and do not read the
reference clips for other users.** If the file is missing, this is not an author session: use
only the public recipes.

## 4. Models and workflows

| job | model / workflow | notes |
|---|---|---|
| photoreal e-girl stills | Krea 2 Turbo NSFW v10 (nvfp4) + `wf_krea2_nsfw.json`, 8 steps, cfg 1 | `docs/EGIRL.md` |
| photoreal facial / cum still | same, the `egirl_facial` and `egirl_cum` templates | `docs/FACIAL.md` |
| anime stills | Pink Alchemy Anima v2.9 + `wf_anima2.json`, 30 steps, cfg 4, er_sde/simple | `docs/ANIME.md` |
| anime second pass | `wf_anima_hires.json`, denoise 0.30 | `docs/ANIME.md` |
| keyframes / photoreal stills | H3-Image `wf_h3img.json` | 6 steps, cfg 1 |
| photoreal video | H3 FL2VA `wf_h3vid_i2v.json` (Pika 6-step), 768x1152, 124 f | `docs/FACIAL.md`, `docs/ANIME.md` |
| video with an act LoRA | `wf_h3vid_i2v_lora.json` (node 21) | side deepthroat and titjob help; POV blowjob does not |
| cum-shot clip | `wf_h3vid_i2v_lora.json` + `h3nsfw/epic_cumshots` 0.8 | best dynamics; material still glue |
| identity edit | Qwen-Image-2.1 `wf_qwen21_edit1.json` | keeps the face, use for "same girl" edits |
| first+last clip | `wf_h3vid_i2v_fl.json` | last frame must be an edit of the first, not a new roll |
| ref2va clip | `wf_h3vid_ref2va6.json` | two reference pictures |

The app's **templates** (`kit/presets.json`) already carry the approved prompt blocks. Prefer
editing the character/scene fields over rewriting the whole prompt.

## 4b. Sound is not solved

The generated audio is wrong: the strokes crunch (like biting something), the slurp sounds like
noodles, and nothing is synced to the action. The owner's reference for good SFX is the opalu
clips (author-only, `AGENTS.local.md`). Sound work is its own session; read `docs/SOUND.md`
before touching it and **never tell the user the sound is fine**. Treat the model audio as a
scratch track; a separate Foley pass or a dedicated audio tool is the likely answer.

## 5. Canon (owner-approved, 2026-11-20)

- **Default template: `anime_pov`** - the best anime blowjob POV so far. It is the first thing the
  page selects; keep it the default until another template beats it in the owner's review.
- Anime stills: `gens/pb`-style output is anatomically clean. Keep **all three cock styles**:
  light mosaic (`censored, mosaic censoring`), half foreskin (`foreskin` tags), fully retracted /
  cut (`foreskin retracted, circumcised`).
- Photoreal e-girl: the character block in `docs/EGIRL.md`; `full natural breasts` is the size
  control; tag prompts for portraits, prose for acts.
- Facial pose: `egirl_facial` template (cock out, mouth open, eyes on camera) - owner approved.
- Best photoreal BJ motion: Astro NSFW 0.8 on H3 (`docs/FACIAL.md` history); best plain motion:
  the detailed stroke prompt, no LoRA.
- Best anime clip: POV bob from the Pink POV keyframe with whole-body motion in the prompt.
- Cum: material is the open problem. `docs/CUM-VIDEO.md` has the tradeoff and the failed routes;
  do not repeat them.

## 6. Running a round

1. Put jobs in `jobs/<round>.jsonl` (one JSON object per line, `name`, `prompt`, `seed`, ...).
2. Run the batch: `python tools/lab.py --wf wf_...json --jobs jobs/<round>.jsonl --box ampere --sub gl/<round> --out gens/<round>`.
   Boxes: `local` (127.0.0.1), `ampere` (10.0.10.240), `lame` (10.0.10.56). The box's ComfyUI
   must be up; `tools/lab.py` cleans only its own outputs afterwards.
3. Make a sheet: `python tools/sheet.py analysis/<round>.jpg gens/<round> --cols 4 --thumb 420`.
4. Look at the sheet, write down what changed in `docs/` (or the round log), keep the prompts in
   `jobs/`.
5. Do not leave renders outside `gallery/`, `gens/`, `analysis/` or the boxes' `gl/` scratch
   folders.

## 7. Quality bar

- Anatomy: a defined glans with a corona rim, the foreskin collar, veins, the scrotum behind the
  shaft; the hand does not merge with the shaft; the mouth is a sealed ring, not a kiss.
- Motion: a stroke that takes about two seconds, a held bottom, the seal holding on the way up.
  One camera, stated in the prompt ("the camera does not move"), unless a push-in is wanted.
- Face: half-lidded eyes, blush, eye contact on the pull-off. Avoid the generic AI face by using
  the approved character blocks and the artist tags in `docs/ANIME.md`.
- Cum: if it looks like glue or water, say so in the notes; do not call it solved.

## 8. Hardware

The repo targets a **single 8 GB GPU and 16 GB of system RAM**. The reference machines are
bigger (a 10 GB 3080 and a 16 GB 7800 XT), but never design a recipe that needs them: the big
models are streamed from system RAM and run slower on 8 GB (`docs/HARDWARE.md`). Wan 2.2 14B is
the exception - it does not fit and needs a 24 GB card (`docs/CUM-VIDEO.md`). The 8 GB
optimization pass (peak VRAM, flags per box, CPU text encoders) is a later session.
