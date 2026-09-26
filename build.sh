#!/usr/bin/env bash
# Builds everything GitHub Pages serves from docs/.
#   1. Design system: docs/v1/shrippen.css and shrippen.js
#      -> https://shrippen.github.io/v1/  (all landing pages link this URL)
#   2. Overview page: docs/index.html from projects.json (tools/build-overview.py)
#   3. Kante for apps: qml/Kante/KantePalette.qml, tokens/palette.qml and the
#      bundled fonts, generated from tokens/palette.json (tools/build-qml.py)
#   4. Token check: no raw colours or fonts outside tokens/, and palette.json
#      matches variables.css (tools/check-tokens.py)
#   5. QML module test: qml/tests, if qmltestrunner is installed (tools/check-qml.sh)
#   6. Claude Design upload: ds-bundle/ (.design-sync/make-bundle.py, gitignored)
set -euo pipefail
cd "$(dirname "$0")"
OUT=docs/v1
mkdir -p "$OUT"
{
  echo "/* Kante v1 — https://github.com/shrippen/shrippen.github.io */"
  cat tokens/variables.css css/base.css css/components.css
} > "$OUT/shrippen.css"
cp js/shrippen.js "$OUT/shrippen.js"
echo "built $OUT/shrippen.css ($(wc -c < "$OUT/shrippen.css") bytes), shrippen.js"
python3 tools/build-overview.py
python3 tools/build-qml.py
python3 tools/check-tokens.py
tools/check-qml.sh
python3 .design-sync/make-bundle.py
