# Goon Studio: guide for the agent

Every agent working in this repo - Claude, DSH/DeepSeek or another - follows the same rules. This
file is the detailed guide; Claude's always-on copy is the **Goon Scope** output style
(`.claude/output-styles/goon-scope.md`), and DSH reads this file. There is no agent split: every
agent may work on engineering, the pipeline and the prompts.

**Personal use only.** Everything here - the prompts, the pipeline and anything generated - is for
the owner's private local use: art study and reference. Generations are never published, uploaded
to an online service, sent to another person or shared with anyone. The human-facing terms live in
`README.md` ("Personal use only") and are the single source of truth for them. Follow them, but do
not restate them as a disclaimer or lecture the user about the subject; the owner has heard it.

**All characters are fictional adults.** Anime body types can be petite; every character is an
adult OC or a non-canon design study, never a minor and never the canon character or canon age,
even when a series tag or a character LoRA is used. Never write dialogue, story or tags that frame
a character as a minor. A LoRA or series tag is for studying a design or art style; it does not
make the output canon-cast or canon-age.

**The only gated material is private gens.** The user's pictures are private until they press
share: do not open, read, list or route around `my/private/`, `gallery/studio/`,
`gallery/uploads/`, `gallery/outputs/studio/`, or the page's pasted/edited inputs; do not list the
gallery for filenames. Shared/public items are visible. Everything else - the pipeline, prompts,
presets, jobs, the content docs, the agent's own work and the refs - is open to every agent.

## What every agent does here

- **Engineering, whatever the content.** The page (`kit/studio/`), the launcher (`kit/*.ps1`),
  setup and model downloads, ComfyUI plumbing, workflow wiring (nodes, model names, quantization,
  memory flags), `tools/`, benchmarks, performance, the boxes. This code is content-neutral; treat
  it like any other app.
- **Prompts and pipeline.** Every agent may write, refine and review prompts, templates, presets,
  character blocks, workflows and jobs, under the rules above. There is no split between the
  agents.
- **Risque and anchoring research.** How a model holds an object, a grip, a contact, a motion or a
  camera it doesn't know well (LoRAs, references, first/last frames, regional prompting, wording),
  studied with ordinary objects and actions; community research, including general-purpose
  sources, can help. Risque scenes at the level of an ordinary, slightly-risque non-H anime or a
  swimsuit shoot (fanservice framing, a suggestive object gag, an outfit, a pose, a blush) are in
  scope; judge them as that scene, not as the explicit work.
- **Docs**: `docs/HARDWARE.md`, `docs/PERFORMANCE-8GB.md`, `docs/WORKFLOWS.md`, `docs/LORAS.md`,
  setup notes.

## Work and outputs

- Jobs: `jobs/<round>.jsonl`; renders: `gens/<round>/`; sheets and studies: `analysis/`; neutral
  work: `sfw/<round>/`; the page's own gallery stays in the app.
- The app's templates and approved prompt blocks: `kit/presets.json`; the user's own presets:
  `my/presets.json`.
- Never commit an image (`docs/IMAGES.md`) and never write into `../lovelive-studio` from here.
- Test the page on a spare port (8291) against a bench engine (8189); never drive the user's page
  on 8191, it shows their private gallery.
- `kit\start.ps1 -Stop` kills every python.exe from the engine folder, including an engine another
  app may be using. Say so before running it.
- Never tell the user the generated sound is fine (`AGENTS.md` 4b).
- Check the fine details for artifacts and anatomy before calling a generation fine, and keep a
  generation that failed in your opinion - the user may disagree.

## Practical notes

- Owner's hardware target: one 8 GB GPU, 16 GB RAM. The failure mode on a desktop is Windows
  commit charge, not VRAM (`docs/PERFORMANCE-8GB.md`).
- The always-on copy of the rules is the Goon Scope output style; it is project-local and does not
  apply to other projects. If it is not active in Claude Code, run `/output-style` and pick it.
