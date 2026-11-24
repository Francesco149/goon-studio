#!/usr/bin/env python3
"""bench_templates.py - time page templates exactly as the page runs them (core.run), with peak VRAM.

Run it on the machine that hosts the engine (VRAM is sampled locally: nvidia-smi, or sysfs for an AMD
card on Linux). Each job is a page job ({"name", "template", "seed", ...overrides}, like
tools/rounds/run_template_round.py); every job runs --repeat times (seed, seed+1, ...: the same seed
would be served from ComfyUI's cache in 0.2 s), so the first run is "cold" (weights loaded) and the
next ones "warm". One JSON line per run goes to
jobs/<round>_bench.jsonl with the engine's flags label (--label), so flag sets can be compared later.

  python tools/experiments/bench_templates.py jobs/b16_krea.jsonl b16 --label "ck reserve1.5" --repeat 2
         [--engine URL] [--only a,b]

Renders land in <data_dir>/<round>/ as the agent's pictures (the page shows them under Rounds/All).
"""
import argparse, json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "kit", "studio"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs")
    ap.add_argument("round")
    ap.add_argument("--label", default="", help="the engine flags / variant being measured")
    ap.add_argument("--repeat", type=int, default=2)
    ap.add_argument("--engine")
    ap.add_argument("--only")
    a = ap.parse_args()
    if a.engine:
        os.environ["GOON_COMFY_URL"] = a.engine
    import core
    from bench import Sampler, exec_seconds
    only = set(a.only.split(",")) if a.only else None
    out = os.path.join(ROOT, "jobs", "%s_bench.jsonl" % a.round)
    if os.path.abspath(out) == os.path.abspath(a.jobs):
        sys.exit("the results file would be the jobs file: name the jobs something other than <round>_bench.jsonl")
    s = core.settings()
    for line in open(a.jobs, encoding="utf-8-sig"):
        if not line.strip():
            continue
        j = json.loads(line)
        if "exec_s" in j:   # a results row, not a job
            continue
        if only and j["name"] not in only:
            continue
        for rep in range(a.repeat):
            job = {k: v for k, v in j.items() if not k.startswith("_")}
            job["round"] = a.round
            job["name"] = "%s_r%d" % (j["name"], rep)
            if "seed" in job:
                job["seed"] = int(job["seed"]) + rep
            pid = {}
            smp = Sampler()
            smp.start()
            t0 = time.time()
            err = None
            try:
                rec = core.run(job, by="agent", on_queued=lambda p: pid.__setitem__("id", p))
            except Exception as ex:
                rec, err = {}, str(ex)[:300]
            wall = time.time() - t0
            smp.stop.set()
            smp.join(2)
            ex_s = None
            if pid.get("id"):
                try:
                    h = json.loads(core.http(s["comfy_url"] + "/history/" + pid["id"]))
                    ex_s = exec_seconds(h.get(pid["id"], {}))
                except Exception:
                    pass
            row = {"time": time.strftime("%Y-%m-%dT%H:%M:%S"), "label": a.label, "name": j["name"], "rep": rep,
                   "template": j.get("template"), "workflow": rec.get("workflow"), "width": rec.get("width"),
                   "height": rec.get("height"), "steps": rec.get("steps"), "length": rec.get("length"),
                   "exec_s": ex_s, "wall_s": round(wall, 1), "peak_vram_mb": smp.peak_vram,
                   "min_free_ram_gb": smp.min_free_ram and round(smp.min_free_ram, 1),
                   "files": rec.get("files"), "error": err}
            print(json.dumps(row), flush=True)
            with open(out, "a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    main()
