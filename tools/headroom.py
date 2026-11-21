#!/usr/bin/env python3
"""headroom.py - is there memory for a job right now, and what should the user close?

  python tools/headroom.py anime_pov            # a template or video recipe
  python tools/headroom.py --workflow wf_h3vid_i2v.json

Prints the profile (ok / lean / critical), the estimate, and the apps that would free the most.
The page and tools/lab.py run the same check before every job (kit/studio/headroom.py).
"""
import argparse, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kit", "studio"))
import headroom as H  # noqa: E402
import modelstore as M  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("template", nargs="?")
    ap.add_argument("--workflow")
    a = ap.parse_args()
    wf, f = M.template_job(a.template) if a.template else (a.workflow or "wf_krea2_nsfw_8gb.json", {})
    wf = a.workflow or wf
    p = H.plan(wf, f)
    print("profile: %s   job needs ~%s GB, free (commit + our engine) ~%s GB, RAM free %s GB, other apps' VRAM %s GB"
          % (p["profile"], p["need_gb"], p.get("have_gb", "?"), p.get("ram_free", "?"), p.get("vram_other_gb", "?")))
    if p["workflow"] != wf:
        print("low-memory mode would use:", p["workflow"])
    txt = H.summary(p)
    print(txt or "enough memory; nothing to close.")


if __name__ == "__main__":
    main()
