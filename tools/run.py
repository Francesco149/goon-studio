#!/usr/bin/env python3
"""run.py - run a JSONL batch of jobs through tools/comfy.py, keep everything private, clean the box.

  python run.py --wf wf_anima.json --jobs jobs.jsonl --box local --sub gl/g01 -o gens/g01 [--dry-run] [--keep]

Job line: {"name": "...", "prompt": "...", "negative": "...", "seed": 1, "steps": 18,
           "width": 832, "height": 1248, "cfg": 4.0, "image": "path/to/ref.png", ...}
  `image`/`image1`/`image2` are uploaded first (their returned input name is passed as the param).
  Any other key is passed as -p key=value (JSON-typed by comfy.py).

After the batch: writes <out>/_manifest.jsonl and <out>/_sheet.jpg, then empties the box's
output/upload folders unless --keep.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COMFY = os.path.join(HERE, "comfy.py")
IMG_KEYS = ("image", "image1", "image2")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wf", required=True)
    ap.add_argument("--jobs", required=True)
    import localboxes
    boxes = {"local": localboxes.local_url()}
    boxes.update({k: v["url"] for k, v in localboxes.load().items()})
    ap.add_argument("--box", default=localboxes.default_name(), choices=sorted(boxes))
    ap.add_argument("--sub", required=True, help="ComfyUI subfolder prefix, e.g. gl/g01")
    ap.add_argument("--out", required=True)
    ap.add_argument("--log", default=None)
    ap.add_argument("--keep", action="store_true", help="leave the renders on the box")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    base = boxes[a.box]
    env = dict(os.environ, COMFY_URL=base)
    os.makedirs(a.out, exist_ok=True)
    jobs = [json.loads(l) for l in open(a.jobs, encoding="utf-8") if l.strip() and not l.startswith("#")]
    log = a.log or os.path.join(a.out, "_run.jsonl")

    for i, job in enumerate(jobs):
        name = job.pop("name")
        wfpath = os.path.join(HERE, a.wf)
        if not os.path.exists(wfpath):
            wfpath = os.path.join(HERE, "..", "workflows", a.wf)
        cmd = [sys.executable, COMFY, "run", wfpath,
               "-o", a.out, "--log", log]
        for k in IMG_KEYS:
            if job.get(k):
                cmd += ["-u", "%s=%s" % (k, job.pop(k))]
        cmd += ["-p", "prefix=%s/%s" % (a.sub, name)]
        for k, v in job.items():
            cmd += ["-p", "%s=%s" % (k, json.dumps(v) if not isinstance(v, str) else v)]
        if a.dry_run:
            print(" ".join(cmd))
            continue
        print("[%d/%d] %s" % (i + 1, len(jobs), name), flush=True)
        r = subprocess.run(cmd, env=env, capture_output=True, text=True)
        for line in (r.stdout or "").strip().splitlines():
            print("   " + line, flush=True)
        if r.returncode != 0:
            print("   FAILED: " + (r.stderr or "").strip()[:600], flush=True)
        if job.get("name") is None:
            pass

    if a.dry_run:
        return
    if not a.keep:
        subprocess.run([sys.executable, os.path.join(HERE, "clean.py"), "--box", a.box, "--sub", a.sub],
                       env=env, check=False)


if __name__ == "__main__":
    main()
