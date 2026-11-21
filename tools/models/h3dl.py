#!/usr/bin/env python3
"""Fetch a short list of HF files to a local dir, resumable, with progress."""
import os, sys, time, urllib.request, urllib.parse

BASE = "https://huggingface.co"
ITEMS = [
    # (repo, path-in-repo, dest subdir)
    ("kimjob/h3_NSFW_lora", "loras/H3/prod/HMNSFW_AIO_V2.safetensors", "loras/h3nsfw"),
    ("kimjob/h3_NSFW_lora", "loras/H3/prod/MM-H3 - Blowjob.safetensors", "loras/h3nsfw"),
    ("kimjob/h3_NSFW_lora", "loras/H3/test/MM-H3 - Blowjob v3.safetensors", "loras/h3nsfw"),
    ("kimjob/h3_NSFW_lora", "loras/H3/test/HMCumshot_V2.safetensors", "loras/h3nsfw"),
    ("kimjob/h3_NSFW_lora", "loras/H3/test/H3_Motion_BoosterV2.safetensors", "loras/h3nsfw"),
    ("kimjob/h3_NSFW_lora", "loras/H3/test/Minimax3_BoobPhysics_v1.safetensors", "loras/h3nsfw"),
    ("kimjob/h3_NSFW_lora", "loras/H3/test/zy_Amateur_Pov_H3.safetensors", "loras/h3nsfw"),
    ("kimjob/h3_NSFW_lora", "loras/H3/test/Titjob - Titfuck ComfyTinker Minimax V0.9safetensors.safetensors", "loras/h3nsfw"),
    ("kimjob/h3_NSFW_lora", "loras/H3/test/h3-sideview-deepthroat-step00007800-k3nk.safetensors", "loras/h3nsfw"),
    ("kimjob/h3_NSFW_lora", "loras/H3/test/HMPenis_v2_e35.safetensors", "loras/h3nsfw"),
    ("kimjob/h3_NSFW_lora", "loras/H3/test/blowjob_in_cheek_101_h3_.safetensors", "loras/h3nsfw"),
    ("RunningHubAI/rh-minimax-h3-astro-nsfw-lora", "Astro nsfw.safetensors", "loras/h3nsfw"),
    ("RunningHubAI/rh-ramthrusts-nsfw-pink-alchemy-anima-v2.9-unet", "ramthrustsNSFWPINK_v29Anima10base.safetensors", "unet"),
]

if len(sys.argv) < 2:
    sys.exit("usage: h3dl.py <ComfyUI models dir>   (e.g. <engine_dir>/ComfyUI/models)")
ROOT = sys.argv[1]

def size(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "goon-studio"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers.get("Content-Length") or 0), r.geturl()

def get(repo, path, destdir):
    url = "%s/%s/resolve/main/%s" % (BASE, repo, urllib.parse.quote(path, safe="/"))
    d = os.path.join(ROOT, destdir)
    os.makedirs(d, exist_ok=True)
    dest = os.path.join(d, os.path.basename(path))
    total, real = size(url)
    if os.path.exists(dest) and total and os.path.getsize(dest) == total:
        print("skip", dest, flush=True)
        return
    have = os.path.getsize(dest) if os.path.exists(dest) else 0
    req = urllib.request.Request(url, headers={"User-Agent": "goon-studio"})
    if have:
        req.add_header("Range", "bytes=%d-" % have)
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "ab") as f:
        got = have
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
            got += len(chunk)
            if got // (20 << 20) != (got - len(chunk)) // (20 << 20):
                el = max(time.time() - t0, 0.001)
                print("  %-40s %6.1f/%6.1f MB  %5.1f MB/s" % (os.path.basename(dest), got / 1e6,
                      (total or got) / 1e6, (got - have) / 1e6 / el), flush=True)
    print("done", dest, os.path.getsize(dest), "bytes", flush=True)

if __name__ == "__main__":
    for repo, path, d in ITEMS:
        try:
            get(repo, path, d)
        except Exception as e:
            print("FAIL", path, e, flush=True)
