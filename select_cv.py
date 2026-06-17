#!/usr/bin/env python3
"""
select_cv.py  -  Generate content_tailored.yaml from tagged bullets in content_base.yaml.

Usage:
    python select_cv.py <application-folder-name>

    e.g.  python select_cv.py 2026-05-arup-project-management-consultant

Reads:
    content_base.yaml                            (source of truth, with tagged bullets)
    applications/<folder>/selected_tags.yaml     (list of tags chosen by Claude)

Writes:
    applications/<folder>/content_tailored.yaml  (plain-string bullets, tags stripped)
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not found. Install it with: pip install pyyaml")


ROOT = Path(__file__).parent


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def select_bullets(bullets, selected_tags):
    """Return bullet texts tagged generic or whose tags overlap with selected_tags."""
    return [
        b["text"]
        for b in bullets
        if "generic" in b.get("tags", []) or any(t in selected_tags for t in b.get("tags", []))
    ]


def best_profile(profiles, selected_tags):
    """Return the profile text with the most tags in common with selected_tags."""
    scored = [
        (len(set(p.get("tags", [])) & selected_tags), p["text"])
        for p in profiles
    ]
    return max(scored, key=lambda x: x[0])[1]


def drop_none(d):
    return {k: v for k, v in d.items() if v is not None}


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python select_cv.py <application-folder-name>")

    folder = ROOT / "applications" / sys.argv[1]
    if not folder.is_dir():
        sys.exit(f"Application folder not found: {folder}")

    tags_path = folder / "selected_tags.yaml"
    if not tags_path.exists():
        sys.exit(f"selected_tags.yaml not found in {folder}")

    base = load(ROOT / "content_base.yaml")
    tags_data = load(tags_path)
    selected = set(tags_data.get("tags", []))

    if not selected:
        sys.exit("selected_tags.yaml contains no tags.")

    # Profile: pick the variant with the highest tag overlap
    profile = best_profile(base["profiles"], selected)

    # Experience: always keep all entries, select only matching bullets
    experience = []
    for role in base["experience"]:
        bullets = select_bullets(role["bullets"], selected)
        experience.append(drop_none({
            "title": role.get("title"),
            "org": role.get("org"),
            "location": role.get("location"),
            "start": role.get("start"),
            "end": role.get("end"),
            "bullets": bullets,
        }))

    # Projects: always keep all entries, select only matching bullets
    projects = []
    for proj in base["projects"]:
        bullets = select_bullets(proj["bullets"], selected)
        projects.append(drop_none({
            "name": proj.get("name"),
            "org": proj.get("org"),
            "location": proj.get("location"),
            "bullets": bullets,
        }))

    output = {"profile": profile, "experience": experience, "projects": projects}

    out_path = folder / "content_tailored.yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(output, f, allow_unicode=True, default_flow_style=False,
                  sort_keys=False, width=120)

    bullet_counts = {e.get("title", "?"): len(e.get("bullets", [])) for e in experience}
    print(f"Written:          {out_path}")
    print(f"Tags used ({len(selected)}):   {sorted(selected)}")
    print(f"Profile selected: {profile[:80]}...")
    print(f"Bullets per role: {bullet_counts}")


if __name__ == "__main__":
    main()
