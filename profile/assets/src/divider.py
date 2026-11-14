"""Row of swaying sprouts used as a section divider."""
import random
from banner import leaf_d

rng = random.Random(3)
W, H = 1280, 48
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="">',
     '<style>.s{animation:s 5s ease-in-out infinite alternate}@keyframes s{from{transform:rotate(-4deg)}to{transform:rotate(4deg)}}'
     '@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>',
     f'<path d="M40 44H{W-40}" stroke="#6fa77a" stroke-opacity=".45" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 8"/>']
x = 60
while x < W - 50:
    h = rng.uniform(10, 26)
    o.append(f'<g transform="translate({x:.0f} 44)"><g class="s" style="animation-delay:-{rng.uniform(0,5):.1f}s">'
             f'<path d="M0 0Q2 {-h/2:.0f} 0 {-h:.0f}" stroke="#5fae6e" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
             f'<path transform="translate(0 {-h:.0f}) rotate(-58)" d="{leaf_d(11,6)}" fill="#7fcf86"/>'
             f'<path transform="translate(0 {-h:.0f}) rotate(58)" d="{leaf_d(11,6)}" fill="#4f9f62"/></g></g>')
    x += rng.uniform(70, 150)
o.append("</svg>")
open("out/divider.svg", "w").write("".join(o))
