import json, os, sys

frames_dir = sys.argv[1]
out_jsonl = sys.argv[2]
denoise = float(sys.argv[3]) if len(sys.argv) > 3 else 0.45
pattern = sys.argv[4] if len(sys.argv) > 4 else "f*.png"

POS = ("masterpiece, best quality, year 2016, 2D anime screenshot, cel shading, 1girl, 1boy, "
       "hetero, blowjob, fellatio, penis in mouth, lips sealed around penis, detailed penis shaft, "
       "veins, erection, uncensored, penis focus, black hair, twintails, pink streaks, silver choker, "
       "half-closed eyes, blush, saliva, bedroom, soft light")
NEG = ("3d, photorealistic, realistic, extra hands, extra fingers, bad anatomy, censored, "
       "mosaic censoring, tongue out, open mouth, blurry, low quality")

files = sorted(f for f in os.listdir(frames_dir) if f.lower().endswith(".png"))
with open(out_jsonl, "w", encoding="utf-8") as fh:
    for i, name in enumerate(files):
        job = {
            "name": os.path.splitext(name)[0],
            "image": os.path.join(frames_dir, name),
            "prompt": POS,
            "negative": NEG,
            "seed": 777,
            "denoise": denoise,
            "steps": 24,
            "cfg": 4.0,
        }
        fh.write(json.dumps(job, ensure_ascii=False) + "\n")
print(len(files), "jobs ->", out_jsonl)
