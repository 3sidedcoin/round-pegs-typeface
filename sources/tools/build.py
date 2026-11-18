"""Build an extended OTF from the designer's SVG glyphs.

Scale: 1 SVG unit = 35 font units (1 pixel cell = 4 SVG units = 140 font units).
Origin: bottom-left of each SVG canvas sits on the baseline / left origin.
Advance: canvas width + one 140-unit gap cell (matches the original caps).
"""
import os, sys
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.roundingPen import RoundingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path
from pathops import Path, PathOp, op
from PIL import Image, ImageDraw, ImageFont

SRC_FONT = os.environ.get('ROUND_PEGS_BASE_OTF', 'RoundPegsBase-Regular.otf')  # earlier game-version OTF (not in this repo)
HERE = os.path.dirname(os.path.abspath(__file__))
SVG_DIR = os.path.join(HERE, 'svg')
OUT = os.path.join(HERE, 'build', 'intermediate.otf')
S = 35
GAP = 140

# svg file stem -> (glyph name, [unicode code points])
MAP = {}
for ch in 'DEFGIKLMNOPQRSTUVWX':
    MAP[ch] = (ch, [])  # existing glyphs, cmap untouched
for low in 'abchjyz':  # capitals exported with lowercase file names
    MAP[low] = (low.upper(), [])
MAP.update({
    'colon': ('colon', []), 'comma': ('comma', []), 'period': ('period', []),
    'hyphen': ('hyphen', []), 'exclamation mark': ('exclam', []),
    'q-mark': ('question', []), 'semi-colon': ('semicolon', []),
    'elipsis': ('u2026', []),
    # new glyphs
    'a-variation': ('at', [0x40]),
    'ampersand': ('ampersand', [0x26]),
    'apostrophe': ('quoteright', [0x2019]),
    'single-straight-quote': ('quotesingle', [0x27]),
    'straight-quote': ('quotedbl', [0x22]),
    'opening-double-quote': ('quotedblleft', [0x201C]),
    'closing-double-quote': ('quotedblright', [0x201D]),
    'opening-parentheses': ('parenleft', [0x28]),
    'closing-parentheses': ('parenright', [0x29]),
    'Slash': ('slash', [0x2F]),
    'UNDERSCORE': ('underscore', [0x5F]),
    'opening-square-bracket': ('bracketleft', [0x5B]),
    'closing-square-bracket': ('bracketright', [0x5D]),
    'equal': ('equal', [0x3D]),
    'plus': ('plus', [0x2B]),
    'asterix': ('asterisk', [0x2A]),
    'hash': ('numbersign', [0x23]),
    'dollar': ('dollar', [0x24]),
    'percentage': ('percent', [0x25]),
    'rupee': ('rupee', [0x20B9]),
    'multiply': ('multiply', [0xD7]),
    'divide': ('divide', [0xF7]),
    'less': ('less', [0x3C]),
    'greater': ('greater', [0x3E]),
    'middle-dot': ('periodcentered', [0xB7]),
    'bullet': ('bullet', [0x2022]),
    'TM': ('trademark', [0x2122]),
    'inverted-exclamation': ('exclamdown', [0xA1]),
    'inverted-question': ('questiondown', [0xBF]),
    'cent': ('cent', [0xA2]),
    'pound': ('sterling', [0xA3]),
    'yen': ('yen', [0xA5]),
    'euro': ('Euro', [0x20AC]),
    'caret': ('asciicircum', [0x5E]),
    'grave_accent': ('grave', [0x60]),
    'tilde': ('asciitilde', [0x7E]),
    'pipe': ('bar', [0x7C]),
    'opening-curly-bracket': ('braceleft', [0x7B]),
    'closing-curly-bracket': ('braceright', [0x7D]),
    'en-dash': ('endash', [0x2013]),
    'em-dash': ('emdash', [0x2014]),
    'arrow-left': ('arrowleft', [0x2190]),
    'arrow-up': ('arrowup', [0x2191]),
    'arrow-right': ('arrowright', [0x2192]),
    'arrow-down': ('arrowdown', [0x2193]),
})
KNOCKOUT = set()  # black star paths over black dots are holes in the original font


def snap(v):
    return round(v) if abs(v - round(v)) < 0.01 else v


MAP.update({
    'copyright': ('copyright', [0xA9]), 'registered': ('registered', [0xAE]),
    'ordfeminine': ('ordfeminine', [0xAA]), 'ordmasculine': ('ordmasculine', [0xBA]),
    'degree': ('degree', [0xB0]), 'section': ('section', [0xA7]), 'pilcrow': ('paragraph', [0xB6]),
    'guillemet-left': ('guillemotleft', [0xAB]), 'guillemet-right': ('guillemotright', [0xBB]),
    'guilsingle-left': ('guilsinglleft', [0x2039]), 'guilsingle-right': ('guilsinglright', [0x203A]),
})
MAP.update({  # extended Latin letters; lowercase / variant code points alias the same (caps-only) glyph
    'Lslash': ('Lslash', [0x141, 0x142]), 'Oslash': ('Oslash', [0xD8, 0xF8]), 'Hbar': ('Hbar', [0x126, 0x127]),
    'Germandbls': ('uni1E9E', [0x1E9E, 0xDF]), 'Thorn': ('Thorn', [0xDE, 0xFE]), 'Eth': ('Eth', [0xD0, 0xF0, 0x110, 0x111]),
    'OE': ('OE', [0x152, 0x153]), 'AE': ('AE', [0xC6, 0xE6]),
})

def rect_d(x, y, w, h, r):
    if r <= 0:
        return f'M{x} {y}H{x+w}V{y+h}H{x}Z'
    return (f'M{x+r} {y}H{x+w-r}A{r} {r} 0 0 1 {x+w} {y+r}V{y+h-r}A{r} {r} 0 0 1 {x+w-r} {y+h}'
            f'H{x+r}A{r} {r} 0 0 1 {x} {y+h-r}V{y+r}A{r} {r} 0 0 1 {x+r} {y}Z')


BASE_OVERRIDE = {'ordfeminine': 24, 'ordmasculine': 24, 'registered': 24, 'copyright': 24}  # ink bottom sits on baseline in these 32-high frames
CROP = {'ordfeminine': (4, 20), 'ordmasculine': (4, 20), 'registered': (4, 24), 'copyright': (4, 24), 'degree': (12, 24), 'guillemet-left': (4, 20), 'guillemet-right': (4, 20), 'pilcrow': (4, 20), 'section': (4, 20), 'guilsingle-left': (12, 20), 'guilsingle-right': (12, 20)}  # frames with side margin: crop to ink columns


def load_svg(stem):
    root = ET.parse(os.path.join(SVG_DIR, stem + '.svg')).getroot()
    W, H = float(root.get('width')), float(root.get('height'))
    base = {28: 24, 32: 28, 36: 32, 40: 32, 44: 32}.get(H, H)  # 28-unit (7-row) frames: baseline y=24; 36-unit (9-row, accent + descender) frames: baseline y=32; others: bottom
    base = BASE_OVERRIDE.get(stem, base)
    shapes = []  # (kind, Path)
    for el in root:
        tag = el.tag.split('}')[1]
        if tag == 'path':
            d = el.get('d')
        elif tag == 'rect':
            g = lambda k: snap(float(el.get(k, 0)))
            d = rect_d(g('x'), g('y'), g('width'), g('height'), g('rx'))
        else:
            raise SystemExit(f'{stem}: unsupported element {tag}')
        p = Path()
        cx0, cx1 = CROP.get(stem, (0, W))
        pen = TransformPen(RoundingPen(p.getPen()), (S, 0, 0, -S, -cx0 * S, base * S))
        parse_path(d, pen)
        shapes.append((tag, p))
    return cx1 - cx0, H, shapes


def combine(stem, shapes):
    if stem in KNOCKOUT:
        solid = [p for k, p in shapes if k == 'rect']
        holes = [p for k, p in shapes if k == 'path']
        res = solid[0]
        for p in solid[1:]:
            res = op(res, p, PathOp.UNION)
        for p in holes:
            res = op(res, p, PathOp.DIFFERENCE)
    else:
        res = shapes[0][1]
        res.simplify(fix_winding=True)
        for _, p in shapes[1:]:
            p.simplify(fix_winding=True)
            res = op(res, p, PathOp.UNION)
    res.simplify(fix_winding=True, clockwise=True)
    return res


def star_path(cx, cy, r=70):
    """Four-pointed concave star, same construction as the stars in the @ SVG (r = half a cell)."""
    p = Path(); pen = p.getPen()
    pen.moveTo((cx, cy + r))
    pen.curveTo((cx, cy + r), (cx, cy), (cx - r, cy))
    pen.curveTo((cx, cy), (cx, cy - r), (cx, cy - r))
    pen.curveTo((cx, cy - r), (cx, cy), (cx + r, cy))
    pen.curveTo((cx, cy), (cx, cy + r), (cx, cy + r))
    pen.closePath()
    return p


def digit_junctions(gs0, ch):
    """Grid corners where two filled cells touch only diagonally."""
    bp = BoundsPen(gs0); gs0[ch].draw(bp); x0, y0, x1, y1 = bp.bounds
    pf = ImageFont.truetype(SRC_FONT, 1000)
    im = Image.new('L', (1200, 1200), 255)
    ImageDraw.Draw(im).text((100, 900), ch, font=pf, fill=0, anchor='ls')
    Wc, Hc = int(round((x1 - x0) / 140)), int(round((y1 - y0) / 140))
    g = [[im.getpixel((int(100 + x0 + 140 * i + 70), int(900 - (y0 + 140 * j + 70)))) < 128
          for i in range(Wc)] for j in range(Hc)]
    out = []
    for j in range(1, Hc):
        for i in range(1, Wc):
            a, b, c, d = g[j-1][i-1], g[j-1][i], g[j][i-1], g[j][i]
            if (a and d and not b and not c) or (b and c and not a and not d):
                out.append((x0 + 140 * i, y0 + 140 * j))
    return out


def main():
    font = TTFont(SRC_FONT)
    cff = font['CFF '].cff
    top = cff.topDictIndex[0]
    cs = top.CharStrings
    private = top.Private
    gsubrs = cff.GlobalSubrs
    gs0 = font.getGlyphSet()  # untouched originals (digits come from here)
    order = font.getGlyphOrder()
    hmtx = font['hmtx'].metrics
    cmaps = [t for t in font['cmap'].tables if t.isUnicode()]
    report = []
    def add_glyph(name, cps, path, adv, stem):
        pen = T2CharStringPen(adv, None)
        path.draw(pen)
        charstring = pen.getCharString(private, gsubrs)
        bp = BoundsPen(None)
        path.draw(bp)
        b = bp.bounds
        isnew = name not in order
        if isnew:
            cs.charStringsIndex.append(charstring)
            cs.charStrings[name] = len(cs.charStringsIndex) - 1
            order.append(name)
            if top.charset is not order:
                top.charset.append(name)
        else:
            cs[name] = charstring
        hmtx[name] = (adv, int(b[0]))
        for cp in cps:
            for t in cmaps:
                t.cmap[cp] = name
        report.append((stem, name, 'new' if isnew else 'replaced', adv, b))

    for stem, (name, cps) in MAP.items():
        W, H, shapes = load_svg(stem)
        path = combine(stem, shapes)
        adv = int(round(W * S)) + GAP
        add_glyph(name, cps, path, adv, stem)
        if stem == 'Slash':  # backslash = slash mirrored left-right about the canvas centre
            bs = Path()
            path.draw(TransformPen(bs.getPen(), (-1, 0, 0, 1, W * S, 0)))
            bs.simplify(fix_winding=True, clockwise=True)
            add_glyph('backslash', [0x5C], bs, adv, 'Slash (mirrored)')
        if stem == 'apostrophe':  # opening single quote = apostrophe mirrored left-right (as the opening double quote mirrors the closing one)
            bp = BoundsPen(None); path.draw(bp); b = bp.bounds
            mir = Path()
            path.draw(TransformPen(mir.getPen(), (-1, 0, 0, 1, b[0] + b[2], 0)))
            mir.simplify(fix_winding=True, clockwise=True)
            add_glyph('quoteleft', [0x2018], mir, adv, 'apostrophe (mirrored)')
    for ch in '0123456789':  # original digits + additive stars at corner-touch junctions
        path = Path(); gs0[ch].draw(path.getPen())
        path.simplify(fix_winding=True)
        pts = digit_junctions(gs0, ch)
        for cx, cy in pts:
            path = op(path, star_path(cx, cy), PathOp.UNION)
        path.simplify(fix_winding=True, clockwise=True)
        add_glyph(ch, [], path, hmtx[ch][0], f'digit {ch} +{len(pts)} stars')
    font.setGlyphOrder(order)
    font['hhea'].ascent, font['hhea'].descent = 840, -160   # 7-row band: -140..840 inside the 1000 em
    font['OS/2'].sTypoAscender, font['OS/2'].sTypoDescender = 840, -160
    font['OS/2'].recalcUnicodeRanges(font)   # declare the blocks the font really covers (Latin-1, currency, letterlike, arrows...)
    font['OS/2'].ulCodePageRange1 |= 1       # Latin 1 (cp1252)
    font['head'].fontRevision = 2.2
    for rec in font['name'].names:
        if rec.nameID == 5:
            rec.string = 'Version 2.200'
        elif rec.nameID == 3:
            rec.string = '2.200;RoundPegsBase-Regular'
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    font.save(OUT)
    for r in report:
        print(r)


if __name__ == "__main__":
    main()
