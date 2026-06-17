---
name: cv-tailoring
description: Tailors Antonio's CV for a specific job application. Use this skill whenever the user wants to tailor a CV, adapt the CV for a job, create a new application, or produce content_tailored.yaml from a job description. Triggers on phrases like "tailor my CV", "new application", "apply for this job", or when the user points to a job_description.md file inside an applications/ folder.
---

# CV Tailoring

This skill tailors Antonio's CV in three steps. Steps 1 and 2 are separated by a review checkpoint so Antonio can adjust the selected tags before the script runs.

## Inputs

- `content_base.yaml` at the repo root (source of truth, with tagged bullets and multiple profile variants).
- `applications/YYYY-MM-company-role/job_description.md` (the posting, pasted by the user).

Before starting, confirm both files exist. If the application folder or `job_description.md` is missing, ask the user to create them.

## Tag taxonomy

There are exactly six tags. Do not invent tags outside this list.

- `real-estate` — real estate development, investment, advisory, asset management, feasibility
- `esg` — sustainability consulting, ESG due diligence, human rights, CSRD, supply chain, LCA
- `infrastructure` — international development consulting, multilateral/bilateral-funded infrastructure projects
- `proptech` — tech-enabled roles in the built environment: data tools, computational analysis, GIS, ML, digital platforms for real estate or cities
- `consulting` — cross-cutting process skills: research, reporting, client deliverables, project coordination
- `generic` — always included regardless of selected tags. Do not select or deselect this tag. It is set in content_base.yaml by Antonio and applied automatically by the script.

When reading a job description, identify which 1–3 of these buckets the role primarily falls into. Most roles map cleanly to one or two. A PropTech startup → `proptech` (+ `real-estate` if focused on property). An ESG consulting firm → `esg + consulting`. A real estate developer → `real-estate`. Infrastructure consulting → `infrastructure + consulting`. A VC investing in PropTech → `real-estate + proptech + consulting`.

## Workflow

### Step 1: Write selected_tags.yaml

Read `content_base.yaml` and `job_description.md`.

Identify 6–12 tags from the list above that best describe what this role requires. Prioritize tags that appear explicitly in the job description or map directly to its core requirements. Avoid over-selecting: a wider tag set means more bullets, which dilutes relevance.

Write `selected_tags.yaml` in the application folder:

```yaml
tags:
  - esg
  - reporting
  - stakeholder-engagement
```

After writing, stop. Tell the user which tags were selected and briefly explain the reasoning (one line per tag is enough). Ask them to review and edit `selected_tags.yaml` directly, then signal when ready to proceed.

### Step 2: Run the selection script

Only proceed after the user signals approval.

Run from the repo root:

```bash
python select_cv.py <application-folder-name>
```

The script reads `selected_tags.yaml` + `content_base.yaml`, selects bullets with any matching tag, picks the profile variant with the highest tag overlap, and writes `content_tailored.yaml` to the application folder with plain strings (tags stripped).

Report the script output to the user (experiences included, projects included, profile chosen).

### Step 3: Light editorial review

Read `content_tailored.yaml` and `job_description.md`.

Look for gaps: specific terminology, frameworks, or requirements named in the job description that are absent or weakly represented in the selected output. Make targeted wording adjustments only where the gap is real and the underlying experience supports the change.

Rules:
- Do not add facts not present in `content_base.yaml`.
- Do not rewrite bullets wholesale. Adjust a verb, a term, or a framing — not the substance.
- Do not touch bullets that already cover the point well.
- If a genuine gap cannot be addressed without invention, flag it to the user.

Write the edited version back to `content_tailored.yaml`.

### Step 4: Update active_application.txt

Write the application folder name to `active_application.txt` at the repo root:

```bash
echo "YYYY-MM-company-role" > active_application.txt
```

Tell the user the CV is ready and they can open `templates/cv.html` in a browser to print.

## Rules recap

All writing rules in `CLAUDE.md` apply throughout. The tag list is the selection constraint — respect it.
