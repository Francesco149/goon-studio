#!/usr/bin/env python3
"""mk_blank.py - the "Start from nothing" templates (2026-11-24): an empty prompt on a picture
workflow and an empty script on the plain H3 i2v workflow, first in their dropdowns. Pick the model
under Expert -> Workflow; nothing is added to what you type."""
import json

P = json.load(open("kit/presets.json", encoding="utf-8"))
blank = {"label": "Blank - an empty prompt, nothing added (pick the workflow under Expert)", "blank": True,
         "workflow": "wf_krea2_nsfw_8gb.json", "prompt": "", "character": "", "scene": "",
         "about": "Nothing from a recipe: what you type in Expert -> Prompt is the whole prompt. The workflow "
                  "(model) is Krea NSFW until you pick another under Expert; size and steps are the workflow's."}
vblank = {"label": "Blank - an empty script, nothing added", "blank": True, "workflow": "wf_h3vid_i2v.json",
          "prompt": "", "width": 512, "height": 768, "length": 85,
          "about": "Nothing from a recipe: the script you write is all the clip gets. Pick a mode (act LoRA, "
                   "first + last, t2v) and LoRAs as you like."}
for sec, entry in (("templates", blank), ("video_templates", vblank)):
    rest = {k: v for k, v in P[sec].items() if k != "blank"}
    P[sec] = {"blank": entry, **rest}
with open("kit/presets.json", "w", encoding="utf-8") as f:
    json.dump(P, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("blank templates added")
