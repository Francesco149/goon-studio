from PIL import Image, ImageDraw, ImageFont
import os

A = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "analysis")


def font(sz):
    for n in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(n, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def pair(out, left, right, ll, rl, h=760):
    ims = []
    for p in (left, right):
        im = Image.open(p).convert("RGB")
        w = int(im.width * h / im.height)
        ims.append(im.resize((w, h), Image.Resampling.LANCZOS))
    canvas = Image.new("RGB", (sum(i.width for i in ims) + 20, h + 34), (18, 18, 18))
    dr = ImageDraw.Draw(canvas)
    f = font(16)
    x = 0
    for im, label in zip(ims, (ll, rl)):
        canvas.paste(im, (x, 34))
        dr.text((x + 6, 8), label, fill=(235, 235, 235), font=f)
        x += im.width + 20
    canvas.save(out, quality=91)
    print(out, canvas.size)


pair(A + "/HIRES_compare.jpg",
     os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "gens/pb/pb3_pov_seal_00001_.png"),
     os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "gens/h1/h1_d30_00001_.png"),
     "pb3 832x1248", "h1_d30 1152x1728 (denoise 0.30)")
pair(A + "/RESTYLE_compare.jpg",
     os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "gens/restyle_full/f000.png"),
     os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "gens/r1/f000_00001_.png"),
     "photoreal frame", "restyled Pink (denoise 0.45)")
