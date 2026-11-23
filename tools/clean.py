#!/usr/bin/env python3
"""clean.py - hygiene pass for one ComfyUI box.

Every render lands in <root>/<outputs>/<sub>/ and every upload in <root>/<inputs>/<sub>/; both
are world-readable over the LAN and a PNG keeps its prompt in the metadata, so the batch is
pulled to the private folder first and then deleted here. Only the prompt ids this run created
are dropped from /history - the box's other history is not ours to erase.

  python clean.py --box local --sub gl/g01 [--input-sub gl_up] [--ids id1,id2] [--keep-files]
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request


def _local():
    """The engine kit/start.ps1 runs on this machine: always 127.0.0.1:8188, with ComfyUI's
    output/input folders at <data_dir>/outputs and <data_dir>/inputs (data_dir from my/settings.json,
    default <repo>/gallery). Not comfy_url: that may point the page at another engine."""
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        with open(os.path.join(repo, "my", "settings.json"), encoding="utf-8-sig") as f:
            s = json.load(f)
    except (OSError, ValueError):
        s = {}
    return "http://127.0.0.1:8188", s.get("data_dir") or os.path.join(repo, "gallery")


# `local` (this PC) is the only box on a normal install; more engines only come from the
# git-ignored tools/boxes.local.json (tools/localboxes.py)
import localboxes  # noqa: E402
BOXES = {
    # url, root, output dir name, input dir name, path separator
    "local": _local() + ("outputs", "inputs", os.sep),
}
SSH = {}
for _k, _v in localboxes.load().items():
    BOXES[_k] = (_v["url"], _v.get("root", ""), "output", "input", "/")
    if _v.get("ssh"):
        SSH[_k] = list(_v["ssh"])


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
    if a.sub.replace("\\", "/").strip("/").split("/")[0] in ("", "studio", "..") or ".." in a.sub:
        sys.exit("clean: refusing --sub %r (outputs/studio is the user's private gallery)" % a.sub)
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
