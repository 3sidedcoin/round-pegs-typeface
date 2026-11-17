#!/bin/sh
# Build Round Pegs from the UFO source.  Needs: pip install -r requirements.txt  (fontmake)
set -e
cd "$(dirname "$0")/.."
mkdir -p build-out
fontmake -u sources/RoundPegs-Regular.ufo -o ttf --conversion-error 0.5 --output-dir build-out
fontmake -u sources/RoundPegs-Regular.ufo -o otf --output-dir build-out
python3 -I sources/tools/postprocess.py build-out/RoundPegs-Regular.ttf   # gasp + smart-dropout prep
echo "built build-out/RoundPegs-Regular.ttf and .otf"
