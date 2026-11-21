#!/usr/bin/env python3
"""mk_video_templates.py - turn the approved anime clip jobs into Video-tab templates.

The prompts are read straight from the jobs files, so the template is exactly what was rendered.
"""
import json

P = json.load(open("kit/presets.json", encoding="utf-8"))


def job(path, name):
    for line in open(path, encoding="utf-8"):
        if line.strip():
            j = json.loads(line)
            if j["name"] == name:
                return j
    raise SystemExit("no %s in %s" % (name, path))


specs = [
    ("anime_ll_cumshot", "Anime - LL cum shot (thin ropes + shaft twitch)", "jobs/a14_twitch.jsonl", "k6_anime_k14_twitch"),
    ("anime_ll_paizuri", "Anime - LL paizuri (tongue stays under the glans)", "jobs/a15_paizuri2.jsonl", "k7_anime_paizuri2"),
    ("anime_ll_suction", "Anime - LL suction deepthroat (hollow cheeks)", "jobs/a13_clips2.jsonl", "k4_anime_suction"),
]

vt = P.setdefault("video_templates", {})
for key, label, path, name in specs:
    j = job(path, name)
    if key in vt:
        print("skip", key)
        continue
    vt[key] = {
        "label": label,
        "workflow": j["wf"],
        "lora": j["nsfw_lora"],
        "strength": j["nsfw_strength"],
        "width": j["width"],
        "height": j["height"],
        "length": j["length"],
        "prompt": j["prompt"],
    }
    print("added", key)

with open("kit/presets.json", "w", encoding="utf-8") as f:
    json.dump(P, f, indent=2, ensure_ascii=False)
    f.write("\n")
