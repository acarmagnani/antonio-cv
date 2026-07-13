#!/usr/bin/env python3
"""
verify_cv.py - Verify a tailored CV against the source of truth.

Usage:
    python verify_cv.py <application-folder-name>

The tailoring step (done by Claude) SELECTS content from content_base.yaml; it
never rewrites it. This script enforces that. It checks
applications/<folder>/content_tailored.yaml against content_base.yaml:

  1. Every experience bullet appears VERBATIM as a variant in content_base.yaml
     (nothing invented or edited during tailoring).           -> hard error
  2. No two bullets come from the same point (no duplicate fact). -> hard error
  3. The profile is one of the base profile variants, verbatim.   -> hard error
  4. Every base role is present and none is left with 0 bullets.  -> warning

Exits non-zero if any hard check fails, so it can gate the pipeline.
Projects, education, and skills are static (always from content_base.yaml) and
are not part of the tailored file, so they are not checked here.
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not found. Install it with: pip install pyyaml")

ROOT = Path(__file__).parent.parent  # script lives in system/; content lives in the repo root


def norm(s):
    """Collapse all whitespace so YAML line-wrapping differences don't matter,
    while any real word change still shows up."""
    return " ".join(str(s).split())


def bullet_text(b):
    return b["text"] if isinstance(b, dict) else b


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def role_key(role):
    return f'{role.get("title")} @ {role.get("org")}'


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python verify_cv.py <application-folder-name>")

    folder = ROOT / "applications" / sys.argv[1]
    tailored_path = folder / "content_tailored.yaml"
    if not tailored_path.exists():
        sys.exit(f"content_tailored.yaml not found in {folder}")

    base = load(ROOT / "content_base.yaml")
    tailored = load(tailored_path)

    # Map each variant text -> the point it belongs to (globally unique id).
    variant_point = {}
    for ri, role in enumerate(base["experience"]):
        for pi, point in enumerate(role["points"]):
            for v in point["variants"]:
                variant_point[norm(v["text"])] = (ri, pi)
    profile_texts = {norm(p["text"]) for p in base["profiles"]}
    base_role_keys = [role_key(r) for r in base["experience"]]
    project_bullets = {norm(b) for proj in base.get("projects", []) for b in proj.get("bullets", [])}

    errors, warnings = [], []

    # 3. Profile must be a verbatim base variant.
    prof = tailored.get("profile")
    if not prof:
        warnings.append("No profile in tailored file.")
    elif norm(prof) not in profile_texts:
        errors.append("Profile is not a verbatim base profile variant (invented or edited).")

    # 1 + 2. Bullets verbatim, no two from the same point.
    used_points = {}
    seen_roles = []
    for role in tailored.get("experience", []) or []:
        rk = role_key(role)
        seen_roles.append(rk)
        bullets = role.get("bullets", []) or []
        if not bullets:
            warnings.append(f"Role has 0 bullets: {rk}")
        for b in bullets:
            t = norm(bullet_text(b))
            if t not in variant_point:
                errors.append(f"INVENTED/EDITED bullet in [{rk}]: {bullet_text(b)!r}")
                continue
            pid = variant_point[t]
            if pid in used_points:
                errors.append(
                    f"DUPLICATE FACT (two bullets from the same point):\n"
                    f"      - {used_points[pid]!r}\n"
                    f"      - {bullet_text(b)!r}"
                )
            else:
                used_points[pid] = bullet_text(b)

    # Project bullets must also be verbatim (projects are selected whole).
    for proj in tailored.get("projects", []) or []:
        pname = proj.get("name", "?")
        for b in proj.get("bullets", []) or []:
            if norm(bullet_text(b)) not in project_bullets:
                errors.append(f"INVENTED/EDITED project bullet in [{pname}]: {bullet_text(b)!r}")

    # 4. Coverage: every base role should appear.
    for rk in base_role_keys:
        if rk not in seen_roles:
            warnings.append(f"Base role missing from tailored CV: {rk}")

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print("  -", w)
        print()
    if errors:
        print("ERRORS:")
        for e in errors:
            print("  -", e)
        print(f"\nFAILED: {len(errors)} error(s). Tailored bullets must copy base text verbatim.")
        sys.exit(1)

    print(f"OK: {len(seen_roles)} roles, {len(used_points)} bullets, all verbatim, no duplicate facts.")


if __name__ == "__main__":
    main()
