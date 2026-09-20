#!/usr/bin/env bash
# Builds the single stylesheet that all landing pages link to.
# Output: docs/v1/shrippen.css  →  https://shrippen.github.io/DesignDefault/v1/shrippen.css
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p docs/v1
{
  echo "/* shrippen Design Default v1 — https://github.com/shrippen/DesignDefault */"
  cat tokens/variables.css css/base.css css/components.css
} > docs/v1/shrippen.css
echo "built docs/v1/shrippen.css ($(wc -c < docs/v1/shrippen.css) bytes)"
