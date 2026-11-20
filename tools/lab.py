#!/usr/bin/env python3
"""lab.py - submit a batch of ComfyUI jobs, poll, pull, then clean the box.

Why not tools/comfy.py: it runs one prompt at a time and its stdout is easy to lose in a
background shell. This queues the whole batch at once, logs every transition with a timestamp
to <out>/_run.log, and pulls each render as soon as its history entry says success.

  python lab.py --wf wf_anima.json --jobs jobs.jsonl --box local --sub gl/g01 -o gens/g01
  python lab.py ... --only a,b --skip c        # pick jobs by name
  python lab.py ... --keep                     # leave the renders on the box
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
BOXES = {
    "local": ("http://127.0.0.1:8188", r"F:\LLStudioTest"),
    "ampere": ("http://10.0.10.240:8188", "/data/comfyui"),
    "lame": ("http://10.0.10.56:8188", "/lamedata/comfyui"),
}
PH = re.compile(r"\{\{(\w+)\}\}")
IMG_KEYS = ("image", "image1", "image2", "last", "video")
T0 = time.time()


def log(msg, fh=None):
    line = "[%6.1fs] %s" % (time.time() - T0, msg)
    print(line, flush=True)
    if fh:
        fh.write(line + "\n")
        fh.flush()


def http(base, path, data=None, timeout=120, raw=False):
    req = urllib.request.Request(base + path, data=data,
                                 method="POST" if data else "GET",
                                 headers={"Content-Type": "application/json"} if data else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read()
    return body if raw else json.loads(body or b"null")


def upload(base, path, sub="gl_up"):
    """Send a picture to ComfyUI's input dir with curl (aiohttp rejects urllib's multipart)."""
    import subprocess
    r = subprocess.run(["curl", "-s", "-F", "image=@" + path, "-F", "overwrite=true",
                        "-F", "subfolder=" + sub, base + "/upload/image"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("upload failed: " + r.stderr[:300])
    j = json.loads(r.stdout)
    return (j.get("subfolder") + "/" if j.get("subfolder") else "") + j["name"]


def coerce(v):
    try:
        return json.loads(v)
    except (ValueError, TypeError):
        return v


def subst(obj, params, where):
    if isinstance(obj, dict):
        return {k: subst(v, params, where) for k, v in obj.items()}
    if isinstance(obj, list):
        return [subst(v, params, where) for v in obj]
    if isinstance(obj, str):
        if PH.fullmatch(obj):
            k = PH.fullmatch(obj).group(1)
            if k not in params:
                sys.exit("%s: needs -p %s" % (where, k))
            return params[k]

        def rep(m):
            k = m.group(1)
            if k not in params:
                sys.exit("%s: needs -p %s" % (where, k))
            return str(params[k])
        return PH.sub(rep, obj)
    return obj


def outputs_of(hist):
    for _node, out in (hist.get("outputs") or {}).items():
        for key in ("images", "gifs", "videos", "audio", "files"):
            for item in out.get(key, []) or []:
                if isinstance(item, dict) and "filename" in item and item.get("type", "output") != "temp":
                    yield item


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wf", required=True)
    ap.add_argument("--jobs", required=True)
    ap.add_argument("--box", default="local", choices=sorted(BOXES))
    ap.add_argument("--sub", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default=None, help="comma list of job names to run")
    ap.add_argument("--skip", default=None)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--timeout", type=int, default=3600)
    a = ap.parse_args()

    base, root = BOXES[a.box]
    os.makedirs(a.out, exist_ok=True)
    # one batch at a time per box: two batches sharing a subfolder clean each other's renders away
    lock = os.path.join(HERE, ".lock." + a.box)
    if os.path.exists(lock):
        age = time.time() - os.path.getmtime(lock)
        if age < 3 * 3600:
            sys.exit("%s is busy: %s started %.0f min ago. Wait for it or delete the lock." %
                     (a.box, open(lock).read().strip(), age / 60))
    with open(lock, "w") as f:
        f.write("%s pid %d" % (a.sub, os.getpid()))
    upload_sub = "gl_up/" + a.sub.replace("/", "_")
    fh = open(os.path.join(a.out, "_run.log"), "a", encoding="utf-8")
    jobs = [json.loads(l) for l in open(a.jobs, encoding="utf-8-sig") if l.strip() and not l.lstrip().startswith("#")]
    only = set(a.only.split(",")) if a.only else None
    skip = set(a.skip.split(",")) if a.skip else set()
    jobs = [j for j in jobs if (only is None or j["name"] in only) and j["name"] not in skip]
    wfs = {}

    def load_wf(name):
        if name not in wfs:
            w = json.load(open(os.path.join(HERE, name), encoding="utf-8-sig"))
            d = w.pop("_params", {})
            for k in [k for k in w if k.startswith("_")]:
                w.pop(k)
            wfs[name] = (w, d)
        return wfs[name]

    queued = []
    try:
        http(base, "/system_stats", timeout=10)
    except Exception as e:
        sys.exit("%s: ComfyUI not answering (%s)" % (base, e))

    for job in jobs:
        job = dict(job)
        name = job.pop("name")
        wf, defaults = load_wf(job.pop("wf", a.wf))
        params = dict(defaults)
        params["prefix"] = "%s/%s" % (a.sub, name)
        for k in IMG_KEYS:
            if job.get(k):
                params[k] = upload(base, job.pop(k), upload_sub)
        for k, v in job.items():
            params[k] = v
        prompt = subst(wf, params, name)
        cid = "lab-" + name
        try:
            r = http(base, "/prompt", data=json.dumps({"prompt": prompt, "client_id": cid}).encode())
        except urllib.error.HTTPError as e:
            log("%-22s REJECTED %s" % (name, e.read().decode()[:300]), fh)
            continue
        queued.append((name, r["prompt_id"], job))
        log("%-22s queued %s" % (name, r["prompt_id"][:8]), fh)
        time.sleep(0.5)

    done = {}
    while len(done) < len(queued):
        time.sleep(3)
        for name, pid, job in queued:
            if name in done:
                continue
            try:
                h = http(base, "/history/" + pid, timeout=30)
            except Exception:
                continue
            if pid not in h:
                continue
            st = h[pid].get("status", {})
            if st.get("status_str") == "error":
                msg = [m for m in st.get("messages", []) if m[0] == "execution_error"]
                log("%-22s ERROR %s" % (name, (msg[0][1].get("exception_message") if msg else "?")[:300]), fh)
                done[name] = None
                continue
            if not st.get("completed"):
                continue
            saved = []
            for item in outputs_of(h[pid]):
                q = urllib.parse.urlencode({"filename": item["filename"], "subfolder": item.get("subfolder", ""),
                                            "type": item.get("type", "output")})
                data = http(base, "/view?" + q, raw=True, timeout=600)
                dest = os.path.join(a.out, item["filename"])
                with open(dest, "wb") as f:
                    f.write(data)
                saved.append(dest)
            done[name] = saved
            log("%-22s done  %s" % (name, ", ".join(os.path.basename(s) for s in saved) or "no output"), fh)
            # ComfyUI sometimes leaves a finished prompt sitting in queue_running, which blocks the
            # next prompt forever. Its history entry is already written, so clearing it is safe.
            try:
                q = http(base, "/queue", timeout=15)
                if any(pid in json.dumps(item) for item in q.get("queue_running", [])):
                    http(base, "/interrupt", data=b"{}")
                    log("%-22s queue was stuck on a finished prompt: interrupted" % name, fh)
            except Exception:
                pass
        if time.time() - T0 > a.timeout:
            log("TIMEOUT with %d/%d" % (len(done), len(queued)), fh)
            break

    if not a.keep:
        import subprocess
        ids = ",".join(pid for _n, pid, _j in queued)
        r = subprocess.run([sys.executable, os.path.join(HERE, "clean.py"), "--box", a.box, "--sub", a.sub,
                            "--input-sub", upload_sub, "--ids", ids], capture_output=True, text=True)
        for line in (r.stdout or "").strip().splitlines():
            log("clean: " + line, fh)
    log("batch complete: %d/%d ok" % (sum(1 for v in done.values() if v), len(queued)), fh)
    try:
        os.remove(lock)
    except OSError:
        pass


if __name__ == "__main__":
    main()

