"""Draft percussion icons as single filled paths on a 1000x1000 canvas.

Builds each icon from simple shapes with shapely and writes one SVG per icon:

    python3 draft-icons.py svg

Hand-drawn icons (pandeiro.svg) are not generated here; don't point this at a
directory you've hand-edited without checking the diff.
"""
import math
import sys
from pathlib import Path

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

G = 44  # negative-space gap width
Q = 48


def ell(cx, cy, rx, ry):
    c = Point(0, 0).buffer(1, quad_segs=Q)
    return affinity.translate(affinity.scale(c, rx, ry, origin=(0, 0)), cx, cy)


def ellpts(cx, cy, rx, ry, a0, a1, n=64):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def rrect(x0, y0, x1, y1, r):
    return box(x0 + r, y0 + r, x1 - r, y1 - r).buffer(r, quad_segs=Q)


def line(pts, w, cap=1):
    return LineString(pts).buffer(w / 2, cap_style=cap, join_style=1, quad_segs=Q)


def U(*gs):
    return unary_union(gs)


def cut(shape, *cutters):
    return shape.difference(unary_union(cutters))


def over(back, front, g=G):
    """Put front on top of back, separated by a gap."""
    return back.difference(front.buffer(g, quad_segs=Q)).union(front)


def rot(g, deg, origin=(500, 500)):
    return affinity.rotate(g, deg, origin=origin)


def polys(g):
    if g.geom_type == "Polygon":
        yield g
    elif hasattr(g, "geoms"):
        for p in g.geoms:
            yield from polys(p)


def to_d(g):
    out = []
    for p in polys(g.simplify(0.35)):
        if p.area < 80:
            continue
        p = orient(p, 1.0)
        for ring in [p.exterior, *p.interiors]:
            c = list(ring.coords)[:-1]
            out.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in c) + "Z")
    return "".join(out)


def svg(g):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">\n'
            f'  <path fill="#000" fill-rule="evenodd" d="{to_d(g)}"/>\n</svg>\n')


# --- shared parts ----------------------------------------------------------

def head_cut(shape, cx, cy, rx, ry):
    """Separate a drumhead ellipse from the shell below it."""
    return cut(shape, ell(cx, cy, rx, ry).exterior.buffer(G / 2, quad_segs=Q))


def front_arc(cx, y, rx, ry, w=G):
    return line(ellpts(cx, y, rx + 40, ry, -5, 185), w, cap=2)


def conga(cx, top, bot, rt, rb, bulge, ry, lugs=True):
    n = 60
    r = lambda t: rt + (rb - rt) * t + bulge * math.sin(math.pi * t ** 0.75)
    y = lambda t: top + (bot - top) * t
    ryb = ry * rb / rt
    right = [(cx + r(i / n), y(i / n)) for i in range(n + 1)]
    left = [(cx - r(i / n), y(i / n)) for i in range(n, -1, -1)]
    shell = U(Polygon(right + ellpts(cx, bot, rb, ryb, 0, 180)[1:-1] + left), ell(cx, top, rt, ry))
    shell = head_cut(shell, cx, top, rt, ry)
    hoop = top + 70
    rh = r(70 / (bot - top))
    shell = cut(shell, front_arc(cx, hoop, rh, ry * rh / rt))
    if lugs:
        for a in (55, 90, 125):
            x = cx + rh * 0.92 * math.cos(math.radians(a))
            yy = hoop + ry * math.sin(math.radians(a)) + G / 2 + 40
            shell = cut(shell, line([(x, yy), (x, yy + 120)], 34))
    return shell


def drum(cx, top, bot, rx, ry, lugs=3, hoop=55):
    shell = U(box(cx - rx, top, cx + rx, bot), ell(cx, bot, rx, ry), ell(cx, top, rx, ry))
    shell = head_cut(shell, cx, top, rx, ry)
    shell = cut(shell, front_arc(cx, top + hoop, rx, ry))
    angles = {2: (60, 120), 3: (45, 90, 135)}.get(lugs, ())
    for a in angles:
        x = cx + rx * math.cos(math.radians(a))
        y0 = top + hoop + ry * math.sin(math.radians(a)) + G / 2
        y1 = bot + ry * math.sin(math.radians(a)) - 30
        if y1 - y0 > 40:
            shell = cut(shell, line([(x, y0 + 30), (x, y1)], 30))
    return shell


def mallet(p0, p1, w=42, ball=62):
    return U(line([p0, p1], w), Point(p1).buffer(ball, quad_segs=Q))


def cymbal(cx, cy, rx, rise, thick, up=True, bell=0.22):
    s = -1 if up else 1
    n = 80
    upper, lower = [], []
    for i in range(n + 1):
        x = -rx + 2 * rx * i / n
        u = abs(x) / rx
        h = rise * (1 - u) ** 1.3
        b = bell * rx
        if abs(x) < b:
            h += rise * 1.2 * math.sqrt(1 - (abs(x) / b) ** 2)
        t = thick * (0.55 + 0.45 * (1 - u))
        upper.append((cx + x, cy + s * h))
        lower.append((cx + x, cy + s * (h - t)))
    return Polygon(upper + lower[::-1]).buffer(6, quad_segs=Q)


# --- icons -----------------------------------------------------------------

def congas():
    back = conga(330, 90, 900, 190, 160, 70, 62)
    front = conga(680, 210, 905, 165, 140, 60, 54)
    return over(back, front)


def quinto():
    return conga(500, 230, 900, 200, 165, 70, 64)


def tumba():
    return conga(500, 110, 890, 290, 245, 100, 84)


def cowbell():
    bell = Polygon([(375, 300), (625, 300), (765, 830), (235, 830)]).buffer(40, quad_segs=Q)
    mouth = ell(500, 830, 265, 70)
    bell = U(bell, mouth)
    bell = cut(bell, line(ellpts(500, 735, 300, 70, 0, 180), G, cap=2))  # rim
    bell = cut(bell, line([(330, 420), (290, 640)], 36))  # sheen
    handle = cut(rrect(400, 120, 600, 300, 50), rrect(455, 175, 545, 300, 10))
    bell = U(bell.difference(box(380, 255, 620, 300 + G / 2)),
             handle.difference(box(0, 300 - G / 2, 1000, 1000)))
    bell = rot(bell, -14, (500, 540))
    stick = line([(910, 150), (730, 390)], 50)
    return over(bell, stick)


def cuica():
    cy, ry = 520, 290
    hx, ox = 240, 720  # head end, open end
    shell = U(box(hx, cy - ry, ox, cy + ry), ell(hx, cy, 95, ry), ell(ox, cy, 110, ry))
    # head end hoop
    shell = cut(shell, line(ellpts(hx + 70, cy, 95, ry + 40, -95, 95), G, cap=2))
    # tension rods along the shell
    for y in (cy - ry * 0.55, cy + ry * 0.55):
        shell = cut(shell, line([(hx + 140, y), (ox - 150, y)], 30))
    # open end: rim and hollow with the stick inside
    shell = cut(shell, ell(ox, cy, 110 - 46, ry - 46))
    stick = U(line([(ox, cy), (ox + 230, cy - 20)], 44), Point(ox, cy).buffer(40))
    return over(shell, stick, 34)


def hihat():
    top = cymbal(500, 250, 420, 70, 70, up=True, bell=0.18)
    bot = cymbal(500, 310, 420, 70, 70, up=False, bell=0.18)
    rod = line([(500, 60), (500, 880)], 40)
    stand = U(line([(500, 650), (220, 920)], 44), line([(500, 650), (780, 920)], 44),
              rrect(466, 580, 534, 720, 16))
    pedal = Polygon([(440, 870), (560, 870), (585, 950), (415, 950)]).buffer(12)
    return U(rod, top, bot, stand, pedal)


def kalimba():
    body = Polygon([(170, 80), (830, 80), (880, 930), (120, 930)]).buffer(70, quad_segs=Q).buffer(-70, quad_segs=Q)
    window = rrect(225, 135, 775, 640, 50)
    g = cut(body, window)
    pitch, w = 104, 60
    tops = [370, 270, 190, 270, 370]
    for i, t in enumerate(tops):
        x = 500 + (i - 2) * pitch
        g = U(g, line([(x, t), (x, 640)], w))
    g = cut(g, line([(250, 560), (750, 560)], 36))  # bridge
    g = cut(g, Point(500, 790).buffer(75, quad_segs=Q))
    return g


def marimba():
    keys = []
    n, x0, x1 = 5, 130, 870
    pitch = (x1 - x0) / n
    for i in range(n):
        cx = x0 + pitch * (i + 0.5)
        keys.append(rrect(cx - 52, 110 + i * 26, cx + 52, 330, 14))
    rail = rrect(60, 350, 940, 410, 10)
    tubes = []
    for i in range(n):
        cx = x0 + pitch * (i + 0.5)
        tubes.append(rrect(cx - 32, 410, cx + 32, 790 - i * 62, 32))
    legs = U(rrect(56, 380, 112, 900, 10), rrect(888, 380, 944, 900, 10),
             Point(84, 912).buffer(36), Point(916, 912).buffer(36), rrect(56, 842, 944, 892, 10))
    g = U(*keys)
    g = U(g, cut(U(rail, *tubes), U(*keys).buffer(36)))
    g = U(g, cut(legs, U(*tubes).buffer(34)), rail)
    return g


def xylophone():
    n = 6
    bars = []
    for i in range(n):
        cx = 150 + i * 140
        h = 300 - i * 32
        bars.append(rrect(cx - 52, 370 - h, cx + 52, 370 + h, 20))
    bars = U(*bars)
    rails = U(line([(60, 200), (940, 270)], 40), line([(60, 540), (940, 470)], 40))
    g = over(rails, bars, 30)
    m1 = mallet((230, 960), (600, 640), 40, 64)
    m2 = mallet((770, 960), (400, 640), 40, 64)
    g = over(g, m1, 36)
    g = over(g, m2, 36)
    return g


def okedo():
    cy, ry = 590, 240
    lx, rx = 230, 770
    shell = Polygon([(lx, cy - ry), (rx, cy - ry), (rx, cy + ry), (lx, cy + ry)])
    shell = U(shell, ell(500, cy - ry, 270, 20), ell(500, cy + ry, 270, 20))
    # rope zigzag between the heads, cinched by a centre belt
    pts = []
    ys = [cy - ry + 40 + k * (2 * ry - 80) / 6 for k in range(7)]
    for k, y in enumerate(ys):
        pts.append((lx + 30 if k % 2 == 0 else rx - 30, y))
    shell = cut(shell, line(pts, 34))
    shell = cut(shell, box(500 - 50 - G, 0, 500 + 50 + G, 1000))
    belt = rrect(450, cy - ry - 25, 550, cy + ry + 25, 20)
    heads = U(ell(lx - 20, cy, 75, ry + 80), ell(rx + 20, cy, 75, ry + 80))
    g = over(U(shell, belt), heads, 34)
    strap = line(ellpts(500, cy - ry - 40, 300, 230, 200, 340), 44, cap=1)
    return over(g, strap, 30)


def timbales():
    left = drum(290, 300, 470, 215, 62, lugs=2, hoop=50)
    right = drum(715, 330, 480, 195, 56, lugs=2, hoop=50)
    drums = U(left, right)
    post = U(rrect(475, 470, 525, 820, 10), line([(290, 560), (715, 560)], 44))
    stand = U(line([(500, 760), (250, 940)], 40), line([(500, 760), (750, 940)], 40), line([(500, 760), (500, 940)], 40))
    g = over(U(post, stand), drums, 36)
    s1 = line([(140, 60), (520, 250)], 34)
    s2 = line([(860, 60), (500, 260)], 34)
    g = over(g, s1, 30)
    g = over(g, s2, 30)
    return g


def timpani():
    cx, cy, rx, ry = 500, 240, 420, 95
    bowl = U(Polygon(ellpts(cx, cy, rx, 470, 0, 180)), ell(cx, cy, rx, ry))
    bowl = head_cut(bowl, cx, cy, rx, ry)
    bowl = cut(bowl, front_arc(cx, cy + 60, rx, ry))
    for a in (60, 90, 120):
        x0 = cx + rx * math.cos(math.radians(a))
        bowl = cut(bowl, line([(x0, cy + 60 + ry * math.sin(math.radians(a)) + 50),
                               (cx + (x0 - cx) * 0.55, 620)], 32))
    base = U(line([(340, 620), (240, 900)], 46), line([(660, 620), (760, 900)], 46),
             Point(240, 915).buffer(42), Point(760, 915).buffer(42),
             rrect(420, 860, 580, 950, 16))
    return over(base, bowl, 36)


ICONS = {
    "congas": congas, "cowbell": cowbell, "cuica": cuica, "hi-hat": hihat,
    "kalimba": kalimba, "marimba": marimba, "okedo": okedo, "quinto": quinto,
    "timbales": timbales, "timpani": timpani, "tumba": tumba, "xylophone": xylophone,
}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in ICONS.items():
        g = fn()
        b = g.bounds
        print(f"{name:10s} bounds {b[0]:.0f},{b[1]:.0f} {b[2]:.0f},{b[3]:.0f}")
        (out / f"{name}.svg").write_text(svg(g))
