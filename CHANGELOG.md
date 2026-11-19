# Changelog

## 1.013
- Added ′ ″ prime and double prime (U+2032-2033), as separate glyphs sharing the straight-quote outlines; they can be redrawn slanted later without other changes
- Added ↔ ↕ (U+2194-2195), ⅓ ⅔ (U+2153-2154), ⁄ fraction slash (U+2044), ‖ double vertical line (U+2016) and № (U+2116), all designer-drawn; ↕ and ⁄ ‖ run from 1 cell below the baseline to 6 above
- Added ↖ ↗ ↘ ↙ (U+2196-2199), designer-drawn diagonal arrows, 4 cells wide and 5 tall
- Added µ ¬ † ‡ ƒ ‰ (U+00B5, U+00AC, U+2020, U+2021, U+0192, U+2030), designer-drawn: Windows-1252 is now complete
- Added ⁰ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ (U+2070, U+2074-2079) and ₀-₉ (U+2080-2089), designer-drawn; superscripts are 3 cells wide and 4 tall, subscripts reuse the same outlines, 2 cells below the baseline to 2 above
- Added ¦ broken bar (U+00A6) and ¤ currency sign (U+00A4); redrew %
- Fractions use the new ¹ numerator with a full-width foot; ¹ redrawn to match
- Added ¼ ½ ¾ (U+00BC-00BE), designer-drawn; they run from 2 cells below the baseline to 1 em
- Redrew ± to fit cap height (5 cells), plus above minus
- Added superscripts ¹ ² ³ (U+00B9, U+00B2, U+00B3), raised 3 cells above the baseline and reaching 1 em, 4 cells tall and 3 wide
- Added ± (designer-drawn)
- Kerning for three pairs only: LV, LY and LT move in by 1 cell so they sit flush (all other pairs keep the default 1-cell gap)
- Word space reduced from 4 to 3 cells
- Design rules for widths and spacing documented in `documentation/DESIGN.md`

## 1.012
- Lithuanian and dictionary tone marks: acute, grave and tilde now attach to Ą Ę Į Ų Ė İ Ū; over Ė, İ and Ū (and i + dot above) the second mark stacks two cells higher via GPOS mark and mkmk. No new drawings. Stacked marks reach 1.25 em above the baseline (above the 1.0 em ascender); vertical metrics are unchanged, usWinAscent raised to cover them.

## 1.011
- Added Ŋ ŋ Ŧ ŧ Ǥ ǥ Ʒ ʒ Ǯ ǯ (designer-drawn Ŋ, Ŧ, Ǥ, Ʒ; Ǯ composed) for Sami, Finnish and Norwegian coverage

## 1.010
- Name table: added description (nameID 10) noting origin in the game Shade, Shade, Hide!!!; designer and vendor URL https://3sided.co.in
- README, description and article now state the origin

## 1.009
- Renamed the family from Edge Case to Round Pegs

## 1.009 (source)
- Added UFO source (sources/RoundPegs-Regular.ufo), fontmake build, config.yaml

## 1.009
- Added Ǿ ǿ Ẽ ẽ ſ ʻ ʼ Ĳ ĳ Ŀ ŀ for language coverage (FontBakery: 0 FAIL, 0 ERROR)

## 1.007
- Copyright record points to the real repo; added Google Fonts packaging drafts

## 1.006
- Redrawn ª

## 1.005
- Added © ® ª º; all Google Fonts required codepoints now covered

## 1.004
- New ¶ with a visible bowl

## 1.003
- Added § ¶ « » ‹ › °

## 1.002
- New ẞ: open middle

## 1.001
- Renamed to Round Pegs; added accented Latin, extra letters, marks
