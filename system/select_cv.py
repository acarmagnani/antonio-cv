#!/usr/bin/env python3
"""
select_cv.py - Validate a CV selection against content_base.yaml.

Usage:
    python system/select_cv.py <application-folder-name> [--preview]
    python system/select_cv.py --preset <preset-name> [--preview]
    python system/select_cv.py --list-presets

Tailoring is pure SELECTION: nothing here holds CV text, only ids resolved against
content_base.yaml. Because no text is ever copied, "is it verbatim?" cannot fail by
construction; these structural checks replace it:

  1. Every id in `profile`, `bullets`, `projects` and `skills` exists.          -> error
  2. No two bullets come from the same point (no duplicate fact).              -> error
  3. No duplicate ids in the list.                                             -> error
  4. Roles with no bullets are listed as deliberately omitted.                 -> info
  5. A profile is selected.                                                    -> warning

An application usually extends a preset from presets.yaml and records only the
delta, which is what makes one application readable at a glance:

    extends: real-estate-investment
    add:
      - ramboll.genesta-supplier-human-rights.v1
    drop:
      - itau.furniture-inventory-tool.v1

--preview prints the resolved CV as plain text.
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


def index_base(base):
    """id -> kind, plus the lookups the resolver and preview need."""
    variants = {}                       # bullet id -> (text, role_index, point_index)
    for ri, role in enumerate(base["experience"]):
        for pi, point in enumerate(role["points"]):
            for v in point["variants"]:
                variants[v["id"]] = (v["text"], ri, pi)
    return {
        "variants": variants,
        "profiles": {p["id"]: p["text"] for p in base["profiles"]},
        "projects": {p["id"]: p for p in base.get("projects", [])},
        "skills": list((base.get("skills") or {}).keys()),
        "role_ids": [r.get("id") for r in base["experience"]],
    }


def resolve(sel, base, presets, idx):
    """Flatten `extends` + `add` + `drop` into a plain selection.

    `add` and `drop` are routed by what the id actually is, so one flat list can
    carry bullets, projects and skill groups without the author having to say
    which is which.
    """
    errors = []
    sel = sel or {}
    preset_name = sel.get("extends")

    if preset_name:
        preset = (presets or {}).get("presets", {}).get(preset_name)
        if preset is None:
            known = ", ".join(sorted((presets or {}).get("presets", {})))
            errors.append(f"Unknown preset: {preset_name} (known: {known})")
            preset = {}
    else:
        preset = {}

    out = {
        "profile": sel.get("profile") or preset.get("profile"),
        "bullets": list(sel.get("bullets") or preset.get("bullets") or []),
        "projects": list(sel.get("projects") or preset.get("projects") or []),
        # `roles` documents which roles the block intends to show. It is validated,
        # never used for ordering: rendering is always reverse-chronological.
        "roles": list(sel.get("roles") or preset.get("roles") or []),
        "skills": list(sel.get("skills") or preset.get("skills") or idx["skills"]),
        "preset": preset_name,
    }

    def kind(i):
        if i in idx["variants"]:
            return "bullets"
        if i in idx["projects"]:
            return "projects"
        if i in idx["skills"]:
            return "skills"
        return None

    for i in sel.get("drop") or []:
        k = kind(i)
        if k is None:
            errors.append(f"Unknown id in drop: {i}")
        elif i in out[k]:
            out[k].remove(i)
        else:
            errors.append(f"drop lists an id the preset does not include: {i}")

    for i in sel.get("add") or []:
        k = kind(i)
        if k is None:
            errors.append(f"Unknown id in add: {i}")
        elif i in out[k]:
            errors.append(f"add lists an id already included: {i}")
        else:
            out[k].append(i)

    return out, errors


def validate(res, base, idx):
    errors, warnings = [], []
    wanted = res["bullets"]

    for i in {b for b in wanted if wanted.count(b) > 1}:
        errors.append(f"Duplicate id listed twice: {i}")
    for b in wanted:
        if b not in idx["variants"]:
            errors.append(f"Unknown bullet id: {b}")

    if not res["profile"]:
        warnings.append("No profile selected.")
    elif res["profile"] not in idx["profiles"]:
        errors.append(f"Unknown profile id: {res['profile']}")

    for pid in res["projects"]:
        if pid not in idx["projects"]:
            errors.append(f"Unknown project id: {pid}")
    for s in res["skills"]:
        if s not in idx["skills"]:
            errors.append(f"Unknown skill group: {s}")

    by_point = {}
    for b in wanted:
        if b in idx["variants"]:
            _, ri, pi = idx["variants"][b]
            by_point.setdefault((ri, pi), []).append(b)
    for ids in by_point.values():
        if len(ids) > 1:
            errors.append(f"DUPLICATE FACT, two variants of the same point: {', '.join(ids)}")

    used = {idx["variants"][b][1] for b in wanted if b in idx["variants"]}
    for rid in res["roles"]:
        if rid not in idx["role_ids"]:
            errors.append(f"Unknown role id in roles: {rid}")
        elif idx["role_ids"].index(rid) not in used:
            warnings.append(f"roles lists '{rid}' but no bullet selects it.")

    return errors, warnings


def ordered_roles(res, base, idx):
    """Roles that actually have bullets, ALWAYS in content_base order, which is
    reverse-chronological. A CV is reverse-chronological, full stop: `roles`
    declares which roles a block shows, never the order they show in."""
    used = {idx["variants"][b][1] for b in res["bullets"] if b in idx["variants"]}
    return sorted(used)


def main():
    argv = sys.argv[1:]
    preview = "--preview" in argv
    presets_path = ROOT / "presets.yaml"
    presets = load(presets_path) if presets_path.exists() else {"presets": {}}

    if "--list-presets" in argv:
        for name, p in (presets.get("presets") or {}).items():
            print(f"{name}\n    {p.get('label', '')}")
            print(f"    roles: {', '.join(p.get('roles') or [])}")
            print(f"    {len(p.get('bullets') or [])} bullets, "
                  f"{len(p.get('projects') or [])} projects")
        return

    base = load(ROOT / "content_base.yaml")
    idx = index_base(base)

    if "--preset" in argv:
        name = argv[argv.index("--preset") + 1]
        sel, label = {"extends": name}, f"preset '{name}'"
    else:
        args = [a for a in argv if not a.startswith("--")]
        if not args:
            sys.exit(__doc__.strip().split("\n\n")[1])
        folder = ROOT / "applications" / args[0]
        sel_path = folder / "selection.yaml"
        if not sel_path.exists():
            sys.exit(f"selection.yaml not found in {folder}")
        sel, label = load(sel_path), args[0]

    res, resolve_errors = resolve(sel, base, presets, idx)
    errors, warnings = validate(res, base, idx)
    errors = resolve_errors + errors

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

    order = ordered_roles(res, base, idx)
    omitted = [f'{r["title"]} @ {r["org"]}'
               for ri, r in enumerate(base["experience"]) if ri not in order]
    if omitted:
        print("ROLES OMITTED (deliberate):")
        for o in omitted:
            print("  -", o)
        print()

    src = f" via preset '{res['preset']}'" if res["preset"] else ""
    print(f"OK: {label}{src} -> {len(order)} roles shown, {len(res['bullets'])} bullets, "
          f"{len(res['projects'])} projects, {len(res['skills'])} skill groups.")

    if preview:
        print("\n" + "=" * 70)
        print("PROFILE\n  " + idx["profiles"].get(res["profile"], "-"))
        for ri in order:
            role = base["experience"][ri]
            print(f'\n{role["title"]} @ {role["org"]}  ({role["start"]} - {role["end"]})')
            for b in res["bullets"]:
                if idx["variants"][b][1] == ri:
                    print("  -", idx["variants"][b][0])
        for pid in res["projects"]:
            print(f'\n[project] {idx["projects"][pid]["name"]}')
            for b in idx["projects"][pid].get("bullets", []):
                print("  -", b)
        print("\n[skills]")
        for s in res["skills"]:
            print(f'  {s}: {", ".join(base["skills"][s])}')


if __name__ == "__main__":
    main()
