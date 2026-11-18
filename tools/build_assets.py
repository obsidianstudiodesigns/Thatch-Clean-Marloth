"""Build web images, favicons, the logo mark and the WhatsApp/social share image.

Run from the project root:  python -I tools/build_assets.py
Needs Pillow and fontTools (with brotli). Raw images live in _source/ (not in git).
"""
import io
import os
import re
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_source")
OUT = os.path.join(ROOT, "assets", "img")
os.makedirs(OUT, exist_ok=True)

NAVY = (12, 42, 82)
NAVY3 = (7, 29, 58)
SAND = (217, 196, 166)
GOLD = (240, 180, 41)
ON = (238, 244, 251)
ON2 = (185, 203, 227)

# name: (source, crop as fractions l, t, r, b or None, widths)
IMAGES = {
    "hero-wide": ("gen/hero-wide.png", None, (960, 1536)),
    "hero-tall": ("gen/hero-tall.png", None, (540, 864)),
    "cobweb": ("gen/cobweb.png", None, (720, 1280)),
    "fumigate": ("gen/fumigate.png", None, (600, 960)),
    "vacuum": ("gen/vacuum.png", None, (600, 960)),
    "mist": ("gen/mist.png", None, (600, 960)),
    "deck": ("gen/deck.png", None, (720, 1280)),
    "house": ("gen/house.png", None, (960, 1280)),
    "landscape": ("gen/landscape.png", None, (960, 1536)),
}


def load(rel, crop=None):
    im = Image.open(os.path.join(SRC, rel)).convert("RGB")
    if crop:
        w, h = im.size
        l, t, r, b = crop
        im = im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))
    return im


def save_sizes(name, im, widths):
    sizes = []
    for w in widths:
        w = min(w, im.width)
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(
            os.path.join(OUT, f"{name}-{w}.webp"), "WEBP", quality=80, method=6)
        sizes.append((w, h))
    return sizes


_CACHE = {}


def font(path, size, **axes):
    key = (path, tuple(sorted(axes.items())))
    if key not in _CACHE:
        from fontTools.varLib.instancer import instantiateVariableFont
        f = TTFont(path)
        f.flavor = None
        names = [a.axisTag for a in f["fvar"].axes]
        f = instantiateVariableFont(f, {n: axes.get(n, 400) for n in names})
        buf = io.BytesIO()
        f.save(buf)
        _CACHE[key] = buf.getvalue()
    return ImageFont.truetype(io.BytesIO(_CACHE[key]), size)


BRIC = os.path.join(ROOT, "assets", "fonts", "bricolage-var.woff2")
MONT = os.path.join(ROOT, "assets", "fonts", "montserrat-var.woff2")


def mark(size):
    """Favicon: navy tile with the logo's two house roofs in sand on a ground line."""
    sc = 4
    s = size * sc
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * .22), fill=NAVY)
    w = max(int(s * .075), 2)
    # logo house lines, fitted into the tile (logo units 25..490 x 45..397)
    def P(x, y):
        return (s * .15 + (x - 25) / 465 * s * .7, s * .2 + (y - 45) / 352 * s * .62)
    gy = 330
    d.line([P(25, gy), P(25, 160), P(205, 47), P(250, 75)], fill=SAND, width=w, joint="curve")
    d.line([P(150, gy), P(150, 160), P(318, 45), P(490, 160), P(490, gy)], fill=SAND, width=w, joint="curve")
    d.line([P(25, gy), P(490, gy)], fill=SAND, width=w)
    # a blue window of CLEAN in the front house
    x0, y0 = P(268, 200)
    x1, y1 = P(368, 290)
    d.rounded_rectangle((x0, y0, x1, y1), radius=int(s * .03), fill=(125, 184, 242))
    return im.resize((size, size), Image.LANCZOS)


def favicons():
    for n in (16, 32, 48, 96):
        mark(n).save(os.path.join(ROOT, f"favicon-{n}.png"))
    mark(256).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    for n, fn in ((192, "icon-192.png"), (512, "icon-512.png")):
        mark(n).save(os.path.join(ROOT, fn))
    for n, fn, pad in ((180, "apple-touch-icon.png", .06), (512, "icon-maskable-512.png", .16)):
        bg = Image.new("RGBA", (n, n), NAVY + (255,))
        inner = mark(int(n * (1 - 2 * pad)))
        bg.paste(inner, (int(n * pad), int(n * pad)), inner)
        bg.convert("RGB").save(os.path.join(ROOT, fn))


def og():
    """WhatsApp / social preview: navy, real logo, headline, photo in the arch window."""
    W, H = 1200, 630
    im = Image.new("RGBA", (W, H), NAVY + (255,))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(520, 0, -8):
        a = int(70 * (1 - r / 520) ** 1.6)
        gd.ellipse((980 - r, 120 - r, 980 + r, 120 + r), fill=(42, 123, 200, a))
    im = Image.alpha_composite(im, glow)
    d = ImageDraw.Draw(im)
    gy = 578
    d.line([(0, gy), (W, gy)], fill=SAND + (150,), width=2)
    # arch photo
    ax0, ax1, top = 790, 1120, 92
    aw = ax1 - ax0
    photo = load("gen/hero-tall.png")
    r = max(aw / photo.width, (gy - top) / photo.height)
    photo = photo.resize((round(photo.width * r), round(photo.height * r)), Image.LANCZOS)
    px = (photo.width - aw) // 2
    py = int((photo.height - (gy - top)) * .4)
    photo = photo.crop((px, py, px + aw, py + gy - top)).convert("RGBA")
    m = Image.new("L", (aw * 4, (gy - top) * 4), 0)
    md = ImageDraw.Draw(m)
    md.rounded_rectangle((0, 0, aw * 4 - 1, (gy - top) * 4 + aw * 2), radius=aw * 2, fill=255)
    m = m.resize((aw, gy - top), Image.LANCZOS)
    im.paste(photo, (ax0, top), m)
    d.rounded_rectangle((ax0 - 14, top - 14, ax1 + 14, gy + aw), radius=(aw + 28) // 2, outline=SAND + (170,), width=2)
    d.rectangle((ax0 - 20, gy + 1, ax1 + 20, H), fill=NAVY + (255,))
    d.line([(0, gy), (W, gy)], fill=SAND + (150,), width=2)
    # logo
    logo = Image.open(os.path.join(SRC, "gen", "logo-light.png")).convert("RGBA")
    lw = 400
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    im.alpha_composite(logo, (64, 52))
    d = ImageDraw.Draw(im)
    h1 = font(BRIC, 60, wght=700)
    y = 236
    for i, line in enumerate(("A thatch ceiling", "that looks and", "smells new.")):
        d.text((68, y), line, font=h1, fill=ON)
        y += 68
    sub = font(MONT, 23, wght=500)
    d.text((70, y + 22), "Fumigation, deep vacuuming and fresh mist", font=sub, fill=ON2)
    d.text((70, y + 54), "in Marloth Park.", font=sub, fill=ON2)
    d.text((70, y + 98), "082 563 1277", font=font(MONT, 26, wght=700), fill=GOLD)
    im.convert("RGB").save(os.path.join(OUT, "og-share.jpg"), quality=88, optimize=True, progressive=True)


def icons():
    src = os.path.join(SRC, "dl", "icons")
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']
    for fn in sorted(os.listdir(src)):
        body = open(os.path.join(src, fn), encoding="utf-8").read()
        inner = re.search(r"<svg[^>]*>(.*)</svg>", body, re.S).group(1)
        out.append(f'<symbol id="i-{fn[:-4]}" viewBox="0 0 256 256" fill="currentColor">{inner}</symbol>')
    out.append("</svg>")
    open(os.path.join(ROOT, "assets", "icons.svg"), "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    lines = []
    for name, (rel, crop, widths) in IMAGES.items():
        sizes = save_sizes(name, load(rel, crop), widths)
        lines.append(f"{name}: " + ", ".join(f"{w}x{h}" for w, h in sizes))
    with open(os.path.join(OUT, "_sizes.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    favicons()
    og()
    icons()
    print("\n".join(lines))
