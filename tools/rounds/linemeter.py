# linemeter.py - line-art drift per clip (a106): dark-pixel share, mean dark-line run width, sharpness; first vs last frame.
# Usage: python_embeded\python.exe -I tools/rounds/linemeter.py clip.mp4 [...]. Dark backgrounds inflate "ink" - compare like with like.
# per clip: ink share (dark pixels), mean dark-line run width, sharpness (Laplacian), first vs last frame
import sys, av, numpy as np
def m(im):
    g = np.asarray(im.convert('L'), dtype=np.float32)
    ink = (g < 90).mean() * 100
    lap = np.abs(4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]).mean()
    runs = []
    for row in (g < 90)[::6]:
        r = 0
        for v in row:
            if v: r += 1
            elif r: runs.append(r); r = 0
    return ink, np.mean([x for x in runs if x < 30]) if runs else 0, lap
for p in sys.argv[1:]:
    fr = [f.to_image() for f in av.open(p).decode(video=0)]
    a, b = m(fr[0]), m(fr[-1])
    print('%-34s first ink %5.2f line %4.2f sharp %5.2f | last ink %5.2f line %4.2f sharp %5.2f' % ((p.split('/')[-1],) + a + b))
