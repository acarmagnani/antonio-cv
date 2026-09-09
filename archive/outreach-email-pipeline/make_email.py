#!/usr/bin/env python3
"""Render an application's email.yaml into outreach_email.md, then validate it.

This is to outreach emails what make_letter.py is to cover letters: the application
folder holds ids plus two short per-job clauses, never a free-written email. All
reusable prose lives in email_base.yaml.

An email is written ONLY when the posting names a person and an address. If there is
no address in the posting, there is no email.yaml and no email.

email.yaml looks like:

    extends: data-built-environment      # a block in email_base.yaml
    to: "GBMF@Novonordisk.com"           # from the posting, never hunted down elsewhere
    contact: "Gábor Máté Farkas"         # the greeting uses the first name
    company: "Novo Nordisk"
    role: "Supply Chain Professional"      # the bare title
    team: "Planning Solution Development"  # optional, renders as "... position in <team>"
    when: "Last week"                    # optional, defaults to "Last week"
    referral: "Fábio Aspis, Global Senior Data Ethics Compliance Counsel at Novo Nordisk"
                                         # ONLY with an opening tagged `referral`
    attention: >                         # completes "What caught my attention in the posting is ..."
      the work of translating user needs into system improvements and then supporting their adoption
    experiences:                         # optional, overrides the block's pair
      - exp.ramboll.systems-and-training
      - exp.isay.plugin-adoption
    relevance:                           # OPTIONAL, one clause per experience. See the skill:
      exp.isay.plugin-adoption: >        # the default is that `attention` connects both.
        ...
    closing_tail: >                      # completes "... could be useful ..."
      in the solution areas your team owns

Usage:
    python system/make_email.py                      # active application
    python system/make_email.py <application-folder>
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))


def load(p):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


def flat(text):
    """YAML folded scalars keep newlines; an email paragraph is one long line."""
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
    sel_path = folder / "email.yaml"
    if not sel_path.exists():
        sys.exit(
            f"no email.yaml in {folder}.\n"
            "An outreach email is only written when the posting names a person and an "
            "address. If it does not, there is nothing to render here."
        )
    sel = load(sel_path)

    blocks = base["blocks"]
    block = {}
    if sel.get("extends"):
        if sel["extends"] not in blocks:
            sys.exit(f"unknown block '{sel['extends']}'. Known: {', '.join(blocks)}")
        block = blocks[sel["extends"]]

    openings = index(base["openings"])
    bridges = index(base["bridges"])
    exps = index(base["experiences"])
    closings = index(base["closings"])

    opening_id = sel.get("opening", block.get("opening"))
    bridge_id = sel.get("bridge", block.get("bridge"))
    closing_id = sel.get("closing", block.get("closing"))
    exp_ids = sel.get("experiences", block.get("experiences", []))

    for label, i, pool in (
        ("opening", opening_id, openings),
        ("bridge", bridge_id, bridges),
        ("closing", closing_id, closings),
    ):
        if not i:
            sys.exit(f"no {label} selected and no block to inherit one from")
        if i not in pool:
            sys.exit(f"unknown {label} id '{i}'. Known: {', '.join(pool)}")
    for i in exp_ids:
        if i not in exps:
            sys.exit(f"unknown experience id '{i}'. Known: {', '.join(exps)}")
    if len(exp_ids) != len(set(exp_ids)):
        sys.exit("the same experience is used twice")
    if not 1 <= len(exp_ids) <= 2:
        sys.exit(f"{len(exp_ids)} experiences; an email takes one or two, never three")

    for field in ("to", "contact", "company", "role", "attention", "closing_tail"):
        if not sel.get(field):
            sys.exit(f"email.yaml needs `{field}`")

    # The referral claim has to be true and has to be backed by a field. An opening
    # tagged `referral` without one would silently render "{referral}".
    tags = openings[opening_id].get("tags") or []
    if "referral" in tags and not sel.get("referral"):
        sys.exit(
            f"opening '{opening_id}' claims a referral but email.yaml has no `referral`.\n"
            "Either name the person and their title, or pick an opening without a referral."
        )
    if sel.get("referral") and "referral" not in tags:
        sys.exit(
            f"email.yaml has a `referral` but opening '{opening_id}' does not use it. "
            "Pick an opening tagged `referral`."
        )

    is_team = "team" in tags
    company, role = sel["company"], sel["role"]
    team = flat(sel.get("team") or "")
    team_clause = f" in {team}" if team else ""
    contact_first = flat(sel.get("greeting_name") or sel["contact"]).split()[0]
    meta = base["meta"]

    def sub(t):
        return (
            t.replace("{company}", company)
            .replace("{role}", role)
            .replace("{team_clause}", team_clause)
            .replace("{contact_first}", contact_first)
            .replace("{contact}", flat(sel["contact"]))
            .replace("{when}", flat(sel.get("when") or "Last week"))
            .replace("{referral}", flat(sel.get("referral") or ""))
        )

    case = [
        flat(f"What caught my attention in the posting is {flat(sel['attention'])}")
        + ", "
        + flat(bridges[bridge_id]["text"])
    ]
    for pos, i in enumerate(exp_ids):
        # `text_second` is the same fact pre-written to follow another experience, so a
        # two-experience email reads as one argument rather than as a list of jobs.
        key = "text_second" if pos and exps[i].get("text_second") else "text"
        case.append(flat(exps[i][key]))
        rel = (sel.get("relevance") or {}).get(i)
        if rel:
            case.append(flat(rel))

    closing = flat(closings[closing_id]["text"]).replace("{closing_tail}", flat(sel["closing_tail"]))

    subject = flat(sel.get("subject") or meta.get("subject", "{role}{team_clause}"))
    header = f"**To:** {sel['to']}\n**Subject:** {sub(subject)}\n\n---"

    parts = [
        header,
        sub(meta["greeting_team"] if is_team else meta["greeting"]),
        sub(flat(openings[opening_id]["text"])),
        sub(" ".join(case)),
        sub(closing),
        meta["signoff"],
    ]
    return "\n\n".join(parts) + "\n"


def main():
    folder = resolve_folder(sys.argv[1] if len(sys.argv) > 1 else None)
    base = load(ROOT / "email_base.yaml")
    text = build(folder, base)
    out = folder / "outreach_email.md"
    out.write_text(text, encoding="utf-8")
    try:
        shown = out.relative_to(ROOT)
    except ValueError:
        shown = out
    print(f"Wrote {shown}")

    import check_email

    errors, warnings, n, paras = check_email.check(out)
    for w in warnings:
        print(f"  warn: {w}")
    if errors:
        print("\nFAIL: the rendered email breaks the voice rules.")
        for e in errors:
            print(f"  error: {e}")
        print("\nFix the prose in email_base.yaml or the per-job clauses in email.yaml.")
        return 1
    print(f"OK: {paras} body paragraphs, {n} words, no banned patterns.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
