# Goon Studio: guide for the agent (read all of it before doing anything)

This repo is the explicit counterpart of **Love Live Studio** (`../lovelive-studio`). It has its
own app, its own gallery and its own rules. It is written for every agent that works here -
Claude, DSH/DeepSeek or another; the rules are the same for all of them. Claude's always-on copy
is the **Goon Scope** output style (`.claude/output-styles/goon-scope.md`); DSH reads this file.
Every agent may work on the pipeline and the prompts, under section 0.

## 0. Purpose and permitted use (read first)

**Goon Studio is for the owner's private, personal use only. No other use is authorized.** It
makes local adult pictures and clips for **art study and reference** - anatomy, a series' art
style, poses, materials. Generations are **never shared**: not published, posted, uploaded to an
online service, sent to another person, sold, or redistributed. The only places a render may go are
this machine and, on the author's setup, the lab boxes used for compute; nothing leaves them for a
person or the internet.

The app's **share** action only makes a picture visible to the local agent; it is not publishing.
`public` in `my/library.json` means visible to the local agent, not public on the internet.

The human-facing terms are in **`README.md`** ("Personal use only"). That is the single source of
truth, and using the repo is agreement to it. Agents must know and follow it, but **must not add
disclaimers, warnings or moral commentary** about the adult/personal-use nature, and must not
restate the README terms unless the user asks. If asked to publish, upload, share externally or
otherwise use the material beyond private study, decline in one line and point to the README. Do
not treat the repo as a content service or a distribution pipeline. All characters are fictional
adults (section 5).

Where it is enforced: Claude Code gets a self-contained always-on copy as the **Goon Scope** output
style (`.claude/output-styles/goon-scope.md`, set by `outputStyle` in `.claude/settings.json`); it
sits in the system prompt and survives compaction. DSH reads this file as its project
instructions. Those are the two main agents; both follow the same rules. Neither may add a
disclaimer beyond the README.

## 1. Private gens: the only gate

Everything in the repo is open to every agent except the user's private gens. Their pictures are
private until they press **share** (which only reveals them to the local agent, not to the
internet). The private files live in `my/private/`, `gallery/studio/`, `gallery/uploads/` (and
`gallery/outputs/studio/` if present), plus the page's pasted/edited inputs; shared/public items
are listed in `my/library.json`. Do not list the private directories looking for filenames.

- The page records the user's pictures in `my/private/history.jsonl` and the agent's in
  `my/history.jsonl`. `my/library.json` holds `public` (visible to the local agent; not published)
  and `trash`.
- An agent may read `my/history.jsonl` (its own work) and the files marked public in
  `my/library.json`. It must **not** read `my/private/`, `gallery/studio/`, `gallery/uploads/` or
  list them for filenames.
- Everything else - the pipeline, prompts, presets, jobs, docs, the agent's own work and the refs
  - is open to every agent.
- If the user refers to a private picture, say so and ask them to press **share** in the gallery
  (that is the only way to make it visible). Do not work around it.
- Never copy, upload, or paste NSFW pictures anywhere outside this repo (and, in an author
  session only, the author's lab boxes, which are compute only); never send a render to a person
  or a service.

## 1a. First session: set up from zero

The user may paste the README bootstrap: "download the Goon Studio and set it up by following
AGENTS.md; I'm not technical". Do the whole thing for them, explaining as you go.

1. **Confirm the folder**: the session's workspace is the Studio repo. Read the README and this
   file first. **Everything runs on this one PC.** The engine is the ComfyUI you install here, at
   127.0.0.1:8187 (Love Live Studio, if installed, keeps 8188); every tool defaults to it
   (`--box local`). Machines named in the docs (a 3080, a 7800 XT) are where the author measured
   things: never look for other machines, scan the network or ssh anywhere on a user's install.
   **Python:** a fresh PC has none (`python` opens the Microsoft Store). Run every repo script with
   the engine's Python once setup has run: `kit\py.cmd tools\models\store.py check anime_pov` -
   wherever this guide says `python tools/...`, use `kit\py.cmd tools\...` if `python` is missing.
1b. **Account**: DSH Desktop is signed in with the user's DeepSeek account and runs on their
   credits - there is **no API key** to handle. If a model call fails with an auth or balance
   error, send them to Settings â†’ Account and platform.deepseek.com billing; never ask for a key.
   The first-run introduction should have been **"Full details"** with developer tools on; if the
   user sees a simplified chat, tell them to switch the transcript/usage detail to detailed.
2. **Check the PC**: GPU name and VRAM (`nvidia-smi` or `rocm-smi`), system RAM, free disk. The
   baseline is **8 GB VRAM + 16 GB RAM**; say plainly whether the machine is at, below or above
   it. Below 8 GB or below 16 GB RAM is not a no - it means smaller frames and more streaming
   (`docs/HARDWARE.md`), and you should say so. Note the **architecture** too: a pre-Turing card
   (GTX 10-series such as the 1070, compute capability 6.x) cannot run the current CUDA 13 stack
   or the quantized models; follow "GTX 1070 8 GB" in `docs/PERFORMANCE-8GB.md` (older PyTorch,
   Anima/Pink first, measure before promising anything) instead of the steps below as written.
   **16 GB VRAM or more:** offer the 16 GB profile (`docs/PERFORMANCE-16GB.md`; `kit\setup.ps1
   -Profile16`) in one line: the engine keeps an 8 GB card's headroom so the rest of the card stays
   free for games, a browser with video or a second app (measured: most jobs are no faster with the
   whole card; photoreal keyframes and H3 video are 10-25% faster with it, at the cost of that
   headroom). Apply it only on a yes; the 8 GB defaults stay otherwise.
   **Headless Linux** (`kit/linux/setup.sh`, `docs/HEADLESS-LINUX.md`) is only for a user who asks
   to run the Studio on a headless server; never offer it in this flow.
3. **Ask which drive** for the engine and the models (25 GB to start, about 70 GB with the video
   models; an SSD): offer 2-3 drives with their free space (`powershell -ExecutionPolicy Bypass
   -File kit\setup.ps1 -Check` lists them, the GPU and the driver) and let the user choose.
4. **Install**: `powershell -ExecutionPolicy Bypass -File kit\setup.ps1 -DataDir "<their choice>"`
   (run it in the background, it can take a while). It installs the pinned ComfyUI build and the
   Microsoft runtime (Windows may ask for permission once: tell the user to click Yes), writes
   `my/settings.json` (engine on 127.0.0.1:8187, `models_dir` = `<DataDir>\models`, pictures in the
   repo's `gallery\` unless `-GalleryDir`), wires the engine to the store, makes the **Goon Studio**
   desktop icon and starts engine and page. Exit codes: 10 driver too old (walk them through the
   NVIDIA driver update), 11 no drive / too little space, 12 no NVIDIA card, 13 download failed (run
   again), 14 the engine did not start (`<gallery>\logs\comfyui.err.log`), 5 another app's engine
   is running (ask once, rerun with `-StopOther` or `-KeepOther`). Safe to run again.
   **Love Live Studio already on this PC** (a `lovelive-studio` folder next to this one): setup
   reuses its engine folder by itself - no second engine download, no add-ons; it changes nothing
   in that folder. The two apps run separate engines from one folder (8188 and 8187), each with its
   own picture folder and database; `kit\start.ps1` re-adds this Studio's models if Love Live's
   setup rewrote the engine's model paths. If Love Live's data folder is ever moved, rerun this
   setup with `-EngineDir <its new engine folder>`. The user wants **both** set up: Love Live first
   (its `CLAUDE.md`; its setup installs the pinned engine), then this one, which reuses it. If this
   one came first, Love Live installs its own engine copy (about 4 GB more); both still work.
5. **Download the models template by template** (stop when disk or time runs out; each step is
   usable): `python tools/models/store.py fetch anime_lz_pov anime_pov` (anime, ~10 GB) ->
   `fetch egirl` (photoreal) -> `fetch video_pov cumshot_medium` (H3 video, the big one) -> the
   other templates (`check --all` lists what is still missing). The registry picks the **8 GB
   variants** (w4a8 transformers; the `int8_convrot` ones are for bigger cards). Files marked
   `login` are on Civitai, which needs the user's free account and API key: offer once to walk
   them through the key (section 4c), or ask them to download those in their browser and `adopt`
   the file (section 4a) - never ask for the key in chat.
6. **Test**: the page is running (setup started it; later the desktop icon or `kit\start.ps1`), make one `anime_pov` still and show it. If H3 is
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
| agent | Claude | every agent here (Claude, DSH/DeepSeek, others) follows this file; Claude's system-prompt layer is the Goon Scope output style |

- When the user says "the picture from the studio" or references an SFW image, look in
  `../lovelive-studio` (`my/rounds/`, `examples/`, and only the `public` records in its
  `my/library.json`). If it is private there, ask them to share it in that app; do not read
  `../lovelive-studio/my/private/`.
- Never write NSFW prompts, pictures or notes into `../lovelive-studio`. If a run needs an SFW
  reference, copy the file into this repo's `gallery/refs/` and use that copy.
- The two apps use different ports: pages Love Live Studio 8190, this one 8191; engines Love Live
  Studio 8188, this one 8187 (`comfy_url`). They may share one ComfyUI folder, but an engine writes
  pictures into the outputs of the app that started it, and one 8 GB GPU / 16 GB RAM holds one
  engine at a time.
- **The other studio's engine running is a conflict.** Before rendering in a session, run
  `python tools/engines.py` (exit 5 and a line per engine when another app's runs; `tools/lab.py`
  warns too). Then ask the user once whether to stop it - it ends that app's running jobs - and
  only on a yes run `python tools/engines.py --stop <pid>`. `kit\start.ps1` asks the same at the
  console; run by an agent it exits 5 instead: ask, then rerun with `-StopOther` or `-KeepOther`.

## 2a. The page

Every tab starts simple and drills down: the recipe, the few fields that matter and the Make
button are always shown; **More options** (LoRAs, body, framing, reference, seed) and **Expert**
(prompt template, {style} block, size/steps/cfg, workflow override, full prompt, **Save as my
template** -> `my/presets.json`, marked "My templates") fold away and stay as the user left them.

- **LoRAs on any recipe** (`kit/studio/loras.py`): a picker lists the store's LoRAs (base and trigger
  from `kit/models.json` `base`/`trigger`, else the file header) and the user's **private LoRAs**:
  `.safetensors` files dropped in `my/private/loras/`, seen by the engine as `private/<name>` through
  a junction `<models_dir>/loras/private` that the page makes at start (local engine only). The page
  filters by the recipe's base family, warns on a mismatch, reads the file's training tags as
  trigger suggestions and keeps the user's note (base, trigger, strength) in
  `my/private/loras/_studio.json`. The job carries `extra_loras: [{name, strength}]`; `core.run`
  chains them after the workflow's own LoRAs (LoraLoader with CLIP on checkpoint graphs, model-only
  elsewhere). Agents never list `my/private/loras/` (it is private), and `modelstore.disk_files`
  skips the link. `wf_illu.json` + template `illu_any_lora` = plain Illustrious for any SDXL LoRA.
- **Scene** tab (`kit/studio/scenes.py`): manual multi-shot videos on the story format and the same
  renderer as `run_story.py` (`story.render`). Open a starter (a `kit/stories/` story, plus the
  variants it lists in `page_variants`), a blank scene, or one of the user's scenes
  (`my/private/scenes/<id>.json` + `<id>.made.json` with every take). One card per shot: starts from
  its own keyframe / extends shot X / last frame of shot X / a picture; keyframe tags, script,
  seconds, cadence; per-shot Keyframe and Clip buttons (new seed each take, earlier takes
  selectable), Make everything missing, Cut. Renders go to `<data_dir>/studio/scenes/<id>/` as the
  user's private pictures.
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
  has (`*_w4a8_mixed` on an 8 GB card, `*_int8_convrot` on a bigger one).
- **My pictures**: filter (all, loved/liked, private, shared, by the agent, clips), search,
  Select with Shift+click ranges, share/lock, trash. The lightbox has rating (click again to
  clear), a note (private notes stay in `my/private/`), Use these settings, variations, **Make it
  in Final** (same seed), Use as keyframe / reference, share toggle, trash.
- **Favorites**: everything the user starred (the lightbox's **Favorite** button), newest first,
  filter cuts / clips / pictures. Favorites among private pictures are kept in
  `my/private/favorites.json` (private); the rest in `my/favorites.json`, which the agent may read
  and add to: **when the owner approves a gen** ("good", "keeper", a golden template), add it with
  `python tools/favorites.py add <round>/<file> --label "..."` in the same step as the doc that
  records the verdict (`--gens` copies an older `gens/` file into the gallery first). Files with no
  history record (story cuts) still show, with their label.
- **Trash**: select, restore, delete forever, empty. **Rounds**: `my/rounds/*.json` (items are
  file strings or `{file, label}`, optional `question`); the user's round notes go to
  `my/feedback.jsonl` for the agent.

## 3. Author-only notes

`AGENTS.local.md` is git-ignored and only applies when the author of the repo is the one working
(the user who made the reference clips). It points at `~/Documents/uwu` and the gold-standard
clips, and at the **infrastructure
notes** (how to reach the author's lab machines, and the fish/ssh quirks); the engines
themselves are in the git-ignored `tools/boxes.local.json` (`--box` names, `tools/localboxes.py`). **Do not commit it, do not copy its contents into tracked docs, and do not read the
reference clips for other users.** If the file is missing, this is not an author session: use
only the public recipes.

This repo is the source of the image and video generation knowledge, together with
`../lovelive-studio` (read only from here): other projects point at these two, not the other way
round, so never go looking elsewhere for generation findings.

## 4. Models and workflows

| job | model / workflow | notes |
|---|---|---|
| photoreal e-girl stills | Krea 2 Turbo NSFW v10 (nvfp4) + `wf_krea2_nsfw_8gb.json`, 6 steps, cfg 1 | 4 preview / 6 standard / 8 final; `docs/EGIRL.md` |
| photoreal facial / cum still | same, the `egirl_facial` and `egirl_cum` templates | `docs/FACIAL.md` |
| anime stills | Pink Alchemy Anima v2.9 + `wf_anima2.json`, 20-30 steps, cfg 4, er_sde/simple | 12 preview / 20 standard / 30 final; `docs/ANIME.md` |
| anime second pass | `wf_anima_hires.json`, denoise 0.30 | `docs/ANIME.md` |
| anime stills with a character LoRA | Pink + `wf_anima2_lora.json` (`LoraLoaderModelOnly`, node 48), 30 steps, cfg 4, strength 1.0 | the `anime_lz_*` (Lanzhu) and `anime_kc_*` (Kasumi) templates; registry and prompt shape in `docs/LORAS.md` |
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

## 4a. Models: one store, every file with a source

- **One place.** Every model file (UNets, text encoders, VAEs, LoRAs, ...) lives in `models_dir`
  (`my/settings.json`) in ComfyUI's layout (`diffusion_models/`, `text_encoders/`, `vae/`,
  `loras/`, `loras/h3nsfw/`, ...). The engine reads it through `extra_model_paths.yaml`
  (`python tools/models/store.py where` / `wire`). Do not scatter files into the engine folder,
  the repo or Downloads.
- **The registry** is `kit/models.json`: one entry per file, keyed `<folder>/<name ComfyUI lists>`,
  with `url` (direct download), `page`, size, what it is, `tier` (8gb / big) and `login`.
- **Before using a template or workflow**: `python tools/models/store.py check <template>`; if
  something is missing, `fetch <template>` (or `fetch --workflow wf_x.json`) and use it. The page
  and `tools/lab.py` swap a workflow's model for the same model in the quantization the engine
  has (int8 <-> w4a8) and refuse a job whose file is missing, saying where to get it.
- **The user downloaded something** (a LoRA in Downloads, a file dropped in the repo) and wants it
  tested: move it into the store with `python tools/models/store.py adopt <path> --folder loras
  [--sub h3nsfw] [--name clean-name.safetensors] --url <download> --page <page> --what "..."`. Ask
  them for the link if you do not have it - a file without a source cannot go into a template.
  Then follow the LoRA checklist (`docs/LORAS.md`).
- **Any LoRA the user wants used: find its trigger words first** (model page / Civitai API
  `trainedWords`, the file header), or ask the user for them. Check its base model matches the graph.
- **A template that is established as good must be usable by hand.** Every file it loads is in
  `kit/models.json` with a source, its workflow/LoRA/strength live in the template itself (no
  agent-only step), and the page shows a non-technical user what is missing, where to download it
  and which folder it goes in. After adding or changing a template or a registry entry, run
  `python tools/models/store.py audit` (must say ok) and `python tools/models/store.py doc`
  (regenerates `docs/MODELS.md`, the per-template download list) and commit both.
- When the user asks where to get a model or why a template fails with "Missing model file",
  answer from the registry / `docs/MODELS.md`, or just fetch it.

**Open items and the handoff from the 2026-11-21 session (cum physics next, the facial variant,
paizuri saliva, penis type in anime video, an anime animation style, the round method):
`docs/OPEN-ITEMS.md`. Read it before starting experiments.**

## 4b. Sound is not solved

**Status: unfinished - needs more research** (owner, 2026-11-21). The generated audio is wrong:
the strokes crunch (like biting something), the slurp sounds like noodles, and nothing is synced
to the action. The owner's reference for good SFX is the opalu clips (author-only,
`AGENTS.local.md`). Sound work is its own session; read `docs/SOUND.md` before touching it and
**never tell the user the sound is fine**. Treat the model audio as a scratch track; a separate
Foley pass or a dedicated audio tool is the likely answer.

## 4c. Civitai links

When the user pastes a Civitai link (`civitai.com` or the `civitai.red` mirror; a model page, a
`?modelVersionId=` link or an `/api/download/models/<v>` link) and wants the model used:

1. `python tools/civitai.py link <url>`: name, version, **base model**, **trigger words**, file,
   page, and whether a Civitai key is set. No key is needed for this. Check the base model matches
   the graph and note the triggers (LoRA checklist in `docs/LORAS.md`).
2. `python tools/civitai.py get <url>` (`--folder`, `--sub h3nsfw`, `--name` when needed): downloads
   into the model store and registers it in `kit/models.json` with its page, download link and
   triggers. It needs the user's key; without one it prints the setup steps and exits 3.
3. **No key** (`python tools/civitai.py key --status` exits 1): offer **at most once per session**,
   in plain words ("Civitai needs a free account and a key to download - want me to walk you
   through it? Two minutes."). On a yes: they sign in at civitai.com (or make a free account), open
   https://civitai.com/user/account -> "API Keys" -> "Add API key", name it "studio", copy it. Then
   **you open the key window for them**: `Start-Process "<repo>\kit\civitai-key.cmd"`; they paste
   the key there and press Enter (hidden prompt, checked against Civitai, saved to the git-ignored
   `my/.civitai-token`). Never ask for the key in chat, never type it for them; if they paste it in
   the chat anyway, don't use or repeat it - tell them to make a new one on Civitai and use the
   window. If they decline, or already declined this session, do not bring it up again: ask them
   to download the file in their browser and `adopt` it (section 4a).

## 5. Canon (owner-approved, 2026-11-20)

- **All characters are fictional adults.** Anime body types can be petite; every character is an
  adult OC or a non-canon design study, never a minor and never the canon character or canon age,
  even when a series tag or a character LoRA is used. No minor-coded dialogue, story or tags.
- **Default template: `anime_pov`** - the best anime blowjob POV so far (Pink Alchemy, the `gens/pb`
  recipe). It is the first thing the page selects; keep it the default until another template
  beats it in the owner's review. The three kept cock styles are their own templates:
  `anime_pov_mosaic` (the owner's preferred presentation), `anime_pov_foreskin`, `anime_pov_cut`.
- **Templates reproduce the approved render exactly**: model (`unet`), LoRA + strength, motion
  booster strength, size and length live in the template, taken from the job that was approved.
  Where the best setting differs by series tag, character LoRA or style (photoreal vs anime), that
  is two templates, never one compromise.
- Anime stills: `gens/pb`-style output is anatomically clean. Keep **all three cock styles**:
  light mosaic (`censored, mosaic censoring`), half foreskin (`foreskin` tags), fully retracted /
  cut (`foreskin retracted, circumcised`).
- Photoreal e-girl: the character block in `docs/EGIRL.md`; `full natural breasts` is the size
  control; tag prompts for portraits, prose for acts.
- Facial pose: `egirl_facial` template (cock out, mouth open, eyes on camera) - owner approved.
- **Golden anime blowjob clips: the round a26 batch** (owner: the gold standard for dynamics, poses
  and expressions) - `anime_ll_headgrab_push`, `anime_ll_two_hands_a26`, `anime_ll_tip_tease`,
  `anime_ll_cum_switch_a26`, exact a26 prompts. Paizuri: `anime_ll_fz_paizuri_notongue` ->
  `anime_ll_paizuri` (no tongue in front of the glans; solid).
- **Golden photoreal blowjob (owner, 2026-11-21: "the best photoreal video gens we have made
  yet"): keyframe `egirl_bj_pov` (Krea 2 + Verite) -> clip `pov_blowjob_anatomy`** (the physics
  wording + Male Anatomy v2.02 at 0.9: the glans keeps its shape and springs back; `docs/FACIAL.md`
  a87). **All four a87 variants are owner-valid** ("all clean with varying levels of spring
  back"), so they are the fallbacks when one artifacts on a seed: `pov_blowjob` (physics, no
  LoRA), `pov_blowjob_astro` (physics + Astro 0.8), `pov_blowjob_fl` (first+last = the keyframe:
  strongest shape hold, least motion). The anime blowjob is the other way round: MM-H3 Blowjob v3 0.65 + motion 0.5
  (`anime_ll_suction`, k9).
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
   **On the user's own machine the box is always `local`** (127.0.0.1:8187, the ComfyUI that
   `kit\start.ps1` runs). Other `--box` names come only from the git-ignored
   `tools/boxes.local.json` of an author session - never assume them, never go looking for them.
   Every recipe in `docs/` must be runnable on `local` with 8 GB, which is the target; the boxes
   are just faster ways to try a variant. `tools/lab.py` cleans only its own outputs afterwards,
   swaps model names for the quantization the engine has, and skips (with the download link) any
   job whose model file is missing - `store.py fetch` it and rerun.
3. Make a sheet: `python tools/sheet.py analysis/<round>.jpg gens/<round> --cols 4 --thumb 420`.
4. Look at the sheet, write down what changed in `docs/` (or the round log), keep the prompts in
   `jobs/`.
5. Do not leave renders outside `gallery/`, `gens/`, `analysis/`, `sfw/` (neutral work) or the
   local engine's `gl/` scratch folders.

## 6a. When the feedback is vague

Users often don't know yet what they want ("make it better", "more anime", "not quite"). Then:

- Look at what exists right now - `templates` and `video_templates` in `kit/presets.json`, the
  Video tab options (`cocks`, `breasts_video`, `dynamics_video`, Anime timing), `my/presets.json`.
  Never keep a copy of that list in the docs; it goes stale.
- Offer the 2-4 closest fits, one short line each: what it would look like and how it differs from
  what they have now.
- Offer to tune a custom style from their pick and save it as a new template.
- Keep it short and scannable: no walls of text, one question at the end.

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

**Memory check before every job** (page and `tools/lab.py`; `python tools/headroom.py
<template>`): when commit is tight the job runs in low-memory mode (cached models dropped first,
light 4B encoder for H3-Image) with a warning and the apps to close. Before a heavy session, run it
and tell the user what to close; never close their apps yourself. Details in
`docs/PERFORMANCE-8GB.md`, "Automatic low-memory mode".

The **16 GB pass** (2026-11-24, a 16 GB 7800 XT on Linux/ROCm; `docs/PERFORMANCE-16GB.md`) is the
opt-in profile for 16 GB+ cards (section 1a step 2). The **8 GB optimization pass is done** (2026-11-20): measured peak VRAM, per-workflow flags,
preview/standard/final step counts, the H3 4B text encoder, RelayVSR x2, and a speculative GTX
1070 section are in `docs/PERFORMANCE-8GB.md`. The measured launch pair is
`--use-ck-attention --fast fp16_accumulation`; 4 steps is a preview, 6 the standard, 8 the final
(same seed), and H3 video is 4-step preview / 6-step final. Do not re-derive this from scratch;
re-run `tools/experiments/bench_engine.ps1` and `tools/experiments/bench.py` if the hardware or
ComfyUI version changes.
