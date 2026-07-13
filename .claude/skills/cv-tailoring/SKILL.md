---
name: cv-tailoring
description: Tailors Antonio's CV for a specific job application by SELECTING content from content_base.yaml (never rewriting it). Use this skill whenever the user wants to tailor a CV, adapt the CV for a job, create a new application, or produce content_tailored.yaml from a job description. Triggers on phrases like "tailor my CV", "new application", "apply for this job", or when the user points to a job_description.md file inside an applications/ folder.
---

# CV Tailoring

This skill tailors Antonio's CV by **selecting** content from `content_base.yaml`. It never rewrites bullets. Every bullet and the profile are copied **verbatim** from `content_base.yaml`. The only decisions are: which facts to include, which phrasing variant to use, how to order them, and which profile to pick. A verifier enforces the verbatim rule.

Why this way: Antonio wrote all his content deliberately with Claude, once. He does not want to re-read a tailored CV hunting for invented or reworded claims. Selection keeps the text provably his.

## How content_base.yaml is structured

- `profiles`: profile variants, each with `tags`. Pick exactly one, verbatim.
- `experience`: the 7 roles. Each role has a list of `points` (underlying facts). Each point has one or more `variants` (different phrasings of that same fact), each with `tags`. Select **at most one variant per point**, verbatim.
- `projects`: each project has `tags`. Select whole projects whose tags overlap the job (bullets are copied verbatim, never split). `education` and `skills` are STATIC, always from `content_base.yaml`, never tailored.

Tags (`real-estate | esg | infrastructure | proptech | consulting | generic`) are hints for selection, not hard rules. `generic` marks a fact that should appear in every CV.

## Inputs

- `content_base.yaml` at the repo root.
- `applications/YYYY-MM-company-role/job_description.md`.

If the folder or `job_description.md` is missing, ask the user to create them.

## Workflow

### 1. Read

Read `job_description.md` and `content_base.yaml` in full. Identify what the role actually requires and which of Antonio's domains it maps to.

### 2. Select (never rewrite)

- Keep **all 7 roles**. Never drop a whole role.
- Go point by point in each role. Include a point if it is relevant to this job, and pick the single variant whose framing best fits. Copy its text verbatim.
- At most one variant per point.
- **Minimum coverage:** no kept role should read empty. If a role is thin for this job, include adjacent variants that still legitimately fit, so every role has substance. Antonio's content skews ESG / consulting / real-estate; for an off-profile role (e.g. a PropTech job) actively look for the bridging variants.
- Order bullets within a role most-relevant first. Ordering is allowed; editing text is not.
- Be selective. Target roughly 2 pages. Not every point belongs in every CV.
- Pick the `profile` variant whose tags best match the job. Copy verbatim.
- Select projects whose `tags` overlap the job (whole project, bullets verbatim). Include only the few most relevant; if none clearly match, include the 2-3 strongest general ones so the section is not empty. Keep the CV to roughly 2 pages.
- If the job genuinely needs something Antonio has not done, flag the gap to the user. Do not invent it.

### 3. Write content_tailored.yaml

Write `applications/<folder>/content_tailored.yaml` with ONLY `profile` and `experience`:

```yaml
profile: "<verbatim profile text>"
experience:
  - title: "..."
    org: "..."
    location: "..."
    start: "..."
    end: "..."
    bullets:
      - "<verbatim bullet text>"
projects:
  - name: "..."
    org: "..."
    location: "..."
    bullets:
      - "<verbatim project bullet>"
```

Roles in reverse-chronological order (same as `content_base.yaml`). Include the selected projects (name/org/location/bullets, verbatim; drop the `tags` field). Do not include meta, education, or skills.

### 4. Verify

```bash
python system/verify_cv.py <application-folder-name>
```

It fails if any bullet or the profile is not verbatim from `content_base.yaml`, or if two bullets come from the same point. If it errors, re-read `content_base.yaml` (do not trust memory) and paste the exact text, then re-run until it prints `OK`.

### 5. Point the renderer and hand off

Write the folder name into `active_application.txt` at the repo root. Then tell the user to run `python system/make_cv_pdf.py` to produce `cv.pdf` (or open `system/templates/cv.html` and Ctrl+P).

### 6. Strategy note (for the cover letter)

Write a short `applications/<folder>/strategy.md`: a one-line positioning statement for this application, the profile variant chosen, and one or two threads to lead with. No EXCLUDE lists. The cover-letter skill builds on this.

## Rules

- **Verbatim only.** Tailoring selects and orders; it never edits bullet or profile text. Rewriting only happens when Antonio and Claude build `content_base.yaml`, never here.
- All 7 roles always present. Projects, education, and skills are always static.
- All writing rules in `CLAUDE.md` apply.
