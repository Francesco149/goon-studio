"""Generate jobs/k01.jsonl - round 1 of the cum-shot sessions.

The design, in one place:

Round 1 varies TWO things against a control, all at one seed, one keyframe, 81 frames:

  A. the SHAPE wording: "rope ... shoots from the tip up across her lips" (the v13 wording
     that produced a hair-thin thread that hangs for the whole clip) versus the new
     "dense bead swells / breaks free / flicks up / lands / spreads into a pool".
     Reason: "rope" and "shoots across" describe a continuous body joining two points, and
     that is exactly what H3 draws. A bead that detaches and lands has no joining geometry.

  B. the LoRA strength x material wording interaction. v14a lowered epic_cumshots to 0.5 AND
     asked for "thin ... strands", and got mist. The two levers were confounded: nobody has
     tested 0.5 with DENSE wording. If the mist came from the wording, 0.5 + dense is the
     sweet spot (it keeps the event and drops some of the learned glue).

  C. the keyframe carrying the material. The still model has the approved material, and H3
     preserves its keyframe (docs/CUM-VIDEO.md, keyframe inheritance). p5_landed_clean is the
     approved landed look: thick milky pool on tongue and lower lip, a heavy drip from the
     chin, and NO strand from the tip. Starting from it makes the clip about a fresh bead
     landing in an existing pool instead of about inventing the whole event.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k01.jsonl"))
REF = r"gallery\refs\cumshot"

SOUND_ONE = ("\n\noverall_soundscape: one soft wet splat, one short male grunt, her sharp breath in, "
             "quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")
SOUND_MULTI = ("\n\noverall_soundscape: three soft wet splats about a second apart, one low male groan, "
               "her breath catching, quiet bedroom room tone. No music.\n\nnon_diegetic_music: N/A")

HEAD = "integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed camera. "
POSE = ("A young adult Asian woman in her mid-twenties with long black hair in pink-streaked twin tails "
        "and a silver choker kneels between the viewer's legs with her mouth wide open and her tongue out, "
        "her eyes on the lens; his erect adult cock stands upright an inch below her open mouth, held at "
        "the base in her hand. ")

CONTROL = (
    "integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video. She holds his cock just "
    "below her open mouth, eyes on the lens. The shaft pulses once and a short translucent milky rope shoots "
    "from the tip up across her lips and cheek, glossy and see-through, then drips down her chin. It is one "
    "short arc, no spray, nothing foams. She flinches, closes one eye, then smiles with half-lidded eyes, "
    "flushed. The camera does not move."
    + SOUND_ONE)

BEAD = (HEAD + POSE +
        "The shaft jerks upward once. A single dense bead of milky semen swells out of the tip, breaks free, "
        "flicks up and lands on her tongue, where it spreads into a glossy milky patch; two or three separate "
        "droplets spatter her lower lip. The tip is clean and separate afterwards and no thread hangs from it. "
        "She flinches, closes her mouth, swallows, and looks back up with half-lidded eyes, flushed. "
        "The camera does not move."
        + SOUND_ONE)

MULTI = (HEAD + POSE +
         "The shaft jerks three times, about a second apart. On each jerk a single dense bead of milky semen "
         "swells out of the tip, breaks free, flicks up and lands on her tongue; each bead stays where it "
         "lands and the patch on her tongue grows thicker and glossier, a little of it spilling onto her "
         "lower lip. Between the jerks nothing comes out of the tip, the tip stays clean and no thread hangs "
         "from it. After the third jerk the semen sits in a thick milky pool on her tongue and lower lip and "
         "a slow heavy drip runs from her chin. She flinches at each spurt, swallows, and looks back up with "
         "half-lidded eyes, flushed. The camera does not move."
         + SOUND_MULTI)

P5_HEAD = ("integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed camera. "
           "Close-up POV: a young adult Asian woman in her mid-twenties with long black hair in pink-streaked "
           "twin tails kneels between the viewer's legs with her mouth open and her tongue out. Thick milky "
           "semen already sits pooled on her tongue and lower lip and hangs in a heavy drip from her chin; "
           "his erect adult cock stands upright below her chin with its tip clean and separate. ")
P5_BEAD = (P5_HEAD +
           "His shaft jerks up once, a fresh dense bead of milky semen swells out of the tip, breaks free and "
           "lands in the pool on her tongue. The pool shifts and spreads, the heavy drip on her chin "
           "lengthens, sags and falls. She flinches slightly, swallows, and looks into the lens with "
           "half-lidded eyes. The camera does not move. Nothing connects the tip to her face."
           + SOUND_ONE)


def job(name, wf, prompt, image, strength=None, lora="h3nsfw/epic_cumshots.safetensors", why=""):
    j = {
        "name": name,
        "wf": wf,
        "image": os.path.join(REF, image),
        "width": 768,
        "height": 1152,
        "length": 81,
        "seed": 901,
        "prompt": prompt,
        "_why": why,
    }
    if strength is not None:
        j["nsfw_lora"] = lora
        j["nsfw_strength"] = strength
    return j


LORA_WF = "wf_h3vid_i2v_lora.json"
I2V_WF = "wf_h3vid_i2v.json"

rows = [
    job("k01_control_rope08", LORA_WF, CONTROL, "p1_pose.png", 0.8,
        why="v13 wording verbatim (the hair-thin hanging thread), new seed+length"),
    job("k01_bead08", LORA_WF, BEAD, "p1_pose.png", 0.8,
        why="bead wording at the strength that gave good dynamics"),
    job("k01_bead05", LORA_WF, BEAD, "p1_pose.png", 0.5,
        why="bead wording at the strength that gave mist - isolates wording from strength"),
    job("k01_multi08", LORA_WF, MULTI, "p1_pose.png", 0.8,
        why="three jerk+bead beats a second apart, pooling end state"),
    job("k01_multi05", LORA_WF, MULTI, "p1_pose.png", 0.5,
        why="same, lower strength"),
    job("k01_nolora_bead", I2V_WF, BEAD, "p1_pose.png", None,
        why="does base H3 do the event with the new shape wording at all"),
    job("k01_p5key08", LORA_WF, P5_BEAD, "p5_landed_clean.png", 0.8,
        why="approved landed material as the keyframe, fresh bead into the pool"),
    job("k01_p5key05", LORA_WF, P5_BEAD, "p5_landed_clean.png", 0.5,
        why="same at 0.5"),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
for r in rows:
    print(" ", r["name"], r.get("nsfw_strength", "no-lora"), len(r["prompt"]), "chars")
