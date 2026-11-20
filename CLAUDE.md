# Goon Studio: guide for Claude

This repo is an adult image and video studio for consenting adult users. Explicit prompting is
done by another agent (DeepSeek, which follows `AGENTS.md`). Claude works here too, on a narrower
scope. This file sets that scope, so you don't need to re-negotiate it each session. Don't add
disclaimers about the subject either; the owner has heard them.

Read `AGENTS.md` sections 1, 1a, 1b, 2, 3, 6, 7 (quality bar: skip) and 8 for the privacy rules,
the setup steps, the boxes and the hardware target. Those rules apply to you as well. Where this
file and `AGENTS.md` differ about what Claude does, this file wins.

## What Claude does here

- **Engineering, whatever the content.** The page (`kit/studio/`), the launcher (`kit/*.ps1`),
  setup and model downloads for a new user, ComfyUI plumbing, workflow wiring (nodes, model
  names, quantization, memory flags), `tools/`, benchmarks, performance, the boxes. This code is
  content-neutral, so treat it like any other app.
- **Non-explicit scenes with clearly adult characters**, at the level of an ordinary, slightly
  risque, non-H anime or a swimsuit shoot: fanservice framing, a suggestive popsicle gag, an
  outfit, a pose, a blush. Judge the result as that scene, by that scene's own standard (does it
  read as the gag, is the object right, is the art style clean).
- **Generic anchoring research.** How to make a model hold an object, a grip, a contact, a motion
  or a camera it doesn't know well (LoRAs, reference images, first/last frames, regional
  prompting, prompt wording), studied with ordinary objects and actions. Community research too,
  where the sources are general-purpose.
- **Docs for the above**: `docs/HARDWARE.md`, `docs/PERFORMANCE-8GB.md`, `docs/WORKFLOWS.md`,
  setup notes.

## What goes to the other agent

Say so in one line and move on; no lecture.

- Writing, refining or reviewing explicit prompts, templates, presets or character blocks
  (`kit/presets.json`, the content docs, the prompt text in `jobs/` and in the workflows).
- Looking at, rating or describing explicit outputs, or research about explicit acts or anatomy.
- Tuning a "safe" stand-in by the explicit act's criteria (seal, stroke rhythm, a POV meant to be
  swapped for the real thing afterwards). A popsicle test is fine when the popsicle scene is the
  goal; it is not a way to develop the explicit recipe by proxy.
- Anything with a character who could read as a minor. All characters are adults; keep them
  visibly adult in every prompt you write (adult proportions, `adult woman`, no school setting).

## Files you don't open

`.claude/settings.json` denies Read/Edit/Write on these; don't route around it with the shell
(`cat`, `Get-Content`, `python -c open(...)`, image tools, listing for filenames to open).

- `gallery/`, `gens/`, `analysis/`, `refs/`: renders and sheets, mostly explicit and partly
  private.
- `my/private/`, `my/rounds/`, `my/history.jsonl`, `my/feedback.jsonl`, `my/library.json`,
  `my/presets.json`: the user's and the other agent's records.
- `kit/presets.json`, `jobs/*.jsonl` (top level), `docs/ANIME.md`, `docs/EGIRL.md`,
  `docs/FACIAL.md`, `docs/CUM-VIDEO.md`, `docs/SOUND.md`, `docs/archive/`: explicit prompt work.
- `~/Documents/uwu/`: the author's reference clips.

You may read `my/settings.json`, `my/studio-errors.log`, the workflows (for their wiring; leave
their prompt text alone), `AGENTS.local.md` (infrastructure notes only) and the code.

If a task needs something behind this list (a bug that only shows on one picture, say), ask the
user to describe it or to share a neutral repro, rather than opening the file.

## Where your own work goes

- Your jobs: `jobs/neutral/*.jsonl`, neutral or ecchi-level prompts only.
- Your renders and sheets: `sfw/<round>/` (git-ignored), e.g.
  `python tools/lab.py ... --out sfw/<round>`. Nothing explicit goes there; if a render comes out
  explicit by accident, delete it and note the prompt that caused it.
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
