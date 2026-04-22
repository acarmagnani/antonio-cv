---
name: cv-tailoring
description: Tailors Antonio's CV for a specific job application. Use this skill whenever the user wants to tailor a CV, adapt the CV for a job, create a new application, generate strategy.md, or produce content_tailored.yaml from a job description. Triggers on phrases like "tailor my CV", "new application", "apply for this job", or when the user points to a job_description.md file inside an applications/ folder.
---

# CV Tailoring

This skill produces a tailored CV for a specific job application, in two steps separated by a review checkpoint.

## Inputs

- `content_base.yaml` at the repo root (Antonio's full history).
- `applications/YYYY-MM-company-role/job_description.md` (the posting, pasted by the user).

Before starting, confirm both files exist. If the application folder or job_description.md is missing, ask the user to create them.

## Workflow

### Step 1: Write strategy.md

Read `content_base.yaml` and the `job_description.md` in the current application folder.

Write `strategy.md` in the same application folder with exactly these four sections and nothing else:


### Strategy: [Company, Role]
**Positioning**
[One sentence. How Antonio is framed for this role.]

**Profile**
[Antonio's profile section tailored for this job opening.]

**Experiences**
[One line per experience from content_base.yaml, in the same order as content_base.yaml, each marked KEEP or EXCLUDE.]

**Projects**
[One line per project from content_base.yaml, in the same order as content_base.yaml, each marked KEEP or EXCLUDE.]

Rules for strategy.md:

- Read the current list of experiences and projects from `content_base.yaml` each time. 
- List every experience and every project from `content_base.yaml`, with KEEP or EXCLUDE next to each.
- Do not give reasons for KEEP/EXCLUDE decisions.

After writing `strategy.md`, stop. Tell the user the strategy is ready for review and to reply when they want to proceed. Do not write `content_tailored.yaml` yet.

### Step 2: Write content_tailored.yaml

Only proceed after the user signals approval.

Before generating the YAML, re-read `strategy.md` from disk. The user may have edited it. The on-disk version is authoritative.

Write `content_tailored.yaml` in the same application folder. It must contain only these three top-level keys: `profile`, `experience`, `projects`. Do not include `meta`, `education`, or `skills`. Those live in `content_base.yaml`.

For `profile`:
- Write 2-3 sentences per the Profile rules in CLAUDE.md.
- Use the Profile bullets in strategy.md as the angle.

For `experience`:
- Include only entries marked KEEP.
- Preserve the exact YAML structure from `content_base.yaml`.
- Bullets may be rephrased per the Writing Rules in CLAUDE.md. Do not invent facts.
- Not every bullet from the source has to appear. 

For `projects`:
- Include only entries marked KEEP.
- Same YAML structure rules as experience.
- Same rephrasing and trimming rules.

### Step 3: Copy to root

After writing `content_tailored.yaml` in the application folder, copy it to the repo root as `content_tailored.yaml`. This lets `layout.html` render it.

Use `cp applications/YYYY-MM-company-role/content_tailored.yaml content_tailored.yaml` (from the repo root).

Tell the user the CV is ready and they can open `templates/layout.html` in a browser to print.

## Rules recap (enforced in both steps)

All writing rules in `CLAUDE.md` apply.

The strategy is the plan. The YAML is the execution. Do not redesign the strategy in Step 2. If the strategy seems wrong while generating the YAML, stop and tell the user.