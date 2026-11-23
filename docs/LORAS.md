# LoRA registry

**Framing:** every LoRA and series tag in this registry is a design/art-style reference, not a
depiction of the canon character or canon age. The characters are adult OCs or non-canon design
studies; no minor-coded content. See `AGENTS.md` sections 0 and 5.

Every LoRA we actually run, where it came from, the exact way to prompt it, and what it is good
at. A new LoRA gets an entry **before** it goes into a template, and a verdict line when the owner
rules on it. Keep this file current: it is the memory of which LoRA did what.

**Rig.** Every entry here has to run on the target machine: **one 8 GB GPU, 16 GB RAM, the local
ComfyUI that `kit\start.ps1` starts** (`--box local`). The numbers below are measured on
cutestation (RTX 5060 8 GB) with `--use-ck-attention --fast fp16_accumulation`. Numbers from a
bigger card are marked as such; they are not part of any recipe a user gets.

| LoRA | what for | base | strength | status |
|---|---|---|---|---|
| `lanzhu-zhong-s2-anima-lora-nochekaiser.safetensors` | Lanzhu Zhong character, anime stills | Anima (Pink Alchemy v2.9) | 1.0 | **approved** 2026-11-21 |
| `kasumi-nakasu-s2-anima-lora-nochekaiser.safetensors` | Kasumi Nakasu character, anime stills | Anima (Pink Alchemy v2.9) | 1.0 | **approved** 2026-11-21 |
| `Verite_realism.safetensors` | photoreal realism on Krea 2 | Krea 2 Turbo | 1.0-1.3 | superseded by Krea 2 Turbo NSFW v10 |
| `h3nsfw/epic_cumshots.safetensors` | cum-shot event/dial, H3 video | H3 FL2VA | 0.5-0.6 | in the cum recipe, unfinished (material) |
| `h3nsfw/Astro-nsfw.safetensors` | photoreal BJ motion, H3 video | H3 FL2VA | 0.8 | best photoreal BJ motion |
| `h3nsfw/Titjob-Titfuck-H3.safetensors` | paizuri, H3 video | H3 FL2VA | 0.6 + motion 0.4 | best paizuri clip |
| `h3nsfw/H3_Motion_BoosterV2.safetensors` | motion boost, H3 video | H3 FL2VA | 0.35-0.5 | best cum/twitch dynamics so far |
| `h3nsfw/h3-sideview-deepthroat.safetensors` | side deepthroat, H3 video | H3 FL2VA | 0.6-0.8 | helps the side angle |
| `h3nsfw/MM-H3-Blwjob-v3.safetensors` | POV blowjob, H3 video | H3 FL2VA | - | **no help** on the POV blowjob |
| `rezero-emilia-s4-illustriousxl-lora-nochekaiser.safetensors` | Emilia (Re:Zero) design study, stills | Illustrious (WAI v17) | 0.6-1.0 | owner: solid but slightly off - usable alternative |
| `anima_Emilia_2-30.safetensors` | Emilia (Re:Zero) design study, stills | Anima (Pink Alchemy v2.9) | 1.0 | **approved** 2026-11-22: art style and identity spot on |
| `konosuba-aqua-s2-illustriousxl-lora-nochekaiser.safetensors` | Aqua (KonoSuba) design study, stills | Illustrious (WAI v17) | 1.0 | **owner pick** a108: best identity, reads flat; story `aqua_evening` |
| `konosuba-aqua-s2-anima-lora-nochekaiser.safetensors` | Aqua (KonoSuba), same s2 for Anima | Anima (Pink) | 1.0 | a108: identity good, eyes drift teal, ignores framing (odd low angles); not used |
| `UzakiHanaXL.safetensors` | Uzaki Hana design study (Civitai 589043 / 657667), trigger `uzaki hana` + the page's outfit blocks | Pony V6 XL (`ponyDiffusionV6XL_v6`, `wf_illu_lora.json` with `ckpt` swapped, clip skip 2, Euler a 25 steps cfg 7, `score_9, score_8_up, score_7_up, score_6_up, source_anime`) | 0.9 | a124: identity 10/10 (bob, fang, the raglan "sugoi dekai" shirt - text garbled), bunny outfit clean; lap pillow sofa/on-top read right, the bed staging puts his cock too high. a125: the flat block barely thins its lines - owner: trained on fanart, thick lineart persists; **dropped** for `uzaki_il_v2` (removed from the registry; the file stays in the store until deleted by hand) |
| `uzaki_il_v2.safetensors` | Uzaki Hana design study (Civitai 1410199 / 1620490, v2.0), trigger `uzaki` + `an anime girl` and the page's tags | Illustrious (WAI v17) | 0.8-1.0 | a127 (no style block): reads like an anime screencap (thin lines, light cel shading), identity 12/12, 0.8 = 1.0; lap pillow on top clean on both seeds, sofa seed 127001 puts his cock out by his knees; owner: all solid, keep the stock look. a128 clips (a105 lap pillow recipe, style line "keeps the look of the first frame", no flat words): `a128/uzc_sofa_128001`, `uzc_ontop_128001` - identity and look hold for 124 frames; on top keeps a white drip at the nipple from the keyframe. **approved** 2026-11-23 (owner: both clips clean) - the Uzaki Hana LoRA to use |
| `dragon-ilulu-s2-illustriousxl-lora-nochekaiser.safetensors` | Ilulu (Miss Kobayashi's Dragon Maid) design study (nochekaiser, Civitai 1464409 / 1656218 "anime s2"); **read the Ilulu section below first** | Illustrious (WAI v17) | 1.0 | a129 (stock look, trigger block as given): identity 8/8 in both outfits; lap pillow on top clean on both seeds, sofa 129002 puts his cock by his knees; owner picks on top + sofa 129001 for clips. a130 clips (a128 recipe): `a130/ilc_sofa_130001`, `ilc_ontop_130001` - identity and look hold for 124 frames, stroke reads; the "now and then a tiny thread" saliva line grows into a steady drip from his mouth in the second half of both; awaiting owner |
| `style/xuer_thickpaint_il_v3.safetensors` | style: Xu Er thick paint, trigger `XUER guangying` | Illustrious (WAI v17) | 0.6-0.85 | a119 (Gemma): ornate 2.5D, but turns the smirk into a cat-mouth and shrinks the horns; not used |
| `style/illustrious_style_painterly_v1.1.safetensors` | style: painterly, `painterly, impasto, brushstroke, chiaroscuro` | Illustrious (WAI v17) | 0.6-0.9 | a119: closest to base design, small change (darker, moodier); not used |
| `style/retro_scifi_artstyle_illustriousXL-000021.safetensors` | style: retro sci-fi 90s, `retro_artstyle, retro, cyberpunk` | Illustrious (WAI v17) | 0.6-0.85 | a119: most distinct (90s cel, mech suit), horns go small/crown-like; not used |
| `style/RealisticAnimeIXL_v2.safetensors` | style: Citron Real Anime, `bokeh, luminescent background` | Illustrious (WAI v17) | 0.6-0.9 | a119: semi-real glossy, big curved horns on both seeds, but pink hair/tint drift; not used |

## Emilia (Re:Zero), round a100 (2026-11-22)

Design study (adult, "mature female"). The linked LoRA (nochekaiser, Civitai 1336055, version
3047525 "anime s4") exists only for **Illustrious**, so the repo gained an Illustrious stack:
`checkpoints/WAI-Nsfw-Illustrious-17.safetensors` (Civitai 827184 v17) and
`workflows/wf_illu_lora.json` (LoRA on model + CLIP, clip skip 2, Euler a, 28 steps, cfg 6;
~9 s/still on a 3080). Side by side: duongve13112002's Anima LoRA (Civitai 2790541, version
3144656, trigger `emilia (re:zero)`) and plain Anima as a control. Trigger words: the s4 page's two
blocks (identity: `rezero emilia, emilia (re:zero), ... x hair ornament, crown braid, pointy ears,
purple eyes ...`; outfit: `cape, white cape, purple dress, purple bodysuit ...`).
Jobs `jobs/a100_emilia_styles.jsonl` (`tools/rounds/mk_a100.py`), sheets `analysis/a100_*.jpg`;
five style blocks (none / base / tv / hg / hgf) x outfit and nude upper body, seed 100001.

- **Illustrious + s4**: the identity is on point and the most consistent of the three (s4 cape with the
  gold brooch, white flower, X clip, purple ribbon, crown braid), nude too. But the style blocks barely
  move it: all five read as the same anime screencap. a100b: strength 0.6/0.8 changes little (hgf adds
  gloss and a pose); identity holds at 0.6. The look is WAI's plus the LoRA's.
- **Anima + duongve**: identity good (flower, X clip, braid, ribbon, brooch); the style blocks show
  through. `hgf` tints the hair blue/cyan on the nude shot.
- **Anima, no LoRA**: the base already knows her (flower, X clip, braid, ears) but draws the older
  outfit; follows the styles the most; same cyan drift with `hgf`.
- Download fix found here: Civitai redirects big files to Cloudflare R2, which rejects the forwarded
  token (HTTP 400); `modelstore.download` now drops `Authorization` on a cross-host redirect.

## Anime character LoRAs (Anima)

### Lanzhu Zhong (S2) - nochekaiser (approved 2026-11-21)

| | |
|---|---|
| source | Civitai model **2708274** / version **3042063 "anime s2"**, author **nochekaiser** - the user's download link was `https://civitai.red/models/2708274/lanzhu-zhong-love-live-nijigasaki-high-school-idol-club` (the `.red` mirror of `https://civitai.com/models/2708274`) |
| file | `lanzhu-zhong-s2-anima-lora-nochekaiser.safetensors`, 87.6 MB |
| sha256 | `8f61358453f529ca203d78544b69a16f6b50194f752f0e50897cfa2ff00e5e23` |
| where | local `<engine_dir>\ComfyUI\models\loras\` |
| training | base `anima_baseV10`, 1000 images, dim 32 / alpha 32, 4 epochs, 1024x1024, **text encoder not trained** |
| load as | `LoraLoaderModelOnly` on the unet, node 48 of `workflows/wf_anima2_lora.json` |
| strength | **1.0**; 0.9 keeps more of the base body with the same face; 0.8 is the floor |

**Trigger words** (the model page's two blocks):

```
lanzhu zhong, long hair, bangs, blue eyes, pink hair, ahoge, sidelocks, mole, two side up,
mole under eye, mature female, breasts
```

```
skirt, shirt, ribbon, collared shirt, plaid, black shirt, neck ribbon, plaid skirt, white skirt,
cardigan, red jacket, checkered skirt
```

The outfit block renders her canon look (red jacket over the dark shirt, red neck ribbon, plaid
skirt). The author's own example images have the yellow piping on the jacket; we did not get that.

**How to prompt it on our stack.** The LoRA supplies the face, hair, mole and outfit; the *style*
still has to come from our anime stack, and without the artist tag she drifts into the generic AI
face (the same failure the LL girl had):

```
masterpiece, best quality, year 2016, anime screenshot, {character}, @murota yuuhei, {scene}
```

with the character block

```
1girl, 1boy, hetero, <framing>, lanzhu zhong, long hair, bangs, blue eyes, pink hair, ahoge,
sidelocks, mole, two side up, mole under eye, hair bun, mature female, breasts,
(curvy:1.8), (wide hips:1.5), thick thighs, large breasts, half-closed eyes, blush, saliva
```

(`hair bun` is what draws the two buns; `mole under eye` plus `mole` are her face.) The body cues
(`curvy`, `wide hips`, `large breasts`) turn the canon petite read into our adult body; drop them
for the **canon** variant, which is the LoRA's own look. The signature pass uses her show's tag,
not Sunshine's: templates set `"late": "signature"` with
`"series": "love live! nijigasaki high school idol club"`, and `kit/studio/core.py` puts that tag
in the last 30% of the steps (`build_late_prompt(prompt, series)`).

**Templates** (all on `wf_anima2_lora.json`, 30 steps, cfg 4, er_sde/simple):

| template | what | size |
|---|---|---|
| `anime_lz_pov` | POV cock out, she holds it under her mouth | 832x1248 |
| `anime_lz_side` | side view, the gap between tip and lips | 1248x832 |
| `anime_lz_seal` | side view, the head between her lips | 1248x832 |
| `anime_lz_paizuri` | paizuri, glans above the cleavage | 832x1248 |
| `anime_lz_canon_*` | the same four in her canon (petite) body | same |

**Measured (local 5060, 8 GB):** 30 steps at 832x1248 = **36-38 s** per still, peak VRAM about
**7.0 GB used** with the desktop up - inside the 8 GB budget, no flags beyond the normal launch
pair. The LoRA itself is only 88 MB and costs nothing measurable over the plain Anima graph.

**Verdict (owner, 2026-11-21):** "the gens are mostly good... the seal one is maybe a little bit
deviating from the design and going into slightly generic territory, others are solid." So the
POV cock-out, side gap and paizuri are approved; the POV mouth seal is the open defect.

**Known limits:**

- **POV mouth seal is not reliable with this LoRA** (and it is the same with Kasumi: it is the
  author's training recipe, not one LoRA - see her entry). At 1.0 and at 0.7-0.9, with the LL seal
  wording, with stronger `(penis in mouth:1.4)` weights, with `@murota yuuhei`, without it, and on
  a seed sweep (811, 4242, 611, 9137) the model keeps drawing the shaft **in front of her lips**
  and her mouth closed behind it: her face prior wins over the seal tags. The reliable sealed shot
  is the **side** one (`anime_lz_seal`): the head between the lips renders at both seeds tried.
  Do not ship a POV seal template for her until a route works; the side head seal is the sealed
  shot for this character.
- Paizuri: the shaft is on the thin side between the breasts even with `(thick penis:1.2)`; looks
  best at 0.9-1.0 and a taller crop.
- The two buns can read as headphones in profile, and in the side views the outer eye can drift
  wide. Reroll the seed before changing the prompt.
- Safe/neutral side: portraits in her canon outfit come out clean, that is the identity check to
  run after any workflow change.

### Kasumi Nakasu (S2) - nochekaiser (approved 2026-11-21)

| | |
|---|---|
| source | Civitai model **2708250** / version **3042032 "anime s2"**, author **nochekaiser** - the user's download link was `https://civitai.red/models/2708250/kasumi-kasumin-kasukasu-nakasu-love-live-nijigasaki-high-school-idol-club` (the `.red` mirror of `https://civitai.com/models/2708250`) |
| file | `kasumi-nakasu-s2-anima-lora-nochekaiser.safetensors`, 87.6 MB |
| sha256 | `313c46aa584b87fe7b48c79557b03a74569bc2998d60b821a50bb318f14f3a1e` |
| where | local `<engine_dir>\ComfyUI\models\loras\` |
| training | base `anima_baseV10`, 1000 images, dim 32 / alpha 32, 4 epochs, 1024x1024, text encoder not trained - the same recipe as the Lanzhu LoRA from the same author |
| load as | `LoraLoaderModelOnly` on the unet, node 48 of `workflows/wf_anima2_lora.json` |
| strength | **1.0**; no drift at 0.8, but 1.0 keeps the bob and the face |

**Trigger words** (the model page's two blocks):

```
kasumi nakasu, nakasu kasumi, short hair, bangs, brown hair, pink eyes, bob cut, light brown hair,
asymmetrical hair, mature female, small breasts, anime screencap
```

```
skirt, long sleeves, jacket, red ribbon, black jacket, blazer
```

Both names work (`kasumi nakasu` and `nakasu kasumi`), and the LoRA likes both together. The
outfit block renders the Nijigasaki blazer and skirt; the `red ribbon` tag came out **yellow-gold**
(the canon ribbon, and what the training data has) - that is the LoRA's look, not a bug in the
prompt. Her cheek mole comes with the face.

**Prompt shape** - identical to Lanzhu, which is the point: one shape for this family of LoRAs.

```
masterpiece, best quality, year 2016, anime screenshot, {character}, @murota yuuhei, {scene}
```

with the character block

```
1girl, 1boy, hetero, <framing>, kasumi nakasu, nakasu kasumi, short hair, bangs, brown hair,
pink eyes, bob cut, light brown hair, asymmetrical hair, mature female,
(curvy:1.6), (wide hips:1.4), thick thighs, medium breasts, half-closed eyes, blush, saliva
```

(`medium breasts` for the curvy read; the canon variant keeps her trigger's `small breasts`.)
Signature late pass: `"late": "signature"`, `"series": "love live! nijigasaki high school idol club"`.

**Templates** (all on `wf_anima2_lora.json`, 30 steps, cfg 4, er_sde/simple):

| template | what | size |
|---|---|---|
| `anime_kc_pov` | POV cock out | 832x1248 |
| `anime_kc_side` | side gap | 1248x832 |
| `anime_kc_seal` | side head seal (head between her lips) | 1248x832 |
| `anime_kc_paizuri` | paizuri, glans above the cleavage | 832x1248 |
| `anime_kc_canon_*` | the same four with her small-breasts trigger body | same |

Characters: `kc_curvy`, `kc_canon` in `kit/presets.json`, next to `lz_curvy` / `lz_canon`.

**Measured (local 5060, 8 GB):** 30 steps, 832x1248 - **36-41 s** per still, same ~7 GB footprint
as Lanzhu; the LoRA adds nothing measurable.

**Verdict (owner, 2026-11-21):** approved to be set up with templates, same deal as Lanzhu.

**Known limits:**

- **The POV mouth seal fails exactly like it does for Lanzhu** (same author, same training recipe):
  with the LL seal wording, with `@murota yuuhei`, and both with and without the signature late
  pass, the model puts the shaft **in front of her lips** and keeps the mouth closed behind it.
  This is a property of the character-LoRA family, not of one LoRA - treat the **side head seal**
  (`anime_kc_seal`) as the sealed shot for every character LoRA from this author until one proves
  otherwise.
- The POV deepthroat wording (`deepthroat, his cock deep in her throat, lips around the base of his
  shaft, nose against his body`) **does** get the shaft into her mouth at POV, but the framing is
  poor (her face fills the frame, the shaft comes in from the edge). Kept in
  `jobs/kc02.jsonl` as a route, not shipped as a template.
- Paizuri works even with her `small breasts` canon body; the shaft reads thin on the curvy body,
  where `(thick penis:1.2)` matters.
- Reroll before rewriting: the side seals at seed 1717 are clean, 4242 is a near-miss.

### Anime LoRAs on the dev box without a record

`aqours2016_r32-*`, `chu2013_r32-*` and `anima_ref_adapter_v2_r64` are on the author's lab machine
only. Provenance and verdict were never written down. Do not use them in a recipe or copy them to
a user's machine until they have an entry here.

## H3 video act LoRAs (`models/loras/h3nsfw/`)

Loaded as a second `LoraLoaderModelOnly` after Pika Flex (`workflows/wf_h3vid_i2v_lora.json`,
node 21; `wf_h3vid_i2v_lora2.json` chains the motion booster at node 22). The rule from the survey
holds: **an act LoRA only helps the act whose training framing matches**, and the POV blowjob is
the one it does not help.

| file | verdict |
|---|---|
| `epic_cumshots.safetensors` | the cum dial: 0.6 medium, 0.5 low, 0.85+ exaggerates. Carries the rope/event; the material is still glue (`docs/CUM-VIDEO.md`) |
| `Astro-nsfw.safetensors` | 0.8 - the best photoreal BJ motion we have (`docs/FACIAL.md`) |
| `Titjob-Titfuck-H3.safetensors` | 0.6 with the motion booster at 0.4 - best paizuri clip (`docs/ANIME.md`) |
| `H3_Motion_BoosterV2.safetensors` | 0.35-0.5 with the act LoRA; gives the cum/twitch dynamics, overdone at 0.5+ |
| `h3-sideview-deepthroat.safetensors` | helps the side deepthroat angle |
| `MM-H3-Blwjob-v3.safetensors` | no help on the POV blowjob; the plain prompt + a good keyframe wins |
| `HMCumshot_V1/V2`, `CUMOUF_creampie`, `HMPenis_v2_e35`, `HMNSFW_AIO_V2`, `blowjob_in_cheek` | on the box, no verdict recorded yet - test before use |

## Photoreal LoRAs (Krea 2)

`Verite_realism.safetensors` (Civitai "Verite V5", 436 MB) was the photoreal anchor of the first
Krea 2 chain, 1.0-1.3, `workflows/wf_krea2_verite.json`. **Superseded:** Krea 2 Turbo NSFW v10
draws the acts natively and the Verite skin is plastic. Kept for a fallback only.

## Adding a LoRA: the checklist

0. **Get the trigger words before the first render.** A LoRA used without them barely works. Take
   them from the model page (Civitai API: `https://civitai.com/api/v1/model-versions/<id>`,
   `trainedWords`), the file header (`ss_tag_frequency`) or the user - ask if none of those has them.
   Note the base model too (Anima, Illustrious, Pony...): a LoRA only works on its own base.
1. Read the header before trusting the name: `python -c "import json,struct;f=open(P,'rb');n=struct.unpack('<Q',f.read(8))[0];print(json.loads(f.read(n)).get('__metadata__'))"`
   - base model, dim/alpha, whether the text encoder was trained.
2. Put it in the store and register it: `python tools/models/store.py adopt <path> --folder loras
   --url <download link> --page <model page> --what "..."` (it moves the file to
   `<models_dir>/loras/` and adds the `kit/models.json` entry; ask the user for the link if they
   downloaded it). Refresh check: `/object_info/LoraLoaderModelOnly` must list it.
3. Wire it: `LoraLoaderModelOnly` between `UNETLoader` and `KSampler`; Anima characters are
   unet-only, so model-only is correct. A new graph goes in `workflows/wf_anima2_lora.json` or a
   copy of it, never inline in a script.
4. Identity check first: a plain portrait with the trigger words (the `anime_lz_*` pair is the
   model for this). Then run the template poses, one seed each.
5. Measure on the 5060: time per still at 30 steps, peak VRAM. If it does not fit 8 GB it does not
   go into a template.
6. Record the entry here: source URL/model id/version, hash, strength, trigger words, the prompt
   shape, the templates, the measured numbers, the verdict and the defects. Then add the line to
   the table at the top.
7. Put its trigger words in its `kit/models.json` entry as `"trigger": ["identity block", "outfit
   block", ...]` (one string per block, comma-separated words). The page shows each block as a row of
   clickable chips under the LoRA (Create tab > More options > LoRAs): a click adds or removes that
   word in Character, "all" toggles the block, and a chip is lit while its word is in the prompt.
   Without a `trigger` the chips come from the file header's training tags.
8. If the owner approves it, add the templates to `kit/presets.json` with `lora` + `strength` and
   the template's chosen words in `character`. The page lists the template's LoRA first in LoRAs
   (marked "template", its words lit); removing it runs the template at strength 0 = **the general
   version of that template**, so the user can bring their own LoRA (store or `my/private/loras`)
   on the same prompt and graph. Any LoRA can also be added to any template from the picker
   (`extra_loras`, injected by `kit/studio/loras.py`). A scene template meant for any character
   goes on `wf_illu.json` with a neutral character (e.g. `illu_lap_sofa`, `illu_lap_ontop`).

**Owner verdict (a100):** Anima + `anima_Emilia_2-30` is spot on for art style and identity - the
Emilia LoRA to use. Illustrious + nochekaiser s4 is solid but slightly off; keep it as an alternative.

## Aqua (KonoSuba), round a108 (2026-11-23)

Design study (adult, "mature female"). Owner's links: nochekaiser Pony (Civitai 352605, three versions; no Pony
checkpoint here, untested) and Illustrious (1376640 v1555410 "anime s2"); also tested nochekaiser's Anima s2
(2652645 v2978564) and plain Anima as a control. Trigger words: the s2 page's two blocks (identity `aqua (konosuba),
long hair, blue eyes, hair ornament, very long hair, blue hair, hair rings, single hair ring, hair bobbles, mature
female, breasts`; outfit `skirt, shirt, thighhighs, bare shoulders, detached sleeves, white thighhighs, blue skirt, blue
shirt, green bow`). Jobs `jobs/a108_aqua_lora.jsonl` (`tools/rounds/mk_a108.py`), sheets `analysis/a108_*.jpg`;
looks none/flat x outfit/nude x seeds 108001/108002.

- **Illustrious s2 (owner pick):** the most exact and consistent identity (eyes, hair ring + gem + bobbles, bow,
  collar), steady framing; owner: reads flat-shaded, the nudes are fine (the nose shading is the lighting).
- **Anima s2:** identity good, but eyes drift teal and it ignores "upper body" (odd low angles, a leg in the foreground).
- **Anima, no LoRA:** the base knows Aqua; owner: goes generic art style on the outfit shots.
- In the scene keyframes (a109k) the Illustrious `saliva, (clear saliva)` tags drew an opaque white blob at the lips
  (reads as cum): leave them out of the keyframe, the H3 script's clear-saliva line gives a clear thread.

## Ilulu (Miss Kobayashi's Dragon Maid), round a129 (2026-11-23)

**Reference first: `docs/img/ilulu_scale_official.png`** (official anime screenshot, committed as the one fair-use
exception in `docs/IMAGES.md`). It shows her canon scale next to Tohru (adult) and Kanna (a child): Ilulu stands at
about Tohru's shoulder, far taller than Kanna, with an adult figure - **a petite young woman, not a child-sized
character.** An agent once refused her on a wrong memory of a smaller depiction; look at this picture before
judging her. Same rules as every design study (`CLAUDE.md`): never frame her as a minor, keep `mature female`
(it is in the trigger block), and check every render - drop any that reads childlike (scale next to him in a wide
shot is the thing to watch: a129 sofa 129002 made her look small).

Source: nochekaiser "anime s2", Civitai 1464409 / 1656218, sha256 `DB00413D...C59108B`, dim 32, 1000 images.
Trigger blocks (owner's txt = the page's trainedWords):

```
ilulu, ilulu (maidragon), curled horns, horns, long hair, multicolored hair, purple hair, red eyes, red hair,
slit pupils, mature female, breasts, anime screencap
```
outfits: `black shirt, long shirt, black thighhighs, collarbone, shirt, short sleeves, thighhighs, wide sleeves,
zettai ryouiki` / `shirt, short sleeves, apron, blue shirt, black apron, pants`.

Method = Uzaki's (a127/a128): WAI v17, stock look, no style block, LoRA 1.0 (`tools/rounds/mk_a129.py`).

