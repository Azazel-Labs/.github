"""Plant → Tend → Weed → Harvest strip (dark + light), gently animated."""
import random
from textpath import text_path
from banner import PALETTES, leaf_d

W, H = 1280, 330
R = 92
XS = [170, 490, 810, 1130]
CY = 132

EXTRA = {
    "dark": dict(disc="#12241a", ring="#2c4a36", sky2="#183022", label="#f3ead3", line="#8fa596", vine="#3e7d4f"),
    "light": dict(disc="#fffaf0", ring="#d9cba8", sky2="#f4ecd8", label="#1c2a20", line="#6a7a6d", vine="#9fc49f"),
}


def sprout(P, x, y, h, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0Q2 {-h/2} 0 {-h}" stroke="{P["stem"]}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<g transform="translate(0 {-h}) rotate(-58)"><path d="{leaf_d(18, 10)}" fill="{P["leaf"]}"/></g>'
            f'<g transform="translate(0 {-h}) rotate(58)"><path d="{leaf_d(18, 10)}" fill="{P["leaf2"]}"/></g></g>')


def soil_band(P, y=30):
    rng = random.Random(y)
    specks = "".join(f'<circle cx="{rng.uniform(-R, R):.0f}" cy="{rng.uniform(y + 8, R):.0f}" r="{rng.uniform(1, 2.4):.1f}" fill="{P["speck"]}"/>'
                     for _ in range(26))
    return f'<path d="M{-R-4} {y}Q-40 {y-5} 0 {y}T{R+4} {y}V{R+4}H{-R-4}Z" fill="{P["soil"]}"/>{specks}'


def plant_vignette(P):
    return (soil_band(P)
            + f'<path d="M-58 -52Q-20 -60 -2 32" fill="none" stroke="{P["seed"]}" stroke-width="2" stroke-dasharray="3 6" stroke-linecap="round"/>'
            + f'<path d="M0 54C-2 62 -8 66 -12 74M0 54C3 64 8 68 10 78" stroke="{P["root"]}" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
            + f'<ellipse cx="0" cy="52" rx="7" ry="9" fill="{P["seed"]}"/>'
            + f'<g class="pulse">{sprout(P, 0, 45, 30)}</g>')


def tend_vignette(P, E):
    can = (f'<g transform="translate(-48 -40) scale(.85) rotate(24)">'
           f'<path d="M-26 -18H22L18 22H-22Z" fill="{P["coral"]}"/>'
           f'<path d="M-14 -18C-14 -40 12 -40 12 -18" fill="none" stroke="{P["coral"]}" stroke-width="5"/>'
           f'<path d="M20 4L50 -16" stroke="{P["coral"]}" stroke-width="6" stroke-linecap="round"/>'
           f'<ellipse cx="53" cy="-18" rx="5" ry="8" transform="rotate(-34 53 -18)" fill="{P["gold"]}"/>'
           f'<path d="M-22 -2H20" stroke="#000" stroke-opacity=".12" stroke-width="3"/></g>')
    drops = "".join(
        f'<path class="drop" d="M0 -5Q4 1 0 4Q-4 1 0 -5Z" transform="translate({x} -30)" fill="{P["lilac"] if 0 else "#7cc4ff"}" style="animation-delay:{d}s"/>'
        for x, d in [(4, 0), (10, .35), (16, .7), (7, 1.05), (13, 1.4)])
    stake = (f'<path d="M40 34V-12" stroke="{P["root"]}" stroke-width="4" stroke-linecap="round"/>'
             f'<path d="M40 4Q34 8 32 4" stroke="{P["gold"]}" stroke-width="2" fill="none"/>')
    plant = (f'<path d="M32 32Q30 10 32 -6" stroke="{P["stem"]}" stroke-width="3" fill="none" stroke-linecap="round"/>'
             f'<g transform="translate(32 10) rotate(-60)"><path d="{leaf_d(20, 10)}" fill="{P["leaf"]}"/></g>'
             f'<g transform="translate(32 -6) rotate(-30)"><path d="{leaf_d(18, 9)}" fill="{P["leaf2"]}"/></g>'
             f'<g transform="translate(32 -6) rotate(40)"><path d="{leaf_d(16, 8)}" fill="{P["leaf"]}"/></g>')
    return soil_band(P) + stake + plant + can + drops


def weed_vignette(P):
    leaves = "".join(
        f'<g transform="rotate({a})"><path d="M0 0L7 -8L4 -12L10 -18L5 -24L9 -32L2 -40L-3 -32L-1 -24L-6 -18L-2 -12L-5 -6Z" fill="{P["weed"] if i % 2 else P["weed2"]}"/></g>'
        for i, a in enumerate([-70, -38, -8, 24, 56]))
    roots = (f'<g stroke="{P["root"]}" stroke-width="1.8" fill="none" stroke-linecap="round">'
             f'<path d="M0 0C2 14 -3 24 -1 40"/><path d="M0 6C-6 14 -12 18 -16 30"/><path d="M0 10C6 18 12 22 13 34"/></g>')
    hole = f'<ellipse cx="0" cy="32" rx="18" ry="5" fill="{P["soil2"]}"/>'
    bits = "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="{P["soil2"]}"/>' for x, y in [(-22, 18), (20, 12), (-12, 6), (26, 24)])
    lines = f'<path d="M-30 -30v-14M30 -26v-14M0 -58v-12" stroke="{P["muted"]}" stroke-width="2" stroke-linecap="round" opacity=".6"/>'
    return soil_band(P) + hole + f'<g class="bob">{bits}<g transform="translate(0 -6)">{roots}{leaves}</g>{lines}</g>'


def harvest_vignette(P):
    packet = (f'<g transform="translate(-10 -4) rotate(-10)">'
              f'<path d="M-30 -44H30V44H-30Z" fill="{P["white"]}" stroke="{P["petal_stroke"] if P["petal_stroke"] != "none" else P["white"]}" stroke-width="1.5"/>'
              f'<path d="M-30 -44L0 -32L30 -44V-30H-30Z" fill="{P["gold"]}" opacity=".9"/>'
              f'<rect x="-22" y="-22" width="44" height="40" rx="4" fill="{P["leaf2"]}" opacity=".25"/>'
              f'<path d="M0 16V-2" stroke="{P["stem"]}" stroke-width="2.5"/>'
              + "".join(f'<ellipse cx="0" cy="-9" rx="3" ry="7" transform="rotate({a} 0 -2)" fill="{P["coral"]}"/>' for a in range(0, 360, 45))
              + f'<circle cx="0" cy="-2" r="4" fill="{P["gold"]}"/>'
              f'<rect x="-20" y="26" width="40" height="4" rx="2" fill="{P["muted"]}" opacity=".5"/>'
              f'<rect x="-14" y="34" width="28" height="3" rx="1.5" fill="{P["muted"]}" opacity=".35"/></g>')
    seeds = "".join(f'<ellipse class="spill" cx="{x}" cy="0" rx="2.6" ry="3.6" fill="{P["seed"]}" style="--sx:{sx}px;animation-delay:{d}s"/>'
                    for x, sx, d in [(26, 10, 0), (30, 20, .5), (24, 28, 1.0), (32, 6, 1.5), (28, 16, 2.0)])
    pile = "".join(f'<ellipse cx="{x}" cy="{y}" rx="2.6" ry="3.4" fill="{P["seed"]}"/>' for x, y in [(34, 28), (42, 30), (48, 27), (40, 25), (54, 30)])
    return soil_band(P) + packet + f'<g transform="translate(6 -12)">{seeds}</g>' + pile


def build(theme):
    P = PALETTES[theme]
    E = EXTRA[theme]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-label="Plant, tend, weed, harvest.">',
         """<style>
.pulse{animation:pulse 3.2s ease-in-out infinite alternate;transform-origin:0 45px}
@keyframes pulse{from{transform:scale(.92)}to{transform:scale(1.06)}}
.drop{animation:drop 1.75s linear infinite;opacity:0}
@keyframes drop{0%{opacity:0;translate:0 0}15%{opacity:1}85%{opacity:1}100%{opacity:0;translate:0 44px}}
.bob{animation:bob 2.6s ease-in-out infinite alternate}
@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-10px)}}
.spill{animation:spill 2.5s cubic-bezier(.4,0,.8,.6) infinite;opacity:0}
@keyframes spill{0%{opacity:0;transform:none}15%{opacity:1}100%{opacity:0;transform:translate(var(--sx),40px)}}
.vine{stroke-dasharray:4 9;animation:vine 6s linear infinite}
@keyframes vine{to{stroke-dashoffset:-130}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.drop,.spill{opacity:1}}
</style>"""]
    # connecting vine
    vine = "M{} {}".format(XS[0], CY)
    for a, b in zip(XS, XS[1:]):
        m = (a + b) / 2
        vine += f"Q{m} {CY - 70} {b} {CY}"
    o.append(f'<path class="vine" d="{vine}" fill="none" stroke="{E["vine"]}" stroke-width="3" stroke-linecap="round"/>')
    for i, m in enumerate(XS[:-1]):
        mx = (m + XS[i + 1]) / 2
        o.append(f'<g transform="translate({mx} {CY - 35})"><path d="{leaf_d(16, 9)}" transform="rotate(-50)" fill="{P["leaf"]}"/>'
                 f'<path d="{leaf_d(14, 8)}" transform="rotate(40)" fill="{P["leaf2"]}"/></g>')
    names = [("Plant", "a small, clear seed"), ("Tend", "AI grows it; we water and stake"),
             ("Weed", "pull what doesn't belong"), ("Harvest", "ship it, save the seeds")]
    vignettes = [plant_vignette(P), tend_vignette(P, E), weed_vignette(P), harvest_vignette(P)]
    for i, (x, (name, line), vg) in enumerate(zip(XS, names, vignettes)):
        o.append(f'<defs><clipPath id="c{i}"><circle r="{R}"/></clipPath></defs>')
        o.append(f'<g transform="translate({x} {CY})"><circle r="{R + 8}" fill="none" stroke="{E["ring"]}" stroke-width="1.5" stroke-dasharray="2 6"/>'
                 f'<circle r="{R}" fill="{E["disc"]}"/><g clip-path="url(#c{i})">{vg}</g>'
                 f'<circle r="{R}" fill="none" stroke="{E["ring"]}" stroke-width="2"/></g>')
        d, _ = text_path(f"{i+1:02d}", "mono", 13, x, CY - R - 22, var={"wght": 600}, anchor="middle", tracking=.2)
        o.append(f'<path d="{d}" fill="{P["accent"]}"/>')
        d, _ = text_path(name, "serif", 38, x, CY + R + 56, var={"wght": 600, "opsz": 72, "SOFT": 100, "WONK": 1}, anchor="middle")
        o.append(f'<path d="{d}" fill="{E["label"]}"/>')
        d, _ = text_path(line, "mono", 14, x, CY + R + 86, var={"wght": 450}, anchor="middle")
        o.append(f'<path d="{d}" fill="{E["line"]}"/>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for t in ("dark", "light"):
        open(f"out/stages-{t}.svg", "w").write(build(t))
