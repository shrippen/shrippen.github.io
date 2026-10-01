#!/usr/bin/env bash
# Builds everything GitHub Pages serves from docs/.
#   1. Kante for the web: docs/v1/ copied unchanged from Kante's build (../Kante/docs/v1, run ./build.sh
#      there first) -> https://shrippen.github.io/v1/  (all landing pages link this URL)
#      Kante (design system, Knust, Kimai plugin kit) lives in its own repo: https://github.com/shrippen/Kante
#   2. Overview page: docs/index.html from overview/projects.json (overview/tools/build-overview.py)
#   3. Token check of the overview page with Kante's checker (no raw colours or fonts)
set -euo pipefail
cd "$(dirname "$0")"
KANTE="${KANTE_DIR:-../Kante}"
if [ ! -f "$KANTE/docs/v1/shrippen.css" ]; then
  echo "build: no Kante build in $KANTE/docs/v1 (clone shrippen/Kante next to this repo or set KANTE_DIR)" >&2
  exit 1
fi
rm -rf docs/v1
cp -r "$KANTE/docs/v1" docs/v1
echo "copied docs/v1 from $KANTE ($(git -C "$KANTE" describe --always --dirty 2>/dev/null || echo unknown))"
python3 overview/tools/build-overview.py
python3 "$KANTE/tools/check-tokens.py" docs/index.html
