# linemeter.py - line-art drift per clip (a106/a107): dark-line run width at luma 90 and 60, and mean luma, for
# frame 0, the mean of frames 8-23 and the mean of the last 24 frames (the jump happens in the first ~8 frames).
# Usage: python_embeded\python.exe -I tools/rounds/linemeter.py clip.mp4[@skip] [...]; @22 skips an extension's context.
# Dark backgrounds inflate the widths - compare like with like (same shot, same start).
import sys, av, numpy as np


def width(g, thr=90):
    runs = []
    for row in (g < thr)[::4]:
        d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]]))
        runs += list(np.where(d == -1)[0] - np.where(d == 1)[0])
    runs = [r for r in runs if r < 30]
    return np.mean(runs) if runs else 0


def stats(g):
    return width(g), width(g, 60), g.mean()


for a in sys.argv[1:]:
    p, _, skip = a.partition('@')
    fr = [np.asarray(f.to_image().convert('L'), dtype=np.float32) for f in av.open(p).decode(video=0)][int(skip or 0):]
    mean = lambda ix: np.mean([stats(fr[i]) for i in ix], axis=0)
    r = [stats(fr[0]), mean(range(8, min(24, len(fr)))), mean(range(max(0, len(fr) - 24), len(fr)))]
    print('%-40s n=%3d ' % (p[-40:], len(fr)) + ' | '.join('w90 %.2f w60 %.2f Y %.0f' % tuple(x) for x in r))
