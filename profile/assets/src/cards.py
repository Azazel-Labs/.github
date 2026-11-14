"""Social-style 2:1 cards for projects without a hero image (twokey, Ferreal)."""
import re
from textpath import text_path

W, H = 1280, 640
C = dict(bg1="#0b1511", bg2="#15291e", text="#f3ead3", muted="#8fa596", panel="#0a120e",
         border="#2a4434", kw="#ff8a6a", str="#f6c453", attr="#b9a2ff", com="#6f8a78",
         typ="#7fcf86", num="#f6c453", punct="#a9b8ad", red="#ff6b6b", green="#7fcf86",
         leaf="#7fcf86", leaf2="#4f9f62", stem="#5fae6e", wood="#a67c52", wood2="#7d5a3a")

MONO = {"wght": 450}


def t(text, x, y, size, color, font="mono", var=None, anchor="start", tracking=0.0, extra=""):
    d, w = text_path(text, font, size, x, y, var=var or MONO, anchor=anchor, tracking=tracking)
    return f'<path d="{d}" fill="{color}"{extra}/>', w


RUST = [(r"//.*", "com"), (r"#\[[^\]]*\]", "attr"), (r'"[^"]*"', "str"),
        (r"\b(pub|struct|impl|fn|use|let|mut|self|return|for|in|if)\b", "kw"),
        (r"\b(String|u32|str|Self)\b|\b[A-Z][A-Za-z0-9]+\b", "typ"), (r"\b\d+\b", "num"),
        (r"[{}()\[\];,.:&<>=!+\-*/#]", "punct"), (r"[A-Za-z_][A-Za-z0-9_]*", "text"), (r"\s+", None)]
TOML = [(r"#.*", "com"), (r"^\[\[.*\]\]", "attr"), (r'"[^"]*"', "str"), (r"^[a-z_]+(?= =)", "typ"),
        (r"[=\[\],]", "punct"), (r"\s+", None), (r".", "text")]
DIFF = [(r"^-.*", "red"), (r"^\+.*", "green"), (r".*", "text")]


def highlight(line, rules):
    out, i = [], 0
    while i < len(line):
        for pat, cls in rules:
            m = re.compile(pat).match(line, i) if not pat.startswith("^") or i == 0 else None
            if m and m.end() > i:
                out.append((m.group(0), cls))
                i = m.end()
                break
        else:
            out.append((line[i], "text"))
            i += 1
    return out


def code_panel(x, y, w, lines, rules, title, size=17, lh=27, h=None):
    h = h or (len(lines) * lh + 78)
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="1.5"/>',
             f'<path d="M{x} {y+46}H{x+w}" stroke="{C["border"]}" stroke-width="1.5"/>']
    for k, col in enumerate(["#ff6b6b", "#f6c453", "#7fcf86"]):
        parts.append(f'<circle cx="{x+26+k*20}" cy="{y+23}" r="6" fill="{col}" opacity=".75"/>')
    p, _ = t(title, x + w - 22, y + 29, 14, C["muted"], anchor="end", tracking=.04)
    parts.append(p)
    cw = text_path("M", "mono", size, var=MONO)[1]
    for li, line in enumerate(lines):
        cx = x + 26
        cy = y + 46 + 34 + li * lh
        for tok, cls in highlight(line, rules):
            if cls and tok.strip():
                d, _ = text_path(tok, "mono", size, cx, cy, var=MONO)
                parts.append(f'<path d="{d}" fill="{C[cls]}"/>')
            cx += cw * len(tok)
    return "".join(parts), h


def leaf(x, y, rot, L, w, color):
    return (f'<path transform="translate({x} {y}) rotate({rot})" '
            f'd="M0 0C{w*.95:.1f} {-L*.22:.1f} {w*.75:.1f} {-L*.78:.1f} 0 {-L:.1f}C{-w*.75:.1f} {-L*.78:.1f} {-w*.95:.1f} {-L*.22:.1f} 0 0Z" fill="{color}"/>')


def frame(inner, name, tagline, chips, label):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{name}: {" ".join(tagline)}">',
           f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["bg1"]}"/><stop offset="1" stop-color="{C["bg2"]}"/></linearGradient>'
           f'<radialGradient id="gl" cx=".78" cy=".55" r=".6"><stop offset="0" stop-color="#2b6a45" stop-opacity=".35"/><stop offset="1" stop-color="#2b6a45" stop-opacity="0"/></radialGradient></defs>',
           f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#gl)"/>']
    p, _ = t("AZAZEL LABS  ·  " + label, 72, 92, 14, C["muted"], tracking=.16, var={"wght": 500})
    out.append(p)
    d, _ = text_path(name, "serif", 104, 66, 238, var={"wght": 620, "opsz": 144, "SOFT": 100, "WONK": 1})
    out.append(f'<path d="{d}" fill="{C["text"]}"/>')
    for i, line in enumerate(tagline):
        d, _ = text_path(line, "serif-italic", 34, 72, 306 + i * 46, var={"wght": 380, "opsz": 36, "SOFT": 100, "WONK": 1})
        out.append(f'<path d="{d}" fill="{C["text"]}" opacity=".88"/>')
    x = 72
    for c in chips:
        _, w = text_path(c, "mono", 16, var={"wght": 550})
        out.append(f'<rect x="{x}" y="{432}" width="{w+28}" height="38" rx="19" fill="none" stroke="{C["border"]}" stroke-width="1.5"/>')
        p, _ = t(c, x + 14, 457, 16, C["typ"], var={"wght": 550})
        out.append(p)
        x += w + 40
    # a little sprout bed along the bottom, the Azazel garden signature
    out.append(f'<path d="M0 600Q320 588 640 598T1280 594V640H0Z" fill="#1c130d"/>')
    for sx, sh in [(96, 26), (170, 18), (250, 30), (520, 22), (760, 18), (880, 24)]:
        out.append(f'<path d="M{sx} 598q2 -{sh/2} 0 -{sh}" stroke="{C["stem"]}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
        out.append(leaf(sx, 598 - sh, -55, 14, 8, C["leaf"]) + leaf(sx, 598 - sh, 55, 14, 8, C["leaf2"]))
    out.append(inner)
    out.append("</svg>")
    return "".join(out)


def twokey():
    toml = ['[[rule]]', 'id = "token-validation"', 'kind = "symbol"', 'paths = ["/src/auth/**"]',
            'symbols = ["verify_token", "Session::verify"]', 'action = "deny"']
    panel, h = code_panel(668, 96, 548, toml, TOML, ".twokey.toml", size=17)
    diff = [' pub fn verify(&self) -> bool {', '-    self.token.len() == 32', '+    true', ' }']
    dpanel, dh = code_panel(728, 96 + h + 22, 488, diff, DIFF, "an AI's edit", size=17)
    y = 96 + h + 22 + dh
    # blocked stamp
    stamp = (f'<g transform="translate(1000 {y+4}) rotate(-6)">'
             f'<rect x="-6" y="-30" width="196" height="44" rx="8" fill="#2a1414" stroke="{C["red"]}" stroke-width="2.5"/>')
    p, _ = t("✕ BLOCKED", 92, 0, 19, C["red"], anchor="middle", tracking=.14, var={"wght": 750})
    stamp += p + "</g>"
    # padlock with two keyholes
    lock = (f'<g transform="translate(640 {96 + h + 70})">'
            f'<path d="M-22 0V-18a22 22 0 0 1 44 0V0" fill="none" stroke="{C["str"]}" stroke-width="7"/>'
            f'<rect x="-34" y="-2" width="68" height="56" rx="10" fill="{C["str"]}"/>'
            f'<circle cx="-12" cy="22" r="6" fill="{C["panel"]}"/><path d="M-14 24h4v14h-4z" fill="{C["panel"]}"/>'
            f'<circle cx="12" cy="22" r="6" fill="{C["panel"]}"/><path d="M10 24h4v14h-4z" fill="{C["panel"]}"/></g>')
    return frame(panel + dpanel + stamp + lock, "twokey",
                 ["Let AI write code.", "Decide what it cannot change."],
                 ["policy as code", "tree-sitter rules", "CI check"], "GUARDRAILS FOR AI EDITS")


def ferreal():
    rust = ['#[uclass(parent = "UObject")]', 'pub struct Greeter {', '    #[uproperty(EditAnywhere)]',
            '    name: String,', '}', '#[uclass_impl]', 'impl Greeter {', '    #[ufunction(BlueprintCallable)]',
            '    fn greet(&mut self) -> String {', '        format!("Hi, {}", self.name())', '    }', '}']
    panel, h = code_panel(640, 70, 470, rust, RUST, "greeter.rs", size=15.5, lh=24)
    # a Blueprint-style node that the class becomes
    nx, ny, nw = 1000, 400, 230
    node = [f'<g filter="none"><rect x="{nx}" y="{ny}" width="{nw}" height="150" rx="12" fill="#101b16" stroke="{C["border"]}" stroke-width="1.5"/>',
            f'<path d="M{nx} {ny+12}a12 12 0 0 1 12 -12h{nw-24}a12 12 0 0 1 12 12v30h-{nw}z" fill="#2b5ea8"/>']
    p, _ = t("ƒ Greet", nx + 18, ny + 28, 17, "#ffffff", var={"wght": 650})
    node.append(p)
    p, _ = t("Target is Greeter", nx + 18, ny + 64, 12.5, C["muted"])
    node.append(p)
    # exec pins
    node.append(f'<path d="M{nx+16} {ny+86}l10 0l8 8l-8 8l-10 0z" fill="#fff"/>')
    node.append(f'<path d="M{nx+nw-34} {ny+86}l10 0l8 8l-8 8l-10 0z" fill="#fff"/>')
    node.append(f'<circle cx="{nx+22}" cy="{ny+124}" r="7" fill="none" stroke="#4fd1c5" stroke-width="3"/>')
    p, _ = t("Target", nx + 36, ny + 129, 14, C["text"])
    node.append(p)
    node.append(f'<circle cx="{nx+nw-22}" cy="{ny+124}" r="7" fill="#ff6fb5"/>')
    p, _ = t("Return", nx + nw - 36, ny + 129, 14, C["text"], anchor="end")
    node.append(p + "</g>")
    # arrow from code to node
    arrow = (f'<path d="M1110 200C1190 200 1200 300 1170 {ny-8}" fill="none" stroke="{C["str"]}" stroke-width="2.5" stroke-dasharray="6 7"/>'
             f'<path d="M1160 {ny-20}l10 12l12 -9" fill="none" stroke="{C["str"]}" stroke-width="2.5" stroke-linecap="round"/>')
    p, _ = t("a real UCLASS, in Blueprints", 1230, ny + 176, 14, C["muted"], anchor="end")
    return frame(panel + arrow + "".join(node) + p, "Ferreal",
                 ["Unreal Engine 5 classes,", "written in Rust. Fer real."],
                 ["UCLASS", "UPROPERTY", "UFUNCTION"], "RUST × UNREAL ENGINE")


if __name__ == "__main__":
    for name, fn in [("twokey", twokey), ("ferreal", ferreal)]:
        open(f"out/card-{name}.svg", "w").write(fn())
