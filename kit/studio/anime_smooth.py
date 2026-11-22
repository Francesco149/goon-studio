#!/usr/bin/env python3
"""anime_smooth.py - make a stepped H3 clip move smoothly (h-game / live2d motion).

The opposite of anime_timing.py. On a flat TV-style keyframe H3 often draws on 2s by itself:
every other frame is an exact copy of the one before, 12 drawings/s (round a99,
docs/ANIME-TIMING.md "Smooth motion"). This drops the copies and redraws the in-betweens with a
frame-interpolation model (RIFE or FILM, the engine's own code), so every output frame is a new
pose. Clip length and audio are unchanged; --mult 2 doubles the frame rate as well.

  python_embeded\\python.exe -I kit/studio/anime_smooth.py in.mp4 out.mp4 [--model rife]
         [--mult 1] [--sheet sheet.jpg]

The model files live in the store (kit/models.json: frame_interpolation/rife_v4.26.safetensors,
frame_interpolation/film_net_fp16.safetensors). Needs the engine's python (torch, PyAV) and the
engine folder (engine_dir in my/settings.json, or the python_embeded this runs from).
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import anime_timing as AT  # noqa: E402  (load / write / sheet)

MODELS = {"rife": "rife_v4.26.safetensors", "film": "film_net_fp16.safetensors"}
# page / job values ("smooth" key): id -> (label, model, frame-rate multiplier)
MODES = {
    "off": ("off (as generated)", None, 1),
    "smooth": ("smooth: RIFE in-betweens", "rife", 1),
    "smooth_film": ("smooth: FILM in-betweens (large motion)", "film", 1),
    "smooth_x2": ("smooth: RIFE, double frame rate (48 fps)", "rife", 2),
}


def settings():
    p = os.path.join(ROOT, "my", "settings.json")
    try:
        with open(p, encoding="utf-8-sig") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def comfy_dir():
    s = settings()
    cands = []
    if s.get("engine_dir"):
        cands.append(os.path.join(s["engine_dir"], "ComfyUI"))
    cands.append(os.path.join(os.path.dirname(os.path.dirname(sys.executable)), "ComfyUI"))
    for c in cands:
        if os.path.isfile(os.path.join(c, "comfy_extras", "nodes_frame_interpolation.py")):
            return c
    raise RuntimeError("no ComfyUI with frame interpolation found (engine_dir in my/settings.json)")


def model_path(name):
    sys.path.insert(0, HERE)
    import modelstore as M
    p = M.dest_path("frame_interpolation", MODELS.get(name, name))
    if not os.path.isfile(p):
        raise RuntimeError("missing %s - run: python tools/models/store.py fetch --file frame_interpolation/%s"
                           % (p, MODELS.get(name, name)))
    return p


def load_model(name):
    c = comfy_dir()
    if c not in sys.path:
        sys.path.insert(0, c)
    import torch
    import comfy.utils
    from comfy_extras.nodes_frame_interpolation import FrameInterpolationModelLoader
    sd = comfy.utils.load_torch_file(model_path(name), safe_load=True)
    m = FrameInterpolationModelLoader._detect_and_load(sd)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dt = torch.float16 if dev.type == "cuda" else torch.float32
    return m.eval().to(dev, dt), dev, dt


def drawings(frames, sep=4.0):
    """start frame of every distinct drawing. The frame-to-frame changes split into two groups on a
    log scale (Otsu): copies (compression noise only) and new drawings. When the groups are not
    clearly apart (means less than `sep` x), the clip is already on 1s and every frame is a drawing."""
    import numpy as np
    small = [f[::4, ::4].astype(np.float32).mean(2) for f in frames]
    d = np.array([np.abs(small[i] - small[i - 1]).mean() for i in range(1, len(small))])
    v = np.sort(np.log(d + 0.05))
    best, cut = -1.0, None
    for k in range(1, len(v)):
        lo, hi = v[:k], v[k:]
        s = len(lo) * len(hi) * (lo.mean() - hi.mean()) ** 2
        if s > best:
            best, cut = s, k
    thr = float(np.exp((v[cut - 1] + v[cut]) / 2) - 0.05)
    lo, hi = d[d <= thr], d[d > thr]
    if not len(lo) or not len(hi) or hi.mean() < sep * lo.mean() or len(lo) < 0.2 * len(d):
        return list(range(len(frames))), 0.0
    keys = [0] + [i for i in range(1, len(frames)) if d[i - 1] > thr]
    return keys, thr


def smooth(src, dst, model="rife", mult=1, keep_ends=True):
    import numpy as np
    import torch
    import torch.nn.functional as F
    frames, rate = AT.load(src)
    n = len(frames)
    keys, thr = drawings(frames)
    if keys[-1] != n - 1 and keep_ends:
        keys.append(n - 1)  # the last drawing's hold becomes motion toward the final frame (no-op if equal)
    net, dev, dt = load_model(model)
    align = getattr(net, "pad_align", 1)
    h, w = frames[0].shape[:2]
    ph, pw = (-h) % align, (-w) % align

    def tens(i):
        x = torch.from_numpy(frames[i]).to(dev).permute(2, 0, 1)[None].to(dt) / 255.0
        return F.pad(x, (0, pw, 0, ph), mode="reflect") if (ph or pw) else x

    out_n = (n - 1) * mult + 1
    out = [None] * out_n
    multi = getattr(net, "forward_multi_timestep", None)
    with torch.inference_mode():
        for a, b in zip(keys, keys[1:]):
            # output slots o with source time o/mult in [a, b)
            slots = [o for o in range(a * mult, b * mult)]
            ts = [(o / mult - a) / (b - a) for o in slots]
            out[slots[0]] = frames[a]
            need = [(o, t) for o, t in zip(slots, ts) if t > 0]
            if not need:
                continue
            x0, x1 = tens(a), tens(b)
            cache = {"img0": net.extract_features(x0), "img1": net.extract_features(x1)}
            tv = [t for _, t in need]
            if multi is not None:
                mids = multi(x0, x1, tv, cache=cache)
            else:
                tt = torch.tensor(tv, device=dev, dtype=dt).reshape(-1, 1, 1, 1).expand(-1, 1, x0.shape[2], x0.shape[3])
                mids = net(x0.expand(len(tv), -1, -1, -1), x1.expand(len(tv), -1, -1, -1), timestep=tt, cache=cache)
            mids = (mids[:, :, :h, :w].clamp(0, 1) * 255).round().byte().permute(0, 2, 3, 1).cpu().numpy()
            for (o, _), m in zip(need, mids):
                out[o] = m
        for o in range(out_n):
            if out[o] is None:
                out[o] = frames[min(n - 1, o // mult)]
    AT.write(out, list(range(out_n)), rate * mult, src, dst)
    return {"frames": n, "drawings": len(keys), "threshold": thr, "out_frames": out_n, "fps": float(rate * mult),
            "_frames": out}


def apply_mode(path, mode):
    """page hook: smooth path in place for a MODES id; the untouched clip is kept as <stem>-raw<ext>.
    Returns the raw path, or None when nothing was done."""
    if not mode or mode == "off" or mode not in MODES or not path.lower().endswith((".mp4", ".webm", ".mov")):
        return None
    _, model, mult = MODES[mode]
    stem, ext = os.path.splitext(path)
    raw = stem + "-raw" + ext
    os.replace(path, raw)
    try:
        smooth(raw, path, model=model, mult=mult)
    except Exception:
        if os.path.exists(path):
            os.remove(path)
        os.replace(raw, path)
        raise
    return raw


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--model", choices=sorted(MODELS), default="rife")
    ap.add_argument("--mult", type=int, default=1, help="frame-rate multiplier (2 = 48 fps)")
    ap.add_argument("--sheet")
    a = ap.parse_args()
    r = smooth(a.src, a.dst, model=a.model, mult=max(1, a.mult))
    if a.sheet:
        AT.sheet(r["_frames"], list(range(len(r["_frames"]))), a.sheet)
    print("%s: %d frames, %d drawings in (copy threshold %.2f) -> %d frames at %.0f fps" % (
        os.path.basename(a.dst), r["frames"], r["drawings"], r["threshold"], r["out_frames"], r["fps"]))


if __name__ == "__main__":
    sys.exit(main())
