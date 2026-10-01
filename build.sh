#!/usr/bin/env bash
# Builds everything GitHub Pages serves from docs/.
#   1. Kante for the web: docs/v1/shrippen.css, shrippen.js, fonts.css and fonts/ from kante/
#      -> https://shrippen.github.io/v1/  (all landing pages link this URL)
#   2. Overview page: docs/index.html from overview/projects.json (overview/tools/build-overview.py)
#   3. Kante for apps: kante/qml/Kante/KantePalette.qml, kante/tokens/palette.qml and the
#      bundled fonts, generated from kante/tokens/palette.json (kante/tools/build-qml.py)
#   4. Knust palette: docs/v1/knust-palette.css (--shr-* for the Kimai theme) from palette.json and
#      variables.css (kante/tools/build-knust.py) -> https://shrippen.github.io/v1/knust-palette.css
#   5. Token check: no raw colours or fonts outside kante/tokens/, and palette.json
#      matches variables.css (kante/tools/check-tokens.py)
#   6. QML module test: kante/qml/tests, if qmltestrunner is installed (kante/tools/check-qml.sh)
#   7. Claude Design upload: kante/ds-bundle/ (.design-sync/make-bundle.py, gitignored)
set -euo pipefail
cd "$(dirname "$0")"
OUT=docs/v1
mkdir -p "$OUT"
{
  echo "/* Kante v1 — https://github.com/shrippen/shrippen.github.io */"
  cat kante/tokens/variables.css kante/css/base.css kante/css/components.css
} > "$OUT/shrippen.css"
cp kante/js/shrippen.js "$OUT/shrippen.js"
# Offline fonts: fonts.css plus the font files next to it (opt-in, apps that must work without Google Fonts)
mkdir -p "$OUT/fonts"
cp kante/fonts/*.ttf kante/fonts/*.woff2 kante/fonts/OFL.txt "$OUT/fonts/"
cp kante/css/fonts.css "$OUT/fonts.css"
echo "built $OUT/shrippen.css ($(wc -c < "$OUT/shrippen.css") bytes), shrippen.js"
python3 overview/tools/build-overview.py
python3 kante/tools/build-qml.py
python3 kante/tools/build-knust.py
python3 kante/tools/check-tokens.py
kante/tools/check-qml.sh
python3 .design-sync/make-bundle.py
