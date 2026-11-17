# Google Fonts submission checklist

- [ ] Repo is public: https://github.com/3sidedcoin/edge-case-typeface
- [ ] OFL.txt in root (done), copyright line matches font name record
- [ ] Run `fontbakery check-googlefonts fonts/ttf/EdgeCase-Regular.ttf` with network and fix new issues
- [ ] Tag a release (v1.007) with the font files attached
- [ ] Fork google/fonts, install `gftools`, run `gftools packager "Edge Case" path/to/google/fonts` to make METADATA.pb (draft in METADATA.pb.draft)
- [ ] Open issue "Add Edge Case" in google/fonts using documentation/ISSUE_DRAFT.md
- [ ] Answer review comments in the issue
