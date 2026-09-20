#!/usr/bin/env bash
# Starts the local landing-page preview: sidebar with all sites, viewport on the right.
# Tries port 8080 and counts up until one is free.
# PORT=9000 ./start.sh   changes the first port tried; NO_OPEN=1 ./start.sh   skips opening the browser.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 preview/server.py
