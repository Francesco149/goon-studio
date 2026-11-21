#!/usr/bin/env python3
"""mk_a27.py - the voice-only sound test on the k9 blowjob base."""
import json

K9 = next(json.loads(l) for l in open("jobs/a19_suction_perf.jsonl", encoding="utf-8") if l.strip())
p = K9["prompt"]
i = p.index("overall_soundscape:")
j = p.index("non_diegetic_music:")
new = ("overall_soundscape: no wet Foley and no skin sounds; only her soft breathy moans and quick breaths, "
       "one low male groan, and the quiet bedroom room tone. No music, no speech, no chewing, no crunch, no "
       "slurp, no clicks.\n\n")
p = p[:i] + new + p[j:]
j2 = dict(K9)
j2["name"] = "k15_voice_only"
j2["seed"] = 93011
j2["prompt"] = p
with open("jobs/a27_voice_sound.jsonl", "w", encoding="utf-8") as f:
    f.write(json.dumps(j2, ensure_ascii=False) + "\n")
print("wrote k15_voice_only")
