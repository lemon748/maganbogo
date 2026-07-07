# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))

# --- fonts (Malgun Gothic Bold) ---
def font(sz, bold=True):
    for p in [r"C:\Windows\Fonts\malgunbd.ttf", r"C:\Windows\Fonts\malgun.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

TOP = (47, 111, 143)      # #2f6f8f accent
BOT = (28, 74, 100)       # darker
WHITE = (255, 255, 255)
GREEN = (63, 199, 133)    # check

def make(size):
    S = 1024  # supersample then downscale for crisp edges
    img = Image.new("RGB", (S, S), TOP)
    d = ImageDraw.Draw(img)
    # vertical gradient
    for y in range(S):
        t = y / (S - 1)
        c = tuple(int(TOP[i] + (BOT[i]-TOP[i])*t) for i in range(3))
        d.line([(0, y), (S, y)], fill=c)

    # soft rounded panel highlight
    pad = int(S*0.11)
    d.rounded_rectangle([pad, pad, S-pad, S-pad], radius=int(S*0.12),
                        outline=(255,255,255,0), width=0)

    # "정자점" small on top
    f_small = font(int(S*0.11))
    txt = "정자점"
    bb = d.textbbox((0,0), txt, font=f_small)
    w = bb[2]-bb[0]; h = bb[3]-bb[1]
    d.text(((S-w)/2 - bb[0], int(S*0.235) - bb[1]), txt, font=f_small,
           fill=(255,255,255))
    # slight translucency effect: overlay semi -> skip, keep solid but softer via lighter tint
    # (draw again lighter to soften)

    # "마감" big
    f_big = font(int(S*0.42))
    txt2 = "마감"
    bb2 = d.textbbox((0,0), txt2, font=f_big)
    w2 = bb2[2]-bb2[0]; h2 = bb2[3]-bb2[1]
    d.text(((S-w2)/2 - bb2[0], int(S*0.40) - bb2[1]), txt2, font=f_big, fill=WHITE)

    # green check badge bottom
    cx, cy, r = int(S*0.5), int(S*0.80), int(S*0.085)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=GREEN)
    lw = int(S*0.028)
    d.line([(cx-r*0.45, cy+r*0.02), (cx-r*0.08, cy+r*0.42), (cx+r*0.55, cy-r*0.42)],
           fill=WHITE, width=lw, joint="curve")

    img = img.resize((size, size), Image.LANCZOS)
    return img

def make_rounded(size, radius_ratio=0.22):
    base = make(size).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0,0,size-1,size-1], radius=int(size*radius_ratio), fill=255)
    base.putalpha(mask)
    return base

os.makedirs(OUT, exist_ok=True)
# iOS applies its own mask -> full square
make(180).save(OUT + "/apple-touch-icon.png")
make(192).save(OUT + "/icon-192.png")
make(512).save(OUT + "/icon-512.png")
# favicon rounded looks nice in tabs
make_rounded(64).save(OUT + "/favicon.png")
# a big preview to show the user
make_rounded(512).save(OUT + "/icon-preview.png")
print("아이콘 생성 완료 ->", OUT)
