"""server.py: the NSFW Studio page (http://127.0.0.1:8191). Standard library only.

Endpoints:
  GET  /api/state       templates, workflows, ComfyUI up?
  POST /api/generate    {job..., count} -> queue images (seed, seed+1, ...)
  GET  /api/jobs        jobs from this page
  GET  /api/history     every picture with rating/public/trashed
  POST /api/rate        {file, rating, note}
  POST /api/visibility  {files, public}
  POST /api/trash       {files};  /api/restore {files};  /api/delete {files}
  POST /api/upload      {data: "data:image/...;base64,..."} -> gallery/uploads/<file>
  GET  /img/<path>      a picture in the gallery
"""
import base64, json, mimetypes, os, queue, threading, time, traceback, urllib.parse
import sys
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("NSFW_STUDIO_PORT", "8191"))
JOBS = []
LOCK = threading.Lock()
Q = queue.Queue()
IMG_MAGIC = {b"\x89PNG": ".png", b"\xff\xd8\xff": ".jpg", b"RIFF": ".webp"}


def worker():
    while True:
        e = Q.get()
        if e["status"] == "cancelled":
            continue
        e["status"] = "running"
        try:
            e["record"] = core.run(e["job"], by="me", on_queued=lambda pid: e.__setitem__("prompt_id", pid))
            e["status"] = "done"
        except Exception as ex:
            e["status"] = "error"
            e["error"] = str(ex)[:500]
            with open(os.path.join(core.MY, "studio-errors.log"), "a", encoding="utf-8") as f:
                f.write("%s %s\n%s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), e["job"].get("template"), traceback.format_exc()))
        e["finished_at"] = time.time()


def safe_join(base, rel):
    p = os.path.normpath(os.path.join(base, rel.replace("/", os.sep)))
    if not p.startswith(os.path.normpath(base)):
        raise PermissionError(rel)
    return p


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype="application/json"):
        if not isinstance(body, (bytes, bytearray)):
            body = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def file(self, path):
        if not os.path.isfile(path):
            return self.send(404, {"error": "not found"})
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            self.send(200, f.read(), ctype)

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n).decode() or "{}") if n else {}

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        p = urllib.parse.unquote(u.path)
        try:
            if p in ("/", "/index.html"):
                return self.file(os.path.join(HERE, "index.html"))
            if p == "/api/state":
                P = core.presets()
                return self.send(200, {"templates": P.get("templates", {}), "characters": P.get("characters", {}),
                                       "scenes": P.get("scenes", {}), "workflows": core.workflow_names(),
                                       "comfy_up": core.comfy_up(), "machine": {k: core.settings().get(k) for k in ("gpu", "data_dir")}})
            if p == "/api/jobs":
                with LOCK:
                    return self.send(200, JOBS[-60:])
            if p == "/api/history":
                return self.send(200, core.all_records())
            if p == "/api/rounds":
                out = []
                d = os.path.join(core.MY, "rounds")
                for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
                    if fn.endswith(".json"):
                        r = core.load_json(os.path.join(d, fn), {})
                        r["id"] = fn[:-5]
                        out.append(r)
                return self.send(200, list(reversed(out)))
            if p.startswith("/img/"):
                return self.file(safe_join(core.settings().get("data_dir", core.GALLERY), p[5:]))
            return self.send(404, {"error": "not found"})
        except PermissionError:
            return self.send(403, {"error": "forbidden"})
        except Exception as e:
            return self.send(500, {"error": str(e)})

    def do_POST(self):
        p = urllib.parse.urlparse(self.path).path
        try:
            b = self.body()
            if p == "/api/generate":
                if not core.comfy_up():
                    return self.send(503, {"error": "ComfyUI is not running."})
                n = max(1, min(int(b.pop("count", 1) or 1), 12))
                seed = b.get("seed")
                base = int(seed) if seed not in (None, "", -1, "-1") else core.random.randint(1, 2**31 - 1 - n)
                made = []
                for i in range(n):
                    job = dict(b, seed=base + i)
                    e = {"id": "%d-%d" % (int(time.time() * 1000), i), "job": job, "status": "queued", "queued_at": time.time()}
                    with LOCK:
                        JOBS.append(e)
                    Q.put(e)
                    made.append(e["id"])
                return self.send(200, {"queued": made})
            if p == "/api/upload":
                raw = base64.b64decode(str(b.get("data", "")).split(",", 1)[-1])
                ext = next((e for m, e in IMG_MAGIC.items() if raw.startswith(m)), None)
                if not ext or len(raw) > 40 * 2**20:
                    return self.send(400, {"error": "not a PNG/JPEG/WebP under 40 MB"})
                rel = "uploads/%s_%d%s" % (time.strftime("%Y%m%d-%H%M%S"), int(time.time() * 1000) % 1000, ext)
                dst = safe_join(core.settings().get("data_dir", core.GALLERY), rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(dst, "wb") as f:
                    f.write(raw)
                return self.send(200, {"file": rel, "path": dst})
            if p == "/api/visibility":
                return self.send(200, {"changed": core.set_public(b.get("files") or [], bool(b.get("public")))})
            if p in ("/api/trash", "/api/restore"):
                return self.send(200, {"changed": core.trash(b.get("files") or [], restore=p == "/api/restore")})
            if p == "/api/delete":
                return self.send(200, {"deleted": core.delete_forever(b.get("files") or [])})
            if p == "/api/rate":
                core.append_jsonl(core.PFEED, {"time": time.time(), "file": b["file"], "rating": b.get("rating"), "note": b.get("note")})
                return self.send(200, {"ok": True})
            return self.send(404, {"error": "not found"})
        except Exception as e:
            return self.send(500, {"error": str(e)})


def main():
    threading.Thread(target=worker, daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    print("NSFW Studio on http://127.0.0.1:%d" % PORT, flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
