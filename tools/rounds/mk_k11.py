"""Generate jobs/k11.jsonl - round 7, the variant presets the owner asked for.

Owner (2026-11-21): "different variants like the goopy one would be a preset of their own. my
preferred is the more normal one like all the tribute videos I added." And on the two mouth refs:
the clean in-mouth swallow has no smudging outside the mouth, while the low-amount outdoor one is
the MESSIER mouth ref, including her sucking him again after he comes as he goes soft - which is
the reference for how the cum evolves as it is spread around while the cock softens.

So the cum presets are a matrix, not one look. This round renders the three variants that are not
yet on disk (the normal is k10, the exaggerated maximum is k07):

  goopy      the dense/semi-solid variant (guide §4.1): no spray, no atomization, heavy cords that
             tumble out and pile like wax, zero splash, stubby drips. Its own preset.
  mouth      the clean swallow (guide §4.6): one rope into the mouth, she closes and swallows, the
             hyoid rises, then the glossy tongue coating with one thread between the lips - nothing
             on her face outside the mouth.
  softening  the messy mouth + aftercare (the low-amount outdoor ref): some lands on her lips, she
             takes him back in while he softens and keeps sucking, the cum mixes with saliva and
             thins and smears, milky threads stretch each time the softening head slips out.

All three use the owner-liked k07 material base and the k10 single-stream/three-pulse mechanics
(one narrow rope from the slit, one stream only, glans bare), so only the variant behaviour differs.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = os.path.abspath(os.path.join(HERE, "..", "..", "jobs", "k11.jsonl"))

P1 = r"C:\Users\headpats\Documents\goon-studio\gallery\refs\cumshot\p1_pose.png"

HEAD = ("integrated_multimodal_description: [Shot 1] Photorealistic amateur POV video, one fixed "
        "camera. A young adult Asian woman in her mid-twenties with long black hair in pink-streaked "
        "twin tails and a silver choker kneels between the viewer's legs, holding his erect adult "
        "cock upright an inch below her open mouth, her tongue out, her eyes on the lens. ")

SOUND = ("\n\noverall_soundscape: soft wet spurts and her breathing, one low male groan, quiet bedroom "
         "room tone. No music.\n\nnon_diegetic_music: N/A")

LORA = "h3nsfw/epic_cumshots.safetensors"

MATERIAL = ("The semen has milky depth and is not flat paint white: a dense cream-white core with thinner "
            "translucent edges that let her skin show faintly through, glossy and wet. ")

GOOPY = ("His cock pulses three times and no more. The semen is extremely dense and semi-solid: creamy "
         "white, thick like melted wax or thick toothpaste, with rounded heavy edges. It does not spray "
         "and does not arc. Each pulse pushes one short heavy cord out of the slit at the tip - one "
         "stream only, never two - that tumbles slowly out and lands with no splash at all, piling up on "
         "itself in a thick mound on her tongue and her lower lip. Nothing atomizes, no droplets fly off, "
         "and nothing lands outside her mouth and lips. His glans stays bare and clean. The mound clings "
         "and barely runs; a short stubby drip hangs from her chin without stretching. She flinches at "
         "each pulse, then looks into the lens with half-lidded eyes, flushed. The camera does not move.")

MOUTH = ("His cock pulses once and one single narrow rope of semen leaves the slit at the tip and goes "
         "straight into her open mouth, landing on her tongue. She closes her mouth and swallows, the "
         "muscle under her jaw lifting once, then opens her mouth again to show a glossy white coating "
         "on her tongue with one thin milky thread bridging her lips and no semen anywhere on her face, "
         "her nose or her cheeks. His glans stays bare and clean, and the tip is only wet. She looks into "
         "the lens with half-lidded eyes, flushed. The camera does not move.")

SOFTENING = ("His cock pulses twice and two single narrow ropes of semen land in her open mouth and on her "
             "lower lip. She swallows, then takes his softening cock back into her mouth and keeps sucking "
             "it gently while it goes soft; her lips slide over it and the semen mixes with her saliva and "
             "thins, smearing glossy and milky around her lips and chin. Each time the softening head slips "
             "out of her mouth a milky thread stretches between her lips and the tip and breaks. The shaft "
             "loses its fullness and droops as she keeps working it. His glans stays wet and clean, no "
             "semen pooling on it. She looks up into the lens with half-lidded eyes and a soft smile, "
             "flushed. The camera does not move.")


def job(name, body, strength):
    return {"name": name, "wf": "wf_h3vid_i2v_lora.json", "image": P1,
            "width": 768, "height": 1152, "length": 124, "seed": 920,
            "nsfw_lora": LORA, "nsfw_strength": strength,
            "prompt": HEAD + MATERIAL + body + SOUND}


rows = [
    job("k11_goopy_06", GOOPY, 0.6),
    job("k11_mouth_06", MOUTH, 0.6),
    job("k11_softening_06", SOFTENING, 0.6),
]

with open(JOBS, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", JOBS, len(rows), "jobs")
