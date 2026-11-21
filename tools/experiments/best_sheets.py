from PIL import Image, ImageDraw, ImageFont
import os

G = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "gens")
A = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "analysis")


def font(sz):
    for n in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(n, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def sheet(name, items, cols, thumb, out):
    ims = []
    for label, path in items:
        im = Image.open(path).convert("RGB")
        im.thumbnail((thumb, thumb), Image.Resampling.LANCZOS)
        ims.append((label, im))
    cellh = max(i.height for _, i in ims) + 30
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * thumb, rows * cellh), (18, 18, 18))
    dr = ImageDraw.Draw(canvas)
    f = font(15)
    for k, (label, im) in enumerate(ims):
        x, y = (k % cols) * thumb, (k // cols) * cellh
        canvas.paste(im, (x + (thumb - im.width) // 2, y + 28))
        dr.text((x + 5, y + 6), label, fill=(235, 235, 235), font=f)
    canvas.save(out, quality=90)
    print(out, canvas.size)


photoreal = [
    ("e3/p1 natural body", G + "/e3/p1_bust_natural_00001_.png"),
    ("e3/p3 mirror", G + "/e3/p3_mirror_00001_.png"),
    ("e3/p4 lingerie", G + "/e3/p4_standing_00001_.png"),
    ("e5/g7 tag portrait", G + "/e5/g7_egirl_00001_.png"),
    ("e3/p5 seal", G + "/e3/p5_bj_seal_00001_.png"),
    ("e3/p7 side", G + "/e3/p7_bj_side_00001_.png"),
    ("e3/p8 paizuri", G + "/e3/p8_paizuri_00001_.png"),
    ("e67/o4 cum-out", G + "/e67/o4_cum_out_00001_.png"),
    ("e67/c3 splatter", G + "/e67/c3_splatter_00001_.png"),
    ("e1/e1e keyframe", G + "/e1/e1e_bj_pov_00001_.png"),
]
anime = [
    ("pa1 side", G + "/pa/pa1_side_base_00001_.png"),
    ("pa2 side anat", G + "/pa/pa2_side_anat_00001_.png"),
    ("pa3 pov", G + "/pa/pa3_pov_base_00001_.png"),
    ("pb1 seal", G + "/pb/pb1_side_seal_00001_.png"),
    ("pb2 seal weight", G + "/pb/pb2_side_seal_w_00001_.png"),
    ("pb3 pov seal", G + "/pb/pb3_pov_seal_00001_.png"),
    ("pb5 mosaic", G + "/pb/pb5_pov_mosaic_00001_.png"),
    ("pb6 bigger", G + "/pb/pb6_side_big_00001_.png"),
    ("pb7 cum", G + "/pb/pb7_cum_face_00001_.png"),
    ("pb8 close", G + "/pb/pb8_side_close_00001_.png"),
]
os.makedirs(A, exist_ok=True)
sheet("photoreal", photoreal, 5, 380, A + "/BEST_photoreal.jpg")
sheet("anime", anime, 5, 380, A + "/BEST_anime.jpg")
