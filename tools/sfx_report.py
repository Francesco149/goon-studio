#!/usr/bin/env python3
"""sfx_report.py - objective read-out of a generated clip's audio, to compare sound prompts.

This does NOT judge whether a sound is "wet suction" or "crunch". It measures the things that
are objective and were part of the owner's complaint:

  * event sync   - correlation between the audio envelope and the picture's motion envelope
  * transient character - how clicky/crunchy the sound is (onset density, high-band ratio)
  * bed          - loudness, silence, clipping, continuous room tone

Usage:
  python tools/sfx_report.py clip.mp4 [clip2.mp4 ...] [--json out.json]

Requires ffmpeg/ffprobe on PATH and numpy.
"""
import argparse
import json
import math
import subprocess
import sys

import numpy as np

FPS = 24.0
SR = 48000


def run(args):
    return subprocess.run(args, capture_output=True, check=True).stdout


def probe(path):
    out = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path])
    j = json.loads(out)
    dur = float(j["format"].get("duration", 0.0))
    has_audio = any(s.get("codec_type") == "audio" for s in j.get("streams", []))
    return dur, has_audio


def load_audio(path):
    raw = run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR),
               "-f", "f32le", "-"])
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def load_motion(path, width=128):
    # one gray frame per output frame; height follows the aspect ratio rounded to even
    raw = run(["ffmpeg", "-v", "error", "-i", path, "-vf",
               "fps=%g,scale=%d:-2,format=gray" % (FPS, width), "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    h = None
    # infer frame height from the stream probe
    j = json.loads(run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", path]))
    v = next(s for s in j["streams"] if s.get("codec_type") == "video")
    h = int(round(width * int(v["height"]) / int(v["width"]) / 2.0) * 2)
    n = len(raw) // (width * h)
    frames = np.frombuffer(raw[: n * width * h], dtype=np.uint8).reshape(n, h, width).astype(np.float32)
    if len(frames) < 2:
        return np.zeros(1)
    return np.abs(np.diff(frames, axis=0)).mean(axis=(1, 2))


def envelope(x, win, hop=None):
    hop = hop or win
    n = max(1, 1 + (len(x) - win) // hop)
    return np.array([np.sqrt(np.mean(x[i * hop:i * hop + win] ** 2) + 1e-12) for i in range(n)])


def z(x):
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-9 else 1.0)


def corr_at_lag(a, b, lag):
    if lag > 0:
        a, b = a[lag:], b[:-lag]
    elif lag < 0:
        a, b = a[:lag], b[-lag:]
    m = min(len(a), len(b))
    if m < 4:
        return 0.0
    a, b = z(a[:m]), z(b[:m])
    return float(np.mean(a * b))


def spectral(path):
    x = load_audio(path)
    sr = SR
    hop = sr  # 1 s windows
    cents, flats, lows, mids, highs = [], [], [], [], []
    for i in range(0, max(1, len(x) - sr + 1), hop):
        w = x[i:i + sr]
        if len(w) < sr // 2:
            continue
        spec = np.abs(np.fft.rfft(w * np.hanning(len(w)))) + 1e-12
        freqs = np.fft.rfftfreq(len(w), 1.0 / sr)
        p = spec ** 2
        p /= p.sum()
        cents.append(float((freqs * p).sum()))
        flats.append(float(np.exp(np.mean(np.log(spec))) / np.mean(spec)))
        lows.append(float(p[freqs < 300].sum()))
        mids.append(float(p[(freqs >= 300) & (freqs < 2000)].sum()))
        highs.append(float(p[freqs >= 2000].sum()))
    return x, dict(centroid_hz=float(np.mean(cents)) if cents else 0.0,
                   flatness=float(np.mean(flats)) if flats else 0.0,
                   band_low=float(np.mean(lows)) if lows else 0.0,
                   band_mid=float(np.mean(mids)) if mids else 0.0,
                   band_high=float(np.mean(highs)) if highs else 0.0)


def report(path):
    dur, has_audio = probe(path)
    motion = load_motion(path)
    out = {"file": path, "duration_s": round(dur, 2), "frames": int(len(motion) + 1), "has_audio": has_audio}
    if not has_audio:
        out["error"] = "no audio stream"
        return out
    x, spec = spectral(path)
    frame = int(math.ceil(SR / FPS))
    aenv = envelope(x, frame)
    menv = motion[: min(len(motion), len(aenv))]
    aenv = aenv[: len(menv)]
    corrs = {lag: corr_at_lag(aenv, menv, lag) for lag in range(-12, 13)}
    best = max(corrs, key=lambda k: abs(corrs[k]))
    out.update(spec)
    out["rms_dbfs"] = round(float(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)), 1)
    out["peak_dbfs"] = round(float(20 * np.log10(np.max(np.abs(x)) + 1e-12)), 1)
    out["clipped_samples"] = int(np.sum(np.abs(x) > 0.999))
    out["silence_frac"] = round(float(np.mean(envelope(x, SR) < 1e-4)), 2)
    onsets = np.maximum(0, np.diff(aenv))
    thr = onsets.mean() + 2 * onsets.std()
    out["onsets_per_s"] = round(float(np.sum(onsets > thr) / max(1e-9, dur)), 1)
    out["motion_std"] = round(float(motion.std()), 2)
    out["sync_best_lag_frames"] = int(best)
    out["sync_best_r"] = round(corrs[best], 2)
    out["sync_r_zero"] = round(corrs[0], 2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    rows = [report(f) for f in a.files]
    for r in rows:
        print(json.dumps(r, indent=1))
    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1)
        print("wrote " + a.json, file=sys.stderr)


if __name__ == "__main__":
    main()
