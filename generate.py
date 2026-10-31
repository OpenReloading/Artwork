#!/usr/bin/env python3
"""Builds the OpenReloading, AutoLever, Ballistics and BuildGuide marks.

Needs python3 with fontTools (pip install fonttools), the Fira Sans font (fontconfig), rsvg-convert and ImageMagick 7.
Usage: python3 generate.py            writes openreloading/, autolever/, ballistics/, buildguide/
       python3 generate.py tooth      variant with the gap cut through the end teeth, written to .build/variant-tooth/
"""
import math, pathlib, subprocess, sys
STYLE = sys.argv[1] if len(sys.argv) > 1 else "ring"
HERE = pathlib.Path(__file__).resolve().parent
BUILD = HERE / ".build"; BUILD.mkdir(exist_ok=True)
DEST = {n: HERE / n for n in ("openreloading", "autolever", "ballistics", "buildguide")}
if STYLE != "ring":
    DEST = {k: BUILD / f"variant-{STYLE}" / k for k in DEST}

CX, CY = 149.02, 625.97          # centre of the cog, in the coordinates of the hand-made organisation mark the case head comes from
CASE_HEAD = "M151.15 672.38C158.35 671.88 165.15 670.34 171.45 666.71C197.81 651.48 204.15 617.09 183.58 594.48C178.56 588.96 172.4 585.43 165.61 582.62C160 580.29 153.21 579.58 147.18 579.86C140.64 580.16 134.48 581.94 128.63 584.79C91.4 602.95 94.74 657.2 134.3 670.07C139.68 671.82 145.47 672.76 151.15 672.38ZM150 647.75C144.94 647.91 140.02 646.38 136.11 643.1C121.64 630.94 129.32 607.01 148.4 606.14C153.36 605.91 158.36 607.51 162.19 610.67C176.81 622.72 169.09 647.16 150 647.75ZM150.58 643.25C167.48 641.56 171.28 618.11 155.29 611.75C152.96 610.82 150.39 610.08 147.85 610.38C132.37 612.2 126.96 633.17 140.92 641.11C143.84 642.77 147.21 643.59 150.58 643.25Z"

R_IN, R_OUT, R_TIP = 55.4, 70.2, 84.5        # measured on the original cog
CUT_L, CUT_R = 6.5, 68.5                      # "tooth" style: radial cut faces through the end teeth, symmetric about 37.5 deg
BASE_HW, TIP_HW = 11.5, 8.0                   # tooth half-widths in degrees at the ring and at the tip
RHO = 2.6                                     # corner radius: outline is inset by RHO and stroked RHO*2 with round joins
TEETH = [77.5 + 40 * k for k in range(8)]     # 9 positions on a 40 deg pitch, the one at 37.5 (gap centre) left out
def P(r, a):
    t = math.radians(a - 90); return (CX + r * math.cos(t), CY + r * math.sin(t))
def cog(col):
    """one closed outline of the open cog; corners rounded by stroking the inset outline with round joins"""
    cl, cr = (CUT_L, CUT_R) if STYLE == "tooth" else (16.5, 58.5)   # "ring": cut through the plain ring past whole teeth
    ri, ro, rt = R_IN + RHO, R_OUT - RHO, R_TIP - RHO
    da = lambda r: math.degrees(RHO / r)
    def seg(r, a_from, a_to):                       # sampled arc at radius r, from a_from down to a_to
        n = max(2, int(abs(a_from - a_to) / 2) + 1)
        return [P(r, a_from + (a_to - a_from) * k / n) for k in range(n + 1)]
    pts = seg(ri, cr + da(ri), cl + 360 - da(ri))   # inner edge, clockwise
    outer = [(c - BASE_HW, c + BASE_HW, c - TIP_HW, c + TIP_HW) for c in TEETH]
    if STYLE == "tooth":
        bl, br, tl, tr = outer[0]; outer[0] = (cr, br, cr, tr)
        bl, br, tl, tr = outer[-1]; outer[-1] = (bl, cl + 360, tl, cl + 360)
    a = cl + 360
    for bl, br, tl, tr in reversed(outer):
        if br < a - 1e-6: pts += seg(ro, a - da(ro), br + da(ro))
        pts.append(P(rt, tr - da(rt))); pts.append(P(rt, tl + da(rt)))
        a = bl
    if a > cr + 1e-6: pts += seg(ro, a - da(ro), cr + da(ro))
    d = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"
    return f'<path d="{d}" stroke="{col}" stroke-width="{2*RHO}" stroke-linejoin="round"/>'
def case_head():
    # the original case head, 5 % smaller so a hairline of background separates it from the ring as in the original
    return f'<path fill-rule="evenodd" transform="translate({CX} {CY}) scale(0.95) translate({-CX} {-CY})" d="{CASE_HEAD}"/>'
def circ(cx, cy, r):
    return f"M{cx-r:.2f} {cy:.2f}a{r} {r} 0 1 0 {2*r} 0a{r} {r} 0 1 0 {-2*r} 0"
LEV_ANG, LEV_L = 37.5, 104                    # lever through the gap: hub with pivot hole, bar, knob (sizes from the original lever)
def lever(col):
    bx, by = P(LEV_L, LEV_ANG); sx, sy = P(18, LEV_ANG)
    return (f'<path d="M{sx:.2f} {sy:.2f}L{bx:.2f} {by:.2f}" fill="none" stroke="{col}" stroke-width="21.4" stroke-linecap="round"/>\n'
            f'<path fill-rule="evenodd" d="{circ(CX, CY, 22.7)}{circ(CX, CY, 5)}"/>\n'
            f'<circle cx="{bx:.2f}" cy="{by:.2f}" r="22.6"/>')
def curve(col):
    # pressure curve chart; curve and baseline reach 4 units into the ring on both sides
    y0 = CY + 30; hw = math.sqrt(R_IN**2 - 30**2) + 4
    base = f'<path d="M{CX-hw:.1f} {y0:.1f}H{CX+hw:.1f}" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"/>'
    d = (f"M{CX-hw+2:.1f} {y0:.1f}C{CX-38:.1f} {y0:.1f} {CX-30:.1f} {CY-38:.1f} {CX-14:.1f} {CY-38:.1f}"
         f"C{CX-2:.1f} {CY-38:.1f} {CX+4:.1f} {y0-6:.1f} {CX+hw-2:.1f} {y0:.1f}")
    return base + "\n" + f'<path d="{d}" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
def page(col):
    # document page inside the ring with a folded corner and two text lines, outer corners 10.8 clear of the ring
    w, h, f = 23, 31, 14
    x0, y0, x1, y1 = CX - w, CY - h, CX + w, CY + h
    return (f'<path d="M{x0:.2f} {y0:.2f}H{x1-f:.2f}L{x1:.2f} {y0+f:.2f}V{y1:.2f}H{x0:.2f}ZM{x1-f:.2f} {y0:.2f}V{y0+f:.2f}H{x1:.2f}" fill="none" stroke="{col}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>\n'
            f'<path d="M{CX-11:.2f} {CY-4:.2f}H{CX+11:.2f}M{CX-11:.2f} {CY+12:.2f}H{CX+11:.2f}" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round"/>')
def mark(name, col):
    if name == "openreloading": return cog(col) + "\n" + case_head()
    if name == "autolever": return cog(col) + "\n" + lever(col)
    if name == "buildguide": return cog(col) + "\n" + page(col)
    return cog(col) + "\n" + curve(col)
E = 212.3                                     # icon square: the same for all marks, cog centred
def icon(name, col="#000"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{CX-E/2:.2f} {CY-E/2:.2f} {E} {E}" fill="currentColor" color="{col}" role="img" aria-label="{label(name)}">\n'
            f'{mark(name, "currentColor")}\n</svg>\n')
# wordmarks: lettering outlined from a font at build time, first word bold, second regular
FONT = "Fira Sans"
KERN = {"Au": -0.07, "Le": -0.03, "ev": -0.015, "Re": -0.01}      # em, pairs that sit loose without the font's own kerning
def load_font(weight):
    from fontTools.ttLib import TTFont
    path = subprocess.run(["fc-match", "-f", "%{file}", f"{FONT}:{weight}"], capture_output=True, text=True, check=True).stdout
    if FONT.lower().replace(" ", "") not in path.lower().replace(" ", ""): print(f"warning: {FONT} {weight} not installed, fontconfig gave {path}")
    return TTFont(path)
FONTS = {}
def text_path(text, weight, size, x, y):
    """outlined text at baseline (x, y); returns (path d, advance)"""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    f = FONTS.setdefault(weight, load_font(weight)); gs = f.getGlyphSet(); cmap = f.getBestCmap(); hm = f["hmtx"]
    sc = size / f["head"].unitsPerEm; d, px = [], x
    for i, ch in enumerate(text):
        g = cmap[ord(ch)]
        if i: px += KERN.get(text[i - 1] + ch, 0) * size
        pen = SVGPathPen(gs); gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, px, y))); d.append(pen.getCommands())
        px += hm[g][0] * sc
    return " ".join(d), px - x
ORG = "openreloading"
WORDS = {ORG: ("Open", "Reloading"), "autolever": ("Auto", "Lever"), "ballistics": ("Ballistics",), "buildguide": ("Build", "Guide")}   # first word bold, the rest regular
def lines(name):  # (words, size, baseline) per text line; project marks carry the org name small above
    return [(WORDS[name], 43, 78)] if name == ORG else [(WORDS[ORG], 20, 52), (WORDS[name], 43, 100)]
def label(name): return " ".join("".join(w) for w, *_ in lines(name))
def lockup(name, variant):
    col = "#fff" if variant == "dark" else "#000"
    H = 126; sc = H / E                                       # the icon square scaled so the cog is 100 tall
    g = f'<g transform="scale({sc:.4f}) translate({E/2-CX:.2f} {E/2-CY:.2f})">\n{mark(name, col)}\n</g>'
    tx = H + 4; paths = []; W = 0
    for words, size, y in lines(name):
        x = tx
        for i, w in enumerate(words):
            d, adv = text_path(w, "regular" if i else "bold", size, x, y); paths.append(f'<path d="{d}"/>'); x += adv
        W = max(W, x)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W+6:.1f} {H}" fill="currentColor" color="{col}" role="img" aria-label="{label(name)}">\n'
            f'{g}\n{"".join(paths)}\n</svg>\n')

def run(*a): subprocess.run(a, check=True)
for name, out in DEST.items():
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}-icon.svg").write_text(icon(name))
    (out / f"{name}-light.svg").write_text(lockup(name, "light"))
    (out / f"{name}-dark.svg").write_text(lockup(name, "dark"))
    (BUILD / "i.svg").write_text(icon(name, "#fff")); run("rsvg-convert", "-w", "880", "-h", "880", "-o", str(BUILD / "i.png"), str(BUILD / "i.svg"))
    run("magick", "-define", "png:exclude-chunk=date,tIME", str(BUILD / "i.png"), "-background", "black", "-gravity", "center", "-extent", "1024x1024", "-alpha", "remove", str(out / f"{name}-icon-1024.png"))
    for variant, bg in (("light", "white"), ("dark", "black")):   # wordmark on a background, 1280 x 640; the dark one is the GitHub social preview
        run("rsvg-convert", "-w", "1120", "-o", str(BUILD / "w.png"), str(out / f"{name}-{variant}.svg"))
        run("magick", "-define", "png:exclude-chunk=date,tIME", str(BUILD / "w.png"), "-fuzz", "5%", "-trim", "+repage", "-background", bg, "-gravity", "center", "-extent", "1280x640", "-alpha", "remove", str(out / f"{name}-{variant}-1280x640.png"))
print("ok:", ", ".join(str(d.relative_to(HERE)) for d in DEST.values()))
