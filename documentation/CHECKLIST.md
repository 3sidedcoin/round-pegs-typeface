# Google Fonts submission checklist

- [ ] Repo is public: https://github.com/3sidedcoin/round-pegs-typeface
- [ ] OFL.txt in root (done), copyright line matches font name record
- [ ] Run `fontbakery check-googlefonts fonts/ttf/RoundPegs-Regular.ttf` with network and fix new issues
- [ ] Tag a release that matches the font version (the font is 1.024; the only tag so far is v1.013) with the font files attached
- [ ] Fork google/fonts, install `gftools`, run `gftools packager "Round Pegs" path/to/google/fonts` to make METADATA.pb (draft in METADATA.pb.draft)
- [ ] Open issue "Add Round Pegs" in google/fonts using documentation/ISSUE_DRAFT.md
- [ ] Answer review comments in the issue
