#!/usr/bin/env python3
"""comfy.py — drive a ComfyUI engine (stdlib only).

Defaults to this machine's engine (127.0.0.1:8188, the one kit/start.ps1 runs). COMFY_URL or
--box picks another engine from the git-ignored tools/boxes.local.json (none on a normal install).

  comfy.py run workflows/h3_t2v.json -p prompt="..." -p seed=7 -o out/ --log results.jsonl
  tools/comfy.py upload persona/mia/ref.png          # into ComfyUI's input/ (images, audio, video)
  tools/comfy.py info UnetLoaderGGUF                 # a node's inputs, from /object_info
  tools/comfy.py free                                # unload models, free VRAM
  tools/comfy.py fetch <prompt_id> -o out/              # outputs of a run whose client died
  tools/comfy.py queue | stats

Workflows are ComfyUI *API format* JSON (node id -> {class_type, inputs}).
Any string value "{{name}}" (whole value) or "...{{name}}..." (inside a
string) is replaced by -p name=value; a whole-value placeholder takes the
JSON type of the value (so -p seed=7 stays an int, -p prompt=... a string).
Defaults can live in the workflow under a top-level "_params" object; other top-level
"_" keys (e.g. "_note") are documentation and never sent.

Never wakes a box or switches what it serves: if ComfyUI is not answering, it says so.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

import localboxes  # noqa: E402
BOXES = {"local": "http://127.0.0.1:8188"}
BOXES.update({k: v["url"] for k, v in localboxes.load().items()})
BASE = os.environ.get("COMFY_URL", BOXES["local"])
PH = re.compile(r"\{\{(\w+)\}\}")


def http(path, data=None, method=None, timeout=60, raw=False, headers=None):
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read()
    return body if raw else json.loads(body or b"null")


def alive():
    try:
        http("/system_stats", timeout=4)
        return True
    except Exception:
        return False


def need_alive():
    # a busy server (model load, tokenizer rebuild) can miss one 4 s check; retry for ~30 s
    for _ in range(6):
        if alive():
            return
        time.sleep(5)
    sys.exit(f"comfy: {BASE} is not answering (local: start it with kit/start.ps1)")


def coerce(v):
    try:
        return json.loads(v)
    except ValueError:
        return v


def substitute(obj, params):
    if isinstance(obj, dict):
        return {k: substitute(v, params) for k, v in obj.items()}
    if isinstance(obj, list):
        return [substitute(v, params) for v in obj]
    if isinstance(obj, str):
        m = PH.fullmatch(obj)
        if m:
            k = m.group(1)
            if k not in params:
                sys.exit(f"comfy: workflow needs -p {k}=...")
            return params[k]
        def rep(m):
            k = m.group(1)
            if k not in params:
                sys.exit(f"comfy: workflow needs -p {k}=...")
            return str(params[k])
        return PH.sub(rep, obj)
    return obj


def upload(path, subfolder=""):
    name = os.path.basename(path)
    boundary = uuid.uuid4().hex
    with open(path, "rb") as f:
        content = f.read()
    parts = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
        f"Content-Type: application/octet-stream\r\n\r\n".encode() + content + b"\r\n",
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n".encode(),
    ]
    if subfolder:
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"subfolder\"\r\n\r\n{subfolder}\r\n".encode())
    body = b"".join(parts) + f"--{boundary}--\r\n".encode()
    r = http("/upload/image", data=body, method="POST",
             headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, timeout=600)
    return (r.get("subfolder") + "/" if r.get("subfolder") else "") + r["name"]


def outputs_of(hist):
    for node_id, out in (hist.get("outputs") or {}).items():
        for key in ("images", "gifs", "videos", "audio", "files", "3d"):  # "3d": SaveGLB (meshes, splats)
            for item in out.get(key, []) or []:
                if isinstance(item, dict) and "filename" in item:
                    yield node_id, item


def download(hist, out, prefix="", temp=False):
    os.makedirs(out, exist_ok=True)
    saved = []
    for node_id, item in outputs_of(hist):
        if item.get("type") == "temp" and not temp:
            continue
        q = urllib.parse.urlencode({"filename": item["filename"], "subfolder": item.get("subfolder", ""),
                                    "type": item.get("type", "output")})
        data = http(f"/view?{q}", raw=True, timeout=600)
        name = (prefix + "_" if prefix else "") + item["filename"]
        dest = os.path.join(out, name)
        with open(dest, "wb") as f:
            f.write(data)
        saved.append(dest)
    return saved


def exec_seconds(hist):
    # server-side execution time (start -> success), excludes queue wait
    msgs = {m[0]: m[1] for m in hist.get("status", {}).get("messages", [])}
    try:
        return round((msgs["execution_success"]["timestamp"] - msgs["execution_start"]["timestamp"]) / 1000, 1)
    except (KeyError, TypeError):
        return None


def run(args):
    need_alive()
    with open(args.workflow) as f:
        wf = json.load(f)
    params = dict(wf.pop("_params", {}))
    for k in [k for k in wf if k.startswith("_")]:  # _note etc.: documentation, not nodes
        wf.pop(k)
    for kv in args.param or []:
        k, _, v = kv.partition("=")
        params[k] = coerce(v)
    for kv in args.upload or []:
        k, _, path = kv.partition("=")
        params[k] = upload(path)
        print(f"uploaded {path} -> {params[k]}")
    prompt = substitute(wf, params)
    client_id = os.environ.get("COMFY_CLIENT_ID", "localgen")  # progress.py listens as this id
    t0 = time.time()
    try:
        r = http("/prompt", data=json.dumps({"prompt": prompt, "client_id": client_id}).encode(),
                 method="POST", headers={"Content-Type": "application/json"})
    except urllib.error.HTTPError as e:
        sys.exit(f"comfy: rejected: {e.read().decode()[:2000]}")
    pid = r["prompt_id"]
    print(f"queued {pid}")
    hist = None
    while True:
        time.sleep(2)
        try:
            h = http(f"/history/{pid}")
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            continue  # the server stalls during some model loads (GGUF tokenizer rebuild); keep waiting
        if pid in h:
            hist = h[pid]
            st = hist.get("status", {})
            if st.get("completed") or st.get("status_str") in ("success", "error"):
                break
        if args.timeout and time.time() - t0 > args.timeout:
            sys.exit(f"comfy: timed out after {args.timeout}s (still queued/running on {BASE})")
    took = time.time() - t0
    st = hist.get("status", {})
    if st.get("status_str") == "error":
        for m in st.get("messages", []):
            if m[0] == "execution_error":
                d = m[1]
                sys.exit(f"comfy: error in node {d.get('node_id')} ({d.get('node_type')}): {d.get('exception_message')}")
        sys.exit("comfy: execution error (see the engine log, gallery/logs/comfyui.err.log for local)")
    saved = download(hist, args.out, args.prefix, args.temp)
    print(f"done in {took:.1f}s")
    for s in saved:
        print(f"  {s}")
    if args.log:
        with open(args.log, "a") as f:
            f.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "workflow": args.workflow,
                                "box": BASE, "params": params, "seconds": round(took, 1), "outputs": saved,
                                "exec_seconds": exec_seconds(hist)}) + "\n")


def main():
    global BASE
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--box", choices=sorted(BOXES), help="default: COMFY_URL, else local (127.0.0.1:8188)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("workflow")
    r.add_argument("-p", "--param", action="append", help="name=value (JSON-typed when it parses)")
    r.add_argument("-u", "--upload", action="append", help="name=path: upload a file, pass its input name")
    r.add_argument("-o", "--out", default="out")
    r.add_argument("--prefix", default="")
    r.add_argument("--timeout", type=int, default=0)
    r.add_argument("--temp", action="store_true", help="also save temp/preview outputs")
    r.add_argument("--log", help="append a JSONL record (params, seconds, outputs)")
    u = sub.add_parser("upload")
    u.add_argument("path")
    u.add_argument("--subfolder", default="")
    i = sub.add_parser("info")
    i.add_argument("node")
    fe = sub.add_parser("fetch", help="download the outputs of a finished prompt (e.g. after the client died)")
    fe.add_argument("prompt_id")
    fe.add_argument("-o", "--out", default="out")
    fe.add_argument("--prefix", default="")
    sub.add_parser("free")
    sub.add_parser("queue")
    sub.add_parser("stats")
    a = ap.parse_args()
    if a.box:
        BASE = BOXES[a.box]
    if a.cmd == "run":
        run(a)
    elif a.cmd == "upload":
        need_alive(); print(upload(a.path, a.subfolder))
    elif a.cmd == "info":
        need_alive()
        d = http(f"/object_info/{a.node}").get(a.node)
        if not d:
            sys.exit(f"comfy: no node {a.node}")
        for sect in ("required", "optional"):
            for k, v in (d["input"].get(sect) or {}).items():
                t = v[0] if isinstance(v[0], str) else f"one of {v[0][:12]}{'…' if len(v[0]) > 12 else ''}"
                extra = v[1] if len(v) > 1 else ""
                print(f"{sect:8} {k:28} {t} {json.dumps(extra)[:120] if extra else ''}")
        print("outputs:", d.get("output"))
    elif a.cmd == "fetch":
        need_alive()
        h = http(f"/history/{a.prompt_id}").get(a.prompt_id)
        if not h:
            sys.exit(f"comfy: no history for {a.prompt_id}")
        print(h.get("status", {}).get("status_str"))
        for s in download(h, a.out, a.prefix):
            print(f"  {s}")
    elif a.cmd == "free":
        need_alive()
        http("/free", data=json.dumps({"unload_models": True, "free_memory": True}).encode(), method="POST",
             headers={"Content-Type": "application/json"}, raw=True)
        print("freed")
    elif a.cmd == "queue":
        need_alive(); q = http("/queue")
        print(f"running {len(q['queue_running'])}, pending {len(q['queue_pending'])}")
    elif a.cmd == "stats":
        need_alive(); s = http("/system_stats")
        for d in s.get("devices", []):
            print(f"{d['name']}: vram {d['vram_free']/2**30:.1f}/{d['vram_total']/2**30:.1f} GiB free")
        print("comfyui", s.get("system", {}).get("comfyui_version"), "torch", s.get("system", {}).get("pytorch_version"))


if __name__ == "__main__":
    main()
