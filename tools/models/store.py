#!/usr/bin/env python3
"""store.py - the model store: what a template needs, fetch it, adopt a file the user downloaded.

  python tools/models/store.py where                       # the store folder; is the engine wired to it?
  python tools/models/store.py wire                        # point ComfyUI at the store (extra_model_paths.yaml)
  python tools/models/store.py check anime_pov             # what a template needs and what is missing
  python tools/models/store.py check --all                 # every template and page workflow
  python tools/models/store.py fetch anime_pov [more ...]  # download what is missing (resumable)
  python tools/models/store.py fetch --workflow wf_h3vid_i2v_fl.json
  python tools/models/store.py adopt "C:/Users/me/Downloads/x.safetensors" --folder loras [--sub h3nsfw]
        [--name y.safetensors] [--url DOWNLOAD] [--page PAGE] [--what "what it is"]
  python tools/models/store.py audit                       # every template's files have a source (exit 1 if not)
  python tools/models/store.py doc                         # rewrite docs/MODELS.md from the registry

The store is `models_dir` in my/settings.json; the registry is kit/models.json. Everything is local:
the only network traffic is the download from the file's own source.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "kit", "studio"))
import modelstore as M  # noqa: E402

# workflows the page's Video tab can switch to by mode, beyond what the recipes name
PAGE_WORKFLOWS = ["wf_h3vid_i2v.json", "wf_h3vid_i2v_lora.json", "wf_h3vid_i2v_fl.json",
                  "wf_h3vid_ref2va6.json", "wf_h3vid_t2v_lora.json"]


def targets(a, P):
    """[(label, workflow, fields)] from the command line."""
    out = []
    if getattr(a, "all", False):
        for sec in ("templates", "video_templates"):
            for tid in P.get(sec, {}):
                wf, f = M.template_job(tid, P)
                out.append((tid, wf, f))
        for wf in PAGE_WORKFLOWS:
            out.append(("page:" + wf, wf, {}))
    for tid in getattr(a, "template", []) or []:
        try:
            wf, f = M.template_job(tid, P)
        except KeyError:
            sys.exit("no template %r (see kit/presets.json templates / video_templates)" % tid)
        out.append((tid, wf, f))
    for wf in getattr(a, "workflow", []) or []:
        out.append((wf, wf, {}))
    if not out:
        sys.exit("name a template, --workflow or --all")
    return out


def cmd_where(a):
    s = M.settings()
    print("models_dir:", M.models_dir(s), "(from my/settings.json)" if s.get("models_dir") else "(default)")
    c = M.engine_comfy(s)
    if not c:
        print("engine: engine_dir is not set in my/settings.json")
        return
    y = os.path.join(c, "extra_model_paths.yaml")
    bases = [os.path.normpath(v.get("base_path", "")) for v in M.yaml_sections(y).values()]
    wired = os.path.normpath(M.models_dir(s)) in bases or os.path.normpath(M.models_dir(s)) == os.path.normpath(os.path.join(c, "models"))
    print("engine:", c)
    print("wired:", "yes" if wired else "no - run: python tools/models/store.py wire (then restart the engine)")


def cmd_wire(a):
    p = M.wire()
    if not p:
        sys.exit("engine_dir is not set in my/settings.json")
    print("wrote", p, "-> models from", M.models_dir())
    print("restart the engine so it sees it: powershell -ExecutionPolicy Bypass -File kit\\start.ps1 -RestartEngine")


def rows_for(a):
    P = M.presets()
    s = M.settings()
    out = []
    for label, wf, f in targets(a, P):
        out.append((label, wf, M.check(wf, f, s)))
    return out


def cmd_check(a):
    res = rows_for(a)
    if a.json:
        print(json.dumps([{"target": l, "workflow": wf, "files": r} for l, wf, r in res], indent=1))
        return
    bad = 0
    for label, wf, rows in res:
        miss = [r for r in rows if not r["present"]]
        bad += len(miss)
        print("%s  (%s)  %s" % (label, wf, "ready" if not miss else "%d missing" % len(miss)))
        for r in rows:
            if r["present"]:
                if a.verbose:
                    print("   ok   %s/%s%s" % (r["folder"], r["use"], "" if r["use"] == r["file"] else "  (for %s)" % r["file"]))
            else:
                print("   MISSING %s/%s  %s  -> %s" % (r["folder"], r["fetch"], "%.2f GB" % r["gb"] if r["gb"] else "",
                                                     r["url"] or "NO SOURCE RECORDED"))
    sys.exit(1 if bad and a.strict else 0)


def cmd_fetch(a):
    todo = {}
    for label, wf, rows in rows_for(a):
        for r in rows:
            if not r["present"]:
                todo[r["dest"]] = r
    if not todo:
        print("nothing to fetch: everything is already in the store")
        return
    total = sum(r["gb"] or 0 for r in todo.values())
    print("%d file(s), about %.1f GB, into %s" % (len(todo), total, M.models_dir()))
    for r in todo.values():
        print("  %s/%s  %.2f GB" % (r["folder"], r["fetch"], r["gb"] or 0))
    if a.dry_run:
        return
    fails = 0
    for dest, r in todo.items():
        if not r["url"]:
            print("SKIP %s: no download link in kit/models.json - ask the user where it came from" % r["fetch"])
            fails += 1
            continue
        print("get %s/%s" % (r["folder"], r["fetch"]), flush=True)
        try:
            M.download(r["url"], dest, r["gb"], log=lambda m: print(m, flush=True))
            print("ok  %s" % dest, flush=True)
        except Exception as e:
            print("FAIL %s: %s" % (r["fetch"], e), flush=True)
            fails += 1
    sys.exit(1 if fails else 0)


def cmd_adopt(a):
    if not os.path.isfile(a.path):
        sys.exit("no such file: %s" % a.path)
    key, dest = M.adopt(a.path, a.folder, a.sub, a.name, {"url": a.url, "page": a.page, "what": a.what})
    e = M.registry()[key]
    print("moved to", dest)
    print("registry entry:", key, json.dumps(e))
    if not e.get("url") and not e.get("page"):
        print("NOTE: no source recorded. Ask the user where they downloaded it and add url/page to kit/models.json"
              " (a template that uses it must carry a source).")


def cmd_audit(a):
    P = M.presets()
    reg = M.registry()
    bad = []
    a.all = True
    for label, wf, f in targets(a, P):
        for folder, name in M.needs(wf, f):
            fname, e = M.suggest(folder, name, reg)
            e = M.entry(folder, name, reg) or e
            if not e:
                bad.append("%s: %s/%s is not in kit/models.json" % (label, folder, name))
            elif not (e.get("url") or e.get("page")):
                bad.append("%s: %s/%s has no url/page" % (label, folder, name))
    for line in bad:
        print(line)
    print("audit: %s" % ("ok - every template and page workflow has a source for every file" if not bad else "%d problem(s)" % len(bad)))
    sys.exit(1 if bad else 0)


def cmd_doc(a):
    P = M.presets()
    reg = M.registry()
    lines = ["# Models: what each template needs and where to get it", "",
             "Generated by `python tools/models/store.py doc` from `kit/models.json` and the templates;",
             "do not edit by hand.", "",
             "**Where the files go.** Every file goes in your models folder (`models_dir` in",
             "`my/settings.json`; the agent sets it up) in the subfolder shown, under exactly the name",
             "shown - rename a download if the site gives it another name. After adding files, restart",
             "the engine (close and reopen Goon Studio) so it sees them. The page tells you on each",
             "template what is still missing.", "",
             "**Easiest:** ask the agent \"download the models for <template>\" - it fetches everything.",
             "", "Files marked *login* are on Civitai, which needs a free account to download. Sizes are",
             "the download size.", ""]

    def block(title, tids, sec):
        lines.extend(["## " + title, ""])
        for tid in tids:
            t = P[sec][tid]
            wf, f = M.template_job(tid, P)
            lines.append("### %s" % (t.get("label") or tid))
            lines.append("")
            lines.append("Template `%s`, workflow `%s`." % (tid, wf))
            lines.append("")
            lines.append("| file | put it in | size | get it from |")
            lines.append("|---|---|---|---|")
            tot = 0
            for folder, name in M.needs(wf, f):
                fname, e = M.suggest(folder, name, reg)
                if M.entry(folder, name, reg) and not (e and e.get("tier") == "8gb"):
                    fname, e = name, M.entry(folder, name, reg)
                e = e or {}
                tot += e.get("gb") or 0
                sub = os.path.dirname(fname)
                src = "[%s](%s)" % ("download" + (" (login)" if e.get("login") else ""), e["url"]) if e.get("url") else "?"
                if e.get("page"):
                    src += " - [page](%s)" % e["page"]
                lines.append("| `%s` | `%s` | %s | %s |" % (os.path.basename(fname), "/".join(p for p in (folder, sub) if p),
                                                         "%.2f GB" % e["gb"] if e.get("gb") else "?", src))
            lines.append("")
            lines.append("Total if you have none of them: about %.1f GB (most templates share files)." % tot)
            lines.append("")
    block("Picture templates", list(P.get("templates", {})), "templates")
    block("Video recipes", list(P.get("video_templates", {})), "video_templates")
    lines.extend(["## Every file", "", "| file | folder | what | size | source | notes |", "|---|---|---|---|---|---|"])
    for key, e in reg.items():
        folder, name = key.split("/", 1)
        lines.append("| `%s` | `%s` | %s | %.2f GB | [download](%s)%s | %s |" % (
            name, folder, e.get("what", ""), e.get("gb") or 0, e.get("url", ""),
            " - [page](%s)" % e["page"] if e.get("page") else "", (e.get("note") or "") + (" Needs a Civitai login." if e.get("login") else "")))
    lines.append("")
    path = os.path.join(ROOT, "docs", "MODELS.md")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print("wrote", path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("where").set_defaults(fn=cmd_where)
    sub.add_parser("wire").set_defaults(fn=cmd_wire)
    for name, fn in (("check", cmd_check), ("fetch", cmd_fetch)):
        p = sub.add_parser(name)
        p.add_argument("template", nargs="*")
        p.add_argument("--workflow", action="append")
        p.add_argument("--all", action="store_true")
        if name == "check":
            p.add_argument("--json", action="store_true")
            p.add_argument("-v", "--verbose", action="store_true")
            p.add_argument("--strict", action="store_true", help="exit 1 when something is missing")
        else:
            p.add_argument("--dry-run", action="store_true")
        p.set_defaults(fn=fn)
    p = sub.add_parser("adopt")
    p.add_argument("path")
    p.add_argument("--folder", required=True, choices=M.WIRED_FOLDERS)
    p.add_argument("--sub", default="")
    p.add_argument("--name")
    p.add_argument("--url")
    p.add_argument("--page")
    p.add_argument("--what")
    p.set_defaults(fn=cmd_adopt)
    sub.add_parser("audit").set_defaults(fn=cmd_audit)
    sub.add_parser("doc").set_defaults(fn=cmd_doc)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
