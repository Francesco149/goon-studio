#!/usr/bin/env python3
"""engines.py - which ComfyUI engines run on this PC, whose they are, and stop another app's.

  python tools/engines.py              # list; exit 5 when another app's engine is running
  python tools/engines.py --stop PID   # stop one engine (a ComfyUI main.py process only)

Goon Studio's engine runs on 127.0.0.1:8187 (comfy_url in my/settings.json); Love Live Studio's on
8188; 8189 is this repo's bench engine (tools/experiments/bench_engine.ps1). One 8 GB GPU and 16 GB
RAM hold one engine at a time, and an engine writes pictures to the output folder of the app that
started it, so another app's engine is a conflict. Agents: when this reports one, ask the user once
whether to stop it (it ends that app's running jobs), and only stop it on a yes.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import localboxes  # noqa: E402

BENCH_PORT = "8189"


def _ps(cmd):
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                       capture_output=True, text=True, timeout=60)
    return r.stdout.strip()


def _arg(cl, flag):
    m = re.search(r'%s\s+("([^"]+)"|(\S+))' % re.escape(flag), cl or "")
    return (m.group(2) or m.group(3)) if m else None


def _answers(port):
    try:
        urllib.request.urlopen("http://127.0.0.1:%s/system_stats" % port, timeout=3).read()
        return True
    except Exception:
        return False


def engines():
    """[{pid, port, outputs, owner, answers}] for every ComfyUI main.py on this PC."""
    if os.name != "nt":
        return []
    out = _ps("Get-CimInstance Win32_Process -Filter \"Name = 'python.exe'\" | "
              "Where-Object { $_.CommandLine -like '*main.py*' } | "
              "Select-Object ProcessId, CommandLine | ConvertTo-Json -Compress")
    if not out:
        return []
    rows = json.loads(out)
    rows = rows if isinstance(rows, list) else [rows]
    s = localboxes.settings()
    mine_port = re.search(r":(\d+)$", localboxes.local_url(s)).group(1)
    outs = os.path.normcase(os.path.normpath(os.path.join(s.get("data_dir") or os.path.join(localboxes.REPO, "gallery"), "outputs")))
    res = []
    for r in rows:
        cl = r.get("CommandLine") or ""
        port = _arg(cl, "--port") or "8188"
        outdir = _arg(cl, "--output-directory") or ""
        ours_dir = bool(outdir) and os.path.normcase(os.path.normpath(outdir)) == outs
        if port == BENCH_PORT:
            owner = "goon-studio bench"
        elif ours_dir and port != mine_port:
            owner = "goon-studio (old port; restart it)"
        elif ours_dir or (port == mine_port and not outdir):
            owner = "goon-studio"
        elif port == mine_port:
            owner = "other app on goon-studio's port"
        else:
            owner = "other app"
        res.append({"pid": r["ProcessId"], "port": port, "outputs": outdir, "owner": owner,
                    "answers": _answers(port)})
    return res


def others(rows=None):
    return [e for e in (engines() if rows is None else rows) if e["owner"].startswith("other")]


def warn_line(e):
    return ("another app's ComfyUI engine is running (port %s, outputs %s, pid %s): it shares the GPU and "
            "RAM with this one. Ask the user whether to stop it: python tools/engines.py --stop %s"
            % (e["port"], e["outputs"] or "?", e["pid"], e["pid"]))


def stop(pid):
    rows = engines()
    e = next((x for x in rows if str(x["pid"]) == str(pid)), None)
    if not e:
        sys.exit("pid %s is not a ComfyUI engine on this PC" % pid)
    _ps("Stop-Process -Id %d -Force" % int(pid))
    print("stopped the engine on port %s (pid %s, outputs %s)" % (e["port"], pid, e["outputs"] or "?"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stop", metavar="PID")
    a = ap.parse_args()
    if a.stop:
        return stop(a.stop)
    rows = engines()
    if not rows:
        print("no ComfyUI engine is running on this PC")
    for e in rows:
        print("port %-5s pid %-7s %-32s %s%s" % (e["port"], e["pid"], e["owner"], e["outputs"] or "(default outputs)",
                                                "" if e["answers"] else "  [not answering]"))
    o = others(rows)
    for e in o:
        print(warn_line(e))
    sys.exit(5 if o else 0)


if __name__ == "__main__":
    main()
