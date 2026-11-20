#!/usr/bin/env python3
"""vsheet.py - one row per clip, N evenly spaced frames across the row, for judging motion.

sheet.py shows three frames of a clip, which is enough to pick a still but not enough to judge a
cum shot: the event is a few frames long and the interesting part is how the material changes
between them. This puts the same instants of every clip under each other, so the shared timing
is visible as a column and the differences read as rows.

  python vsheet.py out.jpg gens/k01 --frames 8 --thumb 260 [--label-prefix ""]

  python vsheet.py out.jpg clipA.mp4 clipB.mp4 --frames 6      # individual files too

Each cell is labelled with its frame number; each row with the clip name and the frame count.
Needs ffmpeg/ffprobe on PATH (it uses them; no PyAV dependency).
"""
import argparse
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont


def font(sz):
    for name in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=nb_frames,r_frame_rate,width,height",
         "-of", "default=nw=1", path],
        capture_output=True, text=True)
    meta = {}
    for line in (out.stdout or "").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            meta[k.strip()] = v.strip()
    try:
        n = int(meta.get("nb_frames") or 0)
    except ValueError:
        n = 0
    if not n:
        # a stream copy can hide nb_frames; fall back to a count
        out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:v:0",
                              "-c", "copy", "-f", "null", "-"],
                             capture_output=True, text=True)
        n = (out.stderr or "").count("frame=") and 0
        n = n or int(meta.get("nb_frames") or 0)
    return n, meta


def extract(path, idx, width):
    """Frame i of path as a PIL image of the given width."""
    tmp = tempfile.mkdtemp()
    sel = "+".join("eq(n\\,%d)" % i for i in idx)
    dst = os.path.join(tmp, "f_%04d.jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path,
                    "-vf", "select='%s'" % sel, "-fps_mode", "passthrough",
                    "-q:v", "2", dst], capture_output=True, text=True)
    got = sorted(os.listdir(tmp))
    ims = []
    for name in got:
        im = Image.open(os.path.join(tmp, name)).convert("RGB")
        im = im.resize((width, int(round(im.height * width / im.width))), Image.Resampling.LANCZOS)
        ims.append(im)
    return ims


def collect(paths):
    vids = []
    for p in paths:
        if os.path.isdir(p):
            vids += [os.path.join(p, f) for f in sorted(os.listdir(p))
                     if f.lower().rsplit(".", 1)[-1] in ("mp4", "webm", "mov")]
        elif os.path.isfile(p):
            vids.append(p)
        else:
            sys.exit("not a file or folder: " + p)
    return [v for v in vids if os.path.isfile(v)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--frames", type=int, default=8, help="frames per row")
    ap.add_argument("--thumb", type=int, default=260, help="cell width in px")
    ap.add_argument("--last", type=int, default=None,
                    help="sample the last N frames instead of the whole clip")
    a = ap.parse_args()

    vids = collect(a.paths)
    if not vids:
        sys.exit("nothing to show")

    rows = []
    for v in vids:
        n, meta = probe(v)
        if n <= 0:
            print("skip (no frame count):", v)
            continue
        if a.last:
            first = max(0, n - a.last)
            span = n - first
        else:
            first, span = 0, n
        idx = [first + int(round(i * (span - 1) / max(1, a.frames - 1))) for i in range(a.frames)]
        ims = extract(v, idx, a.thumb)
        if not ims:
            print("skip (no frames):", v)
            continue
        rows.append((os.path.basename(v).rsplit(".", 1)[0], n, meta.get("r_frame_rate", "?"), idx, ims))

    if not rows:
        sys.exit("no rows")

    tw, th = rows[0][4][0].size
    lab = 28
    head = 22
    W = a.frames * tw
    H = len(rows) * (head + th + 2 + lab)
    out = Image.new("RGB", (W, H), (16, 16, 16))
    dr = ImageDraw.Draw(out)
    f_cell = font(15)
    f_row = font(17)

    y = 0
    for name, n, fps, idx, ims in rows:
        dr.text((4, y + 3), "%s  (%d frames @ %s fps)" % (name, n, fps.split("/")[0]),
                fill=(240, 240, 240), font=f_row)
        y += head
        for i, im in enumerate(ims):
            x = i * tw
            out.paste(im, (x, y))
            if i < len(idx):
                dr.rectangle([x, y, x + tw - 1, y + th - 1], outline=(60, 60, 60))
                dr.text((x + 4, y + 3), str(idx[i]), fill=(255, 235, 120), font=f_cell)
        y += th + 2
        for i, fr in enumerate(idx):
            dr.text((i * tw + 4, y), "f%d" % fr, fill=(200, 200, 200), font=f_cell)
        y += lab

    out.save(a.out, quality=90)
    print(a.out, out.size, "%d clips x %d frames" % (len(rows), a.frames))


if __name__ == "__main__":
    main()
