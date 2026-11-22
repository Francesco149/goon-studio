# Open items and how to pick them up (handoff, 2026-11-21)

Read this before starting experiments. The canon is in `AGENTS.md` section 5; the measured
details are in `docs/ANIME.md`, `docs/FACIAL.md`, `docs/CUM-VIDEO.md`, `docs/EGIRL.md`.

## Golden templates right now (owner verdicts)

| what | template(s) | notes |
|---|---|---|
| photoreal blowjob keyframe | `egirl_bj_pov` | Krea 2 Turbo + Verite 1.0, Verite-style caption ("excellent") |
| photoreal blowjob clip | `pov_blowjob_anatomy` | physics wording + Male Anatomy 0.9 ("best photoreal video yet"); fallbacks `pov_blowjob`, `pov_blowjob_astro`, `pov_blowjob_fl` (all owner-valid) |
| anime blowjob clips | the round a26 batch: `anime_ll_headgrab_push` (k11), `anime_ll_two_hands_a26` (k12), `anime_ll_tip_tease` (k13), `anime_ll_cum_switch_a26` (k14) | "gold standard for dynamics, poses and expressions"; exact a26 prompts, **no physics paragraph** |
| anime blowjob base | `anime_ll_suction` (k9) and family | back to the pre-a88 prompts (see "penis type" below) |
| anime paizuri | still `anime_ll_fz_paizuri_notongue` -> clip `anime_ll_paizuri` (a92) | "solid, right penis type"; no saliva yet |
| anime stills | `anime_pov` (retracted), `anime_pov_foreskin`, `anime_pov_mosaic` | style + nudity locks, round a86 |

## Open items, in the owner's order

1. **Cum physics (next).** Recurring: the amount that lands and splashes is far too much for one
   rope (mass conservation), it spurts and then lands much lower than the arc implies, and the
   physics overall reads unnatural. Close to a good baseline, not there yet. Reference: the
   Gemini analysis in `docs/ART-STUDY.md` - section 4 (viscosity spectrum, crawl rates, splash
   corona, coalescence), 5 (the photoreal reference table), 8.2 (spurt cadence 0.8 s, then
   0.9-1.0 s, then 1.2-1.5 s with decaying velocity; meatal flare; fluid decapitation), 8.3 (5-12
   degree upward recoil per spurt, elastic rebound). The owner points at the BlobCG clips and the
   photoreal references as the good examples (`docs/archive/REFS.md`, `gallery/refs/`). Current
   recipes and their defects: `docs/CUM-VIDEO.md` (the cum dial, `cumshot_*` templates) and the
   anime cum clips (`anime_ll_cumshot*`, `anime_ll_cum_switch*`). Rules learned: **do not add the
   glans-rigidity paragraph to cum clips** (k14 lost the cum, round a89); compare variants from
   the same keyframe and seed.
   **Round a93 (2026-11-22, `docs/CUM-VIDEO.md` "Round a93"):** spelling the physics out in the
   script (constant volume, aimed arc, cadence, recoil) made the photoreal spurts unnatural
   (acceleration, travel) and caused no-cause glans drips. The owner's best default is the
   **`cumshot_medium` template as is** (`pm_base`: `p1_pose`, seed 970, local engine);
   `cumshot_high` is an extreme preset only. Revised rules: an occasional split into splashes is
   realistic; white on the glans is fine only when a spurt visibly lands on it. Leads: `pm_land`'s
   later spurts for a rebuilt `cumshot_low`; the anime cum shot sweeps two ropes side to side in a
   symmetrical arch - round a93b tests seeds, gap keyframes (`gens/a30/n1_handjob_a|b`) and an
   uneven one-side landing. The meter `tools/rounds/cum_mass.py` finds frames, it does not judge.
2. **A convincing facial variant** (owner asked for it after the dynamics work): the photoreal
   facial pose is `egirl_facial` (owner-approved pose); the clip side needs the cum work above.
3. **Paizuri saliva dynamics.** a92 has none. Add saliva wording to `anime_ll_paizuri` and test
   from the same keyframe/seed; avoid skin-drag wording (it painted a shading band on the inner
   breasts, a88).
4. **Penis type in anime video is not controlled by wording.** The physics paragraph and the
   `golden` preset both gave a smoother, glossier shaft than a26 (and one odd fold on the glans,
   a91). Reverted: the anime clips use the a26 prompts. The `cocks` presets stay for stills; on
   video they are experimental and the Video tab default is "as the template". Next ideas: a
   penis LoRA for H3 that matches the a26 look, or first+last frames.
5. **Anime animation style.** The anime clips look like an h-game / live2d avatar: abnormally
   smooth motion compared with a hand-animated h-anime. Not bad, a different style. Future:
   prompt H3 for a more anime-like animation (held frames, limited animation, smears/impact
   frames, "animated on twos") as another style template.
6. Smaller:
   - photoreal veins come out as raised vine-like cords (inherited from the Krea + Verite keyframe);
   - HMPenis v2 is registered but untested (needs a Civitai login - the owner downloads it);
   - `Verite_overcooked` (same Civitai version as Verite_realism) is said to be stronger for
     fluids - worth a try on photoreal keyframes; not in the store yet (Civitai login: the owner
     downloads it), so round a93 skipped it;
   - the LL OC's fangs are awkward in blowjob scenes (character-specific);
   - anime still seal depth: the lips close over the top of the glans; wording does not change it;
   - paizuri shaft skin never moves (needs a LoRA or a first/last pair, not wording);
   - `kit/studio/headroom.py` COMMIT_FACTOR 0.6 is fitted to two runs; refit from `bench.py`.

## How the rounds in this session were run (reuse it)

- **Engine:** the owner's `my/settings.json` `comfy_url` points at the lab box (ampere). For local
  work start the bench engine: `powershell -File tools\experiments\bench_engine.ps1 -Action start
  -Flags "--use-ck-attention --fast fp16_accumulation"` (port 8189; `-Action stop` after) and set
  `GOON_COMFY_URL=http://127.0.0.1:8189` for any tool (`modelstore`, `headroom`, `store.py`).
  Never drive the user's page on 8191.
- **Rounds through the page code:** `python tools/rounds/run_template_round.py jobs/<round>.jsonl
  <round> --engine http://127.0.0.1:8189`. Job lines are page jobs (`template`, `seed`, overrides,
  `image`, `last`, `cock`, `image_from` for a keyframe made earlier in the same round). Renders go
  to `gallery/<round>/` as the agent's pictures; write `my/rounds/<round>.json` (`title`, `items`
  with `file`/`label`, `question`, `note`) for the Rounds tab.
- **Comparing clips:** the system Python has no PIL; use the engine's
  `python_embeded\python.exe -I` (PyAV + PIL) to pull frames and build grids into `analysis/`.
  Compare the same keyframe + seed, at full resolution, at the frames where the defect happens.
  Always look before calling anything fine; keep failed renders.
- **Page JS:** there is no Node here; syntax-check `kit/studio/index.html` by loading its script
  through `new Function(...)` in a scratch page in the browser pane (never load the real page: it
  lists private pictures).
- **Models:** `python tools/models/store.py check|fetch|adopt|audit|doc` (AGENTS.md 4a). Every new
  file needs a source in `kit/models.json`; run `audit` and `doc` before committing.
