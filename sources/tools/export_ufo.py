"""Export the finished OTF to a UFO source (outlines, metrics, names, mark feature)."""
import sys
from fontTools.ttLib import TTFont
import ufoLib2

SRC, DST = sys.argv[1], sys.argv[2]
f = TTFont(SRC); gs = f.getGlyphSet(); cmap = f.getBestCmap()
rev = {}
for cp, g in cmap.items(): rev.setdefault(g, []).append(cp)

u = ufoLib2.Font()
i = u.info
i.familyName = f['name'].getDebugName(1); i.styleName = 'Regular'
i.unitsPerEm = 1024; i.ascender = 1024; i.descender = -384
i.capHeight = 640; i.xHeight = 640
i.versionMajor = 1; i.versionMinor = int(round((f['head'].fontRevision % 1) * 1000))
i.copyright = f['name'].getDebugName(0)
i.openTypeNameDesigner = 'Tejas'
i.openTypeNameDescription = f['name'].getDebugName(10)
i.openTypeNameDesignerURL = 'https://3sided.co.in'
i.openTypeNameManufacturer = '3 Sided Coin'
i.openTypeNameManufacturerURL = 'https://3sided.co.in'
i.openTypeNameLicense = f['name'].getDebugName(13)
i.openTypeNameLicenseURL = 'https://openfontlicense.org'
i.openTypeOS2VendorID = '3SDC'
i.openTypeOS2WeightClass = 400
i.openTypeOS2Type = [] 
i.openTypeOS2TypoAscender = 1024; i.openTypeOS2TypoDescender = -384; i.openTypeOS2TypoLineGap = 0
i.openTypeOS2WinAscent = f['OS/2'].usWinAscent; i.openTypeOS2WinDescent = f['OS/2'].usWinDescent
i.openTypeHheaAscender = 1024; i.openTypeHheaDescender = -384; i.openTypeHheaLineGap = 0
i.openTypeOS2Selection = [7]
i.postscriptUnderlinePosition = f['post'].underlinePosition; i.postscriptUnderlineThickness = f['post'].underlineThickness
i.openTypeGaspRangeRecords = [{'rangeMaxPPEM': 65535, 'rangeGaspBehavior': [0, 1, 2, 3]}]

order = f.getGlyphOrder()
for gn in order:
    g = u.newGlyph(gn)
    g.width = f['hmtx'][gn][0]
    g.unicodes = sorted(rev.get(gn, []))
    gs[gn].draw(g.getPen())
u.lib['public.glyphOrder'] = list(order)

# --- mark feature, read back from the font's GPOS -------------------------------------------------------
gpos = f['GPOS'].table
sub = gpos.LookupList.Lookup[0].SubTable[0]
marks = sub.MarkCoverage.glyphs; bases = sub.BaseCoverage.glyphs
cls_marks = {}
for gname, rec in zip(marks, sub.MarkArray.MarkRecord):
    cls_marks.setdefault(rec.Class, []).append((gname, rec.MarkAnchor.XCoordinate, rec.MarkAnchor.YCoordinate))
right = [c for c, v in cls_marks.items() if any(g == 'uni0328' for g, _, _ in v)]
names = {c: ('RIGHT' if c in right else 'TOP') for c in cls_marks}
fea = []
for c, v in cls_marks.items():
    for g, x, y in v:
        fea.append(f'markClass {g} <anchor {x} {y}> @{names[c]};')
fea.append('')
fea.append('feature mark {')
for b, br in zip(bases, sub.BaseArray.BaseRecord):
    for c in sorted(cls_marks):
        a = br.BaseAnchor[c]
        fea.append(f'  pos base {b} <anchor {a.XCoordinate} {a.YCoordinate}> mark @{names[c]};')
fea.append('} mark;')
fea.append('')
# mark-to-mark (tone marks stacked over a dot above)
mk_sub = gpos.LookupList.Lookup[1].SubTable[0]
assert gpos.LookupList.Lookup[1].LookupType == 6
fea.append('feature mkmk {')
for g2, rec2 in zip(mk_sub.Mark2Coverage.glyphs, mk_sub.Mark2Array.Mark2Record):
    for a2 in rec2.Mark2Anchor:
        if a2 is not None:
            fea.append(f'  pos mark {g2} <anchor {a2.XCoordinate} {a2.YCoordinate}> mark @TOP;')
fea.append('} mkmk;')
fea.append('')
gd = f['GDEF'].table.GlyphClassDef.classDefs
mk = [g for g in order if gd.get(g) == 3]; bs = [g for g in order if gd.get(g) == 1]
fea.append('table GDEF {')
fea.append('  GlyphClassDef [' + ' '.join(bs) + '], , [' + ' '.join(mk) + '], ;')
fea.append('} GDEF;')
# stylistic set 1 (alternate R and 1), read back from GSUB
if 'GSUB' in f:
    gsub = f['GSUB'].table
    for fr in gsub.FeatureList.FeatureRecord:
        if fr.FeatureTag == 'ss01':
            fea.append('feature ss01 {')
            fea.append('  featureNames { name "Alternate R and 1"; };')
            for li in fr.Feature.LookupListIndex:
                for st in gsub.LookupList.Lookup[li].SubTable:
                    for a_, b_ in st.mapping.items():
                        fea.append(f'  sub {a_} by {b_};')
            fea.append('} ss01;')
            fea.append('')
import os
kp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kern.fea')
if os.path.exists(kp):
    fea.append(open(kp).read())
u.features.text = '\n'.join(fea) + '\n'
u.save(DST, overwrite=True)
print(len(order), 'glyphs;', len(mk), 'marks;', len(bases), 'bases')
