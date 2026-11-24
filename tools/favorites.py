#!/usr/bin/env python3
"""favorites.py - the agent's side of the page's Favorites tab (my/favorites.json).

Mark what the user approved as a favorite, so it shows in the Favorites tab. Only the agent-visible
store (my/favorites.json: agent gens and shared pictures) is touched here; favorites among the
user's private pictures live in my/private/ and are never read by this tool.

  python tools/favorites.py add a103/emilia_meadow_cut.mp4 --label "Emilia meadow, final cut"
  python tools/favorites.py add --gens a26/k11_seed.mp4 --label "a26 golden BJ"   # copies gens/<path>
                                                         # into gallery/gens/<path> first
  python tools/favorites.py remove a103/emilia_meadow_cut.mp4
  python tools/favorites.py import list.json    # [{"file": ..., "label": ...}, ...]; "gens": true copies
  python tools/favorites.py list

Files are relative to the gallery (data_dir in my/settings.json, default <repo>/gallery). The page
picks the change up on its next refresh. Record an approval here in the same step as the doc that
records the verdict (docs/SCENES.md, docs/OPEN-ITEMS.md).
"""
import argparse, json, os, shutil, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "kit", "studio"))
import core  # noqa: E402

PRIVATE_PREFIXES = ("studio/", "uploads/", "outputs/studio/")


def gallery():
    return core.settings().get("data_dir", core.GALLERY)


def load():
    return core.load_json(core.FAVS, {}) or {}


def add(items):
    """items: [{file, label?, gens?}]; returns how many were added or relabelled."""
    d = load()
    files = d.setdefault("files", {})
    n = 0
    for it in items:
        rel = it["file"].replace("\\", "/").lstrip("/")
        if rel.startswith(PRIVATE_PREFIXES):
            print("skipped (the user's private gallery):", rel)
            continue
        if it.get("gens"):
            src = os.path.join(REPO, "gens", rel)
            rel = "gens/" + rel
            dst = os.path.join(gallery(), rel)
            if not os.path.isfile(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
        if not os.path.isfile(os.path.join(gallery(), rel)):
            print("missing, not added:", rel)
            continue
        e = files.get(rel) or {"time": core.time.time()}
        if it.get("label"):
            e["label"] = it["label"]
        files[rel] = e
        n += 1
    core._write_json(core.FAVS, d)
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("file")
    a.add_argument("--label")
    a.add_argument("--gens", action="store_true", help="the file is under gens/, copy it into the gallery")
    r = sub.add_parser("remove")
    r.add_argument("file")
    i = sub.add_parser("import")
    i.add_argument("json")
    sub.add_parser("list")
    o = ap.parse_args()
    if o.cmd == "add":
        print("added", add([{"file": o.file, "label": o.label, "gens": o.gens}]))
    elif o.cmd == "import":
        with open(o.json, encoding="utf-8-sig") as f:
            print("added", add(json.load(f)))
    elif o.cmd == "remove":
        d = load()
        print("removed", 1 if d.get("files", {}).pop(o.file, None) else 0)
        core._write_json(core.FAVS, d)
    else:
        for f, e in sorted(load().get("files", {}).items(), key=lambda x: x[1].get("time", 0)):
            print("%s  %s" % (f, e.get("label", "")))


if __name__ == "__main__":
    main()
