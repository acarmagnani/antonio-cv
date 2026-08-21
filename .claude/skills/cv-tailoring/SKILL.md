---
name: cv-tailoring
description: Tailors Antonio's CV for a specific job application by SELECTING content from content_base.yaml (never rewriting it). Use this skill whenever the user wants to tailor a CV, adapt the CV for a job, create a new application, or produce a selection.yaml from a job description. Triggers on phrases like "tailor my CV", "new application", "apply for this job", or when the user points to a job_description.md file inside an applications/ folder.
---

# CV Tailoring

This skill tailors Antonio's CV by **selecting** content from `content_base.yaml`. It never
rewrites bullets, and it never copies CV text into the application folder. An application
folder holds only a list of **ids**; the renderer resolves them against `content_base.yaml`.

Why this way: Antonio wrote all his content deliberately with Claude, once. Because tailoring
writes ids and not prose, invented or reworded text is impossible by construction, and each
application costs a ~30-line file instead of a full copy of the CV.

## How content_base.yaml is structured

- `profiles`: profile variants, each with an `id` and `tags`. Pick exactly one.
- `experience`: the 7 roles. Each role has a list of `points` (underlying facts). Each point has
  one or more `variants` (different phrasings of that same fact), each with an `id` and `tags`.
  Select **at most one variant per point**.
- `projects`: each project has an `id` and `tags`. Select whole projects; bullets are never split.
- `education` and `skills` are STATIC, always from `content_base.yaml`, never tailored.

Ids look like `ramboll.critical-raw-materials-study.v1`, `profile.proptech`,
`project.embodied-carbon-toolkit`. They are stable; never invent one, always read it from
`content_base.yaml`.

Tags (`real-estate | esg | infrastructure | proptech | consulting | generic`) are **hints, not a
filter**. They are coarse: `esg` covers everything from human rights workshops to embodied
carbon. Read the bullet text and decide on meaning, not on tag overlap. `generic` marks a fact
that should appear in every CV.

## Inputs

- `content_base.yaml` at the repo root.
- `applications/<target|wide>/YYYY-MM-company-role/job_description.md`.

If the folder or `job_description.md` is missing, ask the user to create them. For an unsolicited
application there is no posting: write `job_description.md` as a target-role brief, clearly
labelled as such, based on research into the company.

## Workflow

### 1. Read

Read `job_description.md` and `content_base.yaml` in full. Identify what the role actually
requires and which of Antonio's domains it maps to.

### 2. Select (never rewrite)

- Keep **all 7 roles**. Never drop a whole role.
- Go point by point in each role. Include a point if it is relevant to this job, and pick the
  single variant whose framing best fits. Note its `id`.
- At most one variant per point.
- **Minimum coverage:** no kept role should read empty. If a role is thin for this job, include
  adjacent variants that still legitimately fit, so every role has substance.
- Order matters: within a role, list ids most-relevant first. The renderer preserves the order
  they appear in `bullets`.
- Be selective. Target roughly 2 pages, which is about 20-25 bullets plus 4-5 projects. Not
  every point belongs in every CV.
- Pick the `profile` id whose framing best matches the job.
- Select projects whose subject matches the role. Include only the few most relevant; if none
  clearly match, include the 2-3 strongest general ones so the section is not empty.
- If the job genuinely needs something Antonio has not done, flag the gap to the user. Do not
  invent it.

### Choosing the bucket

Every new application goes in `applications/target/` or `applications/wide/`.

- **target/** — aligned with the professional Antonio wants to become AND at a level he could
  realistically get. These are the only ones counted by the `skills-gaps` skill.
- **wide/** — above his level, wrong direction, or a long shot he wants to try anyway.

Decide it when creating the folder and say which bucket you chose and why, in one line. If it is
genuinely borderline, ask him.

### 3. Write selection.yaml

Write `applications/<bucket>/<folder>/selection.yaml`. Ids only, no CV text:

```yaml
profile: profile.proptech

bullets:
  - sweco.department-anchor.v1
  - sweco.climate-risk-assessments.v1
  - ramboll.frameworks-anchor.v1
  # ... grouped by role, most-relevant first within each role

projects:
  - project.rammed-blue-biomass
  - project.embodied-carbon-toolkit
```

List bullets grouped by role, in the same reverse-chronological role order as
`content_base.yaml`. Do not include meta, education, or skills.

### 4. Validate

```bash
python system/select_cv.py <application-folder-name>
```

It fails on an unknown id, a duplicate id, or two variants of the same point. Add `--preview` to
print the resolved CV as text. If it errors, re-read `content_base.yaml` (do not trust memory)
for the correct ids and re-run until it prints `OK`.

### 5. Point the renderer and hand off

Write the folder name into `active_application.txt` at the repo root, then run:

```bash
python system/make_pdfs.py
```

That validates the selection and renders `cv.pdf` plus `cover_letter.pdf` if the letter exists.

### 6. Strategy note (for the cover letter)

Write a short `applications/<folder>/strategy.md`: a one-line positioning statement for this
application, the profile chosen, and one or two threads to lead with. No EXCLUDE lists. The
cover-letter skill builds on this.

### 7. Continue straight into the cover letter

Do not stop here and ask. "Create the application" means the full package: run the **cover-letter** skill next, write `cover_letter.md`, then re-run `python system/make_pdfs.py` so both PDFs exist. Report back in a few short bullets (what was created, where the files are), not a walkthrough of the reasoning.

## Rules

- **Ids only.** Never write CV prose into an application folder. Rewriting a bullet happens only
  when Antonio and Claude edit `content_base.yaml`, never here.
- All 7 roles always present. Education and skills are always static.
- Adding a new bullet to `content_base.yaml` means adding an `id` to it as well.
- Legacy: applications made before this format have a `content_tailored.yaml` with full text and
  are validated by the older `system/verify_cv.py`. The renderer still reads them. Do not create
  new ones.
- All writing rules in `CLAUDE.md` apply.
