"""Redraw the Thatch Clean flyer logo as clean SVG.

Two house outlines on a ground line, THATCH (taupe) CLEAN (blue) lettering, the
tagline, and the canister vacuum. Coordinates follow the logo on the client's flyer.

Run from the project root:  python -I tools/build_logo.py
Writes assets/img/logo.svg (for light backgrounds), logo-light.svg (for navy),
logo-header*.svg (no tagline, for small sizes) and PNG renders in _source/gen/.
"""
import io
import os
import subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
GEN = os.path.join(ROOT, "_source", "gen")
MONT = os.path.join(ROOT, "_source", "dl", "montserrat-700.woff2")

COLOURS = {
    "light": {  # on white / light backgrounds: the flyer colours
        "taupe": "#9a7f62", "blue": "#2a7bc8", "tag": "#2a73b8",
        "hose": "#2b4669", "wand": "#2f7fd0", "body": "#6f95bd", "panel": "#94b1cf",
        "lid": "#7fa2c6", "band": "#2b4669", "label": "#2f7fd0", "label2": "#5fa0e0",
        "stripe": "#c9b98f", "base": "#2b4669", "nozzle": "#2b4669", "nozzle2": "#5f8fc2", "collar": "#d4a04a",
    },
    "dark": {  # on navy: same logo, lifted so it reads
        "taupe": "#d9c4a6", "blue": "#7db8f2", "tag": "#a9cdf3",
        "hose": "#c9dbf0", "wand": "#7db8f2", "body": "#7fa3cb", "panel": "#a7c1dc",
        "lid": "#93b4d6", "band": "#0c2a52", "label": "#2f7fd0", "label2": "#7db8f2",
        "stripe": "#d9c4a6", "base": "#c9dbf0", "nozzle": "#c9dbf0", "nozzle2": "#7db8f2", "collar": "#f0b429",
    },
}

# lettering
CAP_T, CAP_B = 230.0, 316.0
W = 8.8                        # stroke weight
S = W / 2
T, B = CAP_T + S, CAP_B - S    # stroke centrelines
MID = CAP_T + (CAP_B - CAP_T) * .52
R = 13.0                       # corner radius on A, C, N
GAP = 12.0


def letter(ch, x):
    """Return (path d, advance width) for one letter at x."""
    w = {"T": 60, "H": 66, "A": 60, "C": 54, "L": 50, "E": 54, "N": 60}[ch]
    L, Rt = x + S, x + w - S
    if ch == "T":
        d = f"M{x} {T}H{x + w}M{x + w / 2} {T}V{CAP_B}"
    elif ch == "H":
        d = f"M{L} {CAP_T}V{CAP_B}M{Rt} {CAP_T}V{CAP_B}M{L} {MID}H{Rt}"
    elif ch == "A":
        d = (f"M{L} {CAP_B}V{T + R}A{R} {R} 0 0 1 {L + R} {T}H{Rt - R}"
             f"A{R} {R} 0 0 1 {Rt} {T + R}V{CAP_B}M{L} {MID + 6}H{Rt}")
    elif ch == "C":
        d = (f"M{x + w} {T}H{L + R}A{R} {R} 0 0 0 {L} {T + R}V{B - R}"
             f"A{R} {R} 0 0 0 {L + R} {B}H{x + w}")
    elif ch == "L":
        d = f"M{L} {CAP_T}V{B}H{x + w}"
    elif ch == "E":
        d = f"M{x + w} {T}H{L}V{B}H{x + w}M{L} {MID}H{x + w - 4}"
    elif ch == "N":
        d = f"M{L} {CAP_B}V{T}H{Rt - R}A{R} {R} 0 0 1 {Rt} {T + R}V{CAP_B}"
    return d, w


def word(text, x):
    parts = []
    for ch in text:
        d, w = letter(ch, x)
        parts.append(d)
        x += w + GAP
    return "".join(parts), x - GAP


def tagline_path(text, x, baseline, cap, target_w):
    f = TTFont(MONT)
    f.flavor = None
    buf = io.BytesIO()
    f.save(buf)
    f = TTFont(io.BytesIO(buf.getvalue()))
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    capu = f["OS/2"].sCapHeight or 700
    scale = cap / capu
    hmtx = f["hmtx"]
    names = [cmap[ord(c)] for c in text]
    raw = sum(hmtx[n][0] for n in names) * scale
    track = (target_w - raw) / (len(text) - 1)
    pen = SVGPathPen(gs)
    cx = x
    for n in names:
        tp = TransformPen(pen, (scale, 0, 0, -scale, cx, baseline))
        gs[n].draw(tp)
        cx += hmtx[n][0] * scale + track
    return pen.getCommands()


def svg(variant, tagline=True):
    c = COLOURS[variant]
    thatch, end1 = word("THATCH", 76)
    clean, end2 = word("CLEAN", end1 + 53)
    vb = "15 38 1188 372" if tagline else "15 38 1188 372"
    tag = ""
    if tagline:
        tag = f'<path fill="{c["tag"]}" d="{tagline_path("ECO THATCH CLEANING SPECIALISTS", 118, 372, 24.5, 744)}"/>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Thatch Clean, eco thatch cleaning specialists">
<g fill="none" stroke="{c["taupe"]}" stroke-width="4.6" stroke-linejoin="miter" stroke-linecap="butt">
<path d="M1196 397H25V160L205 47L246 73"/>
<path d="M140 322V160L318 45L490 160"/>
</g>
<path fill="none" stroke="{c["taupe"]}" stroke-width="{W}" stroke-linejoin="miter" d="{thatch}"/>
<path fill="none" stroke="{c["blue"]}" stroke-width="{W}" stroke-linejoin="miter" d="{clean}"/>
{tag}
<g>
<path fill="none" stroke="{c["hose"]}" stroke-width="5" stroke-linecap="round" d="M1027 335C995 335 968 331 962 305C956 278 980 250 1010 222C1035 199 1062 180 1066 162C1069 148 1047 145 1027 158C1008 170 994 188 984 203"/>
<path fill="none" stroke="{c["wand"]}" stroke-width="6.5" stroke-linecap="round" d="M984 202L912 384"/>
<path fill="{c["nozzle"]}" d="M866 398C868 391 878 387 892 387H912V398Z"/>
<path fill="{c["nozzle2"]}" d="M910 387H936C941 387 944 392 945 398H910Z"/>
<path fill="{c["collar"]}" d="M902 381H919L917 389H900Z"/>
<path fill="{c["lid"]}" d="M1008 270H1068C1078 270 1084 278 1086 287H990C992 278 998 270 1008 270Z"/>
<rect x="991" y="287" width="95" height="5" rx="2" fill="{c["band"]}"/>
<rect x="993" y="292" width="91" height="88" fill="{c["body"]}"/>
<rect x="1052" y="292" width="32" height="88" fill="{c["panel"]}"/>
<rect x="999" y="324" width="34" height="18" rx="2" fill="{c["label"]}"/>
<rect x="1004" y="328" width="18" height="10" rx="1.5" fill="{c["label2"]}"/>
<rect x="993" y="359" width="91" height="2.6" fill="{c["stripe"]}"/>
<rect x="993" y="366" width="91" height="2.6" fill="{c["stripe"]}"/>
<rect x="988" y="379" width="101" height="6" rx="3" fill="{c["base"]}"/>
<circle cx="1004" cy="392" r="6.5" fill="{c["base"]}"/>
<circle cx="1073" cy="392" r="6.5" fill="{c["base"]}"/>
</g>
</svg>
"""


def render_png(svg_path, png_path, w, h):
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    html = os.path.join(GEN, "_render.html")
    with open(html, "w", encoding="utf-8") as fh:
        fh.write(f'<html><body style="margin:0;background:transparent"><img src="file:///{svg_path.replace(os.sep, "/")}" style="width:{w}px;height:{h}px;display:block"></body></html>')
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--default-background-color=00000000", f"--window-size={w},{h}",
                    f"--screenshot={png_path}", "file:///" + html.replace(os.sep, "/")],
                   check=True, capture_output=True)


if __name__ == "__main__":
    files = {
        "logo.svg": svg("light"),
        "logo-light.svg": svg("dark"),
        "logo-header.svg": svg("light", tagline=False),
        "logo-header-light.svg": svg("dark", tagline=False),
    }
    for fn, body in files.items():
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(body)
    os.makedirs(GEN, exist_ok=True)
    render_png(os.path.join(OUT, "logo.svg"), os.path.join(GEN, "logo.png"), 1188 * 2, 372 * 2)
    render_png(os.path.join(OUT, "logo-light.svg"), os.path.join(GEN, "logo-light.png"), 1188 * 2, 372 * 2)
    print("logo built")
