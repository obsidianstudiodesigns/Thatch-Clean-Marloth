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

COBALT = (35, 80, 168)
INK = (16, 22, 18)
BONE = (241, 242, 236)

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
GEIST = os.path.join(ROOT, "assets", "fonts", "geist-var.woff2")


def lapa(d, s, colour):
    """A conical lapa roof on a pole: the brand mark, drawn at scale s."""
    cx = s / 2
    apex = (cx, s * .2)
    eave_y = s * .57
    half = s * .38

    def flank(t):
        # concave roof flanks, like a real cone of thatch
        return apex[1] + (eave_y - apex[1]) * (t ** .7)

    steps = 32
    pts = [apex]
    for i in range(1, steps + 1):
        t = i / steps
        pts.append((cx + half * t, flank(t)))
    for i in range(steps, -1, -1):
        t = i / steps
        pts.append((cx - half * t, flank(t)))
    d.polygon(pts, fill=colour)
    # ridge cap
    r = s * .035
    d.ellipse((cx - r, apex[1] - r * 1.6, cx + r, apex[1] + r * .4), fill=colour)
    # two gum poles under the eaves
    pw = s * .06
    for px in (cx - half * .62, cx + half * .62):
        d.rectangle((px - pw / 2, eave_y - 2, px + pw / 2, s * .8), fill=colour)


def mark(size, bg=COBALT, fg=BONE):
    sc = 4
    s = size * sc
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * .22), fill=bg)
    lapa(d, s, fg)
    return im.resize((size, size), Image.LANCZOS)


def favicons():
    for n in (16, 32, 48, 96):
        mark(n).save(os.path.join(ROOT, f"favicon-{n}.png"))
    mark(256).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    for n, fn in ((192, "icon-192.png"), (512, "icon-512.png")):
        mark(n).save(os.path.join(ROOT, fn))
    for n, fn, pad in ((180, "apple-touch-icon.png", .1), (512, "icon-maskable-512.png", .18)):
        bg = Image.new("RGBA", (n, n), COBALT + (255,))
        inner = mark(int(n * (1 - 2 * pad)))
        bg.paste(inner, (int(n * pad), int(n * pad)), inner)
        bg.convert("RGB").save(os.path.join(ROOT, fn))
    mark(160).save(os.path.join(OUT, "mark-160.png"))


def og():
    W, H = 1200, 630
    base = load("gen/hero-wide.png")
    r = max(W / base.width, H / base.height)
    base = base.resize((round(base.width * r), round(base.height * r)), Image.LANCZOS)
    x = base.width - W
    im = base.crop((x, 0, x + W, H)).convert("RGBA")
    shade = Image.new("RGBA", (W, H))
    sd = ImageDraw.Draw(shade)
    for i in range(W):
        a = int(240 * max(0, 1 - i / (W * .78)) ** 1.15)
        sd.line([(i, 0), (i, H)], fill=INK + (a,))
    im = Image.alpha_composite(im, shade)
    d = ImageDraw.Draw(im)
    m = mark(76)
    im.paste(m, (72, 64), m)
    d.text((166, 74), "Thatch Clean", font=font(BRIC, 34, wght=700), fill=BONE)
    d.text((166, 114), "Marloth Park", font=font(GEIST, 22, wght=500), fill=(178, 190, 176))
    h1 = font(BRIC, 66, wght=700)
    y = 236
    for line in ("A thatch ceiling", "that looks and", "smells new again."):
        d.text((72, y), line, font=h1, fill=(244, 244, 238))
        y += 74
    sub = font(GEIST, 26, wght=450)
    d.text((72, y + 26), "Fumigation, deep vacuuming and fresh mist", font=sub, fill=(206, 210, 200))
    d.text((72, y + 62), "for thatched homes and lodges.  082 563 1277", font=sub, fill=(206, 210, 200))
    im.convert("RGB").save(os.path.join(OUT, "og-share.jpg"), quality=86, optimize=True, progressive=True)


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
