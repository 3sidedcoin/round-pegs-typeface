Title: Add Round Pegs

**Font Project Git Repo URL:**

https://github.com/3sidedcoin/round-pegs-typeface

**Super short description of the Font Family:**

Round Pegs is a free, capitals-only pixel display typeface built from rounded cells, with concave fillets where cells join diagonally. It is drawn on a whole-cell and half-cell grid and is crisp at 16px multiples. Designed by Tejas at 3 Sided Coin (https://3sided.co.in), originally made for the game Shade, Shade, Hide!!!

**Requirements:**

By opening this issue, I confirm the project meets the following requirements:

- [x] The entire font project is available in a Github repository (repo) and licensed under the [OFL](https://openfontlicense.org/open-font-license-official-text/)
- [x] I confirm that by 'entire font project', no "plus" or "pro" or other larger version of the project exists as a retail font anywhere
- [x] The source files are available in the repo
- [x] I am the sole copyright author of the entire project, or all other copyright authors have licensed their work to me under the OFL, and I commit to clearly disclosing if AI tools were used in the creation of this project.
- [x] There are no "Reserved Font Names" in the OFL license information, or in the project documentation of any known upstream projects. If there are RFNs, they are not used in whole or in part in this family name, or, I want to discuss how Google can work with my use of them.
- [x] The family name is unique according to [namecheck.fontdata.com](https://namecheck.fontdata.com/)
- [x] The name of the font family expected to appear on app menus must be very clearly communicated and definitive. It should not include any copyright holder's full names or acronyms.
- [x] The font supports at least the Google Fonts 'Latin Core' glyphset from [github.com/googlefonts/glyphsets](https://github.com/googlefonts/glyphsets) ([direct link](https://github.com/googlefonts/glyphsets/blob/main/data/results/txt/nice-names/GF_Latin_Core.txt))
- [x] The repo has the [Google Fonts preferred upstream repo structure](https://googlefonts.github.io/gf-guide/upstream.html)
- [x] I have read, agree with, and comply with, the full [Google Fonts contributing requirements](https://googlefonts.github.io/gf-guide/index#pre-production-getting-your-fonts-ready-for-gf)
- [x] I will maintain the repository and participate in the onboarding process (addressing, solving, and responding to issues, merging pull requests, etc)

**Notes:**

- Version 1.022: 376 glyphs, 482 characters. Covers the Google Fonts Latin Core and Latin Kernel glyphsets in full (319 and 116 of 319 and 116), the whole of Windows-1252 (the soft hyphen is left out on purpose, following FontBakery's recommendation), and 76 of the 110 glyphs in the optional Latin Plus set (fractions, super- and subscript digits, currency and typographic marks). Covers about 350 Latin-script languages (shaperglot), including Finnish, Norwegian, Northern Sami and Lithuanian with tone-mark stacking. Vietnamese and non-Latin scripts are not drawn.
- Capitals-only by design: lowercase maps to the capitals. Spacing is the whole-cell grid itself (1-cell gaps), with three kerning pairs (LV and LT sit flush, LY tucks one cell under the Y) and two default-on contextual rules (`calt`) for LL and OO runs. Rules are in documentation/DESIGN.md.
- FontBakery `check-googlefonts` on v1.022 (fonts/ttf/RoundPegs-Regular.ttf): 0 FATAL, 0 FAIL, 6 WARN, 112 PASS. The warnings are alt_caron (Dcaron, Lcaron and Tcaron are composed from base letter and mark), contour count (pixel outlines), article (added after onboarding), unreachable combining-mark subsets, the unregistered vendor ID 3SDC, and outline alignment on ↕ (fillet points 1.5 units under the baseline, from the drawn star joins).
- Editable source: sources/RoundPegs-Regular.ufo, with sources/config.yaml and sources/build.sh (fontmake). The original per-glyph SVG drawings are in sources/svg. The generators (build, release, kerning) are in sources/tools.
- Renamed from "Edge Case" to "Round Pegs" before onboarding; repo renamed to round-pegs-typeface.
- AI disclosure: all glyph shapes were drawn by me. An AI assistant (Claude, by Anthropic) helped write the build and release scripts, composed derived glyphs (accented capitals, subscripts from the superscript drawings, a few ligatures) from my drawn marks and letters, and checked the font against the Google Fonts glyph sets.

**Image:**

(attach documentation/specimen.png)


---

## Comment to post on the open issue (update since the last comment)

Updated the repo to v1.022. Changes since v1.012:

- Added arrows ↖ ↗ ↘ ↙ ↔ ↕, ⅓ ⅔, the fraction slash ⁄, ‖, № and primes ′ ″.
- Windows-1252 is now fully covered (added µ ¬ † ‡ ƒ ‰ ¦ ¤ ± ¹ ² ³ ¼ ½ ¾). Also added ⁰ ⁴-⁹ and ₀-₉.
- Added math and symbols ≠ ≈ ∫ ∞ ⟨ ⟩ ∂ ∏ ∑ π √ ∆ Ω ℓ ℮ ✓, shapes ■ □ ▲ ▼ ▶ ◀ ◆ ◇ ◊ ▪ Ⓓ, ℃ ℉, and simplified the dashes and the degree sign. The cedilla now attaches to its letter. Added eleven stylistic alternates, each in its own set (ss01 R, ss02 1, ss03 B, ss04 P, ss05 slim I, ss06 narrow Y, ss07 narrow X, ss08 narrow N, ss09 slashed zero, ss10 closed four, ss11 narrow O), contextual spacing for LL, LLL, LLY and OO runs, a tighter LY kern, redrew the diagonal arrows, adjusted R and B corners, redrew the figures with fillets built in and refined the inner curve of the A, redrew ∂ at cap height, and set ℃ ℉ with no gap between the ring and the letter.
- 376 glyphs, 482 characters; Latin Core and Latin Kernel remain at 100%, and Latin Plus is at 76 of 110.
- Redrew % and the fractions' numerators; spacing is documented, with kerning for LV, LY and LT and the calt rules for LL and OO runs.
- FontBakery `check-googlefonts`: 0 FATAL, 0 FAIL, 6 WARN, 112 PASS (new warning: outline alignment on ↕, a few fillet points 1.5 units under the baseline).

Repo: https://github.com/3sidedcoin/round-pegs-typeface (tag v1.022). Happy to adjust anything before onboarding.
