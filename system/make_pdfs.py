#!/usr/bin/env python3
"""
make_pdfs.py - Render everything for the active application in one go.

Usage:
    python system/make_pdfs.py

Reads active_application.txt, validates the selection, then renders cv.pdf and,
if the folder has a cover_letter.md, cover_letter.pdf. Use this instead of
calling make_cv_pdf.py / make_cover_pdf.py separately.
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
pointer_file = ROOT / "active_application.txt"
pointer = pointer_file.read_text().strip() if pointer_file.exists() else ""

if not pointer:
    print("active_application.txt is empty: rendering the base CV.")
else:
    folder = ROOT / "applications" / pointer
    if not folder.exists():
        sys.exit(f"Active application folder not found: {folder}")
    print(f"Active application: {pointer}\n")
    if (folder / "selection.yaml").exists():
        if subprocess.run([sys.executable, str(ROOT / "system/select_cv.py"), pointer]).returncode:
            sys.exit("Selection is invalid, not rendering.")
    elif (folder / "content_tailored.yaml").exists():
        print("Legacy content_tailored.yaml found (no selection.yaml).")
        subprocess.run([sys.executable, str(ROOT / "system/verify_cv.py"), pointer])

print()
subprocess.run([sys.executable, str(ROOT / "system/make_cv_pdf.py")], check=True)

if pointer and (ROOT / "applications" / pointer / "cover_letter.md").exists():
    subprocess.run([sys.executable, str(ROOT / "system/make_cover_pdf.py")], check=True)
else:
    print("No cover_letter.md, skipping the cover letter.")
