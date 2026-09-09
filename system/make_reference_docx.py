#!/usr/bin/env python3
"""
make_reference_docx.py - Render a reference letter to .docx for the referee to sign or edit.

    python system/make_reference_docx.py reference_letters/tereza-kramlova
    python system/make_reference_docx.py reference_letters/tereza-kramlova --from-docx

Reads reference_letter.md in that folder and writes reference_letter.docx beside it, then
checks that the result still fits on one page. The .md is the source of truth.

Word is where the letter actually gets edited, though, by Antonio or by the referee, and
those edits must not be lost the next time the .docx is regenerated. --from-docx pulls the
text back out of the .docx and rewrites the .md from it, which reverses the flow for one
run and restores the invariant. Run it after any hand-editing in Word.

Formatting mirrors the cover letters (system/assets/cover-letter.css): Times New Roman,
11pt body, 25mm top margin and 20mm elsewhere, so a letter drafted here looks like the
rest of the pack. Line spacing is tighter than the cover letter's 1.5, because a reference
letter carries more text and has to stay on one page.

Markdown understood: "# Name" becomes the letterhead name, blank lines separate
paragraphs, **text** is bold. Nothing else, on purpose.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape, unescape

FONT = "Times New Roman"
BODY_SZ = 22      # half-points, 11pt
NAME_SZ = 28      # 14pt
SMALL_SZ = 19     # 9.5pt
LINE = 260        # twentieths of a point, 13pt leading (single spacing at 11pt)
AFTER = 100       # 5pt between paragraphs
MARGIN = dict(top=1417, bottom=1134, left=1134, right=1134)  # twips: 25mm / 20mm

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>
<w:sz w:val="{BODY_SZ}"/><w:szCs w:val="{BODY_SZ}"/>
<w:lang w:val="en-GB"/>
</w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr>
<w:spacing w:after="{AFTER}" w:line="{LINE}" w:lineRule="atLeast"/>
</w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal">
<w:name w:val="Normal"/><w:qFormat/>
</w:style>
</w:styles>"""


def runs(text, sz=BODY_SZ):
    """Split **bold** spans into <w:r> runs."""
    out = []
    for part in re.split(r"(\*\*[^*]+\*\*)", text):
        if not part:
            continue
        bold = part.startswith("**") and part.endswith("**")
        body = part[2:-2] if bold else part
        rpr = f'<w:rPr>{"<w:b/>" if bold else ""}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(body)}</w:t></w:r>')
    return "".join(out)


def para(text, sz=BODY_SZ, after=AFTER):
    ppr = f'<w:pPr><w:spacing w:after="{after}" w:line="{LINE}" w:lineRule="atLeast"/></w:pPr>'
    return f"<w:p>{ppr}{runs(text, sz)}</w:p>"


def build(md):
    blocks = [b.strip() for b in re.split(r"\n\s*\n", md.strip()) if b.strip()]
    body = []
    for block in blocks:
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if lines[0].startswith("# "):
            # Letterhead: the name, then any remaining lines of the block as small text.
            body.append(para(f"**{lines[0][2:].strip()}**", sz=NAME_SZ, after=40))
            for extra in lines[1:]:
                body.append(para(extra, sz=SMALL_SZ, after=40))
            continue
        if len(lines) > 1:
            # A block of separate short lines (contact details, signature): keep the breaks.
            for i, line in enumerate(lines):
                body.append(para(line, sz=SMALL_SZ if len(lines) > 2 else BODY_SZ,
                                 after=40 if i < len(lines) - 1 else AFTER))
            continue
        body.append(para(lines[0]))
    sect = (f'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            f'<w:pgMar w:top="{MARGIN["top"]}" w:right="{MARGIN["right"]}" '
            f'w:bottom="{MARGIN["bottom"]}" w:left="{MARGIN["left"]}" '
            f'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body>{"".join(body)}{sect}</w:body></w:document>')


def find_browser():
    """Chrome, Edge, or a Playwright-cached Chromium, for the one-page check."""
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
    ]
    found = next((c for c in candidates if Path(c).exists()), None)
    if found:
        return found
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        if shutil.which(name):
            return shutil.which(name)
    for cache in (Path.home() / "Library/Caches/ms-playwright", Path.home() / ".cache/ms-playwright"):
        if cache.exists():
            for pattern in ("chromium_headless_shell-*/*/chrome-headless-shell",
                            "chromium-*/**/Google Chrome for Testing.app/Contents/MacOS/*",
                            "chromium-*/**/Chromium.app/Contents/MacOS/Chromium",
                            "chromium-*/**/chrome"):
                hits = sorted(cache.glob(pattern))
                if hits:
                    return str(hits[-1])
    return None


def page_count(md):
    """Render the same metrics as HTML and count pages. None if no browser is available."""
    browser = find_browser()
    if not browser:
        return None
    blocks = [b.strip() for b in re.split(r"\n\s*\n", md.strip()) if b.strip()]
    html = []
    for block in blocks:
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if lines[0].startswith("# "):
            html.append(f'<p class="name">{escape(lines[0][2:])}</p>')
            html += [f'<p class="small">{escape(l)}</p>' for l in lines[1:]]
        elif len(lines) > 1:
            cls = "small" if len(lines) > 2 else ""
            html += [f'<p class="{cls}">{escape(l)}</p>' for l in lines]
        else:
            html.append(f"<p>{escape(lines[0])}</p>")
    css = (f"@page{{size:A4;margin:{MARGIN['top']/56.7:.0f}mm {MARGIN['right']/56.7:.0f}mm "
           f"{MARGIN['bottom']/56.7:.0f}mm {MARGIN['left']/56.7:.0f}mm}}"
           f'body{{font-family:"{FONT}",serif;font-size:{BODY_SZ/2}pt;margin:0}}'
           f"p{{line-height:{LINE/20}pt;margin:0 0 {AFTER/20}pt 0}}"
           f"p.name{{font-size:{NAME_SZ/2}pt;font-weight:bold;margin-bottom:2pt}}"
           f"p.small{{font-size:{SMALL_SZ/2}pt;margin-bottom:2pt}}")
    with tempfile.TemporaryDirectory() as tmp:
        src, pdf = Path(tmp) / "letter.html", Path(tmp) / "letter.pdf"
        src.write_text(f"<html><head><meta charset='utf-8'><style>{css}</style></head>"
                       f"<body>{''.join(html)}</body></html>", encoding="utf-8")
        subprocess.run([browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", src.as_uri()], capture_output=True, timeout=120)
        if not pdf.exists():
            return None
        return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))


def docx_to_md(path):
    """Pull the text back out of a .docx, in the same markdown shape the renderer reads."""
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    paras = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        text = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S))
        text = unescape(text).strip()
        if text:
            paras.append((text, "<w:b/>" in p))
    out = []
    for i, (text, bold) in enumerate(paras):
        if i == 0 and bold:
            out.append(f"# {text}")            # letterhead name
        elif i in (1, 2):
            out.append(text)                   # title and contact stay one block
        else:
            out.append(text)
    # The first three paragraphs form the letterhead block; everything else is separated.
    head = "\n\n".join([out[0], "\n".join(out[1:3])]) if len(out) > 2 else "\n\n".join(out)
    return head + "\n\n" + "\n\n".join(out[3:]) + "\n"


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python system/make_reference_docx.py reference_letters/<person>")
    folder = Path(sys.argv[1])
    src = folder / "reference_letter.md"
    out = folder / "reference_letter.docx"

    if "--from-docx" in sys.argv:
        if not out.exists():
            sys.exit(f"no reference_letter.docx in {folder}")
        src.write_text(docx_to_md(out), encoding="utf-8")
        print(f"rewrote {src} from {out.name}")
        return

    if not src.exists():
        sys.exit(f"no reference_letter.md in {folder}")
    md = src.read_text(encoding="utf-8")
    doc = build(md)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", doc)
    print(f"wrote {out}")

    pages = page_count(md)
    if pages is None:
        print("could not check the page count (no browser found); check it in Word")
    elif pages > 1:
        print(f"WARNING: {pages} pages. A reference letter has to fit one, so trim the .md and re-run.")
    else:
        print("fits one page")


if __name__ == "__main__":
    main()
