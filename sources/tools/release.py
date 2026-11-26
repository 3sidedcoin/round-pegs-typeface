"""Release pass: takes the build.py output and produces the OFL release files.
Usage: python3 -I release.py "Family Name" [version]
Does: sliver cleanup, valid glyph names, nbspace, OFL name records, metrics, OTF + TTF + WOFF2 + WOFF.
"""
import os, sys, math
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.roundingPen import RoundingPen
from fontTools.agl import UV2AGL
import unicodedata
sys.path.insert(0, '/home/claude/work')
import build as B

SRC = '/home/claude/work/out/ShadePixel-Regular.otf'
FAMILY = sys.argv[1]
VERSION = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
REPO = sys.argv[3] if len(sys.argv) > 3 else 'https://github.com/3sidedcoin/' + FAMILY.lower().replace(' ', '-')
PS = FAMILY.replace(' ', '') + '-Regular'
OUTDIR = '/home/claude/work/release/' + FAMILY.replace(' ', '')
MIN_SEG = 8          # units; the grid cell is 140, so nothing legitimate is this short
YEAR = 2026

font = TTFont(SRC)
cff = font['CFF '].cff
top = cff.topDictIndex[0]
private, gsubrs = top.Private, cff.GlobalSubrs
gs = font.getGlyphSet()
order = font.getGlyphOrder()


def clean(rec, tol=MIN_SEG):
    """Drop line/curve segments whose chord is shorter than tol (slivers left where stars meet rounded corners)."""
    out, cur, start, dropped = [], None, None, 0
    for op_, args in rec:
        if op_ == 'moveTo':
            cur = start = args[0]; out.append((op_, args))
        elif op_ in ('lineTo', 'curveTo'):
            end = args[-1]
            if math.dist(cur, end) < tol:
                dropped += 1; continue
            out.append((op_, args)); cur = end
        else:
            out.append((op_, args))
    return out, dropped


total_dropped = 0
for name in order:
    rp = RecordingPen(); gs[name].draw(rp)
    cleaned, n = clean(rp.value)
    if n:
        total_dropped += n
        pen = T2CharStringPen(font['hmtx'][name][0], None)
        for op_, args in cleaned:
            getattr(pen, op_)(*args)
        top.CharStrings[name] = pen.getCharString(private, gsubrs)
print('slivers dropped:', total_dropped)

# --- math signs: give < > the same 840 advance as + = x / (ink centred) -----------------------------------
from fontTools.pens.transformPen import TransformPen
for name in ('less', 'greater'):
    rp = RecordingPen(); gs[name].draw(rp)
    pen = T2CharStringPen(840, None)
    rp.replay(TransformPen(pen, (1, 0, 0, 1, 70, 0)))
    top.CharStrings[name] = pen.getCharString(private, gsubrs)
    adv_, lsb_ = font['hmtx'].metrics[name]
    font['hmtx'].metrics[name] = (840, lsb_ + 70)

# --- valid glyph names for the digits -----------------------------------------------------------
digits = dict(zip('0123456789', 'zero one two three four five six seven eight nine'.split()))
for old, new in digits.items():
    i = order.index(old); order[i] = new
    top.CharStrings.charStrings[new] = top.CharStrings.charStrings.pop(old)
    font['hmtx'].metrics[new] = font['hmtx'].metrics.pop(old)
    for t in font['cmap'].tables:
        for cp, g in list(t.cmap.items()):
            if g == old: t.cmap[cp] = new
if top.charset is not order:
    top.charset[:] = order
font.setGlyphOrder(order)

# --- no-break space ------------------------------------------------------------------------------
font['hmtx'].metrics['space'] = (3 * 140, 0)   # word space: 3 cells (was 4); 1-cell side bearing + 3 + 0 = 4 cells between words
adv = font['hmtx']['space'][0]
if 'nbspace' not in order:
    pen = T2CharStringPen(adv, None)
    top.CharStrings.charStringsIndex.append(pen.getCharString(private, gsubrs))
    top.CharStrings.charStrings['nbspace'] = len(top.CharStrings.charStringsIndex) - 1
    order.append('nbspace')
    if top.charset is not order: top.charset.append('nbspace')
    font['hmtx'].metrics['nbspace'] = (adv, 0)
    font.setGlyphOrder(order)
for t in font['cmap'].tables:
    if t.isUnicode(): t.cmap[0xA0] = 'nbspace'


# --- accented capitals: base cap + mark. Marks are anchored on their FRAME centre (frame centre -> letter centre),
#     ogonek on its frame's right edge (-> letter's right ink edge). Half-cell offsets are expected and deliberate. ----
from pathops import Path as PPath, PathOp as POp, op as pop
MARKS = {0x300: 'mark-grave', 0x301: 'mark-acute', 0x302: 'mark-circumflex', 0x303: 'mark-tilde', 0x308: 'mark-diaeresis',
         0x304: 'mark-macron', 0x306: 'mark-breve', 0x307: 'mark-dot-above', 0x30B: 'mark-double-acute', 0x30C: 'mark-caron', 0x30A: 'mark-ring',
         0x326: 'mark-comma-below', 0x327: 'mark-cedilla', 0x328: 'mark-ogonek'}
ANCHOR_RIGHT = {0x328}
mark_data = {}
for mcp, stem in MARKS.items():
    W_, H_, shapes = B.load_svg(stem)
    mp = B.combine(stem, shapes)
    mark_data[mcp] = (mp, W_ * 35)
cmap_t = [t for t in font['cmap'].tables if t.isUnicode()]
cm0 = font.getBestCmap()
composed = []
for cp in list(range(0xC0, 0x250)) + [0x1E80, 0x1E82, 0x1E84, 0x1EF2, 0x1EBC]:
    ch = chr(cp)
    if not ch.isupper(): continue
    d = unicodedata.normalize('NFD', ch)
    if not (len(d) == 2 and ('A' <= d[0] <= 'Z' or d[0] in '\u00d8\u01b7') and ord(d[1]) in MARKS): continue
    base = cm0[ord(d[0])]
    adv_b, lsb_b = font['hmtx'][base]
    bb = BoundsPen(gs); gs[base].draw(bb)
    mp, fw = mark_data[ord(d[1])]
    if ord(d[1]) in ANCHOR_RIGHT:
        dx = bb.bounds[2] - fw
    else:
        dx = (adv_b - 140) / 2 - fw / 2
    dx = int(round(dx / 35)) * 35
    assert dx % 70 == 0, (ch, dx)
    gname = UV2AGL.get(cp, f'uni{cp:04X}')
    bp_ = PPath(); gs[base].draw(bp_.getPen())
    mk = PPath(); mp.draw(TransformPen(mk.getPen(), (1, 0, 0, 1, dx, 0)))
    res = pop(bp_, mk, POp.UNION); res.simplify(fix_winding=True, clockwise=True)
    rr = RecordingPen(); res.draw(rr)
    pen = T2CharStringPen(adv_b, None)
    for op_, args in clean(rr.value)[0]:
        getattr(pen, op_)(*args)
    top.CharStrings.charStringsIndex.append(pen.getCharString(private, gsubrs))
    top.CharStrings.charStrings[gname] = len(top.CharStrings.charStringsIndex) - 1
    order.append(gname)
    if top.charset is not order: top.charset.append(gname)
    rb = BoundsPen(None); res.draw(rb)
    font['hmtx'].metrics[gname] = (adv_b, int(rb.bounds[0]))
    for t in cmap_t:
        t.cmap[cp] = gname
        lc = ch.lower()
        if len(lc) == 1: t.cmap[ord(lc)] = gname
    composed.append((ch, dx))
# --- stylistic sets: accented capitals rebuilt on the alternate bases (R = ss01); reached through GSUB, no cmap entries ----
ALT_BASE = {'R': ('R.ss01', 'ss01'), 'B': ('B.ss03', 'ss03'), 'P': ('P.ss04', 'ss04'), 'I': ('I.ss05', 'ss05'), 'Y': ('Y.ss06', 'ss06'), 'X': ('X.ss07', 'ss07'), 'N': ('N.ss08', 'ss08'), 'O': ('O.ss11', 'ss11')}
SS_PAIRS = {'ss01': [('R', 'R.ss01')], 'ss02': [('one', 'one.ss02')], 'ss03': [('B', 'B.ss03')], 'ss04': [('P', 'P.ss04')], 'ss05': [('I', 'I.ss05')],
            'ss06': [('Y', 'Y.ss06')], 'ss07': [('X', 'X.ss07')], 'ss08': [('N', 'N.ss08')], 'ss09': [('zero', 'zero.ss09')], 'ss10': [('four', 'four.ss10')], 'ss11': [('O', 'O.ss11')]}
SS_NAMES = {'ss01': 'Alternate R', 'ss02': 'Alternate 1', 'ss03': 'Alternate B', 'ss04': 'Alternate P', 'ss05': 'Slim I', 'ss06': 'Narrow Y', 'ss07': 'Narrow X',
            'ss08': 'Narrow N', 'ss09': 'Slashed zero', 'ss10': 'Closed four', 'ss11': 'Narrow O'}
for cp in list(range(0xC0, 0x250)) + [0x1E80, 0x1E82, 0x1E84, 0x1EF2, 0x1EBC]:
    ch = chr(cp)
    if not ch.isupper(): continue
    d = unicodedata.normalize('NFD', ch)
    if not (len(d) == 2 and d[0] in ALT_BASE and ord(d[1]) in MARKS): continue
    base, ss = ALT_BASE[d[0]]
    adv_b, lsb_b = font['hmtx'][base]
    bb = BoundsPen(gs); gs[base].draw(bb)
    mp, fw = mark_data[ord(d[1])]
    if ord(d[1]) in ANCHOR_RIGHT:
        dx = bb.bounds[2] - fw
    else:
        dx = (adv_b - 140) / 2 - fw / 2
    dx = int(round(dx / 35)) * 35
    plain = UV2AGL.get(cp, f'uni{cp:04X}')
    gname = f'{plain}.{ss}'
    bp_ = PPath(); gs[base].draw(bp_.getPen())
    mk = PPath(); mp.draw(TransformPen(mk.getPen(), (1, 0, 0, 1, dx, 0)))
    res = pop(bp_, mk, POp.UNION); res.simplify(fix_winding=True, clockwise=True)
    rr = RecordingPen(); res.draw(rr)
    pen = T2CharStringPen(adv_b, None)
    for op_, args in clean(rr.value)[0]:
        getattr(pen, op_)(*args)
    top.CharStrings.charStringsIndex.append(pen.getCharString(private, gsubrs))
    top.CharStrings.charStrings[gname] = len(top.CharStrings.charStringsIndex) - 1
    order.append(gname)
    if top.charset is not order: top.charset.append(gname)
    rb = BoundsPen(None); res.draw(rb)
    font['hmtx'].metrics[gname] = (adv_b, int(rb.bounds[0]))
    SS_PAIRS[ss].append((plain, gname))
font.setGlyphOrder(order)
print('composed', len(composed), 'accented capitals; half-cell offsets:', sum(1 for _, dx in composed if dx % 140))
print(''.join(c for c, _ in composed))


# --- spacing accents and combining marks (the combining ones attach through GPOS, anchored like the composed glyphs) ----
SPACING = {0xA8: 0x308, 0xB4: 0x301, 0xAF: 0x304, 0xB8: 0x327, 0x2C6: 0x302, 0x2C7: 0x30C, 0x2D8: 0x306, 0x2D9: 0x307,
           0x2DA: 0x30A, 0x2DB: 0x328, 0x2DC: 0x303, 0x2DD: 0x30B}
COMB = []   # (glyph name, frame width in font units, right-anchored?)
COMB_NAME = {}
def put_mark_glyph(gname, cp_list, mp, fw, adv):
    rr = RecordingPen(); mp.draw(rr)
    pen = T2CharStringPen(adv, None)
    for op_, args in clean(rr.value)[0]:
        getattr(pen, op_)(*args)
    top.CharStrings.charStringsIndex.append(pen.getCharString(private, gsubrs))
    top.CharStrings.charStrings[gname] = len(top.CharStrings.charStringsIndex) - 1
    order.append(gname)
    if top.charset is not order: top.charset.append(gname)
    rb = BoundsPen(None); mp.draw(rb)
    font['hmtx'].metrics[gname] = (adv, int(rb.bounds[0]))
    for t in cmap_t:
        for c in cp_list: t.cmap[c] = gname
def uniq(cp, suffix):
    n = UV2AGL.get(cp, f'uni{cp:04X}')
    return n if n not in order else f'uni{cp:04X}{suffix}'
for scp, mcp in SPACING.items():
    mp, fw = mark_data[mcp]
    put_mark_glyph(uniq(scp, '.spc'), [scp], mp, fw, int(fw) + 140)
for mcp, (mp, fw) in mark_data.items():
    gname = uniq(mcp, '.cmb') if UV2AGL.get(mcp, '') not in order else f'uni{mcp:04X}'
    put_mark_glyph(gname, [mcp], mp, fw, 0)
    COMB.append((gname, fw, mcp in ANCHOR_RIGHT)); COMB_NAME[mcp] = (gname, fw)
font.setGlyphOrder(order)
BASES = [cm0[c] for c in range(65, 91)] + [a for a, _ in (v for v in ALT_BASE.values())]
cm1 = font.getBestCmap()
OGON_BASES = [cm1[c] for c in (0x104, 0x118, 0x12E, 0x172)]      # Lithuanian: ogonek below, tone mark above
RAISED_BASES = [cm1[c] for c in (0x116, 0x130, 0x16A)]                  # Lithuanian: dot above, tone mark stacked over it
STACK = 2 * 128   # 2 cells up: the dot is 1 cell tall, plus a 1-cell gap, matches the cap-to-mark gap

# --- derived glyphs: dotless i/j (caps-only font: aliases), minus, low quotes, dotted circle --------------------------
for cp_, src_ in ((0x131, 'I'), (0x237, 'J')):
    for t in cmap_t: t.cmap[cp_] = cm0[ord(src_)]
def gpath(n):
    p_ = PPath(); gs[n].draw(p_.getPen()); return p_
def rect_path(x0, y0, x1, y1):
    p_ = PPath(); pn = p_.getPen(); pn.moveTo((x0, y0)); pn.lineTo((x1, y0)); pn.lineTo((x1, y1)); pn.lineTo((x0, y1)); pn.closePath(); return p_
plus = gpath(cm0[ord('+')]); pb_ = BoundsPen(None); plus.draw(pb_); pbd = pb_.bounds; yc = (pbd[1] + pbd[3]) / 2
minus = pop(plus, rect_path(pbd[0] - 10, yc - 70, pbd[2] + 10, yc + 70), POp.INTERSECTION); minus.simplify(fix_winding=True, clockwise=True)
put_mark_glyph('minus', [0x2212], minus, 0, font['hmtx'][cm0[ord('+')]][0])
qd = gpath(cm0[0x201D]); cmm = gpath(cm0[ord(',')])
qb = BoundsPen(None); qd.draw(qb); cb = BoundsPen(None); cmm.draw(cb)
low = PPath(); qd.draw(TransformPen(low.getPen(), (1, 0, 0, 1, 0, cb.bounds[1] - qb.bounds[1])))
put_mark_glyph('quotedblbase', [0x201E], low, 0, font['hmtx'][cm0[0x201D]][0])
for t in cmap_t: t.cmap[0x201A] = cm0[ord(',')]   # single low-9 quote = comma
# --- extra letters for language coverage: long s, modifier turned comma/apostrophe, IJ ligature, L with middle dot ----------
for t in cmap_t:
    t.cmap[0x17F] = cm0[ord('S')]; t.cmap[0x2BB] = cm0[0x2018]; t.cmap[0x2BC] = cm0[0x27]
def shifted(n, dx):
    q_ = PPath(); gs[n].draw(TransformPen(q_.getPen(), (1, 0, 0, 1, dx, 0))); return q_
for gname_, cps_, a_, b_ in (('IJ', [0x132, 0x133], cm0[ord('I')], cm0[ord('J')]), ('Ldot', [0x13F, 0x140], cm0[ord('L')], cm0[0xB7])):
    adv_a = font['hmtx'][a_][0]; adv_ab = adv_a + font['hmtx'][b_][0]
    u_ = pop(gpath(a_), shifted(b_, adv_a), POp.UNION); u_.simplify(fix_winding=True, clockwise=True)
    put_mark_glyph(gname_, cps_, u_, 0, adv_ab)
dc = PPath()
for i_ in (0, 2, 4):
    for j_ in (0, 2, 4):
        if (i_, j_) == (2, 2): continue
        parse_p = B.parse_path; parse_p(B.rect_d(i_ * 140, j_ * 140, 140, 140, 35), dc.getPen())
dc.simplify(fix_winding=True, clockwise=True)
put_mark_glyph('uni25CC', [0x25CC], dc, 0, 840)
BASES.append('uni25CC')
font.setGlyphOrder(order)

# --- names / licence -------------------------------------------------------------------------------
ver = f'{VERSION:.3f}'
names = {
    0: f'Copyright {YEAR} The {FAMILY} Project Authors ({REPO})',
    1: FAMILY, 2: 'Regular',
    3: f'{ver};3SDC;{PS}',
    4: f'{FAMILY} Regular',
    5: f'Version {ver}',
    6: PS,
    8: '3 Sided Coin', 9: 'Tejas', 10: 'A pixel typeface of rounded cells, originally made for the game Shade, Shade, Hide!!!', 11: 'https://3sided.co.in', 12: 'https://3sided.co.in',
    13: 'This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org',
    14: 'https://openfontlicense.org',
}
nt = font['name']
nt.names = [r for r in nt.names if r.platformID == 3 and r.nameID not in names and r.nameID not in (7, 16, 17, 21, 22, 25)]
cff.fontNames[0] = PS
top.FullName, top.FamilyName = f'{FAMILY} Regular', FAMILY
for i, s in names.items():
    nt.setName(s, i, 3, 1, 0x409)
font['meta'] = newTable('meta'); font['meta'].data = {'dlng': 'Latn', 'slng': 'Latn'}
font['head'].fontRevision = VERSION
font['OS/2'].achVendID = '3SDC'
font['OS/2'].fsType = 0
font['OS/2'].fsSelection = (font['OS/2'].fsSelection & ~0b1) | (1 << 7) | (1 << 6)


def scale_font(path, to_upm=1024, from_cell=140):
    """Rescale so the cell is a power-of-two number of units: 128 of 1024. A half cell (64) then lands on whole pixels at 16px multiples."""
    k = (to_upm / 8) / from_cell
    f = TTFont(path); cf = f['CFF '].cff; tp = cf.topDictIndex[0]; pr = tp.Private; gsb = cf.GlobalSubrs
    g = f.getGlyphSet()
    for n in f.getGlyphOrder():
        w, lsb = f['hmtx'][n]
        rp = RecordingPen(); g[n].draw(rp)
        nw = round(w * k)
        pen = T2CharStringPen(nw, None)
        rp.replay(TransformPen(RoundingPen(pen), (k, 0, 0, k, 0, 0)))
        tp.CharStrings[n] = pen.getCharString(pr, gsb)
        f['hmtx'].metrics[n] = (nw, round(lsb * k))
    f['head'].unitsPerEm = to_upm
    tp.FontMatrix = [1 / to_upm, 0, 0, 1 / to_upm, 0, 0]
    tp.rawDict['FontMatrix'] = tp.FontMatrix
    bp_all = []
    g2 = None
    o, h, p = f['OS/2'], f['hhea'], f['post']
    cell = to_upm // 8
    h.ascent, h.descent, h.lineGap = 8 * cell, -3 * cell, 0   # 8 cells up covers the accents; 1 cell down covers Q and the descender marks
    o.sTypoAscender, o.sTypoDescender, o.sTypoLineGap = 8 * cell, -3 * cell, 0
    o.sCapHeight = o.sxHeight = 5 * cell
    for a in ('ySubscriptXSize', 'ySubscriptYSize', 'ySubscriptXOffset', 'ySubscriptYOffset', 'ySuperscriptXSize',
              'ySuperscriptYSize', 'ySuperscriptXOffset', 'ySuperscriptYOffset', 'yStrikeoutSize', 'yStrikeoutPosition'):
        setattr(o, a, round(getattr(o, a) * k))
    p.underlinePosition, p.underlineThickness = round(p.underlinePosition * k), round(p.underlineThickness * k)
    f.save(path)
    f = TTFont(path)
    ys = []
    g = f.getGlyphSet()
    for n in f.getGlyphOrder():
        bp = BoundsPen(g); g[n].draw(bp)
        if bp.bounds: ys += [bp.bounds[1], bp.bounds[3]]
    f['OS/2'].usWinAscent, f['OS/2'].usWinDescent = int(max(ys)) + STACK, int(-min(ys))
    f['OS/2'].recalcAvgCharWidth(f)
    f.save(path)
    return k


def _calt_text(font):
    """calt: L before L -> L.short; O runs -> narrow O; I with a letter on both sides -> slim I (ss05 form)."""
    import unicodedata
    cm = font.getBestCmap()
    alpha = {g for cp, g in cm.items() if chr(cp).isalpha()}
    letters = sorted(g for g in font.getGlyphOrder() if g.split('.')[0] in alpha)
    ipairs = [(g, g + '.ss05') for g in ('I', 'Igrave', 'Iacute', 'Icircumflex', 'Idieresis', 'Itilde', 'Imacron', 'Ibreve', 'Iogonek', 'Idotaccent')
              if g in font.getGlyphOrder() and g + '.ss05' in font.getGlyphOrder()]
    out = '@LETTER = [' + ' '.join(letters) + '];\n'
    out += "feature calt {\n  sub L' L by L.short;\n  sub O' O by O.ss11;\n  sub O.ss11 O' by O.ss11;\n"
    out += ''.join(f"  sub @LETTER {a}' @LETTER by {b};\n" for a, b in ipairs)
    return out + '} calt;'

def add_mark_gpos(path):
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    f = TTFont(path); k = 128 / 140
    h = f['hmtx']; gl = f.getGlyphSet(); lines = []
    for g, fw, right in COMB:
        lines.append(f"markClass {g} <anchor {round(fw * k) if right else round(fw * k / 2)} 0> @{'RIGHT' if right else 'TOP'};")
    lines.append('feature mark {')
    for b in BASES:
        adv = h[b][0]
        bb = BoundsPen(gl); gl[b].draw(bb)
        lines.append(f'  pos base {b} <anchor {(adv - 128) // 2} 0> mark @TOP;')
        lines.append(f'  pos base {b} <anchor {int(bb.bounds[2])} 0> mark @RIGHT;')
    for b in OGON_BASES:
        adv = h[b][0]; bb = BoundsPen(gl); gl[b].draw(bb)
        lines.append(f'  pos base {b} <anchor {(adv - 128) // 2} 0> mark @TOP;')
        lines.append(f'  pos base {b} <anchor {int(bb.bounds[2])} 0> mark @RIGHT;')
    for b in RAISED_BASES:
        adv = h[b][0]; bb = BoundsPen(gl); gl[b].draw(bb)
        lines.append(f'  pos base {b} <anchor {(adv - 128) // 2} {STACK}> mark @TOP;')
        lines.append(f'  pos base {b} <anchor {int(bb.bounds[2])} 0> mark @RIGHT;')
    lines.append('} mark;')
    dg, dfw = COMB_NAME[0x307]
    lines.append('feature mkmk {')
    lines.append(f'  pos mark {dg} <anchor {round(dfw * k / 2)} {STACK}> mark @TOP;')
    lines.append('} mkmk;')
    for tag, nm in SS_NAMES.items():
        lines.append(f'feature {tag} {{\n  featureNames {{ name "{nm}"; }};')
        lines += [f'  sub {a} by {b};' for a, b in SS_PAIRS[tag]]
        lines.append(f'}} {tag};')
    # figures are tabular by default; pnum gives the 1 a 4-cell advance (ink + 1 cell) so runs like 11 and 2019 close up. It is listed after
    # the stylistic sets so ss02 + pnum picks the proportional alternate 1. tnum returns to the tabular figures.
    lines.append('feature pnum {\n  sub one by one.pnum;\n  sub one.ss02 by one.ss02.pnum;\n} pnum;')
    lines.append('feature tnum {\n  sub one.pnum by one;\n  sub one.ss02.pnum by one.ss02;\n} tnum;')
    # contextual spacing (default-on): L before L takes the 3-cell L.short (normal 1-cell gap, so LL/LLL/LLY are one cell shorter than with the full L); every O in a run of
    # two or more Os takes the narrow O (O.ss11). Plain L and O only - accented forms keep their normal shapes and spacing.
    lines.append(_calt_text(f))
    _kp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kern.fea')
    if os.path.exists(_kp):
        lines.append(open(_kp).read())
    addOpenTypeFeaturesFromString(f, '\n'.join(lines))
    f.save(path)

os.makedirs(OUTDIR, exist_ok=True)
otf_path = f'{OUTDIR}/{PS}.otf'
font['OS/2'].recalcUnicodeRanges(font)
font.save(otf_path)
print('scale', scale_font(otf_path))
add_mark_gpos(otf_path)

# --- TrueType build (Google Fonts takes TTF) ----------------------------------------------------------
f2 = TTFont(otf_path)
gs2 = f2.getGlyphSet()
glyf = newTable('glyf'); glyf.glyphOrder = f2.getGlyphOrder(); glyf.glyphs = {}
for gn in f2.getGlyphOrder():
    tp = TTGlyphPen(gs2)
    gs2[gn].draw(Cu2QuPen(tp, 0.5, reverse_direction=False, all_quadratic=True))
    glyf.glyphs[gn] = tp.glyph()
del f2['CFF ']
if 'VORG' in f2: del f2['VORG']
f2['glyf'] = glyf
f2['loca'] = newTable('loca')
maxp = f2['maxp']; maxp.tableVersion = 0x00010000
for a in ('maxZones', 'maxTwilightPoints', 'maxStorage', 'maxFunctionDefs', 'maxInstructionDefs',
          'maxStackElements', 'maxSizeOfInstructions', 'maxComponentElements'):
    setattr(maxp, a, 0)
maxp.maxZones = 1; maxp.maxComponentDepth = 0
f2['head'].glyphDataFormat = 0
f2['post'].formatType = 2.0
f2['post'].extraNames = []; f2['post'].mapping = {}
f2['post'].glyphOrder = f2.getGlyphOrder()
f2['gasp'] = newTable('gasp'); f2['gasp'].version = 1; f2['gasp'].gaspRange = {0xFFFF: 0x000F}
prep = newTable('prep'); from fontTools.ttLib.tables import ttProgram
prog = ttProgram.Program(); prog.fromBytecode(bytes([0xB8, 0x01, 0xFF, 0x85, 0xB0, 0x04, 0x8D]))  # smart dropout: SCANCTRL 511, SCANTYPE 4
prep.program = prog; f2['prep'] = prep
f2.sfntVersion = '\x00\x01\x00\x00'
ttf_path = f'{OUTDIR}/{PS}.ttf'
f2.save(ttf_path)

# --- web fonts --------------------------------------------------------------------------------------------
for flavor in ('woff2', 'woff'):
    w = TTFont(ttf_path); w.flavor = flavor
    w.save(f'{OUTDIR}/{PS}.{flavor}')
print('built', PS, ver, os.listdir(OUTDIR))
