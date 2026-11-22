#!/usr/bin/env python3
"""mk_a94.py - round a94: Verite_overcooked vs Verite_realism on photoreal keyframes.

Verite_overcooked ships in the same Civitai version as Verite_realism (3431552) and is said to be
stronger for fluids. Fetched 2026-11-22 (store.py fetch --file, sha256 verified). The owner
doubts it is useful (the extreme cum preset is already extreme enough) but wants the result
documented.

Same template (egirl_bj_pov: Krea 2 Turbo + Verite, 8 steps), same seed, only the LoRA changes:
  bj_*    the egirl_bj_pov caption as is (saliva is the fluid)
  fac_*   a landed facial in the same Verite caption style, two seeds
  fac_over08   overcooked at 0.8 (it may simply be stronger)
Every job pins its prompt (lesson from a93c: a template can change mid-queue).
Writes jobs/a94_verite_overcooked.jsonl.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = json.load(open(os.path.join(ROOT, "kit", "presets.json"), encoding="utf-8"))["templates"]
T = "egirl_bj_pov"
BJ = P[T]["prompt"]
FAC = ("A facial, close-up POV from above. {character} She kneels between a man's legs, her mouth "
       "open and her tongue out, right after he came on her face. His erect cock is out in front of "
       "her face, his hand wrapped around the shaft; it has a defined glans with a rim, the foreskin "
       "folded back behind it and a natural veined shaft. Milky white semen lies on her face where "
       "the ropes landed: a thick glossy rope across her lips and up onto one cheek, a smaller patch "
       "on her tongue, a heavy drip hanging from her chin, uneven and lumpy, wet and slightly "
       "translucent at the thin edges. Her hand rests on his thigh. Her eyes lift to the camera, "
       "half-lidded, light blush. Dim bedroom lit by pink and purple LED strips. Candid amateur "
       "phone photo.")
RE, OV = "Verite_realism.safetensors", "Verite_overcooked.safetensors"
jobs = [
    dict(name="bj_real", template=T, seed=94001, prompt=BJ, lora=RE, strength=1.0),
    dict(name="bj_over", template=T, seed=94001, prompt=BJ, lora=OV, strength=1.0),
    dict(name="fac_real", template=T, seed=94002, prompt=FAC, lora=RE, strength=1.0),
    dict(name="fac_over", template=T, seed=94002, prompt=FAC, lora=OV, strength=1.0),
    dict(name="fac_over08", template=T, seed=94002, prompt=FAC, lora=OV, strength=0.8),
    dict(name="fac_real_b", template=T, seed=94003, prompt=FAC, lora=RE, strength=1.0),
    dict(name="fac_over_b", template=T, seed=94003, prompt=FAC, lora=OV, strength=1.0),
]
out = os.path.join(ROOT, "jobs", "a94_verite_overcooked.jsonl")
with open(out, "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("wrote", out, len(jobs))
