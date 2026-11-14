"""Generate the animated Azazel Labs garden banner (dark + light)."""
import math
import random
from textpath import text_path
import goat as G

W, H = 1280, 460
GROUND = 392

PALETTES = {
    "dark": dict(
        bg1="#0a130f", bg2="#122519", glow="#2b6a45", glow_op=0.35,
        text="#f3ead3", muted="#8fa596", accent="#f6c453",
        soil="#1c130d", soil2="#2b1d13", speck="#46321f", soiltext="#8a7258",
        stem="#5fae6e", leaf="#7fcf86", leaf2="#4f9f62", rib="#2c6a3c",
        coral="#ff7b5c", pink="#ff6394", gold="#f6c453", lilac="#b9a2ff", white="#f6efe0",
        petal_stroke="none", center="#3a2412",
        weed="#a39b55", weed2="#7c7439", root="#c8b38a",
        mote="#ffe28a", sky="#f3ead3", seed="#d9b98a", star="#f3ead3", goatline="#05080a",
    ),
    "light": dict(
        bg1="#f8f2e4", bg2="#efe5cd", glow="#fff9e8", glow_op=0.9,
        text="#1c2a20", muted="#6a7a6d", accent="#c9861a",
        soil="#5a3e29", soil2="#6e4e34", speck="#86664a", soiltext="#d9c3a3",
        stem="#3f8a4f", leaf="#5ea865", leaf2="#3f8a4f", rib="#2a5d35",
        coral="#e85d3c", pink="#da4377", gold="#e3a92c", lilac="#8a6fe0", white="#fffaf0",
        petal_stroke="#d6c7a2", center="#5a3a1c",
        weed="#8c8540", weed2="#6b6530", root="#8f6f4a",
        mote="#e3a92c", sky="#f0ad3a", seed="#8a6a46", star="#c9b896", goatline="#4a3b30",
    ),
}

rng = random.Random(7)


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d
                 for a, b, c, d in zip(p0, p1, p2, p3))


def bez_angle(p0, p1, p2, p3, t):
    u = 1 - t
    dx = 3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0])
    dy = 3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1])
    return math.degrees(math.atan2(dy, dx))


def leaf_d(L, w):
    return (f"M0 0C{w*.95:.1f} {-L*.22:.1f} {w*.75:.1f} {-L*.78:.1f} 0 {-L:.1f}"
            f"C{-w*.75:.1f} {-L*.78:.1f} {-w*.95:.1f} {-L*.22:.1f} 0 0Z")


class Plant:
    def __init__(self, P, x, h, delay, lean=0.0, sway_dur=None):
        self.P, self.x, self.h, self.delay, self.lean = P, x, h, delay, lean
        self.sway_dur = sway_dur or rng.uniform(5.5, 8)
        self.parts = []
        dx = lean * h
        self.c = ((0, 0), (dx * 0.1, -h * 0.35), (dx * 0.6, -h * 0.75), (dx, -h))

    def stem(self, width=3.2, color=None, dur=1.1):
        c = self.c
        d = f"M0 0C{c[1][0]:.1f} {c[1][1]:.1f} {c[2][0]:.1f} {c[2][1]:.1f} {c[3][0]:.1f} {c[3][1]:.1f}"
        self.parts.append(
            f'<path class="grow" pathLength="1" d="{d}" fill="none" stroke="{color or self.P["stem"]}" '
            f'stroke-width="{width}" stroke-linecap="round" style="animation-delay:{self.delay:.2f}s;animation-duration:{dur}s"/>')
        self.stem_dur = dur

    def at(self, t):
        return bez(*self.c, t), bez_angle(*self.c, t)

    def leaf(self, t, side, L, w, color=None, extra_delay=None):
        (x, y), ang = self.at(t)
        rot = ang + 90 + side * rng.uniform(48, 64)
        dl = self.delay + self.stem_dur * t + (extra_delay or 0.05)
        P = self.P
        self.parts.append(
            f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f})">'
            f'<g class="leaf" style="animation-delay:{dl:.2f}s">'
            f'<path d="{leaf_d(L, w)}" fill="{color or rng.choice([P["leaf"], P["leaf2"]])}"/>'
            f'<path d="M0 -1L0 {-L*.85:.1f}" stroke="{P["rib"]}" stroke-width="1.1" stroke-linecap="round" opacity=".55"/>'
            f'</g></g>')

    def top(self, inner, extra=0.0, cls="bloom"):
        (x, y), ang = self.at(1)
        dl = self.delay + self.stem_dur * 0.92 + extra
        self.parts.append(
            f'<g transform="translate({x:.1f} {y:.1f})"><g class="{cls}" style="animation-delay:{dl:.2f}s">{inner}</g></g>')
        return dl

    def svg(self):
        return (f'<g transform="translate({self.x} {GROUND})"><g class="sway" '
                f'style="animation-duration:{self.sway_dur:.1f}s;animation-delay:-{rng.uniform(0,4):.1f}s">'
                + "".join(self.parts) + "</g></g>")


def daisy(P, r, n, color, center_r):
    petals = []
    for i in range(n):
        a = 360 / n * i
        petals.append(f'<ellipse cx="0" cy="{-r*.55:.1f}" rx="{r*.2:.1f}" ry="{r*.5:.1f}" '
                      f'transform="rotate({a:.1f})" fill="{color}" stroke="{P["petal_stroke"]}" stroke-width="1"/>')
    return "".join(petals) + f'<circle r="{center_r}" fill="{P["gold"] if color != P["gold"] else P["center"]}"/>'


def coneflower(P, r, color):
    petals = []
    for i in range(11):
        a = -90 + (i - 5) * 17
        petals.append(f'<path d="M0 0Q{r*.25:.1f} {r*.35:.1f} 0 {r:.1f}Q{-r*.25:.1f} {r*.35:.1f} 0 0Z" '
                      f'transform="rotate({a + 90 + 180:.1f})" fill="{color}"/>')
    # droop the petals downward around a raised cone
    out = []
    for i in range(12):
        a = 200 + i * (140 / 11)
        out.append(f'<path d="M0 0Q{r*.28:.1f} {-r*.4:.1f} 0 {-r:.1f}Q{-r*.28:.1f} {-r*.4:.1f} 0 0Z" '
                   f'transform="rotate({a - 270:.1f}) translate(0 2)" fill="{color}" opacity=".95"/>')
    return "".join(out) + (f'<ellipse cx="0" cy="-4" rx="{r*.42:.1f}" ry="{r*.5:.1f}" fill="{P["center"]}"/>'
                           f'<ellipse cx="-3" cy="-8" rx="{r*.14:.1f}" ry="{r*.18:.1f}" fill="{P["gold"]}" opacity=".5"/>')


def tulip(P, s, color):
    return (f'<path d="M0 4C{-s*.75:.1f} 2 {-s*.8:.1f} {-s*.9:.1f} {-s*.55:.1f} {-s*1.25:.1f}'
            f'L{-s*.25:.1f} {-s*.85:.1f}L0 {-s*1.35:.1f}L{s*.25:.1f} {-s*.85:.1f}L{s*.55:.1f} {-s*1.25:.1f}'
            f'C{s*.8:.1f} {-s*.9:.1f} {s*.75:.1f} 2 0 4Z" fill="{color}"/>'
            f'<path d="M0 2C{-s*.2:.1f} {-s*.4:.1f} {-s*.1:.1f} {-s*.9:.1f} 0 {-s*1.2:.1f}" stroke="#000" stroke-opacity=".15" fill="none" stroke-width="2"/>')


def sunflower(P, r):
    petals = []
    for ring, (rr, op) in enumerate([(r, 1), (r * .85, .85)]):
        for i in range(16):
            a = 360 / 16 * i + ring * 11
            petals.append(f'<ellipse cx="0" cy="{-rr*.62:.1f}" rx="{rr*.15:.1f}" ry="{rr*.42:.1f}" '
                          f'transform="rotate({a:.1f})" fill="{P["gold"]}" opacity="{op}"/>')
    seeds = []
    for k in range(40):
        a = k * 137.5
        rad = r * .3 * math.sqrt(k / 40)
        seeds.append(f'<circle cx="{rad*math.cos(math.radians(a)):.1f}" cy="{rad*math.sin(math.radians(a)):.1f}" r="1.3" fill="{P["gold"]}" opacity=".55"/>')
    return "".join(petals) + f'<circle r="{r*.36:.1f}" fill="{P["center"]}"/>' + "".join(seeds)


def make(P):
    plants = []
    S = P

    def grass(x, delay, n=4, h=26):
        p = Plant(S, x, h, delay)
        for i in range(n):
            bx = (i - n / 2) * 3
            tip = bx + rng.uniform(-10, 10)
            hh = h * rng.uniform(.6, 1.1)
            d = f"M{bx:.1f} 0Q{bx + (tip-bx)*.2:.1f} {-hh*.6:.1f} {tip:.1f} {-hh:.1f}"
            p.parts.append(f'<path class="grow" pathLength="1" d="{d}" fill="none" stroke="{rng.choice([S["leaf"], S["leaf2"]])}" '
                           f'stroke-width="2.2" stroke-linecap="round" style="animation-delay:{delay + i*.08:.2f}s;animation-duration:.7s"/>')
        plants.append(p)

    def seedling(x, delay, h=20):
        p = Plant(S, x, h, delay, lean=rng.uniform(-.15, .15))
        p.stem(width=2.4, dur=.6)
        (tx, ty), ang = p.at(1)
        for side in (-1, 1):
            p.parts.append(
                f'<g transform="translate({tx:.1f} {ty:.1f}) rotate({side*62})"><g class="leaf" style="animation-delay:{delay+.5:.2f}s">'
                f'<path d="{leaf_d(15, 9)}" fill="{S["leaf"]}"/></g></g>')
        plants.append(p)

    def lavender(x, delay, h):
        p = Plant(S, x, h, delay, lean=-.08)
        p.stem(width=2.6)
        for t, side in [(.18, 1), (.3, -1), (.45, 1)]:
            p.leaf(t, side, 26, 6)
        for k in range(11):
            t = .58 + k * .04
            (bx, by), _ = p.at(t)
            dl = delay + 1.1 * t + .1
            sc = 1 - k * .05
            p.parts.append(
                f'<g transform="translate({bx:.1f} {by:.1f}) scale({sc:.2f})"><g class="bloom" style="animation-delay:{dl:.2f}s">'
                f'<ellipse cx="-4.2" cy="1" rx="2.6" ry="3.6" transform="rotate(-28 -4.2 1)" fill="{S["lilac"]}"/>'
                f'<ellipse cx="4.2" cy="-1" rx="2.6" ry="3.6" transform="rotate(28 4.2 -1)" fill="{S["lilac"]}" opacity=".8"/></g></g>')
        (tx, ty), _ = p.at(1)
        p.parts.append(f'<g transform="translate({tx:.1f} {ty:.1f})"><g class="bloom" style="animation-delay:{delay+1.25:.2f}s">'
                       f'<ellipse cx="0" cy="-3" rx="2.4" ry="3.8" fill="{S["lilac"]}"/></g></g>')
        plants.append(p)

    def flower(x, delay, h, kind, color=None, lean=0.0, size=22):
        p = Plant(S, x, h, delay, lean=lean)
        p.stem(width=3.4 if h > 180 else 2.8)
        n = 3 if h > 160 else 2
        for i in range(n):
            p.leaf(.2 + i * .22, 1 if i % 2 == 0 else -1, 34 - i * 4, 11 - i)
        if kind == "daisy":
            p.top(daisy(S, size, 12, color, size * .28))
        elif kind == "cone":
            p.top(coneflower(S, size, color))
        elif kind == "tulip":
            p.top(tulip(S, size, color))
        elif kind == "sun":
            p.top(sunflower(S, size))
        elif kind == "berries":
            dots = "".join(f'<circle cx="{bx}" cy="{by}" r="{r}" fill="{color}" opacity="{o}"/>'
                           for bx, by, r, o in [(-8, -2, 6, .9), (6, -4, 7, 1), (-1, -13, 6.5, .95), (10, -15, 5, .8), (-10, -15, 4.5, .8), (2, -24, 5, .9)])
            p.top(dots)
        plants.append(p)

    def fern(x, delay, h, lean=.25):
        p = Plant(S, x, h, delay, lean=lean)
        p.stem(width=2.4, color=S["leaf2"], dur=1.3)
        k = 9
        for i in range(k):
            t = .18 + i * (.8 / k)
            L = 30 * (1 - t) + 6
            p.leaf(t, 1, L, L * .32, color=S["leaf"], extra_delay=.02)
            p.leaf(t + .02, -1, L, L * .32, color=S["leaf2"], extra_delay=.04)
        plants.append(p)

    # ── left bed: seedlings and grass under the title ─────────────────────
    for x, d in [(64, .5), (180, .8), (330, 1.0), (470, 1.2)]:
        grass(x, d, n=rng.choice([3, 4]), h=rng.uniform(16, 26))
    for x, d in [(118, .9), (256, 1.1), (398, 1.3), (536, 1.5)]:
        seedling(x, d, h=rng.uniform(14, 22))

    # ── right bed: the tended garden ─────────────────────────────────────
    lavender(758, 1.0, 150)
    flower(800, 1.3, 205, "daisy", S["white"], lean=-.05, size=24)
    fern(846, 1.1, 168, lean=.3)
    seedling(878, 2.0, 24)
    flower(956, 1.5, 248, "cone", S["coral"], lean=.04, size=30)
    flower(1012, 1.85, 138, "tulip", S["pink"], lean=-.06, size=22)
    flower(1066, 1.6, 262, "sun", lean=-.03, size=34)
    flower(1124, 2.1, 176, "berries", S["lilac"], lean=.08)
    fern(1172, 2.3, 128, lean=-.25)
    flower(1214, 2.4, 108, "daisy", S["coral"], lean=.05, size=16)
    grass(1250, 1.2, 4, 28)
    return plants


def weed(P, x, appear=2.6, pluck=5.15):
    """A dandelion-ish weed that sprouts, then gets eaten by the goat."""
    leaves = []
    for i, (ang, L) in enumerate([(-78, 44), (-46, 52), (-14, 40), (16, 46), (48, 54), (78, 42)]):
        teeth = []
        n = 8
        for k in range(n + 1):
            t = k / n
            teeth.append(((4.5 * (1 - t) + 1.5) * (1.9 if k % 2 else 1), -L * t + (3 if k % 2 else 0)))
        right = " ".join(f"L{a:.1f} {b:.1f}" for a, b in teeth)
        left = " ".join(f"L{-a*.8:.1f} {b:.1f}" for a, b in reversed(teeth))
        d = f"M0 0{right}{left}Z"
        leaves.append(
            f'<g transform="rotate({ang})"><g class="leaf" style="animation-delay:{appear + i*.12:.2f}s">'
            f'<path d="{d}" fill="{P["weed"] if i % 2 else P["weed2"]}"/></g></g>')
    roots = (f'<g stroke="{P["root"]}" stroke-width="1.6" fill="none" stroke-linecap="round">'
             f'<path d="M0 0C1 14 -3 26 -1 44"/><path d="M0 6C-6 14 -12 18 -16 30"/>'
             f'<path d="M0 10C6 18 12 22 13 34"/><path d="M-1 22C-5 28 -4 34 -8 40"/></g>')
    head = (f'<g transform="translate(2 -62)"><g class="bloom" style="animation-delay:{appear + .6:.2f}s">'
            f'<path d="M0 62C-1 40 1 20 0 0" stroke="{P["weed2"]}" stroke-width="2" fill="none"/>'
            + "".join(f'<line x1="0" y1="0" x2="{9*math.cos(math.radians(a)):.1f}" y2="{9*math.sin(math.radians(a)):.1f}" '
                      f'stroke="{P["text"]}" stroke-opacity=".55" stroke-width="1"/>' for a in range(0, 360, 24))
            + f'<circle r="2.4" fill="{P["weed2"]}"/></g></g>')
    dirt = "".join(
        f'<circle class="dirt" r="{rng.uniform(1.5, 3):.1f}" fill="{P["soil2"]}" '
        f'style="--dx:{rng.uniform(-40, 40):.0f}px;--dy:{rng.uniform(-38, -12):.0f}px;animation-delay:{pluck + .05:.2f}s"/>'
        for _ in range(12))
    return (f'<g transform="translate({x} {GROUND})">'
            f'<g class="eaten" style="animation-delay:{pluck}s">{"".join(leaves)}{head}</g></g>', "")


def weed_sprig(P):
    """A torn-off bit of the weed, hanging out of the goat's mouth."""
    return (f'<path d="M0 0L-7 3L-12 0L-18 5L-24 2L-30 8L-36 6L-31 12L-24 10L-18 14L-11 9L-5 10Z" fill="{P["weed"]}"/>'
            f'<path d="M0 2L-6 8L-5 14L-11 18L-10 24L-15 30L-8 28L-4 22L-1 16L2 9Z" fill="{P["weed2"]}"/>')


def goat(P, x, enter=3.0, walk=1.6, dip=4.7):
    """The logo goat: walks in from the right, grazes the weed, and chews."""
    line = P["goatline"]
    C = G.CREAM
    S = 0.24
    hx, hy = -46, -104          # head anchor (between the eyes), relative to the goat's feet
    legs = ""
    for i, lx in enumerate([-30, -19, 20, 31]):
        cls = "legA" if i in (0, 3) else "legB"
        shade = "" if i in (0, 2) else ' opacity=".82"'
        legs += (f'<g transform="translate({lx} -38)"><g class="{cls}" style="animation-delay:{enter}s">'
                 f'<path d="M-4.5 0H4.5V31H-4.5Z" fill="{C}" stroke="{line}" stroke-width="2.4" stroke-linejoin="round"{shade}/>'
                 f'<path d="M-5 30H5V38H-5Z" fill="{G.INK}"/></g></g>')
    body = (f'<path d="M-40 -66C-40 -80 -20 -78 0 -77C24 -76 44 -80 47 -62C50 -46 40 -32 18 -31H-18C-36 -32 -42 -48 -40 -66Z" '
            f'fill="{C}" stroke="{line}" stroke-width="2.6"/>'
            f'<path d="M-22 -36C-6 -32 10 -32 26 -36" fill="none" stroke="{line}" stroke-opacity=".18" stroke-width="5" stroke-linecap="round"/>'
            # tail
            f'<path d="M44 -70C52 -78 56 -86 52 -92C60 -86 58 -74 48 -64Z" fill="{C}" stroke="{line}" stroke-width="2.2" stroke-linejoin="round"/>'
            # neck
            f'<path d="M-40 -60C-46 -70 -52 -82 -56 -94L-34 -96C-32 -84 -28 -76 -22 -70Z" fill="{C}" stroke="{line}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<path d="M-38 -62C-30 -66 -26 -70 -24 -73" stroke="{C}" stroke-width="6"/>')
    sprig = (f'<g transform="translate(222 342) scale({1/S:.3f})"><g class="sprig" style="animation-delay:{dip + .55:.2f}s">'
             f'<g class="chew" style="animation-delay:{dip + 1.3:.2f}s">{weed_sprig(P)}</g></g></g>')
    head = (f'<g transform="translate({hx} {hy})"><g class="graze" style="animation-delay:{dip}s">'
            f'<g transform="scale({S}) translate(-232 -268)">{G.head(line=line, line_w=9)}{sprig}</g></g></g>')
    crumbs = "".join(
        f'<path class="crumb" d="M0 0l3 -2l2 3l-3 2z" fill="{P["weed"]}" transform="translate({hx - 6 + dx} {hy + 20})" '
        f'style="--cy:{cy}px;animation-delay:{dip + 1.4 + k*.5:.2f}s"/>'
        for k, (dx, cy) in enumerate([(-2, 70), (4, 64), (-6, 72)]))
    return (f'<g transform="translate({x} {GROUND})"><g class="walk" style="animation-delay:{enter}s;animation-duration:{walk}s">'
            f'<g class="trot" style="animation-delay:{enter}s">{legs}{body}{head}</g>{crumbs}</g></g>')


def soil(P):
    pts = []
    for i in range(0, W + 41, 40):
        pts.append((i, GROUND + rng.uniform(-3, 3)))
    d = f"M0 {H}L0 {GROUND}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d += f"Q{x0 + 20} {y0 + rng.uniform(-3, 3):.1f} {x1} {y1:.1f}"
    d += f"L{W} {H}Z"
    specks = "".join(
        f'<ellipse cx="{rng.uniform(0, W):.0f}" cy="{rng.uniform(GROUND + 10, H - 4):.0f}" rx="{rng.uniform(1, 3.4):.1f}" '
        f'ry="{rng.uniform(.8, 2):.1f}" fill="{rng.choice([P["speck"], P["soil2"]])}"/>' for _ in range(170))
    return f'<path d="{d}" fill="url(#soilg)"/>{specks}'


def label(P, text, x, y, size=12.5, color=None, delay=0.0, anchor="start", tracking=0.06, font="mono", var=None):
    d, w = text_path(text, font, size, x, y, var=var or {"wght": 500}, tracking=tracking, anchor=anchor)
    return f'<path class="rise" d="{d}" fill="{color or P["muted"]}" style="animation-delay:{delay}s"/>', w


def build(theme):
    global rng
    rng = random.Random(11)
    P = PALETTES[theme]
    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
               f'aria-label="Azazel Labs. Software, grown, not manufactured. A small garden grows; a weed sprouts, and the Azazel goat trots in and eats it.">')
    out.append("""<style>
.grow{stroke-dasharray:1;stroke-dashoffset:0;animation:grow 1.1s cubic-bezier(.3,.7,.4,1) both}
@keyframes grow{from{stroke-dashoffset:1}}
.leaf{animation:unfurl .75s cubic-bezier(.3,1.5,.5,1) both}
@keyframes unfurl{from{transform:scale(0)}}
.bloom{animation:bloom .9s cubic-bezier(.3,1.5,.5,1) both}
@keyframes bloom{from{transform:scale(0) rotate(-50deg)}}
.sway{animation:sway 6s ease-in-out infinite alternate}
@keyframes sway{from{transform:rotate(-1.4deg)}to{transform:rotate(1.4deg)}}
.seed{opacity:0;animation:drop .7s cubic-bezier(.5,0,.9,.6) both}
@keyframes drop{0%{transform:translateY(-150px);opacity:0}20%{opacity:1}85%{transform:translateY(0);opacity:1}100%{transform:translateY(5px);opacity:0}}
.eaten{opacity:0;animation:eaten .5s cubic-bezier(.5,0,.8,.4) both}
@keyframes eaten{0%{transform:none;opacity:1}100%{transform:translate(-4px,-30px) scale(.1,.2);opacity:0}}
.walk{animation:walk 1.6s cubic-bezier(.25,.6,.35,1) both}
@keyframes walk{from{transform:translateX(720px)}}
.legA{animation:step .4s ease-in-out 4 both}
.legB{animation:step2 .4s ease-in-out 4 both}
@keyframes step{0%,100%{transform:none}25%{transform:rotate(22deg)}75%{transform:rotate(-22deg)}}
@keyframes step2{0%,100%{transform:none}25%{transform:rotate(-22deg)}75%{transform:rotate(22deg)}}
.trot{animation:trot .2s ease-in-out 8 both}
@keyframes trot{50%{transform:translateY(-2.5px)}}
.graze{animation:graze 1.4s ease-in-out both}
@keyframes graze{0%,100%{transform:none}28%,62%{transform:translate(-4px,30px) rotate(-10deg)}}
.sprig{animation:sprig .3s cubic-bezier(.3,1.6,.5,1) both}
@keyframes sprig{from{transform:scale(0)}}
.chew{animation:chew 2.4s ease-in-out infinite}
@keyframes chew{0%,40%,100%{transform:none}8%{transform:rotate(-12deg) translateY(3px)}16%{transform:rotate(6deg)}24%{transform:rotate(-9deg) translateY(2px)}32%{transform:rotate(4deg)}}
.crumb{opacity:0;animation:crumb .9s ease-in both}
@keyframes crumb{0%{opacity:1;transform:none}100%{opacity:0;transform:translate(-6px,var(--cy)) rotate(160deg)}}
.blink{animation:blink 5s infinite;transform-origin:232px 268px}
@keyframes blink{0%,94%,100%{transform:none}97%{transform:scaleY(.1)}}
.rise{animation:rise 1s cubic-bezier(.2,.7,.3,1) both}
@keyframes rise{from{opacity:0;transform:translateY(10px)}}
.mote{animation:mote 9s ease-in-out infinite}
@keyframes mote{0%,100%{transform:translate(0,0);opacity:.0}20%{opacity:.9}50%{transform:translate(var(--mx),var(--my));opacity:.35}80%{opacity:.85}}
.twinkle{animation:twinkle 4s ease-in-out infinite alternate}
@keyframes twinkle{from{opacity:.15}to{opacity:.7}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>""")
    out.append(f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P['bg1']}"/><stop offset="1" stop-color="{P['bg2']}"/></linearGradient>
<radialGradient id="glow" cx="0.74" cy="0.78" r="0.55"><stop offset="0" stop-color="{P['glow']}" stop-opacity="{P['glow_op']}"/><stop offset="1" stop-color="{P['glow']}" stop-opacity="0"/></radialGradient>
<linearGradient id="soilg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P['soil2']}"/><stop offset=".35" stop-color="{P['soil']}"/></linearGradient>
<radialGradient id="sky" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{P['sky']}" stop-opacity=".35"/><stop offset="1" stop-color="{P['sky']}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{P['muted']}" stroke-opacity="{'.10' if theme=='light' else '.0'}" stroke-width="1"/></pattern>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>""")
    out.append('<g clip-path="url(#frame)">')
    out.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>'
               f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')
    # stars (dark) / nothing (light)
    if theme == "dark":
        for _ in range(46):
            x, y = rng.uniform(20, W - 20), rng.uniform(16, 250)
            if x < 700 and 90 < y < 320:
                continue
            out.append(f'<circle class="twinkle" cx="{x:.0f}" cy="{y:.0f}" r="{rng.uniform(.6, 1.5):.1f}" fill="{P["star"]}" '
                       f'style="animation-delay:-{rng.uniform(0, 4):.1f}s;animation-duration:{rng.uniform(2.5, 5):.1f}s"/>')
        # crescent moon
        out.append(f'<circle cx="1166" cy="82" r="70" fill="url(#sky)"/>'
                   f'<path d="M1180 54a30 30 0 1 0 14 52a26 26 0 1 1 -14 -52z" fill="{P["sky"]}" opacity=".92"/>')
    else:
        out.append(f'<circle cx="1166" cy="84" r="86" fill="url(#sky)"/><circle cx="1166" cy="84" r="28" fill="{P["sky"]}"/>'
                   + "".join(f'<line x1="1166" y1="{84-40}" x2="1166" y2="{84-52}" stroke="{P["sky"]}" stroke-width="3" stroke-linecap="round" transform="rotate({a} 1166 84)"/>'
                             for a in range(0, 360, 30)))

    # ── words ──────────────────────────────────────────────────────────────
    lab, _ = label(P, "AZAZEL LABS  ·  FIELD NOTES  ·  PLATE Nº 1", 72, 70, size=12.5, delay=.1, tracking=.16)
    out.append(lab)
    d, tw = text_path("Azazel Labs", "serif", 112, 66, 192, var={"wght": 620, "opsz": 144, "SOFT": 100, "WONK": 1})
    out.append(f'<path class="rise" d="{d}" fill="{P["text"]}" style="animation-delay:.2s"/>')
    d, _ = text_path("Software, grown — not manufactured.", "serif-italic", 31, 72, 246,
                     var={"wght": 380, "opsz": 36, "SOFT": 100, "WONK": 1})
    out.append(f'<path class="rise" d="{d}" fill="{P["text"]}" opacity=".88" style="animation-delay:.55s"/>')
    # stage words, each lighting up in turn
    x = 72
    stages = [("PLANT", 1.0), ("TEND", 2.2), ("WEED", 4.9), ("HARVEST", 6.3)]
    for i, (wd, dl) in enumerate(stages):
        p, w = label(P, wd, x, 300, size=15, color=P["accent"], delay=dl, tracking=.22, var={"wght": 650})
        out.append(p)
        x += w + 14
        if i < len(stages) - 1:
            p, w = label(P, "→", x, 300, size=15, color=P["muted"], delay=dl + .3, tracking=0)
            out.append(p)
            x += w + 14
    # ── garden ─────────────────────────────────────────────────────────────
    plants = make(P)
    # seeds dropping where the right-bed plants will grow
    for pl in plants:
        if pl.x > 680 and pl.h > 60:
            out.append(f'<ellipse class="seed" cx="{pl.x}" cy="{GROUND - 3}" rx="3.2" ry="4.4" fill="{P["seed"]}" '
                       f'style="animation-delay:{max(pl.delay - .75, .05):.2f}s"/>')
    weed_svg, _ = weed(P, 634)
    out.extend(pl.svg() for pl in plants)
    out.append(goat(P, 688))
    out.append(weed_svg)
    out.append(soil(P))
    # field-note annotations engraved in the soil
    for text, x, dl in [("↑ sown", 238, 1.6), ("↑ weed, eaten", 616, 6.2), ("↑ tended", 1054, 3.4)]:
        p, _ = label(P, text, x, 428, size=12, color=P["soiltext"], delay=dl, tracking=.05)
        out.append(p)
    # fireflies / pollen
    for _ in range(16):
        mx, my = rng.uniform(-30, 30), rng.uniform(-40, -10)
        out.append(f'<circle class="mote" cx="{rng.uniform(660, 1260):.0f}" cy="{rng.uniform(150, 370):.0f}" r="{rng.uniform(1.4, 2.6):.1f}" '
                   f'fill="{P["mote"]}" style="--mx:{mx:.0f}px;--my:{my:.0f}px;animation-delay:{rng.uniform(3, 10):.1f}s;'
                   f'animation-duration:{rng.uniform(7, 12):.1f}s"/>')
    out.append("</g></svg>")
    return "\n".join(out)


if __name__ == "__main__":
    import os
    os.makedirs("out", exist_ok=True)
    for t in ("dark", "light"):
        with open(f"out/banner-{t}.svg", "w") as f:
            f.write(build(t))
        print(t, os.path.getsize(f"out/banner-{t}.svg"))
