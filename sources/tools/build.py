"""Build an extended Shade Pixel OTF from the designer's SVG glyphs.

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

SRC_FONT = '/mnt/user-data/uploads/260051fe-ShadePixel-Regular.otf'
SVG_DIR = '/home/claude/work/zip/pixel-typeface'
OUT = '/home/claude/work/out/ShadePixel-Regular.otf'
S = 35
GAP = 140

# svg file stem -> (glyph name, [unicode code points])
MAP = {}
for ch in 'DEFGIKLMNOPQRSTUVWX':
    MAP[ch] = (ch, [])  # existing glyphs, cmap untouched
for low in 'abchjyz':  # capitals exported with lowercase file names
    MAP[low] = (low.upper(), [])
MAP.update({
    'zero': ('0', []), 'one': ('1', []), 'two': ('2', []), 'three': ('3', []), 'four': ('4', []), 'six': ('6', []), 'seven': ('7', []), 'eight': ('8', []), 'nine': ('9', []),  # designer-drawn digits (stars included)
    'R-alt': ('R.ss01', []), 'one-alt': ('one.ss02', []),  # stylistic sets: ss01 alternate R, ss02 alternate 1
    'b-alt': ('B.ss03', []), 'P-alt': ('P.ss04', []), 'I-alt': ('I.ss05', []), 'y-alt': ('Y.ss06', []), 'X-alt': ('X.ss07', []), 'N-alt': ('N.ss08', []),
    'zero-alt': ('zero.ss09', []), 'four-alt': ('four.ss10', []), 'O-alt': ('O.ss11', []),  # ss03 B, ss04 P, ss05 slim I, ss06 narrow Y, ss07 narrow X, ss08 narrow N, ss09 slashed zero, ss10 closed four, ss11 narrow O
    'L-short': ('L.short', []),  # calt: L before L (3 cells, normal 1-cell gap); the narrow O (O.ss11) is also the calt form in O runs
    'five': ('5', []),  # designer-drawn 5 replaces the source digit (it already carries its own fillets)
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
    'arrow-nw': ('arrowupleft', [0x2196]),
    'arrow-ne': ('arrowupright', [0x2197]),
    'arrow-se': ('arrowdownright', [0x2198]),
    'arrow-sw': ('arrowdownleft', [0x2199]),
    'arrow-leftright': ('arrowboth', [0x2194]),
    'arrow-updown': ('arrowupdn', [0x2195]),
    'onethird': ('onethird', [0x2153]),
    'twothirds': ('twothirds', [0x2154]),
    'fraction-slash': ('fraction', [0x2044]),
    'pipe-double': ('dblverticalbar', [0x2016]),
    'numero': ('numero', [0x2116]),
    'sun': ('sun', [0x2600]),
    'moon': ('moon', [0x263E]),
    'moon-waxing': ('moonwaxing', [0x263D]),
    'arrow-wall': ('arrowbarright', [0x21E5]),
    'arrow-wall-left': ('arrowbarleft', [0x21E4]),
    'up-caret': ('control', [0x2303]),
    'down-caret': ('downarrowhead', [0x2304]),
    'command': ('command', [0x2318]),
    'option': ('option', [0x2325]),
    'burger': ('burger', [0x2261, 0x2630]),
    'vertical-dots': ('ellipsisvertical', [0x22EE]),
    'not-equal': ('notequal', [0x2260]),
    'approx-equal': ('approxequal', [0x2248]),
    'integral': ('integral', [0x222B]),
    'partial': ('partialdiff', [0x2202]),
    'product': ('product', [0x220F]),
    'summation': ('summation', [0x2211]),
    'pi': ('pi', [0x03C0]),
    'check': ('uni2713', [0x2713]),
    'root': ('radical', [0x221A]),
    'omega': ('uni2126', [0x2126, 0x3A9]),
    'estimated': ('estimated', [0x212E]),
    'ell': ('uni2113', [0x2113]),
    'delta': ('uni2206', [0x2206, 0x394]),
    'small-square': ('H18543', [0x25AA]),
    'circle-d': ('uni24B9', [0x24B9]),
    'infinity': ('infinity', [0x221E]),
    'angle-open': ('uni27E8', [0x27E8]),
    'angle-close': ('uni27E9', [0x27E9]),
    'square-solid': ('filledbox', [0x25A0]),
    'square-border': ('H22073', [0x25A1]),
    'tri-up': ('triagup', [0x25B2]),
    'tri-up-small': ('uni25B4', [0x25B4]),
    'tri-right': ('uni25B6', [0x25B6]),
    'tri-right-small': ('uni25B8', [0x25B8]),
    'tri-down': ('triagdn', [0x25BC]),
    'tri-down-small': ('uni25BE', [0x25BE]),
    'tri-left': ('uni25C0', [0x25C0]),
    'tri-left-small': ('uni25C2', [0x25C2]),
    'diamond': ('uni25C6', [0x25C6]),
    'diamond-empty': ('uni25C7', [0x25C7]),
    'lozenge': ('lozenge', [0x25CA]),
    'prime': ('minute', [0x2032]),
    'double-prime': ('second', [0x2033]),
})
KNOCKOUT = set()  # black star paths over black dots are holes in the original font


def snap(v):
    return round(v) if abs(v - round(v)) < 0.01 else v


MAP.update({
    'copyright': ('copyright', [0xA9]), 'circle-p': ('soundrecording', [0x2117]), 'registered': ('registered', [0xAE]),
    'ordfeminine': ('ordfeminine', [0xAA]), 'ordmasculine': ('ordmasculine', [0xBA]),
    'degree': ('degree', [0xB0]), 'section': ('section', [0xA7]), 'pilcrow': ('paragraph', [0xB6]),
    'guillemet-left': ('guillemotleft', [0xAB]), 'guillemet-right': ('guillemotright', [0xBB]),
    'guilsingle-left': ('guilsinglleft', [0x2039]), 'guilsingle-right': ('guilsinglright', [0x203A]),
})
MAP.update({  # extended Latin letters; lowercase / variant code points alias the same (caps-only) glyph
    'Lslash': ('Lslash', [0x141, 0x142]), 'Oslash': ('Oslash', [0xD8, 0xF8]), 'Hbar': ('Hbar', [0x126, 0x127]),
    'Germandbls': ('uni1E9E', [0x1E9E, 0xDF]), 'plusminus': ('plusminus', [0xB1]), 'mu': ('mu', [0xB5]), 'logicalnot': ('logicalnot', [0xAC]), 'dagger': ('dagger', [0x2020]), 'daggerdbl': ('daggerdbl', [0x2021]), 'florin': ('florin', [0x192]), 'perthousand': ('perthousand', [0x2030]), 'zerosuperior': ('zerosuperior', [0x2070]), 'zeroinferior': ('zeroinferior', [0x2080]), 'oneinferior': ('oneinferior', [0x2081]), 'twoinferior': ('twoinferior', [0x2082]), 'threeinferior': ('threeinferior', [0x2083]), 'foursuperior': ('foursuperior', [0x2074]), 'fourinferior': ('fourinferior', [0x2084]), 'fivesuperior': ('fivesuperior', [0x2075]), 'fiveinferior': ('fiveinferior', [0x2085]), 'sixsuperior': ('sixsuperior', [0x2076]), 'sixinferior': ('sixinferior', [0x2086]), 'sevensuperior': ('sevensuperior', [0x2077]), 'seveninferior': ('seveninferior', [0x2087]), 'eightsuperior': ('eightsuperior', [0x2078]), 'eightinferior': ('eightinferior', [0x2088]), 'ninesuperior': ('ninesuperior', [0x2079]), 'nineinferior': ('nineinferior', [0x2089]),  'currency': ('currency', [0xA4]), 'brokenbar': ('brokenbar', [0xA6]), 'onehalf': ('onehalf', [0xBD]), 'onequarter': ('onequarter', [0xBC]), 'threequarters': ('threequarters', [0xBE]), 'onesuperior': ('onesuperior', [0xB9]), 'twosuperior': ('twosuperior', [0xB2]), 'threesuperior': ('threesuperior', [0xB3]), 'Eng': ('Eng', [0x14A, 0x14B]), 'Tbar': ('Tbar', [0x166, 0x167]), 'Gbar': ('Gbar', [0x1E4, 0x1E5]), 'Ezh': ('Ezh', [0x1B7, 0x292]), 'Thorn': ('Thorn', [0xDE, 0xFE]), 'Eth': ('Eth', [0xD0, 0xF0, 0x110, 0x111]),
    'OE': ('OE', [0x152, 0x153]), 'AE': ('AE', [0xC6, 0xE6]),
})

def rect_d(x, y, w, h, r):
    if r <= 0:
        return f'M{x} {y}H{x+w}V{y+h}H{x}Z'
    return (f'M{x+r} {y}H{x+w-r}A{r} {r} 0 0 1 {x+w} {y+r}V{y+h-r}A{r} {r} 0 0 1 {x+w-r} {y+h}'
            f'H{x+r}A{r} {r} 0 0 1 {x} {y+h-r}V{y+r}A{r} {r} 0 0 1 {x+r} {y}Z')


BASE_OVERRIDE = {'moon': 22, 'command': 22, 'moon-waxing': 22, 'mu': 20, 'zerosuperior': 32, 'foursuperior': 32, 'fivesuperior': 32, 'sixsuperior': 32, 'sevensuperior': 32, 'eightsuperior': 32, 'ninesuperior': 32, 'zeroinferior': 8, 'oneinferior': 8, 'twoinferior': 8, 'threeinferior': 8, 'fourinferior': 8, 'fiveinferior': 8, 'sixinferior': 8, 'seveninferior': 8, 'eightinferior': 8, 'nineinferior': 8, 'currency': 30, 'ordfeminine': 32, 'ordmasculine': 32, 'registered': 22, 'copyright': 22, 'circle-p': 22, 'section': 24, 'pilcrow': 24, 'onehalf': 24, 'onequarter': 24, 'onethird': 24, 'twothirds': 24, 'threequarters': 24}  # ink bottom sits on baseline in these 32-high frames
CROP = {'sun': (2, 26), 'small-square': (6, 14), 'zerosuperior': (4, 16), 'zeroinferior': (4, 16), 'oneinferior': (12, 24), 'twoinferior': (12, 24), 'threeinferior': (12, 24), 'foursuperior': (4, 16), 'fourinferior': (4, 16), 'fivesuperior': (4, 16), 'fiveinferior': (4, 16), 'sixsuperior': (4, 16), 'sixinferior': (4, 16), 'sevensuperior': (4, 16), 'seveninferior': (4, 16), 'eightsuperior': (4, 16), 'eightinferior': (4, 16), 'ninesuperior': (4, 16), 'nineinferior': (4, 16), 'onesuperior': (12, 24), 'twosuperior': (12, 24), 'threesuperior': (12, 24), 'ordfeminine': (0, 12), 'ordmasculine': (0, 12), 'degree': (12, 24), 'guillemet-left': (4, 20), 'guillemet-right': (4, 20), 'pilcrow': (4, 20), 'section': (4, 20), 'guilsingle-left': (12, 20), 'guilsingle-right': (12, 20), 'arrow-updown': (4, 24), 'square-solid': (4, 16), 'square-border': (4, 16), 'tri-up': (4, 16), 'tri-up-small': (4, 16), 'tri-down': (4, 16), 'tri-down-small': (4, 16), 'tri-right': (4, 16), 'tri-left': (4, 16), 'tri-right-small': (8, 16), 'tri-left-small': (4, 12), 'lozenge': (4, 16)}  # frames with side margin: crop to ink columns


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
        flush_path, prop_adv = path, adv  # proportional 1 (pnum): ink flush left, advance = ink + 1 cell
        if name in ('1', 'one.ss02'):  # figures are tabular: centre the 3-cell ink in the 5-cell advance
            adv = 5 * GAP
            sh = Path(); path.draw(TransformPen(sh.getPen(), (1, 0, 0, 1, (adv - int(round(W * S))) / 2, 0)))
            path = sh
        add_glyph(name, cps, path, adv, stem)
        if name in ('1', 'one.ss02'):
            add_glyph('one.pnum' if name == '1' else 'one.ss02.pnum', [], flush_path, prop_adv, stem + ' (proportional)')
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
    for cp, name, letter in [(0x2103, 'uni2103', 'C'), (0x2109, 'uni2109', 'F')]:  # degree Celsius / Fahrenheit = degree sign + letter, same spacing as typing them
        dW, dH, dshapes = load_svg('degree')
        dpath = combine('degree', dshapes)
        doff = int(round(dW * S))  # zero gap: the letter starts where the ring ends (typed degree + letter keeps the normal 1-cell gap)
        lp = Path(); gs0[letter].draw(TransformPen(lp.getPen(), (1, 0, 0, 1, doff, 0)))
        comp = op(dpath, lp, PathOp.UNION)
        comp.simplify(fix_winding=True, clockwise=True)
        add_glyph(name, [cp], comp, doff + hmtx[letter][0], f'{name} = degree + {letter}')
    for ch in '':  # original digits + additive stars at corner-touch junctions (5 comes from five.svg)
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
            rec.string = '2.200;ShadePixel-Regular'
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    font.save(OUT)
    for r in report:
        print(r)


if __name__ == "__main__":
    main()
