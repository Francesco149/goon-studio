"""mk_a120.py - round a120: Gemma LoRA dataset, raw material (Illustrious / WAI v17, base look).

Owner: canon picture gallery/a117/gm_lock_114001 (huge segmented horns, popped collar with gold-edged
lapels, gold V trim, her anatomy); art style = base WAI (a118/a119). This round renders varied shots
from the a117 block; the keepers are curated against the canon picture (horns first) - expect about
half to two thirds to pass on the horns alone (docs/OC.md).

The block is split so a shot swaps only its own part: IDENT (always), FACE (cold, the default),
EARRINGS (always), OUTFIT (canon; nude and alt-outfit shots replace it). "popped collar" added to
match the canon jacket. Variety: framing, angle, pose, expression, background, outfit, aspect.
18 shots x 4 seeds. Adult OC.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mk_a117 import NEG

IDENT = ("1girl, solo, succubus, mature female, very long hair, light purple hair, straight hair, hair between eyes, "
         "sidelocks, pink eyes, glowing eyes, demon horns, black horns, (curved horns:1.3), large horns, thick horns, "
         "pointy ears, butterfly wings, pink wings, black wing veins, demon tail, black tail, large breasts")
FACE = "tsurime, smug, half-closed eyes, closed mouth, smile"
EARRINGS = "pink gem drop earrings"
OUTFIT = ("black bodysuit, latex bodysuit, shiny clothes, high collar, popped collar, gold trim, glowing yellow neon trim, "
          "pink gemstone on collar, see-through cleavage, black elbow gloves, cyberpunk")
NUDE = "completely nude, navel, collarbone"
HOODIE = "oversized black hoodie, hood down, black shorts, bare legs"
BIKINI = "black bikini, gold trim, string bikini"

P, L, S = (832, 1216), (1216, 832), (1024, 1024)
# name: (size, outfit, face, shot tags)
SHOTS = {
    "portrait":   (S, OUTFIT, FACE, "portrait, close-up, looking at viewer, dark blue background, glowing particles"),
    "ub_34":      (P, OUTFIT, FACE, "upper body, three-quarter view, looking at viewer, night, neon lights, city, bokeh"),
    "cowboy_hip": (P, OUTFIT, FACE, "cowboy shot, hand on own hip, standing, looking at viewer, throne room, dark, candlelight"),
    "full_front": (P, OUTFIT, FACE, "full body, standing, front view, looking at viewer, simple background, white background"),
    "full_side":  (P, OUTFIT, FACE, "full body, from side, profile, walking, night, neon street, rain"),
    "from_behind":(P, OUTFIT, FACE, "full body, from behind, looking back, looking over shoulder, night sky, moon"),
    "throne":     (P, OUTFIT, FACE, "full body, sitting, crossed legs, on throne, looking at viewer, throne room, dark"),
    "lying":      (L, OUTFIT, FACE, "lying, on back, on bed, from above, looking at viewer, bedroom, dim lighting"),
    "from_below": (P, OUTFIT, FACE, "cowboy shot, from below, crossed arms, looking down at viewer, rooftop, night, city lights"),
    "laugh":      (P, OUTFIT, "laughing, open mouth, closed eyes, happy", "upper body, front view, dark blue background, glowing particles"),
    "pout":       (P, OUTFIT, "pout, annoyed, frown, looking away", "upper body, three-quarter view, dark blue background"),
    "seductive":  (S, OUTFIT, "seductive smile, blush, half-closed eyes, finger to own lips", "portrait, looking at viewer, pink lighting, dark background"),
    "nude_ub":    (P, NUDE, FACE, "upper body, looking at viewer, front view, bedroom, dim lighting"),
    "nude_full":  (P, NUDE, FACE, "full body, standing, contrapposto, looking at viewer, simple background, grey background"),
    "hoodie":     (P, HOODIE, "light smile, half-closed eyes", "cowboy shot, sitting, cafe, window, daytime, looking at viewer"),
    "bikini":     (P, BIKINI, FACE, "cowboy shot, standing, beach, night, ocean, looking at viewer"),
    "flying":     (L, OUTFIT, FACE, "full body, flying, wings spread, midair, night sky, clouds, looking at viewer"),
    "dynamic":    (P, OUTFIT, "grin, smug, half-closed eyes", "dynamic pose, dutch angle, reaching towards viewer, cyberpunk city, neon lights"),
}
SEEDS = (120001, 120002, 120003, 120004)


def jobs():
    out = []
    for name, ((w, h), outfit, face, shot) in SHOTS.items():
        for seed in SEEDS:
            p = "masterpiece, best quality, amazing quality, " + ", ".join((IDENT, face, EARRINGS, outfit, shot))
            out.append({"workflow": "wf_illu_lora.json", "lora": "konosuba-aqua-s2-illustriousxl-lora-nochekaiser.safetensors",
                        "strength": 0.0, "width": w, "height": h, "negative": NEG, "seed": seed,
                        "name": "gm_ds_%s_%d" % (name, seed), "prompt": p})
    return out


if __name__ == "__main__":
    js = jobs()
    with open(os.path.join(ROOT, "jobs", "a120_gemma_dataset.jsonl"), "w", encoding="utf-8") as f:
        for j in js:
            f.write(json.dumps(j) + "\n")
    print(len(js), "jobs")
