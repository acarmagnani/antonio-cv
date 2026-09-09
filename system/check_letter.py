#!/usr/bin/env python3
"""Validator for cover letters, the letter equivalent of select_cv.py.

Reads a cover_letter.md and rejects the things Antonio has said he does not want.
It is a floor, not a guarantee: it catches mechanical tells (fragments used for
effect, banned phrases, transition framing, em dashes, length) but it cannot judge
whether a sentence is empty. The real protection is that the prose comes
pre-written from letter_base.yaml rather than being improvised per application.

Usage:
    python system/check_letter.py                      # active application
    python system/check_letter.py <application-folder> # e.g. target/2026-09-eidra-...
    python system/check_letter.py path/to/cover_letter.md
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "letter_base.yaml"

# Abbreviations that must not be treated as sentence ends.
ABBREV = ["M.Arch.", "B.Arch.", "Ph.D.", "e.g.", "i.e.", "etc.", "U.S.", "Mr.", "Ms.", "Dr.", "St."]

PARAGRAPH_FINAL_MIN_WORDS = 12   # a paragraph must not end on a short beat
SENTENCE_WARN_WORDS = 7          # anything shorter gets flagged for a human read


def split_sentences(text):
    masked = text
    for i, ab in enumerate(ABBREV):
        masked = masked.replace(ab, f"\x00{i}\x00")
    parts = re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑÜ¿¡])", masked)
    out = []
    for p in parts:
        for i, ab in enumerate(ABBREV):
            p = p.replace(f"\x00{i}\x00", ab)
        p = p.strip()
        if p:
            out.append(p)
    return out


def words(s):
    return [w for w in re.findall(r"[\w'’-]+", s) if w]


def body_paragraphs(text):
    """Everything except the greeting line and the sign-off.

    Detected structurally rather than by salutation wording, so changing the greeting
    or the sign-off in letter_base.yaml never silently turns one into a body paragraph.
    """
    paras = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    # Greeting: first paragraph, short and ending in a comma or colon.
    if paras and len(words(paras[0])) < 12 and paras[0].rstrip().endswith((",", ":")):
        paras = paras[1:]
    # Sign-off: any trailing paragraph carrying his name.
    while paras and "Antonio Carmagnani" in paras[-1]:
        paras = paras[:-1]
    return paras


def check(path):
    text = Path(path).read_text(encoding="utf-8")
    cfg = yaml.safe_load(BASE.read_text(encoding="utf-8")) if BASE.exists() else {}
    lo, hi = (cfg.get("meta", {}).get("word_range") or [320, 430])

    errors, warnings = [], []
    paras = body_paragraphs(text)
    body = "\n\n".join(paras)

    # 1. Unresolved template placeholders.
    for m in set(re.findall(r"\{[a-z_]+\}", text)):
        errors.append(f"unresolved placeholder {m}")

    # 2. Banned phrases, verbatim.
    low = body.lower()
    for phrase in cfg.get("banned_phrases", []):
        if phrase.lower() in low:
            errors.append(f'banned phrase: "{phrase}"')

    # 3. Banned patterns, with a stated reason.
    for entry in cfg.get("banned_patterns", []):
        m = re.search(entry["pattern"], body, re.IGNORECASE)
        if m:
            errors.append(f'banned pattern ({entry["reason"]}): "{m.group(0)}"')

    # 4. House rule: no em dashes.
    if "—" in body or "–" in body:
        errors.append("em dash present, house rule is commas, periods or parentheses")

    # 5. Colons read as the AI 'statement: reveal' tic.
    colons = body.count(":")
    colon_warn = cfg.get("meta", {}).get("colon_warn", 4)
    colon_max = cfg.get("meta", {}).get("colon_max", 8)
    if colons > colon_max:
        errors.append(f"{colons} colons in the body, the ceiling is {colon_max}")
    elif colons > colon_warn:
        warnings.append(f"{colons} colons in the body, consider cutting one or two")

    # 6. Length.
    n = len(words(body))
    if n < lo or n > hi:
        errors.append(f"body is {n} words, outside the {lo}-{hi} range")

    # 7. No paragraph may end on a short sentence used as a beat.
    for i, p in enumerate(paras, 1):
        sents = split_sentences(p)
        if not sents:
            continue
        last = sents[-1]
        if len(words(last)) < PARAGRAPH_FINAL_MIN_WORDS:
            errors.append(
                f'paragraph {i} ends on a {len(words(last))}-word sentence, reads as a beat: "{last}"'
            )

    # 8. Short sentences anywhere: flagged for a human, not auto-failed.
    for i, p in enumerate(paras, 1):
        for s in split_sentences(p):
            if len(words(s)) < SENTENCE_WARN_WORDS:
                warnings.append(f'paragraph {i}, {len(words(s))}-word sentence, read it: "{s}"')

    # 9. Every body paragraph should carry a real claim, not one line.
    for i, p in enumerate(paras, 1):
        if len(words(p)) < 25:
            warnings.append(f"paragraph {i} is only {len(words(p))} words")

    return errors, warnings, n, len(paras)


def resolve(arg):
    if arg is None:
        pointer = ROOT / "active_application.txt"
        if not pointer.exists() or not pointer.read_text().strip():
            sys.exit("no active application and no path given")
        arg = pointer.read_text().strip()
    p = Path(arg)
    if not p.is_absolute():
        p = ROOT / arg if (ROOT / arg).exists() else ROOT / "applications" / arg
    if p.is_dir():
        p = p / "cover_letter.md"
    if not p.exists():
        sys.exit(f"no cover letter at {p}")
    return p


def main():
    path = resolve(sys.argv[1] if len(sys.argv) > 1 else None)
    errors, warnings, n, paras = check(path)
    rel = path.relative_to(ROOT) if str(path).startswith(str(ROOT)) else path

    for w in warnings:
        print(f"  warn: {w}")
    if errors:
        print(f"\nFAIL: {rel}")
        for e in errors:
            print(f"  error: {e}")
        print(f"\n{len(errors)} error(s). Fix in letter_base.yaml or letter.yaml, then re-render.")
        return 1
    print(f"\nOK: {rel} -> {paras} body paragraphs, {n} words, no banned patterns.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
