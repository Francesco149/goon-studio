"""Build the cum-shot preset matrix in kit/presets.json from the jobs that produced each look.

The owner's spec (2026-11-21): "k14 are the best ones so far, i'd say that's the maximum
exaggeration standard. we want to be able to turn down the twitching and the amount per shot to
medium and low (default to medium)."

So the cum presets are a DIAL on two axes at once (amount per shot + twitch), plus the three looks
that are different fluids/acts rather than tiers:

  cumshot_high       k14 - the maximum exaggeration standard (full ropes, splash, shaft kicks)
  cumshot_medium     k16_medium - the default: shorter/thinner ropes, small twitch, only the first
                     rope splashes
  cumshot_low        k16_low - two pulses, a thin rope, no kick, mostly ooze
  cumshot_goopy      k11_goopy_06 - semi-solid wax-like extreme (owner: unrealistic, kept as an
                     option); also the only wording that reliably keeps the rope short
  cumshot_mouth      k11_mouth_06 - clean in-mouth swallow, nothing outside the mouth
  cumshot_softening  k11_softening_06 - messy mouth, keeps sucking while he softens

Prompts are copied out of the job files rather than retyped, so the page cannot drift from what was
actually rendered and judged. Run: python tools/rounds/mk_presets_cum.py
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def load_jobs(name):
    rows = {}
    for line in io.open(os.path.join(ROOT, "jobs", name), encoding="utf-8"):
        line = line.strip()
        if line:
            j = json.loads(line)
            rows[j["name"]] = j
    return rows


k11 = load_jobs("k11.jsonl")
k14 = load_jobs("k14.jsonl")
k16 = load_jobs("k16.jsonl")

LORA = "h3nsfw/epic_cumshots.safetensors"


def tmpl(label, prompt, strength=0.6):
    return {"label": label, "workflow": "wf_h3vid_i2v_lora.json", "lora": LORA,
            "strength": strength, "width": 768, "height": 1152, "length": 124,
            "prompt": prompt}


CUM = {
    "cumshot_high": tmpl("Cum shot - HIGH (maximum exaggeration: full ropes + shaft kicks)",
                         k14["k14_direct_p1_06"]["prompt"]),
    "cumshot_medium": tmpl("Cum shot - MEDIUM (default: shorter thinner ropes, small twitch)",
                           k16["k16_medium"]["prompt"]),
    "cumshot_low": tmpl("Cum shot - LOW (two thin pulses, no kick; caveat: mists - see docs)",
                        k16["k16_low"]["prompt"]),
    "cumshot_goopy": tmpl("Cum shot - goopy dense (extreme variant: wax-like, no spray)",
                          k11["k11_goopy_06"]["prompt"]),
    "cumshot_mouth": tmpl("Cum shot - clean swallow (into the mouth, nothing outside)",
                          k11["k11_mouth_06"]["prompt"]),
    "cumshot_softening": tmpl("Cum shot - messy mouth + keeps sucking while he softens",
                              k11["k11_softening_06"]["prompt"]),
}

PP = os.path.join(ROOT, "kit", "presets.json")
P = json.load(io.open(PP, encoding="utf-8"))
old = P["video_templates"]

# keep the blowjob-side presets in their place, and put the cum dial where the cum presets were
new = {}
cum_inserted = False
for key, val in old.items():
    if key.startswith("cumshot_"):
        if not cum_inserted:
            new.update(CUM)
            cum_inserted = True
        continue
    new[key] = val
if not cum_inserted:
    new.update(CUM)

P["video_templates"] = new

# the Generate-tab duplicate tracks the default tier
P["templates"]["video_facial"]["label"] = "Video - cum shot, MEDIUM (the default tier)"
P["templates"]["video_facial"]["prompt"] = k16["k16_medium"]["prompt"]
P["templates"]["video_facial"]["nsfw_strength"] = 0.6

with io.open(PP, "w", encoding="utf-8", newline="\n") as f:
    json.dump(P, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("video_templates:", list(new))
