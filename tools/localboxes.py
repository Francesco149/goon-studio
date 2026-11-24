"""localboxes.py - extra ComfyUI engines for the tools' --box option, from tools/boxes.local.json.

Every install renders on its own PC (`local`: 127.0.0.1, port from my/settings.json comfy_url,
default 8187 - the engine kit/start.ps1 runs; Love Live Studio keeps 8188).
tools/boxes.local.json is git-ignored and exists only where someone set up more engines:

  {"name": {"url": "http://host:8188", "root": "/path/to/comfyui", "ssh": ["ssh", "user@host"]}}

root: the ComfyUI folder on that machine (output/ and input/ under it, or the names in "outputs" /
"inputs" when the engine writes elsewhere, e.g. a Studio's gallery/outputs); ssh: optional, for
tools/clean.py. "_default": "<name>" makes that box the tools' default instead of `local` (the round
runners' engine too, when no --engine is given). Nothing here is needed on a normal install.
"""
import json, os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "boxes.local.json")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Goon Studio's engine port. Love Live Studio uses 8188 (page 8190); a different default keeps the two
# apps from sharing one engine, whose --output-directory belongs to whichever app started it.
DEFAULT_URL = "http://127.0.0.1:8187"


def settings():
    try:
        with open(os.path.join(REPO, "my", "settings.json"), encoding="utf-8-sig") as f:
            return json.load(f) or {}
    except (OSError, ValueError):
        return {}


def local_url(s=None):
    """The engine kit/start.ps1 runs on this PC: comfy_url when it is 127.0.0.1/localhost (the port
    the launcher uses too), else 127.0.0.1:8187."""
    import re
    u = str((settings() if s is None else s).get("comfy_url") or "").rstrip("/")
    if u in ("http://127.0.0.1:8188", "http://localhost:8188"):
        return DEFAULT_URL   # an install from before the split; kit/start.ps1 rewrites it
    return u if re.match(r"^https?://(127\.0\.0\.1|localhost)(:\d+)?$", u) else DEFAULT_URL


def default_name():
    """The box the tools use when none is given: boxes.local.json "_default" when it names a box
    there, else `local`."""
    try:
        with open(PATH, encoding="utf-8-sig") as f:
            name = (json.load(f) or {}).get("_default")
    except (OSError, ValueError, AttributeError):
        return "local"
    return name if name in load() else "local"


def default_url():
    """The default box's engine URL when it is not this PC (None for `local`)."""
    name = default_name()
    return None if name == "local" else load()[name]["url"]


def load():
    try:
        with open(PATH, encoding="utf-8-sig") as f:
            d = json.load(f)
    except (OSError, ValueError):
        return {}
    return {k: v for k, v in d.items() if isinstance(v, dict) and v.get("url")}
