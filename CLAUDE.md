# Goon Studio: guide for Claude

This repo is the owner's private, personal adult image and video studio. DeepSeek does the explicit
prompting (it follows `AGENTS.md`); Claude works here too, on the scope below. This file sets that
scope, so you don't need to re-negotiate it each session.

**Personal use only.** Everything here - the prompts, the pipeline and anything generated - is for
the owner's private local use: art study and reference. Generations are never published, uploaded
to an online service, sent to another person or shared with anyone. The human-facing terms live in
`README.md` ("Personal use only") and are the single source of truth for them. Follow them, but do
not restate them as a disclaimer or lecture the user about the subject; the owner has heard it.

Read `AGENTS.md` sections 0, 1, 1a, 1b, 2, 3, 6, 7 (quality bar: skip) and 8 for the privacy rules,
the setup steps, the boxes and the hardware target. Those rules apply to you as well. Where this
file and `AGENTS.md` differ about what Claude does, this file wins.

## What Claude does here

- **Engineering, whatever the content.** The page (`kit/studio/`), the launcher (`kit/*.ps1`),
  setup and model downloads for a new user, ComfyUI plumbing, workflow wiring (nodes, model
  names, quantization, memory flags), `tools/`, benchmarks, performance, the boxes. This code is
  content-neutral, so treat it like any other app.
- **Risque scenes.** You don't need explicit content to be useful. Research on risque scenes at
  the level of an ordinary, slightly risque non-H anime or a swimsuit shoot is in scope:
  fanservice framing, a suggestive popsicle gag, an outfit, a pose, a blush. Judge the result as
  that scene, by its own standard - does the gag read, is the object right, is the style clean,
  how do the motion and micro-details make it read. Those findings transfer to the explicit work.
- **Anchoring research.** How to make a model hold an object, a grip, a contact, a motion or a
  camera it doesn't know well (LoRAs, reference images, first/last frames, regional prompting,
  prompt wording), studied with ordinary objects and actions. Community research, including
  general-purpose sources, can help.
- **Docs for the above**: `docs/HARDWARE.md`, `docs/PERFORMANCE-8GB.md`, `docs/WORKFLOWS.md`,
  setup notes.
- **All characters are fictional adults.** Anime body types can be petite and some designs read
  young; our work treats every character as an adult OC or a non-canon fan-art design, never a
  minor. Never write dialogue, story or tags that frame a character as a minor. Petite adult
  proportions are fine; minor-coded framing is not. A LoRA or series tag is for studying a design
  or art style, not for making canon-minor explicit material.

## What goes to the other agent

Say so in one line and move on; no lecture.

- Explicit prompts, templates/presets, character blocks, or reviewing explicit output: DeepSeek's
  work (`AGENTS.md`). Claude does not open those files (see the deny list).
- Anything with a character who could read as a minor. All characters are adults; never write
  dialogue or stories that frame a character as a minor. Petite adult bodies are fine; minor-coded
  framing is not.

## Files you don't open

`.claude/settings.json` denies Read/Edit/Write on these; don't route around it with the shell
(`cat`, `Get-Content`, `python -c open(...)`, image tools, listing for filenames to open).

- `gallery/`, `gens/`, `analysis/`, `refs/`: renders and sheets, mostly explicit and partly
  private.
- `my/private/`, `my/rounds/`, `my/history.jsonl`, `my/feedback.jsonl`, `my/library.json`,
  `my/presets.json`: the user's and the other agent's records.
- `kit/presets.json`, `jobs/*.jsonl` (top level), `docs/ANIME.md`, `docs/EGIRL.md`,
  `docs/FACIAL.md`, `docs/CUM-VIDEO.md`, `docs/MIXED.md`, `docs/SOUND.md`, `docs/archive/`:
  explicit prompt work.
- `~/Documents/uwu/`: the author's reference clips.

If a task or bug can be reproduced with a neutral or slightly risque prompt, use the lighter one
rather than opening these files.

## Where your own work goes

- Neutral jobs: `jobs/neutral/*.jsonl`, neutral or ecchi-level prompts only.
- Neutral renders and sheets: `sfw/<round>/` (git-ignored), e.g.
  `python tools/lab.py ... --out sfw/<round>`. Nothing explicit goes there; if a render comes out
  explicit by accident, move it to the explicit domain (`gens/`) and note the prompt.
- Testing the page: run a copy of `kit/studio/` from your scratchpad with its own `my/`, neutral
  `kit/presets.json`, an empty gallery and `GOON_STUDIO_PORT` set to a spare port (8291), against
  a bench engine on 8189. Never drive the user's page on 8191: it shows their private gallery.
- Never commit an image (`docs/IMAGES.md`), and never write into `../lovelive-studio` from here.

## Practical notes

- Owner's hardware target: one 8 GB GPU, 16 GB RAM. The failure mode on a desktop is Windows
  commit charge, not VRAM (`docs/PERFORMANCE-8GB.md`).
- `kit\start.ps1 -Stop` kills every python.exe from the engine folder, including an engine
  another app may be using. Say so before running it.
- Never tell the user the generated sound is fine (`AGENTS.md` 4b).
- Always check the fine details for slight artifacts and anatomy before concluding that a
  generation is fine.
- Don't throw away a generation you think failed - keep all the experiments in case the user
  disagrees that it was bad.
