#!/usr/bin/env python3
"""Render an application's letter.yaml into cover_letter.md, then validate it.

This is to letters what select_cv.py is to the CV: the application folder holds ids
plus a handful of per-job sentences, never a free-written letter. All reusable prose
lives in letter_base.yaml.

letter.yaml looks like:

    extends: data-built-environment      # a block in letter_base.yaml
    company: "Eidra"
    role: "Graduate Programme"           # optional, only if the prose uses {role}
    language: en                         # en (default) or es
    hook: >                              # closes paragraph 1: why this employer
      ...
    paragraphs:                          # optional, overrides the block's two
      - exp.ramboll.esg-data
      - exp.sweco.consulting-delivery
    relevance:                           # one sentence per paragraph, per job
      exp.ramboll.esg-data: >
        ...
    closing_reason: >                    # opens the closing: what this employer is
      ...

Usage:
    python system/make_letter.py                      # active application
    python system/make_letter.py <application-folder>
"""
import sys
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))


def load(p):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


def flat(text):
    """YAML folded scalars keep newlines; a letter paragraph is one long line."""
    return " ".join(str(text).split())


def index(items):
    return {it["id"]: it for it in items}


def resolve_folder(arg):
    if arg is None:
        pointer = ROOT / "active_application.txt"
        if not pointer.exists() or not pointer.read_text().strip():
            sys.exit("no active application; pass a folder or write active_application.txt")
        arg = pointer.read_text().strip()
    p = ROOT / "applications" / arg
    if not p.is_dir():
        p = ROOT / arg
    if not p.is_dir():
        sys.exit(f"no such application folder: {arg}")
    return p


def build(folder, base):
    sel_path = folder / "letter.yaml"
    if not sel_path.exists():
        sys.exit(f"no letter.yaml in {folder}. Write one (see the docstring) before rendering.")
    sel = load(sel_path)

    blocks = base["blocks"]
    block = {}
    if sel.get("extends"):
        if sel["extends"] not in blocks:
            sys.exit(f"unknown block '{sel['extends']}'. Known: {', '.join(blocks)}")
        block = blocks[sel["extends"]]

    openings, exps, closings = index(base["openings"]), index(base["experiences"]), index(base["closings"])

    opening_id = sel.get("opening", block.get("opening"))
    closing_id = sel.get("closing", block.get("closing"))
    para_ids = sel.get("paragraphs", block.get("paragraphs", []))

    for label, i, pool in (("opening", opening_id, openings), ("closing", closing_id, closings)):
        if not i:
            sys.exit(f"no {label} selected and no block to inherit one from")
        if i not in pool:
            sys.exit(f"unknown {label} id '{i}'. Known: {', '.join(pool)}")
    for i in para_ids:
        if i not in exps:
            sys.exit(f"unknown experience id '{i}'. Known: {', '.join(exps)}")
    if len(para_ids) != len(set(para_ids)):
        sys.exit("the same experience paragraph is used twice")
    if not 1 <= len(para_ids) <= 3:
        sys.exit(f"{len(para_ids)} experience paragraphs; the letter takes two, three at most")

    company = sel.get("company")
    if not company:
        sys.exit("letter.yaml needs a `company`")
    role = sel.get("role", "")
    es = str(sel.get("language", "en")).lower().startswith("es")
    meta = base["meta"]

    missing = [i for i in para_ids if not (sel.get("relevance") or {}).get(i)]
    if missing:
        sys.exit(
            "every experience paragraph needs a `relevance` sentence tying it to this job.\n"
            "Missing for: " + ", ".join(missing)
        )
    if not sel.get("hook"):
        sys.exit("letter.yaml needs a `hook`: the sentence closing paragraph 1, naming this employer")
    if not sel.get("closing_reason"):
        sys.exit("letter.yaml needs a `closing_reason`: what this employer is, opening the close")

    def sub(t):
        return t.replace("{company}", company).replace("{role}", role)

    parts = [sub(meta["greeting_es" if es else "greeting"])]
    parts.append(sub(flat(openings[opening_id]["text"]) + " " + flat(sel["hook"])))
    for i in para_ids:
        parts.append(sub(flat(exps[i]["text"]) + " " + flat(sel["relevance"][i])))
    parts.append(sub(flat(closings[closing_id]["text"]).replace("{closing_reason}", flat(sel["closing_reason"]))))
    parts.append(meta["signoff_es" if es else "signoff"])
    return "\n\n".join(parts) + "\n"


def main():
    folder = resolve_folder(sys.argv[1] if len(sys.argv) > 1 else None)
    base = load(ROOT / "letter_base.yaml")
    text = build(folder, base)
    out = folder / "cover_letter.md"
    out.write_text(text, encoding="utf-8")
    try:
        shown = out.relative_to(ROOT)
    except ValueError:
        shown = out
    print(f"Wrote {shown}")

    import check_letter

    errors, warnings, n, paras = check_letter.check(out)
    for w in warnings:
        print(f"  warn: {w}")
    if errors:
        print("\nFAIL: the rendered letter breaks the voice rules.")
        for e in errors:
            print(f"  error: {e}")
        print("\nFix the prose in letter_base.yaml or the per-job sentences in letter.yaml.")
        return 1
    print(f"OK: {paras} body paragraphs, {n} words, no banned patterns.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
