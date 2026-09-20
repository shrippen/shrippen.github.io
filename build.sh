#!/usr/bin/env bash
# Builds the files all landing pages link to.
# Output: docs/v1/shrippen.css and docs/v1/shrippen.js
#         → https://shrippen.github.io/DesignDefault/v1/
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p docs/v1
{
  echo "/* shrippen Design Default v1 — https://github.com/shrippen/DesignDefault */"
  cat tokens/variables.css css/base.css css/components.css
} > docs/v1/shrippen.css
cp js/shrippen.js docs/v1/shrippen.js
echo "built docs/v1/shrippen.css ($(wc -c < docs/v1/shrippen.css) bytes), shrippen.js"
