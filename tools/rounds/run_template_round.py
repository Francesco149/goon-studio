#!/usr/bin/env python3
"""run_template_round.py - render a round through the page's own engine layer (core.run), so the
templates are tested exactly as the page runs them (model, LoRAs, motion, memory check).

  python tools/rounds/run_template_round.py jobs/a85_template_review.jsonl a85 [--engine URL]

Each job line is a page job: {"name", "template", "seed", ...overrides}. "image_from": "<name>"
uses the first file another job in the round produced (a keyframe made in the same round).
Keys starting with "_" are notes. Renders go to <data_dir>/<round>/ as the agent's pictures.
"""
import json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "kit", "studio"))


def main():
    args = sys.argv[1:]
    if "--engine" in args:
        i = args.index("--engine")
        os.environ["GOON_COMFY_URL"] = args[i + 1]
        del args[i:i + 2]
    else:
        sys.path.append(os.path.join(ROOT, "tools"))   # after kit/studio: tools/headroom.py is another module
        import localboxes
        if localboxes.default_url():   # tools/boxes.local.json "_default" (author setups only)
            os.environ["GOON_COMFY_URL"] = localboxes.default_url()
    jobs_path, rnd = args
    import core  # after the engine override
    data = core.settings().get("data_dir", core.GALLERY)
    made, log = {}, open(os.path.join(ROOT, "jobs", os.path.basename(jobs_path).replace(".jsonl", ".log")), "a", encoding="utf-8")

    def say(msg):
        line = "%s %s" % (time.strftime("%H:%M:%S"), msg)
        print(line, flush=True)
        log.write(line + "\n")
        log.flush()

    for line in open(jobs_path, encoding="utf-8-sig"):
        if not line.strip():
            continue
        j = json.loads(line)
        job = {k: v for k, v in j.items() if not k.startswith("_") and k != "image_from"}
        job["round"] = rnd
        if j.get("image_from"):
            src = made.get(j["image_from"])
            if not src:
                say("%s: skipped, no %s" % (j["name"], j["image_from"]))
                continue
            job["image"] = os.path.join(data, src)
        t0 = time.time()
        try:
            rec = core.run(job, by="agent", on_note=lambda txt, plan: say("%s: memory %s - %s" % (j["name"], plan["profile"], txt)))
            made[j["name"]] = rec["files"][0] if rec["files"] else None
            say("%s: ok %.0fs %s %s" % (j["name"], time.time() - t0, rec["workflow"], rec["files"]))
        except Exception as e:
            say("%s: FAILED after %.0fs: %s" % (j["name"], time.time() - t0, e))
    say("round %s done" % rnd)


if __name__ == "__main__":
    main()
