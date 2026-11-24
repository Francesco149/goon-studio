#!/usr/bin/env python3
"""civitai.py - search, inspect and download Civitai models without a browser.

The public API answers search and metadata without any auth. Downloads and the .red (NSFW)
front end need a token: put one in my/.civitai-token (git-ignored) (Account settings -> API Keys) or
export CIVITAI_TOKEN. A browser session cookie is not usable from here - Firefox encrypts its
cookie store with NSS, so a token is the supported path.

  python civitai.py search "krea 2 blowjob" [--limit 10] [--base "Krea 2"]
  python civitai.py model 1234567                 # versions, trained words, example images
  python civitai.py images 1234567 --out ex/      # download the example images (to judge a LoRA)
  python civitai.py download <versionId> --to loras/

A link the user pastes (civitai.com or the civitai.red mirror, /models/<id>[?modelVersionId=<v>] or
/api/download/models/<v>):
  python civitai.py link <url>                    # name, version, base model, trigger words, file, page
  python civitai.py get <url> [--folder loras] [--sub h3nsfw] [--name x.safetensors]
        # download into the model store (models_dir) and register it in kit/models.json with its source
  python civitai.py key --status                  # is a key set? (never prints it)
  python civitai.py key                           # the USER runs this in their own terminal: paste the key
        # at the hidden prompt, it is saved to my/.civitai-token. An agent never asks for the key in chat.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://civitai.com/api/v1"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_FILE = os.path.join(ROOT, "my", ".civitai-token")
try:  # model names carry emoji and CJK; the Windows console defaults to cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def token():
    t = os.environ.get("CIVITAI_TOKEN", "").strip()
    if not t and os.path.exists(TOKEN_FILE):
        t = open(TOKEN_FILE).read().strip()
    return t


def get(url, raw=False):
    req = urllib.request.Request(url, headers={"User-Agent": "goon-studio/1.0"})
    t = token()
    if t:
        req.add_header("Authorization", "Bearer " + t)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if raw else json.loads(data)


def strip_html(s):
    s = re.sub(r"<br\s*/?>", "\n", s or "")
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\n{3,}", "\n\n", s).replace("&amp;", "&").replace("&quot;", '"')


KEY_STEPS = """  1. Sign in at https://civitai.com (create a free account if needed).
  2. Open https://civitai.com/user/account -> "API Keys" -> "Add API key"; name it "studio"; copy it."""
KEY_HELP = ("No Civitai key saved. Downloading needs a free account and an API key (looking up works without).\n"
            + KEY_STEPS + "\n  3. Paste it into the key window: double-click kit\\civitai-key.cmd (the agent opens it for the\n"
            "     user with Start-Process). Never paste the key into the chat.")


def parse_link(link):
    """(model_id, version_id) from a Civitai URL (civitai.com / civitai.red / api/download) or an id."""
    link = str(link).strip()
    if link.isdigit():
        return int(link), None
    u = urllib.parse.urlparse(link if "://" in link else "https://" + link)
    if not re.search(r"(^|\.)civitai\.(com|red)$", u.netloc.lower()):
        sys.exit("not a Civitai link: %s" % link)
    d = re.search(r"/api/download/models/(\d+)", u.path)
    if d:
        return None, int(d.group(1))
    m = re.search(r"/models/(\d+)", u.path)
    if not m:
        sys.exit("no model id in %s" % link)
    v = (urllib.parse.parse_qs(u.query).get("modelVersionId") or [""])[0]
    return int(m.group(1)), int(v) if v.isdigit() else None


def resolve(link):
    """(model, version) for a link: the version the link names, else the newest."""
    mid, vid = parse_link(link)
    if mid is None:
        mid = get("%s/model-versions/%d" % (API, vid))["modelId"]
    m = get("%s/models/%d" % (API, mid))
    vs = m.get("modelVersions") or []
    v = next((x for x in vs if x["id"] == vid), None) if vid else (vs[0] if vs else None)
    if not v:
        sys.exit("version %s not found on model %s" % (vid, mid))
    return m, v


# Civitai's "baseModel" -> the registry's model families (kit/studio/loras.py FAMILIES)
BASES = [("illustrious", "sdxl"), ("pony", "sdxl"), ("noobai", "sdxl"), ("sdxl", "sdxl"), ("anima", "anima"),
         ("flux", "flux"), ("sd 1.5", "sd15"), ("wan", "wan"), ("qwen", "qwen"), ("krea", "krea2")]


def family(base):
    b = (base or "").lower()
    return next((fam for k, fam in BASES if k in b), None)


def blocks(words):
    """trainedWords -> trigger blocks (Civitai lists one block per entry, or one word per entry)."""
    words = [w.strip().strip(",").strip() for w in words or [] if w and w.strip()]
    if words and all("," not in w for w in words):
        return [", ".join(words)]
    return words


def main_file(v):
    fs = v.get("files") or []
    return next((f for f in fs if f.get("primary")), None) or next(
        (f for f in fs if f.get("name", "").endswith(".safetensors")), fs[0] if fs else {})


def cmd_link(a):
    m, v = resolve(a.url)
    f = main_file(v)
    print("%s  -  %s (model %d, version %d, %s)" % (m["name"], v["name"], m["id"], v["id"], m.get("type", "")))
    print("base model: %s" % v.get("baseModel"))
    print("trigger words: %s" % ("; ".join(v.get("trainedWords") or []) or "(none listed - check the description or the file header)"))
    print("file: %s (%d MB)" % (f.get("name"), (f.get("sizeKB") or 0) // 1024))
    print("page: https://civitai.com/models/%d?modelVersionId=%d" % (m["id"], v["id"]))
    print("download: %s" % (v.get("downloadUrl") or ""))
    print("description: " + strip_html(m.get("description", ""))[:a.desc].replace("\n", " "))
    print("Civitai key: %s" % ("set" if token() else "NOT set - downloading needs one (offer the key window: kit\\civitai-key.cmd)"))


def cmd_get(a):
    sys.path.insert(0, os.path.join(ROOT, "kit", "studio"))
    import modelstore as M
    m, v = resolve(a.url)
    if not token():
        print(KEY_HELP)
        sys.exit(3)
    f = main_file(v)
    name = a.name or f.get("name") or "%d.safetensors" % v["id"]
    folder = a.folder or {"Checkpoint": "checkpoints", "VAE": "vae"}.get(m.get("type"), "loras")
    sub = a.sub.strip("/\\")
    dest = M.dest_path(folder, M.norm("/".join(p for p in (sub, name) if p)))
    url = v.get("downloadUrl") or "https://civitai.com/api/download/models/%d" % v["id"]
    page = "https://civitai.com/models/%d?modelVersionId=%d" % (m["id"], v["id"])
    words = "; ".join(v.get("trainedWords") or [])
    what = "%s - %s (%s)%s" % (m["name"], v["name"], v.get("baseModel"), ("; trigger: " + words) if words else "")
    if os.path.exists(dest):
        print("already in the store:", dest)
    else:
        M.download(url, dest, log=print)
    meta = {"url": url, "page": page, "what": what, "login": True, "base": family(v.get("baseModel")),
            "trigger": blocks(v.get("trainedWords")), "sha256": ((f.get("hashes") or {}).get("SHA256") or "").upper()}
    known = M.registry().get("%s/%s" % (folder, M.norm("/".join(p for p in (sub, name) if p))), {})
    meta = {k: v for k, v in meta.items() if not known.get(k)}   # never overwrite a curated entry
    key, dest = M.adopt(dest, folder, sub, name, meta)
    print("stored:", dest)
    print("registry:", key)
    print("base model: %s   trigger words: %s" % (v.get("baseModel"), words or "(none listed)"))
    print("if the engine does not list it yet: kit\\start.ps1 -RestartEngine")


def cmd_key(a):
    if a.status:
        src = "CIVITAI_TOKEN" if os.environ.get("CIVITAI_TOKEN", "").strip() else TOKEN_FILE
        print("Civitai key: %s" % (("set (%s)" % src) if token() else "not set"))
        sys.exit(0 if token() else 1)
    import getpass
    print("Civitai key for Goon Studio\n" + KEY_STEPS + "\n  3. Paste it here and press Enter (it stays hidden).\n")
    for _try in range(3):
        t = getpass.getpass("Civitai API key: ").strip()
        if not t:
            sys.exit("nothing saved")
        try:  # an authenticated call: a wrong key answers 401
            req = urllib.request.Request(API + "/models?limit=1&favorites=true",
                                         headers={"User-Agent": "goon-studio/1.0", "Authorization": "Bearer " + t})
            urllib.request.urlopen(req, timeout=30).read()
            note = "Civitai accepted it"
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                print("Civitai says this key is not valid (HTTP %d). Copy the whole key again and paste it." % e.code)
                continue
            note = "could not check it right now (HTTP %d)" % e.code
        except Exception as e:
            note = "could not check it right now (%s)" % e
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, "w") as fh:
            fh.write(t + "\n")
        print("Saved on this PC (%s). You can close this window." % note)
        return
    sys.exit("Not saved: Civitai did not accept the key. Make a new one on the Civitai page and try again.")


def cmd_search(a):
    q = urllib.parse.urlencode({"query": a.query, "limit": a.limit, "nsfw": "true", "sort": "Most Downloaded"})
    for m in get(API + "/models?" + q)["items"]:
        bases = ",".join(m["baseModels"])
        if a.base and a.base.lower() not in bases.lower():
            continue
        print("%-8d %-52s %-30s dl=%-8d up=%d" % (m["id"], m["name"][:52], bases[:30],
                                                  m["stats"]["downloadCount"], m["stats"]["thumbsUpCount"]))


def cmd_model(a):
    m = get("%s/models/%d" % (API, a.id))
    print("%s  (%s)" % (m["name"], ",".join(m["baseModels"])))
    print(strip_html(m.get("description", ""))[:a.desc])
    for v in m["modelVersions"]:
        print("\n  version %d  %s  base=%s  file=%s" % (v["id"], v["name"], v["baseModel"],
              ", ".join("%s (%d MB)" % (f["name"], f["sizeKB"] // 1024) for f in v["files"])))
        if v.get("trainedWords"):
            print("    words: " + "; ".join(v["trainedWords"])[:300])
        print("    url:   " + (v.get("downloadUrl") or ""))
        for im in (v.get("images") or [])[:4]:
            print("    image: " + im["url"])


def cmd_images(a):
    m = get("%s/models/%d" % (API, a.id))
    os.makedirs(a.out, exist_ok=True)
    n = 0
    for v in m["modelVersions"][:1]:
        for im in (v.get("images") or [])[:a.n]:
            ext = os.path.splitext(urllib.parse.urlparse(im["url"]).path)[1] or ".jpg"
            dest = os.path.join(a.out, "%s_%d%s" % (a.id, n, ext))
            with open(dest, "wb") as f:
                f.write(get(im["url"], raw=True))
            n += 1
            print(dest)
    print("%d image(s)" % n)


def cmd_download(a):
    if not token():
        print(KEY_HELP)
        sys.exit(3)
    sys.path.insert(0, os.path.join(ROOT, "kit", "studio"))
    import modelstore as M  # resumable; drops the token on Civitai's redirect to its file host (R2 rejects it)
    v = get("%s/model-versions/%s" % (API, a.version))
    dest = os.path.join(a.to, os.path.basename(main_file(v).get("name") or str(a.version) + ".safetensors"))
    M.download("https://civitai.com/api/download/models/%s" % a.version, dest, log=print)
    print(dest, os.path.getsize(dest) // (1 << 20), "MB")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--limit", type=int, default=10); s.add_argument("--base")
    s.set_defaults(f=cmd_search)
    s2 = sub.add_parser("model"); s2.add_argument("id", type=int); s2.add_argument("--desc", type=int, default=1200)
    s2.set_defaults(f=cmd_model)
    s3 = sub.add_parser("images"); s3.add_argument("id", type=int); s3.add_argument("--out", default="ex"); s3.add_argument("-n", type=int, default=4)
    s3.set_defaults(f=cmd_images)
    s4 = sub.add_parser("download"); s4.add_argument("version", type=int); s4.add_argument("--to", default=".")
    s4.set_defaults(f=cmd_download)
    s5 = sub.add_parser("link"); s5.add_argument("url"); s5.add_argument("--desc", type=int, default=400)
    s5.set_defaults(f=cmd_link)
    s6 = sub.add_parser("get"); s6.add_argument("url"); s6.add_argument("--folder"); s6.add_argument("--sub", default="")
    s6.add_argument("--name"); s6.set_defaults(f=cmd_get)
    s7 = sub.add_parser("key", description=KEY_HELP, formatter_class=argparse.RawDescriptionHelpFormatter)
    s7.add_argument("--status", action="store_true"); s7.set_defaults(f=cmd_key)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
