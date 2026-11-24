#!/usr/bin/env python3
"""mk_a132.py - the photoreal pose candidates from rounds a132/a132b (16 GB session, 2026-11-24).

Verite chain (Krea 2 Turbo INT8 + Verite_realism 1.0, `egirl_bj_pov`'s workflow) for the oral/breast
acts; Krea 2 Turbo NSFW v10 for penetration (the Verite chain draws a baked-in mosaic on the
penetration on most seeds; NSFW v10 does not). Owner-approved 2026-11-24 (all but missionary seed 16202); docs/EGIRL.md
"Poses (a132)".
"""
import json

P = json.load(open("kit/presets.json", encoding="utf-8"))
T = P["templates"]
CHAR = T["egirl_bj_pov"]["character"]
LED = "Dim bedroom lit by pink and purple LED strips."
CAM = "Candid amateur phone photo."
SKIN = "Natural skin texture with pores, no beauty filter, phone camera, slight grain."
SHAFT = "a defined glans with a rim and a natural shaft with smooth skin and faint veins under it"

verite = dict(workflow="wf_krea2_lora_8gb.json", width=896, height=1344, steps=8, cfg=1.0,
              unet="krea2_turbo_int8_convrot.safetensors", lora="Verite_realism.safetensors", strength=1.0,
              character=CHAR, scene="")
nsfw = dict(workflow="wf_krea2_nsfw_8gb.json", width=896, height=1344, steps=6, cfg=1.0, character=CHAR, scene="")

new = {
    "egirl_paizuri": dict(verite, label="Photoreal e-girl - paizuri POV (Krea 2 + Verite; a132, owner-approved)",
        about="Round a132/a132b: 4/4 seeds a clean titjob, the shaft wrapped in cleavage, eyes to camera. 'smooth skin, faint veins' calms Verite's vine-like veins (a132b).",
        prompt="A titjob, close-up POV from above. {character} She kneels between a man's legs, pressing her bare breasts together around his erect cock with both hands so the shaft is wrapped in soft cleavage and only the glans shows above her breasts. The man sits on the edge of the bed; his cock has " + SHAFT + ". Her chin is tucked, her eyes lift to the camera, half-lidded, light blush, a little saliva glistening on her breasts. " + LED + " " + CAM),
    "egirl_prone_bj": dict(verite, label="Photoreal e-girl - blowjob lying on her stomach, feet up (Krea 2 + Verite; a132b, owner-approved)",
        about="Round a132b: 2/2 seeds lying on her stomach between his legs, feet raised behind her, lips sealed. Naming her body 'stretched out behind her' and the raised feet is what moved her off her knees (a132: kneeling).",
        prompt="A blowjob, POV from above. {character} She lies flat on her stomach on the bed between a man's legs, her body stretched out behind her along the bed, her round ass and her bare feet raised in the air at the back of the frame, propped on her elbows. His erect cock is in her mouth: her lips sealed in a tight wet ring around the shaft just behind the glans, her cheeks hollowed. The man lies back against the pillows; his cock has " + SHAFT + ". Her hand wraps the base, her eyes lift to the camera, half-lidded, light blush. " + LED + " " + CAM),
    "egirl_cowgirl": dict(nsfw, label="Photoreal e-girl - cowgirl POV from below (Krea NSFW v10; a132b, owner-approved)",
        about="Round a132b: NSFW v10, 2/2 seeds clean penetration, no mosaic (the Verite chain baked one in on a132 seed 16101).",
        prompt="Photorealistic candid photo. Cowgirl sex, POV from below. {character} She is naked, straddling a man who lies on his back on the bed, his erect cock inside her pussy, her hips sitting down on him. Her hands rest on his chest, her breasts hang forward, her hair falls past her shoulders. She looks down at the camera with half-lidded eyes, mouth slightly open, flushed cheeks. His thighs and stomach are at the bottom of the frame. " + SKIN + " " + LED),
    "egirl_revcowgirl": dict(nsfw, label="Photoreal e-girl - reverse cowgirl POV (Krea NSFW v10; a132b, owner-approved)",
        about="Round a132b: NSFW v10, 2/2 seeds her ass and hips filling the frame, looking back over her shoulder; his hands on her hips.",
        prompt="Photorealistic candid photo. Reverse cowgirl sex, POV from below. {character} She is naked, straddling a man who lies on his back, facing away from him, his erect cock inside her pussy between her spread thighs. Her round ass and wide hips fill the frame, her back arched, her hands on his knees. She looks back over her shoulder at the camera with a flushed smile. " + SKIN + " " + LED),
    "egirl_missionary": dict(nsfw, label="Photoreal e-girl - missionary POV from above (Krea NSFW v10; a132b, owner-approved)",
        about="Round a132b: NSFW v10, 2/2 seeds clean penetration, legs spread, looking up at the camera; check the hands (her hand holds her thigh beside his).",
        prompt="Photorealistic candid photo. Missionary sex, POV from above. {character} She lies naked on her back on the bed, her legs spread and bent around a man kneeling between them, his erect cock inside her pussy. Her breasts rest heavy on her chest, her hair spread around her face on the pillow. She looks up at the camera, lips parted, flushed, eyes half-lidded. His hands hold her thighs. " + SKIN + " " + LED),
    "egirl_doggy": dict(nsfw, label="Photoreal e-girl - doggy from behind (Krea NSFW v10; a132c, candidate)",
        about="Round a132c: NSFW v10, 3/3 seeds on all fours from behind and above, clean penetration, looking back. The camera placement ('behind and above her, looking down along her arched back') and 'her chest lowered to the sheets' fixed a132/a132b (riding poses).",
        prompt="Photorealistic candid photo. Doggy style sex, seen from behind. {character} She is on all fours on the bed, her knees apart on the mattress, her chest lowered to the sheets and her ass raised. The camera is behind and above her, looking down along her arched back: her round ass and wide hips fill the foreground, a man's hands grip her hips, his erect cock is inside her pussy from behind. She looks back over her shoulder at the camera, mouth open, flushed cheeks, her twin tails spilling over the sheets. " + SKIN + " " + LED),
}
for k in ("egirl_paizuri", "egirl_prone_bj", "egirl_cowgirl", "egirl_revcowgirl", "egirl_missionary"):
    new[k]["about"] += " Owner (2026-11-24): approved; the light mosaic the Verite chain sometimes draws is acceptable."
new["egirl_missionary"]["about"] += " Seed 16202 changed her face (the one reject); re-roll when the face drifts."
for k, v in new.items():
    T[k] = v
with open("kit/presets.json", "w", encoding="utf-8") as f:
    json.dump(P, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("added", ", ".join(new))
