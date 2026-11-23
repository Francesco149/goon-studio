"""localboxes.py - extra ComfyUI engines for the tools' --box option, from tools/boxes.local.json.

Every install renders on its own PC (`local`, 127.0.0.1:8188, the engine kit/start.ps1 runs).
tools/boxes.local.json is git-ignored and exists only where someone set up more engines:

  {"name": {"url": "http://host:8188", "root": "/path/to/comfyui", "ssh": ["ssh", "user@host"]}}

root: the ComfyUI folder on that machine (output/ and input/ under it); ssh: optional, for
tools/clean.py. Nothing here is needed on a normal install.
"""
import json, os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "boxes.local.json")


def load():
    try:
        with open(PATH, encoding="utf-8-sig") as f:
            d = json.load(f)
    except (OSError, ValueError):
        return {}
    return {k: v for k, v in d.items() if isinstance(v, dict) and v.get("url")}
