# Round Pegs

![Round Pegs specimen](documentation/specimen.png)

**Round Pegs** is a free, open-source pixel typeface with rounded cells and concave
fillets where cells join diagonally. It is drawn on a grid of whole and half cells,
so it stays crisp at 16px multiples. It is a capitals-only design: lowercase letters
map to the same shapes.

Designed by Tejas at [3 Sided Coin](https://3sided.co.in). Originally made for the game *Shade, Shade, Hide!!!*, then extended and released as a free, open typeface.

## Coverage

**Version 1.019: 330 glyphs, 482 characters.** Latin Core and Latin Kernel in full, and 76 of the 110 glyphs in Google Fonts' optional Latin Plus set. The history of what was added is in [CHANGELOG.md](CHANGELOG.md).

- **Latin:** the Google Fonts Latin Core and Latin Kernel sets in full, and all of Windows-1252. Accented capitals are composed from consistent marks, with combining marks positioned through OpenType `mark`. Covers about 350 Latin-script languages (shaperglot), including Finnish, Norwegian, Northern Sami and Lithuanian (with tone-mark stacking).
- **Letters:** ẞ Æ Œ Ø Ł Ħ Þ Ð Ŋ Ŧ Ǥ Ʒ Ǯ and the rest of the European Latin range.
- **Numbers:** lining figures, fractions ¼ ½ ¾ ⅓ ⅔, superscripts ⁰–⁹ and subscripts ₀–₉.
- **Math and science:** + − × ÷ = ≠ ≈ ± ∫ ∞ ∂ ∏ ∑ √ ∆ π Ω ℓ ℮ ℃ ℉ № ⟨ ⟩, with the degree sign, primes ′ ″ and the fraction slash ⁄.
- **Arrows and shapes:** ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙, ■ □ ▲ ▼ ▶ ◀ ◆ ◇ ◊ ▪ Ⓓ and ✓.
- **Punctuation and currency:** typographic quotes and guillemets, dashes, bullets, daggers, and $ ¢ £ ¤ ¥ € ₹.
- Stacked accents (Lithuanian Ė́, Ū́ and similar) rise to 1.25 em above the baseline, above the 1.0 em ascender; very tight line-heights may clip them. A few tall glyphs (∂ ∑ ∏ ∫ ℓ ↕ and the fractions) run 1 cell below the baseline to 6 above, so use a line-height of at least 1.4.
- Not yet drawn: Vietnamese and non-Latin scripts.

## Download

Fonts are in [`fonts/`](fonts): `otf/`, `ttf/` and `webfonts/` (WOFF, WOFF2).

## Using it

Best at multiples of 16px (cell = 1/8 em). At multiples of 8px, whole-cell
shapes are crisp but half-cell marks (e.g. some accents) fall on half pixels.
Turn off font smoothing or use `image-rendering: pixelated` canvases for exact pixels.

```css
@font-face {
  font-family: "Round Pegs";
  src: url("fonts/webfonts/RoundPegs-Regular.woff2") format("woff2");
}
```

## Building

The editable source is [`sources/RoundPegs-Regular.ufo`](sources/RoundPegs-Regular.ufo) (open it in Glyphs, RoboFont, or any UFO editor).
The glyph drawings it came from are in [`sources/svg`](sources/svg), one SVG per glyph, on a 4-unit-per-cell grid.

```sh
pip install -r requirements.txt
sh sources/build.sh
```

Output goes to `build-out/`. See [`sources/tools/README.md`](sources/tools/README.md) for the older SVG import scripts and [`documentation/DESIGN.md`](documentation/DESIGN.md) for the drawing rules.

## Contributing

Issues and pull requests are welcome. Please keep new glyphs on the cell grid and
follow the rules in `documentation/DESIGN.md`. By contributing you agree your work is
released under the OFL.

## License

Licensed under the SIL Open Font License, Version 1.1. See [OFL.txt](OFL.txt).
This applies to the font software and the source files in this repository.
