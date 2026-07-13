#!/usr/bin/env python3
"""
make_cover_pdf.py - Render the active application's cover letter to cover_letter.pdf.

Same idea as make_cv_pdf.py, but for the cover letter. Which letter is rendered is set
by active_application.txt (read by the template). Run from any shell:

    python system/make_cover_pdf.py                 # writes cover_letter.pdf
    python system/make_cover_pdf.py my-name.pdf     # writes a named file
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
PORT = 8124

CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
chrome = next((c for c in CANDIDATES if Path(c).exists()), None) \
    or shutil.which("chrome") or shutil.which("msedge")
if not chrome:
    sys.exit("No Chrome or Edge found. Add its path to CANDIDATES in make_cover_pdf.py.")

def company_name(app):
    """From 'YYYY-MM-company-role', take the token after the date (jacobs -> Jacobs)."""
    rest = re.sub(r"^\d{4}-\d{2}-", "", app)
    return rest.split("-")[0].capitalize() or "Application"


# A cover letter belongs to an application. Save it straight into that folder as
# cover_letter_Antonio_Carmagnani_<Company>.pdf. An explicit filename argument wins.
app = ""
pointer = ROOT / "active_application.txt"
if pointer.exists():
    app = pointer.read_text(encoding="utf-8").strip()

if len(sys.argv) > 1:
    out_path = (ROOT / sys.argv[1]).resolve()
elif app:
    out_path = (ROOT / "applications" / app / f"cover_letter_Antonio_Carmagnani_{company_name(app)}.pdf").resolve()
else:
    sys.exit("No active application set (active_application.txt is empty). A cover letter needs an application.")


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
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--virtual-time-budget=5000",
            f"--print-to-pdf={out_path}",
            f"http://localhost:{PORT}/system/templates/cover_letter.html",
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
