#!/usr/bin/env python3
"""
make_cv_pdf.py - Render the active CV to a PDF, deterministically.

Cross-shell: run it the same way from PowerShell, CMD, or Git Bash:

    python make_cv_pdf.py     # active application -> applications/<app>/cv_Antonio_Carmagnani_<Company>.pdf
                           # no active application -> cv.pdf at the repo root
    python make_cv_pdf.py out.pdf   # explicit filename wins

Why a local server: templates/cv.html loads the YAML with fetch(), which the
browser blocks over file://. Serving the repo over http://localhost makes it
work, then headless Chrome prints it to PDF with no manual dialog.
"""
import http.server
import os
import re
import shutil
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

# This script lives in system/; the repo root (served to the browser) is its parent.
ROOT = Path(__file__).parent.parent.resolve()
os.chdir(ROOT)
PORT = 8123

# Prefer Chrome; fall back to Edge/Chromium (all are Chromium and support --print-to-pdf).
if sys.platform == "win32":
    CANDIDATES = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
elif sys.platform == "darwin":
    CANDIDATES = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
else:
    CANDIDATES = [
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
    ]

chrome = next((c for c in CANDIDATES if Path(c).exists()), None) \
    or shutil.which("chrome") or shutil.which("google-chrome") \
    or shutil.which("chromium") or shutil.which("msedge")

if not chrome:
    # No system browser: fall back to a Playwright-downloaded Chromium if one
    # is already cached locally (e.g. from `npx playwright install`), so
    # rendering doesn't require installing a full browser just for this.
    for cache in (Path.home() / "Library/Caches/ms-playwright", Path.home() / ".cache/ms-playwright"):
        if cache.exists():
            matches = sorted(cache.glob("chromium*/**/Chromium.app/Contents/MacOS/Chromium")) \
                or sorted(cache.glob("chromium*/**/chrome"))
            if matches:
                chrome = str(matches[-1])
                break

if not chrome:
    sys.exit("No Chrome, Edge, or Chromium found. Install one, or add its path to CANDIDATES in make_cv_pdf.py.")

# Ad-hoc Chromium builds (e.g. Playwright's) lack the setuid sandbox helper a
# packaged browser install has; --no-sandbox is safe since we only render
# trusted local HTML. Harmless to keep off on Windows, where it isn't needed.
SANDBOX_FLAGS = [] if sys.platform == "win32" else ["--no-sandbox"]

def company_name(app):
    """From an application folder 'YYYY-MM-company-role', take the token right
    after the date as the company (e.g. jacobs -> Jacobs)."""
    rest = re.sub(r"^\d{4}-\d{2}-", "", app.split("/")[-1])
    return rest.split("-")[0].capitalize() or "Application"


# Output path:
#   - an explicit filename argument always wins;
#   - if an application is active, save straight into its folder as
#     cv_Antonio_Carmagnani_<Company>.pdf;
#   - otherwise (base/master CV) write cv.pdf at the repo root.
app = ""
pointer = ROOT / "active_application.txt"
if pointer.exists():
    app = pointer.read_text(encoding="utf-8").strip()

if len(sys.argv) > 1:
    out_path = (ROOT / sys.argv[1]).resolve()
elif app:
    out_path = (ROOT / "applications" / app / f"cv_Antonio_Carmagnani_{company_name(app)}.pdf").resolve()
else:
    out_path = (ROOT / "cv.pdf").resolve()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
try:
    subprocess.run(
        [
            chrome,
            *SANDBOX_FLAGS,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--virtual-time-budget=5000",
            f"--print-to-pdf={out_path}",
            f"http://localhost:{PORT}/system/templates/cv.html",
        ],
        check=True,
        stderr=subprocess.DEVNULL,
    )
finally:
    httpd.shutdown()

try:
    print(f"Wrote {out_path.relative_to(ROOT)}")
except ValueError:
    print(f"Wrote {out_path}")
