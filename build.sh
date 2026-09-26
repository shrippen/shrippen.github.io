#!/usr/bin/env bash
# Builds everything GitHub Pages serves from docs/.
#   1. Design system: docs/v1/shrippen.css and shrippen.js
#      -> https://shrippen.github.io/v1/  (all landing pages link this URL)
#   2. Overview page: docs/index.html from projects.json (tools/build-overview.py)
#   3. Token check: no raw colours or fonts outside tokens/ (tools/check-tokens.py)
#   4. Claude Design upload: ds-bundle/ (.design-sync/make-bundle.py, gitignored)
set -euo pipefail
cd "$(dirname "$0")"
OUT=docs/v1
mkdir -p "$OUT"
{
  echo "/* shrippen Design Default v1 — https://github.com/shrippen/shrippen.github.io */"
  cat tokens/variables.css css/base.css css/components.css
} > "$OUT/shrippen.css"
cp js/shrippen.js "$OUT/shrippen.js"
echo "built $OUT/shrippen.css ($(wc -c < "$OUT/shrippen.css") bytes), shrippen.js"
python3 tools/build-overview.py
python3 tools/check-tokens.py
python3 .design-sync/make-bundle.py
