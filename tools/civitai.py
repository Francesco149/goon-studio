#!/usr/bin/env python3
"""civitai.py - search, inspect and download Civitai models without a browser.

The public API answers search and metadata without any auth. Downloads and the .red (NSFW)
front end need a token: put one in ~/goonlab/.civitai-token (Account settings -> API Keys) or
export CIVITAI_TOKEN. A browser session cookie is not usable from here - Firefox encrypts its
cookie store with NSS, so a token is the supported path.

  python civitai.py search "krea 2 blowjob" [--limit 10] [--base "Krea 2"]
  python civitai.py model 1234567                 # versions, trained words, example images
  python civitai.py images 1234567 --out ex/      # download the example images (to judge a LoRA)
  python civitai.py download <versionId> --to loras/
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

API = "https://civitai.com/api/v1"
TOKEN_FILE = os.path.join(os.path.expanduser("~"), "goonlab", ".civitai-token")
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
    req = urllib.request.Request(url, headers={"User-Agent": "goonlab/1.0"})
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
    t = token()
    if not t:
        sys.exit("no token: put one in %s (Civitai > Account settings > API Keys)" % TOKEN_FILE)
    url = "https://civitai.com/api/download/models/%s" % a.version
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + t, "User-Agent": "goonlab/1.0"})
    with urllib.request.urlopen(req, timeout=600) as r:
        name = (r.headers.get("Content-Disposition") or "").split("filename=")[-1].strip('"; ')
        name = name or str(a.version) + ".safetensors"
        dest = os.path.join(a.to, os.path.basename(name))
        os.makedirs(a.to, exist_ok=True)
        with open(dest, "wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
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
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
