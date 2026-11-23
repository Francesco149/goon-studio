"""mk_a112.py - round a112: penis size continuity between beats (owner, a110: s2 shorter than t1) + t1 upper-lip phasing.

Base: kit/stories/aqua_evening.json (a110). Same keyframe seeds as a110k s2 (110101-110104), same clip seeds.
  keys  KA - size tags in the shared partner block: (long penis:1.2), (large penis:1.1)
        KB - KA + composition: the shaft between her lips and his body stays in view, framing like t1
        KC - KA, her lips on the upper shaft instead of "lips stretched along the shaft" (`keys KC`)
  clips C  - s2 as an `extend` (22-frame context) from the t1 clip: same angle, the size is copied, not redrawn
        P5 - t1 phasing: she raises her head above the tip and lowers her open mouth onto it from above
        AB - s2 clip on the best KA/KB keyframe (`--clip KEY`, after the keyframes are scored)
  suck  S1-S3 - s2 extended from P5 with a sealed-lips suction script (owner: C showed no suction)
Usage: python tools/rounds/mk_a112.py keys|clips [--clip a112k/xx.png]  -> jobs/a112k_keys.jsonl / jobs/a112_clips.jsonl
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = json.load(open(os.path.join(ROOT, "kit/stories/aqua_evening.json"), encoding="utf-8"))
B, ST, CL = D["blocks"], D["still"], D["clip"]
SH = {s["id"]: s for s in D["shots"]}
GAL = os.path.join(ROOT, "gallery").replace("\\", "/")

SIZE = "(long penis:1.2), (large penis:1.1)"
COMP = "(shaft visible:1.2), (penis between her lips and his body:1.1), upper body, (centered:1.1)"


def fill(s, **kw):
    v = dict(B, **kw)
    for k, x in v.items():
        s = s.replace("{" + k + "}", x)
    return s


def still(var, seed):
    partner = B["partner"] + ", " + SIZE
    p = fill(SH["s2"]["still"], partner=partner)
    if var == "KB":
        p = p.replace(", uncensored,", ", " + COMP + ", uncensored,")
    if var == "KC":  # her lips on the upper shaft, the rest of the shaft in view (KA/KB drew her lips at the base)
        p = p.replace("(lips stretched along the shaft:1.2)", "(sucking the tip:1.2), (glans in mouth:1.1), "
                      "(long shaft visible below her lips:1.2), (penis upright:1.1)")
    j = {k: ST[k] for k in ("workflow", "lora", "strength", "width", "height", "steps", "cfg")}
    j.update(SH["s2"].get("still_job", {}), name=f"{var}_{seed}", seed=seed, prompt=p)
    return j


def clip(name, seed, script, image, **kw):
    j = {k: CL[k] for k in ("width", "height", "unet", "motion_lora")}
    j.update(name=name, template="anime_ll_headgrab_push", seed=seed, prompt=fill(script), length=124, anime_timing="off",
             image=image)
    j.update(kw)
    return j


S2 = SH["s2"]["script"]
S2C = S2.replace("POV from above: {script_character} lies on her stomach between the man's legs, her hips raised behind her, "
                 "with his cock in her mouth.",
                 "Continuing, the same view: {script_character} takes more of his cock into her mouth.")
assert S2C != S2
T1 = SH["t1"]["script"]
P5 = T1.replace("then lifts her head a little, moves her open mouth over the tip, closes her lips around the head of his cock",
                "then raises her head until her mouth is above the tip, opens her mouth wide and lowers it down onto the tip "
                "from above, closing her lips around the head of his cock")
assert P5 != T1


# a112s (owner: C keeps the size but shows zero suction - her lips keep t1's open smile). The extension has no keyframe
# to carry the suction face, so the script must close the seal itself: a transition sentence, the approved a106 suction
# line (docs/SCENES.md), no smile, no saliva sentence (it built a white curtain in C).
SUCK = ("integrated_multimodal_description: [Shot 1] {script_style} Continuing, the same view: {script_character} stops "
        "smiling, closes her lips tight around the shaft and begins to suck. She bobs her head slowly and steadily along "
        "the upper half of the shaft, her lips sealed tight around it. Her lips stay softly sealed around the shaft and are "
        "drawn a little forward along it as she pulls back, her cheeks drawn in slightly by the suction. She looks up into "
        "the camera with sweet, needy eye contact, her brows tilted up, blushing. His cock stays long and thick, with clear "
        "veins along the shaft; its head is the same skin tone as the shaft. The camera does not move.\n\n"
        "overall_soundscape: close-miked Foley, loud and present, over the quiet of a wooden bedroom in the evening, no "
        "music and no speech: {sound}\n\nnon_diegetic_music: N/A")
SND1 = "a slow, soft wet suction, her nose breathing."
SND2 = "strong, tight wet suction on every stroke, a soft slurp as she pulls back, her nose breathing."


def main():
    mode = sys.argv[1]
    if mode == "keys":
        vs = sys.argv[2:] or ["KA", "KB"]
        out = [still(v, s) for v in vs for s in (110101, 110102, 110103, 110104)]
        path = "jobs/a112k_keys.jsonl" if not sys.argv[2:] else f"jobs/a112k_{'_'.join(vs)}.jsonl"
    elif mode == "suck":
        src = GAL + "/a112/P5_lower_00001_.mp4"
        ext = dict(length=141, ctx_len=22, ctx_start=102)
        out = [clip("S1_seal", 109002, SUCK.replace("{sound}", SND1), src, **ext),
               clip("S2_seal_snd", 109002, SUCK.replace("{sound}", SND2), src, **ext),
               clip("S3_seal_s2", 109012, SUCK.replace("{sound}", SND2), src, **ext)]
        path = "jobs/a112s_suck.jsonl"
    else:
        out = [clip("C_ext_t1", 109002, S2C, GAL + "/a110p/p4_upright_trans_00001_.mp4", length=141, ctx_len=22, ctx_start=102),
               clip("P5_lower", 109001, P5, GAL + "/a110k/t1c_110112_00001_.png")]
        if "--clip" in sys.argv:
            out.append(clip("AB_s2", 109002, S2, GAL + "/" + sys.argv[sys.argv.index("--clip") + 1]))
        path = "jobs/a112_clips.jsonl"
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        for j in out:
            f.write(json.dumps(j, ensure_ascii=False) + "\n")
    print(path, len(out))


if __name__ == "__main__":
    main()
