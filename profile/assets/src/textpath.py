"""Shape text with HarfBuzz and return SVG path data, so SVGs need no fonts."""
import os
import uharfbuzz as hb

FONT_DIR = os.environ.get("FONT_DIR", os.path.join(os.path.dirname(__file__), "fonts"))

FONTS = {
    "serif": FONT_DIR + "/Fraunces.ttf",
    "serif-italic": FONT_DIR + "/Fraunces-Italic.ttf",
    "mono": FONT_DIR + "/JetBrainsMono.ttf",
}
_cache = {}


def _font(name):
    if name not in _cache:
        blob = hb.Blob.from_file_path(FONTS[name])
        face = hb.Face(blob)
        _cache[name] = (face, face.upem)
    return _cache[name]


class _Pen:
    def __init__(self, scale, ox, oy):
        self.s, self.ox, self.oy, self.d = scale, ox, oy, []

    def _p(self, x, y):
        return f"{self.ox + x * self.s:.1f} {self.oy - y * self.s:.1f}"

    def move_to(self, x, y, c=None):
        self.d.append("M" + self._p(x, y))

    def line_to(self, x, y, c=None):
        self.d.append("L" + self._p(x, y))

    def quadratic_to(self, x1, y1, x, y, c=None):
        self.d.append("Q" + self._p(x1, y1) + " " + self._p(x, y))

    def cubic_to(self, x1, y1, x2, y2, x, y, c=None):
        self.d.append("C" + self._p(x1, y1) + " " + self._p(x2, y2) + " " + self._p(x, y))

    def close_path(self, c=None):
        self.d.append("Z")


def text_path(text, font="serif", size=48, x=0, y=0, var=None, features=None,
              tracking=0.0, anchor="start"):
    """Return (path_d, width). tracking is in em units added after each glyph."""
    face, upem = _font(font)
    f = hb.Font(face)
    if var:
        f.set_variations(var)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(f, buf, features or ({"kern": True, "liga": False, "calt": False} if font == "mono" else {"kern": True, "liga": True}))
    s = size / upem
    width = sum(p.x_advance for p in buf.glyph_positions) * s + tracking * size * len(text)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    pen_x = x
    parts = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = _Pen(s, pen_x + pos.x_offset * s, y - pos.y_offset * s)
        funcs = hb.DrawFuncs()
        funcs.set_move_to_func(lambda x_, y_, c, p=pen: p.move_to(x_, y_))
        funcs.set_line_to_func(lambda x_, y_, c, p=pen: p.line_to(x_, y_))
        funcs.set_quadratic_to_func(lambda a, b, x_, y_, c, p=pen: p.quadratic_to(a, b, x_, y_))
        funcs.set_cubic_to_func(lambda a, b, c_, d, x_, y_, c, p=pen: p.cubic_to(a, b, c_, d, x_, y_))
        funcs.set_close_path_func(lambda c, p=pen: p.close_path())
        f.draw_glyph(info.codepoint, funcs, None)
        parts.extend(pen.d)
        pen_x += pos.x_advance * s + tracking * size
    return "".join(parts), width
