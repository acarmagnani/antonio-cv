#!/usr/bin/env python3
"""Validator for outreach emails, the email equivalent of check_letter.py.

Reads an outreach_email.md and rejects the things Antonio has said he does not want.
It inherits the letter's banned phrases and patterns from letter_base.yaml, so the
voice rules live in one place, and adds the email-only bans from email_base.yaml
(bureaucratic openers, "referred me", requests for meetings).

Length is the rule that matters most here. An outreach email that reads like a
second cover letter does not get read, so the ceiling is deliberately low.

Usage:
    python system/check_email.py                      # active application
    python system/check_email.py <application-folder> # e.g. wide/2026-09-novo-...
    python system/check_email.py path/to/outreach_email.md
"""
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_letter import split_sentences, words  # noqa: E402  same rules, one definition

ROOT = Path(__file__).resolve().parent.parent
EMAIL_BASE = ROOT / "email_base.yaml"
LETTER_BASE = ROOT / "letter_base.yaml"

PARAGRAPH_FINAL_MIN_WORDS = 12   # a paragraph must not end on a short beat
SENTENCE_WARN_WORDS = 7          # anything shorter gets flagged for a human read

HEADER = re.compile(r"^\s*(\*\*)?(To|Subject|Cc|Bcc)\b", re.IGNORECASE)


def body_paragraphs(text):
    """Everything except the To/Subject header, the rule under it, the greeting and
    the sign-off. Detected structurally so changing the header never turns a line
    into a body paragraph."""
    paras = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    paras = [p for p in paras if not HEADER.match(p) and p.strip("-* \t")]
    if paras and len(words(paras[0])) < 12 and paras[0].rstrip().endswith((",", ":")):
        paras = paras[1:]
    while paras and "Antonio Carmagnani" in paras[-1]:
        paras = paras[:-1]
    return paras


def check(path):
    text = Path(path).read_text(encoding="utf-8")
    cfg = yaml.safe_load(EMAIL_BASE.read_text(encoding="utf-8")) if EMAIL_BASE.exists() else {}
    letter = yaml.safe_load(LETTER_BASE.read_text(encoding="utf-8")) if LETTER_BASE.exists() else {}
    meta = cfg.get("meta", {})
    lo, hi = (meta.get("word_range") or [110, 200])

    errors, warnings = [], []
    paras = body_paragraphs(text)
    body = "\n\n".join(paras)
    low = body.lower()

    # 1. Unresolved template placeholders.
    for m in sorted(set(re.findall(r"\{[a-z_]+\}", text))):
        errors.append(f"unresolved placeholder {m}")

    # 2. Banned phrases: the letter's, plus the email-only ones.
    for phrase in (letter.get("banned_phrases") or []) + (cfg.get("banned_phrases") or []):
        if phrase.lower() in low:
            errors.append(f'banned phrase: "{phrase}"')

    # 3. Banned patterns, inherited from the letter with their stated reasons.
    for entry in letter.get("banned_patterns") or []:
        m = re.search(entry["pattern"], body, re.IGNORECASE)
        if m:
            errors.append(f'banned pattern ({entry["reason"]}): "{m.group(0)}"')

    # 4. House rule: no em dashes.
    if "—" in body or "–" in body:
        errors.append("em dash present, house rule is commas, periods or parentheses")

    # 5. Colons, kept tighter than the letter because the email is three paragraphs.
    colons = body.count(":")
    if colons > meta.get("colon_max", 4):
        errors.append(f"{colons} colons in the body, the ceiling is {meta.get('colon_max', 4)}")
    elif colons > meta.get("colon_warn", 2):
        warnings.append(f"{colons} colons in the body, consider cutting one")

    # 6. Length. The rule that matters most for an email.
    n = len(words(body))
    if n < lo or n > hi:
        errors.append(f"body is {n} words, outside the {lo}-{hi} range")

    # 7. Exactly three body paragraphs: opening, the case, the close.
    want = meta.get("paragraphs", 3)
    if len(paras) != want:
        errors.append(f"{len(paras)} body paragraphs, the email takes exactly {want}")

    # 8. No question anywhere. A question invites a one-line answer that ends the thread.
    if "?" in body:
        errors.append("the email asks a question; the close is an opening for a conversation, not a question")

    # 9. No paragraph may end on a short sentence used as a beat.
    for i, p in enumerate(paras, 1):
        sents = split_sentences(p)
        if sents and len(words(sents[-1])) < PARAGRAPH_FINAL_MIN_WORDS:
            errors.append(
                f'paragraph {i} ends on a {len(words(sents[-1]))}-word sentence, reads as a beat: "{sents[-1]}"'
            )

    # 10. Short sentences anywhere: flagged for a human, not auto-failed.
    for i, p in enumerate(paras, 1):
        for s in split_sentences(p):
            if len(words(s)) < SENTENCE_WARN_WORDS:
                warnings.append(f'paragraph {i}, {len(words(s))}-word sentence, read it: "{s}"')

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
        p = p / "outreach_email.md"
    if not p.exists():
        sys.exit(f"no outreach email at {p}")
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
        print(f"\n{len(errors)} error(s). Fix in email_base.yaml or email.yaml, then re-render.")
        return 1
    print(f"\nOK: {rel} -> {paras} body paragraphs, {n} words, no banned patterns.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
