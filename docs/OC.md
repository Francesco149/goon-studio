# Original characters: design, lock, LoRA

How to take an OC from an idea (or one lucky picture) to a character that renders the same on
every seed, and then optionally into a LoRA. First OC through it: **Gemma** (cyber succubus),
rounds a114-a115. All OCs are fictional adults (`AGENTS.md` section 0/5).

## The method

1. **Describe the design as tags, one trait per tag.** Hair colour + length + style, eye colour +
   shape, horns/ears/wings/tail as separate tags, the outfit as its parts (base garment, material,
   collar, trim colour, the one signature accessory). Prefer tags the model knows (Danbooru
   vocabulary) over invented phrases - a tag it knows is a trait it holds.
2. **Pick the stack with a side-by-side** (same block, same seeds, upper body, plain background):
   which model holds the outfit and draws the art style you want. Then stay on it.
3. **Find the unstable traits with 4+ seeds**, judged on a head-crop sheet at full size (small
   details - earrings, pupils, horn shape - are invisible on a full sheet). For each unstable trait,
   test 2-4 alternative designs side by side and keep the one that holds; a design that does not
   hold on the base model will not hold in a LoRA either.
4. **Lock the expression.** The same face reads sweeter or colder by seed; eye-shape tags
   (`tsurime` / `tareme`) and one smile tag pin the personality.
5. **Save the block** as a character in `kit/presets.json` (or `my/presets.json`), verbatim. Every
   later prompt pastes it unchanged; scene tags go after it.
6. **Prove it off the portrait**: full body, back view, side view, a different outfit, a different
   expression, a scene. The traits that break here are the next round.

Tools: a `tools/rounds/mk_<round>.py` that writes the jobs, `run_template_round.py` on the bench
engine, `tools/sheet.py` for the full sheet and a head-crop sheet for the details.

## Lessons (Gemma)

- **Illustrious (WAI v17) > Anima (Pink) for this design** (a114): WAI held the high-collar latex
  bodysuit, the collar gem, the neon trim and the patterned wings on 16/16; Anima turned the suit
  into a bare-shouldered halter and drew plainer wings. Owner: Illustrious is the less generic style.
- **Small accessories: pick a bold, known shape.** `gold hoop earrings` held 4/4; `pink gem drop
  earrings` 4/4 but the size wanders; `pink gem stud earrings` turned into dangles. `no earrings`
  (negative `earrings`) is clean 4/4 if the design can do without.
- **Expression tags are a strong switch** (a115, 12/12 each): `tsurime, smug, half-closed eyes,
  closed mouth, smile` = sly heavy-lidded smirk ("cold"); `tareme, gentle smile, light blush` = round
  innocent eyes ("sweet", more generic). Owner pick: cold.
- **Earrings** (a115): hoops 12/12, pink gem drops 12/12 once the face is locked. Owner pick: pink drops
  (they echo the collar gem).
- **Horn shape is a seed trait, not a prompt trait.** Canon = a114 seed 114002 (thick, glossy, rising
  from the sides, sweeping out then up: an upward crescent). `ram horns` gives ram curls (wrong);
  `curved horns, large horns` 4/6 (a116); "horns pointing up" bled into a pointing finger; weighting
  `(curved horns:1.3), thick horns` + weighted negative `(ram horns:1.3), (goat horns:1.2)` did
  *worse* - 4/8, two ram curls through the negative and pink glowing tips on three (a117). Some seeds
  (114004) curl on every wording. Prompting tops out around 2/3 for the horns; the rest is curation,
  then a LoRA trained only on canon-horn pictures.

- **Canon picture: `gallery/a117/gm_lock_114001_00001_.png`** (owner, after a117): huge chunky
  segmented black horns, popped high collar with gold-edged lapels, gold V trim under the bust, her
  anatomy. The dataset matches this picture, not just the block.
- **Art style: the base WAI look stays** (owner). a118: artist tags (kantoku, fuzichoco, mika pikazo,
  redjuice, nixeu, the flat and h-game blocks) mostly nudge WAI's house look; kantoku/fuzichoco turn the
  face sweet; nixeu paints a signature. a119: four Illustrious style LoRAs (`docs/LORAS.md`) each change
  the design along with the look. **Any style change also redraws the horns** (the seed's composition
  moves), so restyling always means re-curating.

**Locked block:** `kit/presets.json` character `gemma` = the a117 wording (`tools/rounds/mk_a117.py`
`GEMMA`), which drew the canon picture at seed 114001 (Illustrious / WAI v17, 832x1216);
negative add-on `GEMMA_NEG` there: `(ram horns:1.3), (goat horns:1.2), curled horns, spiral horns,
horizontal horns, multiple girls`. Face, earrings and outfit
held on 8/8 in a117.

## Making a LoRA of an OC (plan, not yet done)

Next for Gemma: a dataset round with the locked block across framings, angles, expressions,
backgrounds and a couple of alternate outfits, many seeds each, then keep only the canon-horn,
on-model pictures (expect roughly half to two thirds to pass on horns alone).

Cherry-picking the base model's best gens works - it is the standard way to make an OC LoRA - as
long as the set is varied and every picture is on-model:

- **20-40 pictures**, all on-model (every locked trait right; fix a near-miss with an inpaint/edit
  rather than keep it). Variety matters more than count: framings (close-up, upper body, cowboy,
  full body), angles (front, 3/4, side, back), expressions, poses, backgrounds, lighting, and at
  least a few other outfits. All-portrait sets teach "Gemma = front portrait on dark blue".
- **Captions**: tags, with a trigger word (`gemma_oc`) first. Leave out the tags of the traits that
  are always there (hair colour, horns, wings, ears, eyes, earrings) so they bind to the trigger;
  keep the tags of what varies (pose, framing, expression, background, outfit when it changes).
- **Train on the same base** the pictures came from (Illustrious / WAI v17). SDXL-class LoRA training
  fits 8 GB with the usual memory settings (batch 1, gradient checkpointing, 8-bit optimizer, cached
  latents and text-encoder outputs); not yet measured on this rig. Tooling is not in the repo yet.
- **Check it** like a downloaded LoRA (`docs/LORAS.md`): trigger alone vs trigger + block, strength
  0.6-1.0, the poses that were not in the set.
