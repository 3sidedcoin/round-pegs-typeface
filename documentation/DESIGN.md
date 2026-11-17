# Design rules

- One cell = 4 SVG units = 128 font units (UPM 1024). Half cell = 2 units.
- Cap height is 5 cells (640 units). Letter frames are 20 units high; baseline at the bottom.
- Taller frames: 28 high = baseline at y=24; 32 high = baseline y=28; 36, 40, 44 high = baseline y=32.
- Convex corners: radius 1 unit. Concave fillets and four-pointed stars where cells join only diagonally (radius = half cell).
- Accent marks are one canonical shape each, anchored to the base letter's frame centre (ogonek: right edge), and always land on half-cell offsets.
- Lowercase and accented lowercase map to the same glyphs as capitals.
