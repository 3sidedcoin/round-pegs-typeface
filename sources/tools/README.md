# Tools

`RoundPegs-Regular.ufo` in the parent folder is the editable source of truth. Build it with `sources/build.sh`.

The scripts here are history, kept for transparency, not part of the normal build:

- `build.py` imports the glyph SVGs in `../svg` into a copy of the earlier game-version OTF of this typeface. That file is **not** in this repository; set `ROUND_PEGS_BASE_OTF` to a copy if you have one.
- `release.py` post-processed that output: composed accented capitals, derived glyphs, metrics, names, mark positioning.
- `export_ufo.py` produced the UFO from the finished font. `postprocess.py` adds `gasp` and a smart-dropout `prep` table to the compiled TTF.
