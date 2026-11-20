# goonlab

One folder for the porn-generation experiments: refs, renders, analysis and the recipes they
produced. Nothing here is published; nothing here leaves the folder.

```
refs/       the six source clips the brief named (moved in from Documents\uwu\refs)
analysis/   contact sheets, filmstrips, audio spectrograms; larger read-only aids
gens/       every render, one folder per round (g01, p01, v01, ...), with _run.log + _run.jsonl
jobs/       the JSONL job files that produced each round - the exact prompts, seeds and sizes
tools/      the drivers (lab.py, clean.py, wf_*.json, strip.py)
notes/      REFS.md (what the references do), RECIPE.md (the working recipe), LOG.md
```

`DOCS/` does not exist: the writeups live in the two repos that own them (see "Where the
writeups go").

## Hygiene - the rules this folder runs on

Copied from how bunker treats its own renders, because a render here is worse than most data:
the PNG keeps its prompt in the metadata, both ComfyUI boxes serve `/view` and `/history` to
anyone on the LAN with no auth, and ampere's output tree used to be plaintext.

1. **One place.** Every reference, render and note lives under `~/goonlab`. Nothing in
   `Documents\lovelive-studio` (a friend's project, and its `my/private` book is not ours),
   `~/Pictures`, `~/Videos`, the Desktop or a Downloads folder.
2. **The boxes are a scratch pad.** Renders are written to a dedicated subfolder
   (`gl/<round>`), pulled here, and the subfolder is deleted (`tools/clean.py`). Uploads go to
   `input/gl_up` and are deleted with it. The batch driver does this itself unless `--keep`.
3. **Drop only our own history.** `/history` on both boxes was cleared once while setting this
   up; from then on a batch deletes only the prompt ids it created. Do not wipe a box's history
   wholesale - other sessions' prompts are not ours.
4. **No plaintext prompts lying around on the boxes.** A prompt that describes the scene sits in
   `/history` while it is queued; keeping the queue short is the point of point 2.
5. **Name by round, not by content.** `g01/c_anatomy_00001_.png`, not `huge_cumshot_final.png`:
   the folder name stays boring on a file listing.
6. **The repo copies are for reading.** `~/src/nix-lab` and `~/src/bunker` are checkouts of other
   machines' repos; findings go back over ssh into the real repos, not by editing the copies and
   forgetting them.

## Where the writeups go

| what | where | audience |
|---|---|---|
| porn-specific knowledge: prompt shapes, tag lists, model verdicts, the shot grammar, the LoRA route | `bunker:/opt/src/bunker/docs/SEX-SCENES.md` + `docs/NSFW-RESEARCH.md`, linked from its `docs/STYLE-LOCK.md` (commit `ea47d1d`) | the sessions that make these renders |
| the sanitised, matter-of-fact lessons that help any generation (a small part must be named and pinned, resolution floor, depth order, mosaic is post, the queue-stuck workaround, the upload multipart, model willingness) | `nix-lab:research/local-gen/ROUND-2026-11-20-detail-and-order.md` + two inserts in `research/local-gen/MODEL-NOTES.md` (commit `5d7931d`) | any lab session |

## Machines

- **cutestation / win-wifi** (this box, RTX 5060 8 GB, 16 GB RAM): ComfyUI `127.0.0.1:8188`,
  data in `F:\LLStudioTest`. Works, but a 12.5 GB video model plus AMaL stream off NVMe: a batch
  of images degrades badly and one render can crawl. Fine for one clip at a time.
- **ampere** (`10.0.10.240`, RTX 3080, 67 GB RAM): ComfyUI `:8188` when the owner has it on
  ComfyUI instead of Speedy. 2.5-3x faster, has every model that matters. This is the main box.
- **bunker** (`ssh maximus` then `ssh bunker`, or `ssh -J` with maximus's key): repo reachable
  only through maximus; root ssh opened by the owner for this session.
