import xml.etree.ElementTree as ET
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import roles

FONTS = Path(__file__).parent / "fonts"
STYLES = {"fas": "solid-900", "far": "regular-400", "fab": "brands-400"}
NS = "{http://www.w3.org/2000/svg}"
GLYPHS = {}


def load_glyphs(style):
    font = ET.parse(FONTS / f"fa-{style}.svg").getroot().find(f"{NS}defs/{NS}font")
    default_adv = font.get("horiz-adv-x")
    return {
        g.get("glyph-name"): (g.get("horiz-adv-x", default_adv), g.get("d"))
        for g in font.iter(f"{NS}glyph")
    }


def rst_icon(name, rawtext, text, lineno, inliner, options={}, content=[]):
    style = STYLES[name]
    if style not in GLYPHS:
        GLYPHS[style] = load_glyphs(style)
    adv, d = GLYPHS[style][text]
    svg = (
        '<svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {adv} 512">'
        f'<path transform="translate(0,448) scale(1,-1)" d="{d}"/></svg>'
    )
    return [nodes.raw("", svg, format="html")], []


def register():
    for role in STYLES:
        roles.register_local_role(role, rst_icon)
