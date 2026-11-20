#!/usr/bin/env python3
"""clean.py - hygiene pass for one ComfyUI box.

Every render lands in <root>/<outputs>/<sub>/ and every upload in <root>/<inputs>/<sub>/; both
are world-readable over the LAN and a PNG keeps its prompt in the metadata, so the batch is
pulled to the private folder first and then deleted here. Only the prompt ids this run created
are dropped from /history - the box's other history is not ours to erase.

  python clean.py --box local|ampere --sub gl/g01 [--input-sub gl_up] [--ids id1,id2] [--keep-files]
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

BOXES = {
    # url, root, output dir name, input dir name, path separator
    "local": ("http://127.0.0.1:8188", r"F:\LLStudioTest", "outputs", "inputs", "\\"),
    "ampere": ("http://10.0.10.240:8188", "/data/comfyui", "output", "input", "/"),
    "lame": ("http://10.0.10.56:8188", "/lamedata/comfyui", "output", "input", "/"),
}
SSH = {"ampere": ["ssh", "-o", "BatchMode=yes", "root@10.0.10.240"],
       "lame": ["ssh", "-o", "BatchMode=yes", "root@10.0.10.56"]}


def http(base, path, data=None, timeout=60):
    req = urllib.request.Request(base + path, data=data, method="POST" if data else "GET",
                                 headers={"Content-Type": "application/json"} if data else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode() or "null")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--box", choices=sorted(BOXES), required=True)
    ap.add_argument("--sub", required=True)
    ap.add_argument("--input-sub", default=None)
    ap.add_argument("--ids", default=None, help="comma list of prompt ids to drop from history")
    ap.add_argument("--keep-files", action="store_true")
    a = ap.parse_args()
    base, root, outs, ins, sep = BOXES[a.box]

    if a.ids:
        ids = [i for i in a.ids.split(",") if i]
        try:
            http(base, "/history", json.dumps({"delete": ids}).encode())
            print("history: dropped %d of this run's prompt(s)" % len(ids))
        except Exception as e:
            print("history: %s" % e)

    if a.keep_files:
        return
    dirs = [root + sep + outs + sep + a.sub.replace("/", sep)]
    if a.input_sub:
        dirs.append(root + sep + ins + sep + a.input_sub)
    for d in dirs:
        if a.box == "local":
            n = 0
            for base_dir, _dirs, files in os.walk(d):
                for f in files:
                    os.remove(os.path.join(base_dir, f))
                    n += 1
            print("%s: removed %d file(s)" % (d, n))
        else:
            r = subprocess.run(SSH[a.box] + ["rm -rf %s; echo removed" % d], capture_output=True, text=True)
            print("%s: %s %s" % (d, r.stdout.strip(), r.stderr.strip()[:200]))


if __name__ == "__main__":
    main()
