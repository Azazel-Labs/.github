"""The Azazel Labs goat (from the org logo), as vector parts, in logo pixel space (460x460)."""

CREAM = "#f6f0e2"
INK = "#14110f"
ORANGE = "#f47512"

HORN_L = "M142 194C138 170 124 148 94 138C92 132 98 120 112 114C140 104 170 120 184 154Z"
EAR_L = "M128 192C98 186 62 194 40 205C56 230 92 251 122 256Z"
EAR_L_IN = "M55 213C80 209 104 214 121 224L121 248C95 241 71 229 55 213Z"
FACE = ("M173 162L136 190C118 215 110 245 112 277C114 305 125 330 140 343C155 360 172 368 187 372"
        "C190 380 194 392 200 398Q208 406 216 400Q224 410 232 403Q240 410 248 400Q256 406 264 398C270 392 274 380 277 372"
        "C292 368 309 360 324 343C339 330 350 305 352 277C354 245 346 215 328 190L291 162Z")
FLASK_OUT = "M196 70H268Q276 70 276 78V84Q276 92 268 92H264V148L300 198L232 268L164 198L200 148V92H196Q188 92 188 84V78Q188 70 196 70Z"
FLASK = "M213 92H251V150L289 197L232 256L175 197L213 150Z"
LIQUID = "M187 198L207 176C222 168 236 180 250 174C262 169 270 174 276 182L277 197L232 238Z"


def mirror(d, cx=232):
    """Mirror an absolute-coordinate path across x=cx."""
    import re
    toks = re.findall(r"[A-Za-z]|-?\d+(?:\.\d+)?", d)
    out, i, cmd, idx = [], 0, None, 0
    for tk in toks:
        if tk.isalpha():
            cmd, idx = tk, 0
            out.append(tk)
            continue
        v = float(tk)
        if cmd == "H":
            v = 2 * cx - v
        elif cmd in "MLCQT":
            if idx % 2 == 0:
                v = 2 * cx - v
        idx += 1
        out.append(f"{v:g}")
    return " ".join(out)


def head(line="#3b302a", line_w=7, blink=True, mouth_extra=""):
    cream_shapes = [HORN_L, mirror(HORN_L), EAR_L, mirror(EAR_L), FACE, FLASK_OUT]
    sil = "".join(f'<path d="{d}"/>' for d in cream_shapes)
    eyes = ""
    for cx, ox, px in [(165, -3, 6), (299, 3, -6)]:
        eyes += (f'<circle cx="{cx}" cy="268" r="30" fill="{INK}"/>'
                 f'<circle cx="{cx+ox}" cy="272" r="25" fill="{ORANGE}"/>'
                 f'<circle cx="{cx+px}" cy="265" r="21" fill="{INK}"/>'
                 f'<circle cx="{cx+px+2}" cy="259" r="6.5" fill="#fff"/>')
    if blink:
        eyes = f'<g class="blink">{eyes}</g>'
    return (f'<g stroke="{line}" stroke-width="{line_w}" stroke-linejoin="round" fill="{line}">{sil}</g>'
            f'<g fill="{CREAM}">{sil}</g>'
            f'<path d="{EAR_L_IN}" fill="{INK}"/><path d="{mirror(EAR_L_IN)}" fill="{INK}"/>'
            f'<path d="{FLASK}" fill="{INK}"/><path d="{LIQUID}" fill="{ORANGE}"/>'
            f'<circle cx="235" cy="124" r="7" fill="{ORANGE}"/><circle cx="227" cy="151" r="9" fill="{ORANGE}"/>'
            + eyes +
            f'<path d="M206 306C214 300 224 304 232 309C240 304 250 300 258 306C262 314 244 324 232 328C220 324 202 314 206 306Z" fill="{INK}"/>'
            f'<path d="M232 326V340" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M178 326C192 352 214 356 232 340C250 356 272 352 286 326" fill="none" stroke="{INK}" stroke-width="6.5" stroke-linecap="round"/>'
            + mouth_extra)


if __name__ == "__main__":
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 460" width="460" height="460">'
           f'<rect width="460" height="460" fill="#123"/>{head()}</svg>')
    open("goat-test.svg", "w").write(svg)
