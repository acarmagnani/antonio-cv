#!/usr/bin/env python3
"""
select_cv.py - Validate an application's selection.yaml against content_base.yaml.

Usage:
    python system/select_cv.py <application-folder-name> [--preview]

Tailoring is pure SELECTION: an application folder holds only IDs, never CV text.
This script checks that the selection is well formed. Because no text is ever
copied, "is it verbatim?" cannot fail by construction; the old verify_cv.py check
is replaced by these structural checks:

  1. Every id in `profile`, `bullets` and `projects` exists in content_base.yaml.  -> error
  2. No two bullets come from the same point (no duplicate fact).                  -> error
  3. No duplicate ids in the list.                                                 -> error
  4. Every base role keeps at least one bullet.                                    -> warning
  5. A profile is selected.                                                        -> warning

--preview prints the resolved CV as plain text (useful for a quick read without
opening the PDF).
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not found. Install it with: pip install pyyaml")

ROOT = Path(__file__).parent.parent


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    preview = "--preview" in sys.argv
    if not args:
        sys.exit("Usage: python system/select_cv.py <application-folder-name> [--preview]")

    folder = ROOT / "applications" / args[0]
    sel_path = folder / "selection.yaml"
    if not sel_path.exists():
        sys.exit(f"selection.yaml not found in {folder}")

    base = load(ROOT / "content_base.yaml")
    sel = load(sel_path)

    # Index everything by id.
    variants = {}   # id -> (text, role_index, point_index)
    for ri, role in enumerate(base["experience"]):
        for pi, point in enumerate(role["points"]):
            for v in point["variants"]:
                variants[v["id"]] = (v["text"], ri, pi)
    profiles = {p["id"]: p["text"] for p in base["profiles"]}
    projects = {p["id"]: p for p in base.get("projects", [])}

    errors, warnings = [], []
    wanted = sel.get("bullets") or []

    # 3. Duplicate ids.
    for i in {b for b in wanted if wanted.count(b) > 1}:
        errors.append(f"Duplicate id listed twice: {i}")

    # 1. Unknown ids.
    for b in wanted:
        if b not in variants:
            errors.append(f"Unknown bullet id: {b}")
    prof_id = sel.get("profile")
    if not prof_id:
        warnings.append("No profile selected.")
    elif prof_id not in profiles:
        errors.append(f"Unknown profile id: {prof_id}")
    for pid in sel.get("projects") or []:
        if pid not in projects:
            errors.append(f"Unknown project id: {pid}")

    # 2. Two bullets from the same point.
    by_point = {}
    for b in wanted:
        if b not in variants:
            continue
        _, ri, pi = variants[b]
        by_point.setdefault((ri, pi), []).append(b)
    for ids in by_point.values():
        if len(ids) > 1:
            errors.append(f"DUPLICATE FACT, two variants of the same point: {', '.join(ids)}")

    # 4. Role coverage.
    used_roles = {variants[b][1] for b in wanted if b in variants}
    for ri, role in enumerate(base["experience"]):
        if ri not in used_roles:
            warnings.append(f'Role has 0 bullets: {role["title"]} @ {role["org"]}')

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print("  -", w)
        print()
    if errors:
        print("ERRORS:")
        for e in errors:
            print("  -", e)
        print(f"\nFAILED: {len(errors)} error(s).")
        sys.exit(1)

    print(f"OK: {len(used_roles)} roles, {len(wanted)} bullets, "
          f"{len(sel.get('projects') or [])} projects, all ids resolve.")

    if preview:
        print("\n" + "=" * 70)
        print("PROFILE\n  " + profiles.get(prof_id, "-"))
        for ri, role in enumerate(base["experience"]):
            mine = [b for b in wanted if b in variants and variants[b][1] == ri]
            if not mine:
                continue
            print(f'\n{role["title"]} @ {role["org"]}  ({role["start"]} - {role["end"]})')
            for b in mine:
                print("  -", variants[b][0])
        for pid in sel.get("projects") or []:
            print(f'\n[project] {projects[pid]["name"]}')
            for b in projects[pid].get("bullets", []):
                print("  -", b)


if __name__ == "__main__":
    main()
