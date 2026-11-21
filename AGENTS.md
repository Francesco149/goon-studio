# Goon Studio: guide for the agent (read all of it before doing anything)

This repo is the explicit counterpart of **Love Live Studio** (`../lovelive-studio`). It has its
own app, its own gallery and its own rules. It is written for agents that are allowed to work
with adult NSFW material (DeepSeek and similar). Claude also works here, on a narrower scope set in
`CLAUDE.md`: engineering, setup, performance and non-explicit (ecchi-level) tests. Explicit
prompts, presets and reviewing explicit output stay with you. Claude's neutral jobs are in
`jobs/neutral/` and its renders in `sfw/`.

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

The user may paste the README bootstrap: "download the Goon Studio and set it up by following
AGENTS.md; I'm not technical". Do the whole thing for them, explaining as you go.

1. **Confirm the folder**: the session's workspace is the Studio repo. Read the README and this
   file first.
1b. **Account**: DSH Desktop is signed in with the user's DeepSeek account and runs on their
   credits - there is **no API key** to handle. If a model call fails with an auth or balance
   error, send them to Settings â†’ Account and platform.deepseek.com billing; never ask for a key.
   The first-run introduction should have been **"Full details"** with developer tools on; if the
   user sees a simplified chat, tell them to switch the transcript/usage detail to detailed.
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

| | Love Live Studio (`../lovelive-studio`) | Goon Studio (here) |
|---|---|---|
| content | SFW anime pictures | explicit stills and video |
| gallery | its own `my/`, `examples/` | `gallery/` and `my/` here |
| agent | Claude | DeepSeek and other NSFW-tolerant agents; Claude for engineering only (`CLAUDE.md`) |

- When the user says "the picture from the studio" or references an SFW image, look in
  `../lovelive-studio` (`my/rounds/`, `examples/`, and only the `public` records in its
  `my/library.json`). If it is private there, ask them to share it in that app; do not read
  `../lovelive-studio/my/private/`.
- Never write NSFW prompts, pictures or notes into `../lovelive-studio`. If a run needs an SFW
  reference, copy the file into this repo's `gallery/refs/` and use that copy.
- The two apps use different ports: Love Live Studio 8190, this one 8191.

## 2a. The page

- **Generate**: template, body type, framing, character/scene/prompt/negative, **quality**
  (Preview / Standard / Final = the measured 4/6/8 or 12/20/30 steps), size/steps/cfg, seed/count,
  reference picture, a live "what the model reads" preview and a time estimate. The reference slot
  takes a dropped/pasted picture, an uploaded file, or **"Pick from my pictures"** (the gallery
  picker). "Just made" shows the last 12; a job card shows elapsed time with per-job Stop
  (Shift+Esc stops all).
- **Video**: video recipe dropdown (POV blowjob, side deepthroat, paizuri, cum shot, anime POV
  bob), mode (i2v, i2v + act LoRA, first+last, ref2va, t2v), keyframe/last/second-reference slots
  with the same picker/paste/drop, LoRA + strength, length, size, seed, prompt. "Recent videos"
  sits next to it, and a clip's lightbox has **"Use the last frame as keyframe"** (PyAV, ffmpeg
  fallback) to chain the next one. Workflow model names fall back to the quantization the engine
  has (`*_int8_convrot` on ampere vs `*_w4a8_mixed` on an 8 GB card).
- **My pictures**: filter (all, loved/liked, private, shared, by the agent, clips), search,
  Select with Shift+click ranges, share/lock, trash. The lightbox has rating (click again to
  clear), a note (private notes stay in `my/private/`), Use these settings, variations, **Make it
  in Final** (same seed), Use as keyframe / reference, share toggle, trash.
- **Trash**: select, restore, delete forever, empty. **Rounds**: `my/rounds/*.json` (items are
  file strings or `{file, label}`, optional `question`); the user's round notes go to
  `my/feedback.jsonl` for the agent.

## 3. Author-only notes

`AGENTS.local.md` is git-ignored and only applies when the author of the repo is the one working
(the user who made the reference clips). It points at `~/Documents/uwu` and the gold-standard
clips, at the author's nix-lab copy for general generation findings, and at the **infrastructure
notes** (how to reach ampere, lame, maximus and bunker from this machine, and the fish/ssh
quirks). **Do not commit it, do not copy its contents into tracked docs, and do not read the
reference clips for other users.** If the file is missing, this is not an author session: use
only the public recipes.

## 4. Models and workflows

| job | model / workflow | notes |
|---|---|---|
| photoreal e-girl stills | Krea 2 Turbo NSFW v10 (nvfp4) + `wf_krea2_nsfw_8gb.json`, 6 steps, cfg 1 | 4 preview / 6 standard / 8 final; `docs/EGIRL.md` |
| photoreal facial / cum still | same, the `egirl_facial` and `egirl_cum` templates | `docs/FACIAL.md` |
| anime stills | Pink Alchemy Anima v2.9 + `wf_anima2.json`, 20-30 steps, cfg 4, er_sde/simple | 12 preview / 20 standard / 30 final; `docs/ANIME.md` |
| anime second pass | `wf_anima_hires.json`, denoise 0.30 | `docs/ANIME.md` |
| anime stills with a character LoRA | Pink + `wf_anima2_lora.json` (`LoraLoaderModelOnly`, node 48), 30 steps, cfg 4, strength 1.0 | the `anime_lz_*` templates (Lanzhu Zhong); registry and prompt shape in `docs/LORAS.md` |
| keyframes / photoreal stills | H3-Image `wf_h3img_4bte.json` (draft) / `wf_h3img_8gb.json` (final) | 4/6/8 steps, cfg 1 |
| photoreal video | H3 FL2VA `wf_h3vid_i2v.json` (Pika 6-step), 768x1152, 124 f | 4-step preview in `wf_h3vid_i2v_4step.json`; `docs/FACIAL.md`, `docs/ANIME.md` |
| video with an act LoRA | `wf_h3vid_i2v_lora.json` (node 21) | side deepthroat and titjob help; POV blowjob does not |
| cum-shot clip | `wf_h3vid_i2v_lora.json` + `h3nsfw/epic_cumshots` 0.6 | the `cumshot_high` / `cumshot_medium` (default) / `cumshot_low` dial, plus `cumshot_goopy`, `cumshot_mouth`, `cumshot_softening`. `docs/CUM-VIDEO.md` |
| identity edit | Qwen-Image-2.1 `wf_qwen21_edit1.json` | keeps the face, use for "same girl" edits |
| first+last clip | `wf_h3vid_i2v_fl.json` | last frame must be an edit of the first, not a new roll |
| ref2va clip | `wf_h3vid_ref2va6.json` | two reference pictures |

The app's **templates** (`kit/presets.json`) already carry the approved prompt blocks. Prefer
editing the character/scene fields over rewriting the whole prompt.

**Reanchor what frame 0 does not show.** H3 video only knows what is visible in the first frame
(i2v) or in the reference pictures (ref2va). Anything that appears later but is not on screen at
frame 0 - the glans of a cock that starts hidden in her mouth, a hand entering, cum, a second
person, a prop - is invented by the video model and usually wrong (the glans comes out the wrong
shape, the mouth stops reading as suction). When the clip needs it, give the model a picture of
it: `wf_h3vid_ref2va6.json` with two references (the pose/scene + the real cock/glans), or a
first+last pair whose last frame shows it (`wf_h3vid_i2v_fl.json`). Do not rely on the prompt to
describe something the model has never seen; reanchor it. The same applies to anything the model
has not learned and that is not on screen in the first frame.
The mixed-cock version of this rule is solved the other way round: **start on a head-out seal with
the real glans in frame 0 and have her take it in** (`docs/MIXED.md`). The glans is anchored
because it is visible, then hidden; no reveal is needed. A clip that reveals a glans hidden at
frame 0 will invent it. **Mixed reality is still unfinished - needs more research** (owner,
2026-11-21: the video dynamics are below the pure-anime BJs - one clip puffs, the other reads as
chewing - and the audio is unusable). The still/fill and the frame-0 anchoring hold; do not call
the video recipe proven.

## 4b. Sound is not solved

**Status: unfinished - needs more research** (owner, 2026-11-21). The generated audio is wrong:
the strokes crunch (like biting something), the slurp sounds like noodles, and nothing is synced
to the action. The owner's reference for good SFX is the opalu clips (author-only,
`AGENTS.local.md`). Sound work is its own session; read `docs/SOUND.md` before touching it and
**never tell the user the sound is fine**. Treat the model audio as a scratch track; a separate
Foley pass or a dedicated audio tool is the likely answer.

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
- Cum (2026-11-21 session 5): the recipe works and is a **dial**, not one look. `epic_cumshots` at
  0.6, 768x1152/124f, the P1 or wide-gap keyframe. Three tiers in `kit/presets.json`:
  `cumshot_high` (k14, the owner's maximum exaggeration standard), **`cumshot_medium` (the
  default)**, `cumshot_low`; plus the variant looks `cumshot_goopy` (wax-like extreme, owner calls
  it unrealistic), `cumshot_mouth` (clean swallow) and `cumshot_softening` (messy, keeps sucking as
  he goes soft). Hard rules: one rope per pulse out of the slit, never a split into two cords;
  three decaying pulses; the rope is an inch or two long and **hits her face and stops there** with
  a little splash on impact - it must never arc over her head; and **the glans stays bare** - which
  is a volume effect, met by the medium tier and below, and not fixable by wording at high volume.
  Never use "bead/blob/ball/glob" for the emission. Judge the material at 1:1, never on a
  downscaled sheet. **Not finished** (owner verdict at the close of session 5): the in-flight cum
  looks like far more than what lands (**mass conservation** - the top defect, untouched so far),
  the low tier atomises into mist, and occasional unnatural splitting remains. `docs/CUM-VIDEO.md`
  has the dial, the wording ladder, the open defects, the measured costs and the failed routes; do
  not repeat them.

## 6. Running a round

1. Put jobs in `jobs/<round>.jsonl` (one JSON object per line, `name`, `prompt`, `seed`, ...).
2. Run the batch: `python tools/lab.py --wf wf_...json --jobs jobs/<round>.jsonl --box local --sub gl/<round> --out gens/<round>`.
   **On the user's own machine the box is always `local`** (127.0.0.1:8188, the ComfyUI that
   `kit\start.ps1` runs). `ampere` (10.0.10.240) and `lame` (10.0.10.56) only exist on the author's
   home network for experiments - never assume them, never go looking for them on a normal install.
   Every recipe in `docs/` must be runnable on `local` with 8 GB, which is the target; the boxes
   are just faster ways to try a variant. `tools/lab.py` cleans only its own outputs afterwards.
3. Make a sheet: `python tools/sheet.py analysis/<round>.jpg gens/<round> --cols 4 --thumb 420`.
4. Look at the sheet, write down what changed in `docs/` (or the round log), keep the prompts in
   `jobs/`.
5. Do not leave renders outside `gallery/`, `gens/`, `analysis/`, `sfw/` (Claude's neutral renders) or the local engine's
   `gl/` scratch folders.

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
the exception - it does not fit and needs a 24 GB card (`docs/CUM-VIDEO.md`).

The **8 GB optimization pass is done** (2026-11-20): measured peak VRAM, per-workflow flags,
preview/standard/final step counts, the H3 4B text encoder, RelayVSR x2, and a speculative GTX
1070 section are in `docs/PERFORMANCE-8GB.md`. The measured launch pair is
`--use-ck-attention --fast fp16_accumulation`; 4 steps is a preview, 6 the standard, 8 the final
(same seed), and H3 video is 4-step preview / 6-step final. Do not re-derive this from scratch;
re-run `tools/experiments/bench_engine.ps1` and `tools/experiments/bench.py` if the hardware or
ComfyUI version changes.
