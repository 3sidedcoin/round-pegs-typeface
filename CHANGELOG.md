# Changelog

## 1.030
- Added symbols: sun ☀ and the crescent moons ☾ and ☽ (all 6 cells tall, centred on the capital height; ☽ is ☾ mirrored), the menu bars ≡ (also mapped to ☰), the vertical ellipsis ⋮ and keyboard symbols: the command key ⌘ (6 cells, centred like the sun), tab ⇥ and back-tab ⇤ (⇤ is ⇥ mirrored), and the control caret ⌃ with its opposite ⌄ (the same drawing flipped, sitting at the bottom of the capital height)
- 388 glyphs, 493 characters
- Version bumped so installed copies are replaced

## 1.029
- Kerned Y and V before a period or comma (Y. Y, V. V,) by 2 cells, so the mark tucks under the arm and ends 1 cell from the stem instead of 3 away. T. is unchanged
- Kerned ST by 1 cell: every row of the S was 2 cells from the T, and now sits 1 cell away with the T's bar overhanging the S's top-right corner
- Version bumped so installed copies are replaced

## 1.028
- Gave the short L (`L.short`, used in LL, LLL and LLY) a normal 1-cell gap; it used to run straight into the next L's stem, which looked too close. LL is now 8 cells wide instead of 7 (9 without the rule)
- Version bumped so installed copies are replaced

## 1.027
- Changed the LY kern from -2 cells to -1 cell, so the foot of the L now stops flush against the Y (gap 0, like LV and LT) instead of sliding a cell under it, which looked too close inside words
- Version bumped so installed copies are replaced

## 1.026
- Added a contextual rule for I (part of `calt`): an I with a letter on both sides takes the slim 1-cell I, so PIXEL, BIG and MILLION tighten up, while a standalone I and the first or last letter of a word (I, INK, IN, IT'S) keep their bars. Accented capital Is follow the same rule. `ss05` still forces the slim I everywhere and `calt` off returns every I to the barred form
- Version bumped so installed copies are replaced

## 1.025
- Redrew the numero sign № with a narrower N (4 cells wide instead of 5), so the glyph is 8 cells of ink instead of 9
- Version bumped so installed copies are replaced

## 1.024
- Redrew the cent sign ¢ and the dollar sign $ five cells tall (0 to 5) so they sit level with £ € ¥; both were seven cells tall. The dollar stem is now drawn as notches in the S instead of a stroke that overshoots
- Added proportional figures (`pnum`): the 1 takes a 4-cell advance (ink flush left, one cell of gap) so 11, 2019 and 1,111 close up; the `ss02` alternate 1 has its own proportional form, and `tnum` returns to the tabular 1. The default stays tabular
- 378 glyphs, 482 characters
- Version bumped so installed copies are replaced

## 1.023
- Redrew © ® ª º as small superscript forms that sit above the letters, level with ¹ ² ³ (top at 8 cells): © and ® are 2 cells wide and 3 tall (a bare c and r), ª and º are 3 wide with the underline bar kept as drawn
- Lowered § and ¶ by one cell so they run from one cell below the baseline to six above, matching $ ¢ and Q instead of sitting on the baseline
- Redrew the fractions ½ ¼ ¾ ⅓ ⅔ eight cells tall (they were ten), hanging two cells below the baseline and rising one cell above the caps, with the numerator, slash and denominator spaced so the slash stays readable at small sizes
- Redrew the ellipsis: three one-cell dots with half-cell gaps, four cells wide and on the cell grid (it was 3.5 cells)
- 376 glyphs, 482 characters
- Version bumped so installed copies are replaced

## 1.022
- Added nine more stylistic alternates, each in its own set so they can be mixed: `ss03` alternate B and `ss04` alternate P (square top-left, notched right side, matching `ss01` R), `ss05` slim I (one cell wide), `ss06` narrow Y and `ss07` narrow X (3 cells), `ss08` narrow N (4 cells), `ss09` slashed zero, `ss10` closed four, and `ss11` narrow O (4 cells). The accented forms of I, Y, N and O have alternates too (31 glyphs). Figures in `ss09` and `ss10` stay tabular. The defaults of these letters are unchanged.
- Added contextual spacing, on by default (`calt`): in LL, LLL and LLY every L except the last becomes a 3-cell short L (`L.short`) that runs straight into the next L, and every plain O in a run of two or more Os takes the narrow O (`O.ss11`), so OO is 9 cells instead of 11. Accented L and O keep their normal shapes and spacing. Turn it off with `font-feature-settings: "calt" 0`.
- LY now kerns a further cell (the L's foot slides one cell under the Y's open lower-left); LT and LV are unchanged
- Redrew the default R and B so the three letters share one corner treatment: R's top-left corner cell is now cut out (like P's) and B's top-right corner is now square. Accented R (Ŕ Ř Ŗ) rebuild from the new R. The default P is unchanged.
- Redrew the diagonal arrows ↖ ↗ ↘ ↙ (a smoother stepped diagonal)
- 376 glyphs, 482 characters
- Version bumped so installed copies are replaced

## 1.021
- Added stylistic alternates, each in its own set so they can be mixed: `ss01` alternate R (notched right side) and `ss02` alternate 1 (plain stem with a foot), both designer-drawn. The accented forms of R (Ŕ Ř Ŗ) have alternates too, and the alternate R takes combining marks. The default R and 1 are unchanged.
- Redrew ∂ (partial differential) at cap height: 4 cells wide and 5 tall, sitting on the baseline, instead of 5 wide and running from 1 cell below the baseline to 6 above, so it no longer towers over neighbouring letters
- Refined the default A: the inner curve at the foot of its left leg is now rounded, and every accented A rebuilds from it
- Figures 0–9 are now designer-drawn (sources/svg/zero.svg … nine.svg) with their corner fillets drawn in, replacing the source digits plus computed stars. Shapes are the same except small fillets added at diagonal joins on 0, 2, 4, 5, 6 and 9. Figures stay tabular (5 cells wide each).
- ℃ and ℉ now have no gap between the degree ring and the letter (the letter starts where the ring ends, with the ring sitting above the cap line as usual). Typing ° and C separately keeps the normal 1-cell gap.
- Dashes now step up in width: the en dash is 4 cells (half an em, was 3) and the em dash is 7 cells (a full em with its gap, was 5), so the em dash is clearly wider than the minus (5) and the en dash is wider than the hyphen (2). Both designer-drawn bars on the same height as before.
- Redrew ✓ at cap height: 6 cells wide and 5 tall (was 5 by 4), keeping the same 45° staircase; advance is now 7 cells
- Version bumped so installed copies are replaced

## 1.020
- Redrew S and 5 so they are no longer near-twins: S now has a short, rounded top bar and 5 a flat, full-width top. They differ in three cells instead of two, and the difference sits in the top bar where the eye looks. The accented S letters rebuild from the new S; the superscript and subscript 5 are unchanged.
- The 5 is now a drawn glyph (sources/svg/five.svg) instead of the source digit plus corner stars
- Version bumped so installed copies are replaced

## 1.019
- Added ∆ (U+2206 increment, shared with the Greek capital delta U+0394), ▪ (U+25AA) and Ⓓ (U+24B9), all designer-drawn. ∆ is a 5-cell hollow triangle with the star fillets at its diagonal joins; ▪ is 2×2 cells, centred on the middle of the cap height (half-cell vertical offset); Ⓓ is a 6×7 ring from 1 cell below the baseline to 6 above, with a solid d-shaped letter inside.
- Version bumped so installed copies are replaced

## 1.018
- Added Ω (U+2126 ohm sign and U+03A9 Greek capital omega share one glyph), √ (U+221A), ℮ (U+212E) and ℓ (U+2113), all designer-drawn. Ω, √ and ℮ are 5 cells wide at cap height; ℓ is 4 wide and runs from 1 cell below the baseline to 6 above.
- Version bumped so installed copies are replaced

## 1.017
- Added ∂ ∏ ∑ (U+2202, U+220F, U+2211) and π (U+03C0), designer-drawn; ∂ ∏ ∑ run from 1 cell below the baseline to 6 above and are 5 cells wide, π is cap height
- Added ✓ check mark (U+2713), designer-drawn, 5 cells wide and 4 tall
- The cedilla now hangs from the letter: the mark moved up 1 cell so it joins the base instead of floating 1 cell below it. Applies to Ç Ş Ģ Ķ Ļ Ņ Ŗ Ţ and the spacing and combining cedilla (the comma-below on Ș Ț is unchanged). Ç and the rest descend 1 cell instead of 2.
- Version bumped so installed copies are replaced

## 1.015
- Redrew the degree sign ° as a simplified round ring (4 cells around a hole, the same construction as º); ℃ and ℉ pick it up
- Added ℃ (U+2103) and ℉ (U+2109), composed from the degree sign and C / F with the same spacing as typing them, so pasted text with the combined characters stays in the font. Version bumped so installed copies are replaced.

## 1.014
- Version bumped so installing the new files replaces 1.013 in font managers and design tools
- Simplified the en dash and em dash to plain bars (no decorative pinch); en dash is 3 cells wide, em dash 5
- Added ≠ ≈ ∫ ∞ ⟨ ⟩ and the geometric shapes ■ □ ▲ ▴ ▶ ▸ ▼ ▾ ◀ ◂ ◆ ◇ ◊ (19 glyphs). ≠ and ≈ were re-fitted to the cell grid; ▶ ▸ ▾ ◀ ◂ are rotations and flips of the drawn triangles. Hollow triangles are intentionally not included.
- Added ′ ″ prime and double prime (U+2032-2033), as separate glyphs sharing the straight-quote outlines; they can be redrawn slanted later without other changes
- Added ↔ ↕ (U+2194-2195), ⅓ ⅔ (U+2153-2154), ⁄ fraction slash (U+2044), ‖ double vertical line (U+2016) and № (U+2116), all designer-drawn; ↕ and ⁄ ‖ run from 1 cell below the baseline to 6 above
- Added ↖ ↗ ↘ ↙ (U+2196-2199), designer-drawn diagonal arrows, 4 cells wide and 5 tall

## 1.013
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
