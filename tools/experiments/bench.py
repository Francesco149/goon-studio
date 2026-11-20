#!/usr/bin/env python3
"""bench.py - run a workflow batch and record wall time, server exec time, peak VRAM.

Unlike tools/lab.py this is for measurement, not for keeping a gallery round: it keeps the
renders, appends one JSON line per job to <out>/_bench.jsonl, and samples nvidia-smi while the
job runs. Use it against the benchmark ComfyUI on port 8189 (tools/experiments/bench_engine.ps1)
so the user's 8188 engine is not restarted.

  python tools/experiments/bench.py --wf wf_anima2.json --jobs jobs/bench_anima.jsonl \
      --port 8189 --sub gl/bench/anima_base --out gens/bench/anima_base --repeat 2

Jobs are JSONL: {"name": "...", ...workflow params}. A job field wins over the workflow _params.
"""
import argparse
import ctypes
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PH = re.compile(r"\{\{(\w+)\}\}")
IMG_KEYS = ("image", "image1", "image2", "last", "video")


def http(base, path, data=None, timeout=120, raw=False):
    req = urllib.request.Request(
        base + path, data=data, method="POST" if data else "GET",
        headers={"Content-Type": "application/json"} if data else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read()
    return body if raw else json.loads(body or b"null")


def upload(base, path, sub):
    r = subprocess.run(["curl", "-s", "-F", "image=@" + path, "-F", "overwrite=true",
                        "-F", "subfolder=" + sub, base + "/upload/image"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("upload failed: " + r.stderr[:300])
    j = json.loads(r.stdout)
    return (j.get("subfolder") + "/" if j.get("subfolder") else "") + j["name"]


def coerce(v):
    try:
        return json.loads(v)
    except (ValueError, TypeError):
        return v


def subst(obj, params):
    if isinstance(obj, dict):
        return {k: subst(v, params) for k, v in obj.items()}
    if isinstance(obj, list):
        return [subst(v, params) for v in obj]
    if isinstance(obj, str):
        m = PH.fullmatch(obj)
        if m:
            k = m.group(1)
            if k not in params:
                raise KeyError(k)
            return params[k]

        def rep(mm):
            k = mm.group(1)
            if k not in params:
                raise KeyError(k)
            return str(params[k])
        return PH.sub(rep, obj)
    return obj


def outputs_of(hist):
    for _node, out in (hist.get("outputs") or {}).items():
        for key in ("images", "gifs", "videos", "audio", "files"):
            for item in out.get(key, []) or []:
                if isinstance(item, dict) and "filename" in item and item.get("type", "output") != "temp":
                    yield item


def exec_seconds(hist):
    msgs = {m[0]: m[1] for m in hist.get("status", {}).get("messages", [])}
    try:
        return round((msgs["execution_success"]["timestamp"] - msgs["execution_start"]["timestamp"]) / 1000, 2)
    except (KeyError, TypeError):
        return None


class Sampler(threading.Thread):
    """Poll nvidia-smi and system memory until stopped."""

    def __init__(self, interval=0.4):
        super().__init__(daemon=True)
        self.interval = interval
        self.stop = threading.Event()
        self.peak_vram = 0
        self.peak_gpu = 0
        self.min_free_ram = None
        self.min_free_commit = None

    def run(self):
        while not self.stop.is_set():
            try:
                out = subprocess.run(
                    ["nvidia-smi", "--query-gpu=memory.used,utilization.gpu",
                     "--format=csv,noheader,nounits"],
                    capture_output=True, text=True, timeout=5,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)).stdout.strip()
                used, gpu = [int(x.strip()) for x in out.split(",")[:2]]
                self.peak_vram = max(self.peak_vram, used)
                self.peak_gpu = max(self.peak_gpu, gpu)
            except Exception:
                pass
            try:
                class MEMSTATUS(ctypes.Structure):
                    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
                st = MEMSTATUS()
                st.dwLength = ctypes.sizeof(MEMSTATUS)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st))
                free_gb = st.ullAvailPhys / (1 << 30)
                self.min_free_ram = free_gb if self.min_free_ram is None else min(self.min_free_ram, free_gb)
                # commit headroom (RAM + pagefile): when this hits 0 Windows kills allocations
                commit_gb = st.ullAvailPageFile / (1 << 30)
                self.min_free_commit = commit_gb if self.min_free_commit is None else min(self.min_free_commit, commit_gb)
            except Exception:
                pass
            self.stop.wait(self.interval)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wf", required=True, help="workflow name (resolved in workflows/ or tools/)")
    ap.add_argument("--jobs", required=True)
    ap.add_argument("--url", default="http://127.0.0.1:8189")
    ap.add_argument("--sub", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--seed", type=int, default=None, help="override seed for every job (increments per repeat)")
    ap.add_argument("--only", default=None)
    ap.add_argument("--skip", default=None)
    ap.add_argument("--timeout", type=int, default=7200)
    ap.add_argument("--no-download", action="store_true")
    a = ap.parse_args()

    base = a.url.rstrip("/")
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(ROOT, "workflows", a.wf)
    if not os.path.exists(path):
        path = os.path.join(ROOT, "tools", a.wf)
    wf = json.load(open(path, encoding="utf-8-sig"))
    defaults = dict(wf.pop("_params", {}))
    for k in [k for k in wf if k.startswith("_")]:
        wf.pop(k)
    jobs = [json.loads(l) for l in open(a.jobs, encoding="utf-8-sig") if l.strip() and not l.lstrip().startswith("#")]
    only = set(a.only.split(",")) if a.only else None
    skip = set(a.skip.split(",")) if a.skip else set()
    jobs = [j for j in jobs if (only is None or j["name"] in only) and j["name"] not in skip]
    jobs = jobs * a.repeat

    http(base, "/system_stats", timeout=10)
    upload_sub = "gl_up/" + a.sub.replace("/", "_")
    results = []
    for idx, job in enumerate(jobs):
        job = dict(job)
        name = job.pop("name")
        params = dict(defaults)
        params["prefix"] = "%s/%s" % (a.sub, name)
        for k in IMG_KEYS:
            if job.get(k):
                params[k] = upload(base, job.pop(k), upload_sub)
        for k, v in job.items():
            params[k] = v
        if a.seed is not None:
            params["seed"] = a.seed + idx
        prompt = subst(wf, params)
        sampler = Sampler()
        sampler.start()
        t0 = time.time()
        try:
            r = http(base, "/prompt", data=json.dumps({"prompt": prompt, "client_id": "bench-" + name}).encode())
        except urllib.error.HTTPError as e:
            sampler.stop.set()
            msg = e.read().decode()[:600]
            print("%-24s REJECTED %s" % (name, msg), flush=True)
            results.append({"name": name, "status": "rejected", "error": msg})
            continue
        pid = r["prompt_id"]
        hist = None
        while True:
            time.sleep(0.5)
            try:
                h = http(base, "/history/" + pid, timeout=30)
            except Exception:
                continue
            if pid in h:
                st = h[pid].get("status", {})
                if st.get("completed") or st.get("status_str") in ("success", "error"):
                    hist = h[pid]
                    break
            if time.time() - t0 > a.timeout:
                break
        sampler.stop.set()
        sampler.join(timeout=3)
        wall = round(time.time() - t0, 2)
        st = (hist or {}).get("status", {})
        row = {"name": name, "wf": a.wf, "status": st.get("status_str", "timeout"),
               "wall_s": wall, "exec_s": exec_seconds(hist) if hist else None,
               "peak_vram_mb": sampler.peak_vram, "peak_gpu_pct": sampler.peak_gpu,
               "min_free_ram_gb": round(sampler.min_free_ram, 2) if sampler.min_free_ram is not None else None,
               "min_free_commit_gb": round(sampler.min_free_commit, 2) if sampler.min_free_commit is not None else None,
               "params": {k: params[k] for k in ("unet", "width", "height", "steps", "length", "cfg", "sampler", "denoise")
                          if k in params and isinstance(params[k], (int, float, str))}}
        if hist and st.get("status_str") != "error":
            saved = []
            if not a.no_download:
                for item in outputs_of(hist):
                    q = urllib.parse.urlencode({"filename": item["filename"], "subfolder": item.get("subfolder", ""),
                                                "type": item.get("type", "output")})
                    data = http(base, "/view?" + q, raw=True, timeout=600)
                    dest = os.path.join(a.out, item["filename"])
                    with open(dest, "wb") as f:
                        f.write(data)
                    saved.append(os.path.relpath(dest, ROOT))
            row["outputs"] = saved
        elif hist:
            msgs = [m for m in st.get("messages", []) if m[0] == "execution_error"]
            row["error"] = (msgs[0][1].get("exception_message") if msgs else "?")[:500]
        results.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        with open(os.path.join(a.out, "_bench.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    ok = sum(1 for r in results if r.get("status") == "success")
    print("done: %d/%d ok" % (ok, len(results)))


if __name__ == "__main__":
    main()
