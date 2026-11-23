# clipsheet.py out.jpg clip.mp4 [first last count] - a frame sheet of one clip (4 columns, frame numbers)
import sys, av
from PIL import Image, ImageDraw
out, p = sys.argv[1], sys.argv[2]
fr = [f.to_image() for f in av.open(p).decode(video=0)]
a, b, n = (int(x) for x in sys.argv[3:6]) if len(sys.argv) > 5 else (0, len(fr) - 1, 8)
idx = [a + round(i * (b - a) / (n - 1)) for i in range(n)]
w, h = 576, int(576 * fr[0].height / fr[0].width)
C = Image.new('RGB', (4 * w, -(-n // 4) * h))
for i, k in enumerate(idx):
    C.paste(fr[k].resize((w, h)), ((i % 4) * w, (i // 4) * h)); ImageDraw.Draw(C).text(((i % 4) * w + 6, (i // 4) * h + 4), str(k), fill='red')
C.save(out, quality=88)
