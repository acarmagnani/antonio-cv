#!/usr/bin/env python3
"""
make_preset_pdfs.py - Render every preset block in presets.yaml to a PDF.

    python system/make_preset_pdfs.py                       # all blocks
    python system/make_preset_pdfs.py real-estate-investment  # just one

Output goes to preset_previews/cv_<block>.pdf. These are review copies, for
reading a whole block side by side with content_base.yaml to see whether it
points one direction. They are regenerated from the yaml every run, so they are
not committed. This never touches active_application.txt, so it is safe to run
while an application is active.
"""
import http.server
import socketserver
import subprocess
import sys
import shutil
import threading
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not found. Install it with: pip install pyyaml")

ROOT = Path(__file__).parent.parent.resolve()
OUT_DIR = ROOT / "preset_previews"
PORT = 8124

if sys.platform == "win32":
    CANDIDATES = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
elif sys.platform == "darwin":
    CANDIDATES = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
else:
    CANDIDATES = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"]

chrome = next((c for c in CANDIDATES if Path(c).exists()), None) \
    or shutil.which("chrome") or shutil.which("google-chrome") \
    or shutil.which("chromium") or shutil.which("msedge")

if not chrome:
    # Fall back to a Playwright-cached Chromium, so rendering does not require
    # installing a full browser just for this.
    for cache in (Path.home() / "Library/Caches/ms-playwright", Path.home() / ".cache/ms-playwright"):
        if not cache.exists():
            continue
        matches = sorted(cache.glob("chromium*/**/Chromium.app/Contents/MacOS/Chromium")) \
            or sorted(cache.glob("chromium*/**/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")) \
            or sorted(cache.glob("chromium*/**/chrome"))
        if matches:
            chrome = str(matches[-1])
            break

if not chrome:
    sys.exit("No Chrome, Edge, or Chromium found.")

SANDBOX_FLAGS = [] if sys.platform == "win32" else ["--no-sandbox"]

presets = (yaml.safe_load((ROOT / "presets.yaml").read_text(encoding="utf-8")) or {}).get("presets") or {}
wanted = [a for a in sys.argv[1:] if not a.startswith("--")] or list(presets)

unknown = [w for w in wanted if w not in presets]
if unknown:
    sys.exit(f"Unknown preset(s): {', '.join(unknown)}\nKnown: {', '.join(presets)}")

OUT_DIR.mkdir(exist_ok=True)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, *args):
        pass


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
try:
    for name in wanted:
        out = OUT_DIR / f"cv_{name}.pdf"
        subprocess.run(
            [
                chrome, *SANDBOX_FLAGS,
                "--headless=new",
                "--disable-gpu",
                "--no-pdf-header-footer",
                "--virtual-time-budget=5000",
                f"--print-to-pdf={out}",
                f"http://127.0.0.1:{PORT}/system/templates/cv.html?preset={name}",
            ],
            check=True,
            stderr=subprocess.DEVNULL,
        )
        size = out.stat().st_size if out.exists() else 0
        label = presets[name].get("label", name)
        print(f"  {out.relative_to(ROOT)}  ({size // 1024} KB)  {label}")
finally:
    httpd.shutdown()

print(f"\n{len(wanted)} preset CV(s) written to {OUT_DIR.relative_to(ROOT)}/")
