# NSFW Studio

A local, private lab for explicit image and video generation: its own gallery, its own app, and
its own recipes. It is the NSFW companion to [Love Live Studio](../lovelive-studio) - the SFW app
stays SFW and this folder stays out of it.

- **Its own gallery.** Everything this app makes goes in `gallery/`, which is not in git. The SFW
  app's pictures are never touched.
- **Two models that matter.** Photoreal: Krea 2 Turbo NSFW v10. Anime: Pink Alchemy Anima v2.9.
  Both are in `docs/EGIRL.md` and `docs/ANIME.md`, with the prompts that survived the owner's
  review.
- **Agent-first.** `AGENTS.md` is the guide for the agent that runs this repo. `AGENTS.local.md`
  (git-ignored) holds notes that are only for the author, including the reference clips.
- **Nothing leaves the PC.** The app talks to the local ComfyUI only.

## Quick start

1. Copy `my/settings.example.json` to `my/settings.json` and set `engine_dir` (the ComfyUI folder
   with `python_embeded`) and `data_dir` (where the gallery should live).
2. Double-click `NSFW Studio.cmd`, or run:
   `powershell -ExecutionPolicy Bypass -File kit\start.ps1`
3. The page opens at http://127.0.0.1:8191. Pick a template, edit the character/scene, press
   **Make pictures**. Pictures can be rated and locked (private) from the gallery.

## The default

The page opens on **`anime_pov`**, the best anime blowjob POV so far. Change the template
dropdown for anything else; the default is only a starting point.

## Images in git

**No NSFW image is committed.** If an example is needed in the repo it must be fully censored
(baguette over the cock, genitals/anus/nipples hidden, no act visible), stripped of prompt
metadata, and **vetted by a human** before `git add`. References are kept but never committed
(`gallery/refs/`, git-ignored). Full rule: `docs/IMAGES.md`.

## What is in here

```
kit/studio/        the app (server.py, core.py, index.html) - standard library only
kit/presets.json   templates: workflow + size + prompt shape (e-girl, anime, facial, video)
workflows/         ComfyUI API graphs with {{placeholders}} (Krea 2, Anima/Pink, H3, Qwen edit)
templates/         extra prompt snippets for manual runs (optional)
tools/             lab.py batch driver, clean.py, sheet.py, strip.py, comfy.py
docs/              EGIRL.md, ANIME.md, FACIAL.md, CUM-VIDEO.md, WORKFLOWS.md
gallery/           renders (git-ignored)
my/                settings, history, private records (git-ignored)
```

## Hardware

The reference box is a Windows PC with an RTX 3080 (10 GB) and a second Linux box with an
RX 7800 XT (16 GB). Krea 2 NSFW and Pink Alchemy run on the 3080; H3 video runs on both. Wan 2.2
14B does **not** fit 16 GB (documented in `docs/CUM-VIDEO.md`).

## Privacy

Pictures made on the page are private by default. The agent only sees them after the user
presses **share** in the gallery; the app records that in `my/library.json`. `my/private/` is
never read by the agent. This is the same rule as Love Live Studio and it is not optional.
