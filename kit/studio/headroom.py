"""headroom.py: is there enough memory for this job, and what to do when there is not.

Measured on the 8 GB / 16 GB target (docs/PERFORMANCE-8GB.md, "Desktop headroom"):
- VRAM is not the failure mode: DynamicVRAM streams more of the model when other apps hold VRAM
  (1.5 GB taken mid-job cost ~20%; 3 GB still finished).
- Windows **commit charge** (RAM + pagefile) is: when it runs out, the next allocation fails and a
  browser tab or ComfyUI (MemoryError) dies. An engine's commit grows to about the size of the
  models it has loaded and stays there while idle.
- The P-H3 4B encoder instead of the 32B one is the single best RAM fix for H3-Image.

So before a job: estimate what it needs (the model files it loads, from kit/models.json, plus a
margin), compare it with free commit plus what our engine already holds, and pick a profile:
  ok       enough room
  lean     tight: unload the engine's cached models first (the next load is slower) and use the
           light encoder where there is one; warn and list what to close
  critical not enough even then: lean, plus a stronger warning (it still runs; the pagefile has to
           grow mid-job, which is when a browser tab can crash)
The thresholds are estimates from the measured runs, not a calibration; bench.py can refine them.
Standard library only; Windows numbers via ctypes and one PowerShell call, other systems report
what they can.
"""
import ctypes, json, os, re, subprocess, time, urllib.request

import modelstore

MARGIN_GB = 2.0          # runtime buffers, latents, the VAE decode on top of the weights
# DynamicVRAM streams weights, so the engine does not commit every file at once. Fitted to the two
# measured engine commits: 16.3 GB after an H3 video (32 GB of files) and 19.6 GB after Krea + H3.
COMMIT_FACTOR = 0.6
TIGHT_GB = 4.0           # less spare than this after the job's estimate -> lean
OTHER_VRAM_GB = 1.5      # other apps holding this much VRAM -> a slower run (measured ~20%)
# light alternatives that keep the same inputs and look (measured: free RAM 1.9 GB instead of 0.5)
LEAN_WORKFLOW = {"wf_h3img.json": "wf_h3img_4bte.json", "wf_h3img_8gb.json": "wf_h3img_4bte.json"}
# never suggest closing these (Windows itself, the antivirus, the agent's own app, the engine)
KEEP = re.compile(r"^(system|registry|idle|memory compression|smss|csrss|wininit|winlogon|services|lsass|"
                  r"svchost|dwm|fontdrvhost|msmpeng|nissrv|securityhealth\w*|explorer|sihost|ctfmon|"
                  r"searchhost|startmenuexperiencehost|shellexperiencehost|textinputhost|runtimebroker|"
                  r"conhost|wudfhost|audiodg|spoolsv|dllhost|taskhostw|lsaiso|memcompression|"
                  r"claude|deepseek\w*|dsh\w*|windowsterminal|openconsole|powershell|pwsh|cmd|python|pythonw)$", re.I)


FRIENDLY = {"steamwebhelper": "Steam", "steam": "Steam", "msedge": "Edge", "chrome": "Chrome",
            "firefox": "Firefox", "discord": "Discord", "telegram": "Telegram", "spotify": "Spotify",
            "obs64": "OBS", "brave": "Brave", "opera": "Opera", "epicgameslauncher": "Epic Games"}


class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]


def memory():
    """{ram_total, ram_free, commit_limit, commit_free} in GB (Windows), else {}."""
    if os.name != "nt":
        return {}
    m = MEMORYSTATUSEX()
    m.dwLength = ctypes.sizeof(m)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
        return {}
    g = 1e9
    return {"ram_total": m.ullTotalPhys / g, "ram_free": m.ullAvailPhys / g,
            "commit_limit": m.ullTotalPageFile / g, "commit_free": m.ullAvailPageFile / g}


def vram():
    """{vram_total, vram_used} in GB for GPU 0 from nvidia-smi, else {}."""
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=memory.total,memory.used", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=10)
        tot, used = [float(x) for x in r.stdout.strip().splitlines()[0].split(",")]
        return {"vram_total": tot / 1024, "vram_used": used / 1024}
    except Exception:
        return {}


_PROCS = [0.0, []]


def processes(ttl=15):
    """[(name, commit GB, is_engine, exe, command line)] for every process (Windows), biggest first."""
    if os.name != "nt":
        return []
    if time.time() - _PROCS[0] < ttl:
        return _PROCS[1]
    ps = ("Get-CimInstance Win32_Process | Select-Object Name,ProcessId,PrivatePageCount,ExecutablePath,CommandLine"
          " | ConvertTo-Json -Compress")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                           capture_output=True, text=True, timeout=30, creationflags=0x08000000)
        rows = json.loads(r.stdout or "[]")
    except Exception:
        return []
    out = []
    for p in rows if isinstance(rows, list) else [rows]:
        cl = p.get("CommandLine") or ""
        eng = (p.get("Name") or "").lower() == "python.exe" and "main.py" in cl
        out.append(((p.get("Name") or "?").rsplit(".exe", 1)[0], (p.get("PrivatePageCount") or 0) / 1e9, eng,
                    p.get("ExecutablePath") or "", cl, p.get("ProcessId")))
    out.sort(key=lambda x: -x[1])
    _PROCS[:] = [time.time(), out]
    return out


def gpu_by_pid():
    """{pid: dedicated VRAM GB} from the Windows "GPU Process Memory" counters (WDDM hides this
    from nvidia-smi), or {} when unavailable."""
    if os.name != "nt":
        return {}
    ps = (r'(Get-Counter "\GPU Process Memory(*)\Dedicated Usage" -ErrorAction SilentlyContinue).CounterSamples'
          ' | Where-Object {$_.CookedValue -gt 0} | ForEach-Object { "$($_.InstanceName) $($_.CookedValue)" }')
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                           capture_output=True, text=True, timeout=30, creationflags=0x08000000)
    except Exception:
        return {}
    out = {}
    for line in r.stdout.splitlines():
        m = re.match(r"pid_(\d+)_\S*\s+([\d.]+)", line.strip())
        if m:
            out[int(m.group(1))] = out.get(int(m.group(1)), 0) + float(m.group(2)) / 1e9
    return out


def engine_stats(s):
    try:
        with urllib.request.urlopen(s["comfy_url"].rstrip("/") + "/system_stats", timeout=5) as r:
            d = json.loads(r.read())
        dev = (d.get("devices") or [{}])[0]
        return {"torch_vram": (dev.get("torch_vram_total") or 0) / 1e9}
    except Exception:
        return None


def job_gb(workflow, fields=None, s=None):
    """Estimated commit a job needs: the files the engine will actually load (the quantization it
    has; the 8 GB variant when missing) times COMMIT_FACTOR, plus MARGIN_GB."""
    reg = modelstore.registry()
    tot = 0.0
    for r in modelstore.check(workflow, fields, s):
        e = modelstore.entry(r["folder"], r["use"] or r["fetch"], reg) or {}
        if not e.get("gb") and r["use"]:
            for d in modelstore.search_dirs(r["folder"], s):
                f = os.path.join(d, *r["use"].split("/"))
                if os.path.isfile(f):
                    e = {"gb": os.path.getsize(f) / 1e9}
                    break
        tot += e.get("gb") or 0
    return tot * COMMIT_FACTOR + MARGIN_GB


def plan(workflow, fields=None, s=None, procs=None):
    """What to do for this job. Returns a dict the page, the engine layer and lab.py share:
    profile ok|lean|critical, workflow (maybe the light one), unload (bool), warnings [str],
    close [(app, GB)], numbers."""
    s = s or modelstore.settings()
    local = modelstore.is_local(s)
    mem = memory() if local else {}
    vr = vram() if local else {}
    procs = processes() if (local and procs is None) else (procs or [])
    eng = engine_stats(s)
    need = job_gb(workflow, fields, s)
    ours = sum(p[1] for p in procs if p[2] and (not s.get("engine_dir") or
                                                 os.path.normcase(s["engine_dir"]) in os.path.normcase(p[3])))
    others_engines = [p for p in procs if p[2] and s.get("engine_dir") and
                      os.path.normcase(s["engine_dir"]) not in os.path.normcase(p[3])]
    out = {"profile": "ok", "workflow": workflow, "unload": False, "warnings": [], "close": [],
           "need_gb": round(need, 1), "local": local}
    out.update({k: round(v, 1) for k, v in mem.items()})
    if not mem:                       # not Windows or a remote engine: nothing to judge locally
        return out
    have = mem["commit_free"] + ours
    out["have_gb"] = round(have, 1)
    spare = have - need
    if spare < TIGHT_GB:
        out["profile"] = "lean" if spare >= 0 else "critical"
        out["unload"] = True
        lean_wf = LEAN_WORKFLOW.get(workflow)
        if lean_wf and all(r["present"] for r in modelstore.check(lean_wf, fields, s)):
            out["workflow"] = lean_wf
            need2 = job_gb(lean_wf, fields, s)
            out["warnings"].append("Using the light 4B text encoder for this picture (about %.0f GB less memory)." % (need - need2))
            out["need_gb"] = round(need2, 1)
            if have - need2 >= 0 and out["profile"] == "critical":
                out["profile"] = "lean"
        out["warnings"].insert(0, "Low memory: about %.0f GB free for a job that needs about %.0f GB. Generating anyway "
                               "in low-memory mode: the engine drops its cached models first, so this one loads slower."
                               % (have, need))
        if out["profile"] == "critical":
            out["warnings"].append("Windows will have to grow the pagefile during the job - that is when a browser tab "
                                   "or the engine can crash with 'out of memory'. Close something below first if you can; "
                                   "a fixed 32-48 GB pagefile stops it for good (docs/PERFORMANCE-8GB.md).")
    if others_engines:
        out["warnings"].append("Another ComfyUI engine is running (%.1f GB): stop it if you are not using it "
                               "(the other studio's kit\\start.ps1 -Stop)." % sum(p[1] for p in others_engines))
    gp = gpu_by_pid() if vr else {}
    if gp:
        engine_pids = {p[5] for p in procs if p[2]}
        other_v = sum(g for pid, g in gp.items() if pid not in engine_pids)
    elif vr and eng is not None:
        other_v = max(0.0, vr["vram_used"] - eng["torch_vram"])
    else:
        other_v = None
    if other_v is not None:
        out["vram_other_gb"] = round(other_v, 1)
        if other_v > OTHER_VRAM_GB:
            out["warnings"].append("Other apps hold %.1f GB of video memory (a browser playing video, a game): this "
                                   "still works, about 20%% slower." % other_v)
    if out["profile"] != "ok" or out.get("vram_other_gb", 0) > OTHER_VRAM_GB:
        apps = {}
        for name, gb, is_eng, exe, cl, _pid in procs:
            if is_eng or KEEP.match(name) or gb < 0.05:
                continue
            name = FRIENDLY.get(name.lower(), name)
            apps[name] = apps.get(name, 0) + gb
        out["close"] = [(n, round(g, 1)) for n, g in sorted(apps.items(), key=lambda kv: -kv[1]) if g >= 0.3][:6]
    return out


def unload(s=None):
    """Ask the engine to drop its cached models and free memory before a job."""
    s = s or modelstore.settings()
    try:
        req = urllib.request.Request(s["comfy_url"].rstrip("/") + "/free",
                                     data=json.dumps({"unload_models": True, "free_memory": True}).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=30).read()
        time.sleep(2)
        return True
    except Exception:
        return False


def summary(p):
    """One readable paragraph for a job card or a terminal."""
    if p["profile"] == "ok" and not p["warnings"]:
        return ""
    txt = " ".join(p["warnings"])
    if p["close"]:
        txt += " Closing these frees the most: " + ", ".join("%s (%.1f GB)" % c for c in p["close"]) + "."
    return txt
