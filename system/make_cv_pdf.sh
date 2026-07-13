#!/usr/bin/env bash
#
# make_cv_pdf.sh — Render the active CV to a PDF, deterministically.
#
# Why a local server instead of opening the file directly: templates/cv.html
# loads the YAML with fetch(), which the browser blocks over file://. Serving
# the repo over http://localhost makes fetch() work, same as Ctrl+P would,
# but without the manual print dialog (and its run-to-run variance).
#
# Usage:
#   ./make_cv_pdf.sh                # writes <active-application>.pdf (or cv.pdf)
#   ./make_cv_pdf.sh antonio-cv.pdf # writes a named file
#
set -euo pipefail

# This script lives in system/; the repo root (served to the browser) is its parent.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PORT=8123

# Prefer Chrome; fall back to Edge (both are Chromium and support --print-to-pdf).
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
[ -x "$CHROME" ] || CHROME="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
[ -x "$CHROME" ] || { echo "No Chrome or Edge found. Edit CHROME in make_cv_pdf.sh." >&2; exit 1; }

# Output name: cv.pdf by default. WHICH CV is rendered (base vs a tailored
# application) is decided by active_application.txt, read by the template.
OUT="${1:-cv.pdf}"
OUT_WIN="$(cygpath -w "$ROOT/$OUT")"

# Start a throwaway local server, kill it on exit no matter what.
python -m http.server "$PORT" >/dev/null 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT
sleep 1

# --virtual-time-budget gives the page's async fetch()+render time to finish
# before the PDF is snapshotted. --no-pdf-header-footer drops the browser's
# default URL/date header so @page margins are the only margins.
"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-pdf-header-footer \
  --virtual-time-budget=5000 \
  --print-to-pdf="$OUT_WIN" \
  "http://localhost:$PORT/system/templates/cv.html" 2>/dev/null

echo "Wrote $OUT"
