# CV & Cover Letter Project

This repository holds Antonio Carmagnani's CV content and a workflow for producing tailored CVs and cover letters for specific job applications.


## About Antonio

Antonio is an architect by training (B.Arch., Mackenzie São Paulo) currently finishing an M.Arch. in Architecture Computation at The Royal Danish Academy. His background spans four domains that can be framed in different combinations depending on the role:

- **Real estate development** — feasibility studies, financial modeling, zoning analysis (OSPA, Itaú-Unibanco)
- **ESG and sustainability consulting** — Human Rights Impact Assessments, CSRD/double materiality, supply chain due diligence (Ramboll), infrastructure project work (Sweco)
- **Computational design and data** — Python, GIS, parametric modeling, machine learning (academic projects, Isay Weinfeld)
- **Architecture practice** — BIM, Revit, Grasshopper, project documentation

He is based in Copenhagen and applying to roles across consulting, real estate, ESG, and computational/data-adjacent fields. He does not have a fixed target role — the CV should be tailored to present a coherent, job-specific purpose for each application, drawing from the relevant parts of his background rather than defaulting to one framing.

**Important**: The goal of each tailored CV is to look like its purpose is aligned with the specific job — not scattered across all his interests. Inclusion decisions should be deliberate. Not every experience and not every bullet belongs in every CV.

## Writing rules

These apply to all outputs from this project — tailored CVs, cover letters, everything.

### Truthfulness

- Never invent experiences, roles, responsibilities, or outcomes that are not in content_base.yaml.
- Rephrasing to shift emphasis is expected and encouraged: changing the verb, the framing, or which aspect of a bullet is highlighted is fine, as long as the underlying facts are preserved.
- Minor specificity additions are allowed only when (a) the job description names a specific tool, method, or terminology that is clearly central to the role, and (b) it would be reasonable to infer Antonio used or encountered it given what's in his CV. Do not add generic industry buzzwords under this rule. When in doubt, don't add.
- If the job description calls for something Antonio genuinely hasn't done, flag the gap and ask. Do not stretch an existing experience to cover it.
- Avoid em dashes. Use commas, periods, or parentheses instead.

### Bullet style

- Preserve concrete details: tool names, numbers, specific outputs, project names.
- Bullets should convey analysis, decision support, or delivery — not just activity. 

### Profile summary

It must do a different job than the rest of the CV.

- Length: 2 to 3 sentences. Tight.
- Do not list experiences or skills. Those are already listed below.
- Convey profile, purpose, and direction. Who Antonio is professionally, and what he is trying to do in the context of this specific role.

## File structure

content_base.yaml:         Source of truth. Full history, never edit during tailoring.
content_tailored.yaml:     Scratch file at root. The last tailored CV, copied here by the skill so that layout.html can render it. Not authoritative, do not edit directly.
templates/layout.html:     Renders a CV from content_base.yaml + content_tailored.yaml.
assets/styles.css:         CV styling.
applications/:             One folder per job application.
YYYY-MM-company-role/:     Naming convention: year-month-company-role, kebab-case.
job_description.md:        Pasted from the job posting.
strategy.md:               Tailoring strategy for this application.
content_tailored.yaml:     The tailored CV content. Authoritative for this application.
cover_letter.md:           Optional. Cover letter for this application.
.claude/skills/:           Claude Code skills for CV tailoring and cover letters.

### Application folder naming

- Format: `YYYY-MM-company-role`, lowercase, hyphens for spaces.

### The root `content_tailored.yaml`

- It is a copy of the tailored YAML from the most recently worked-on application.
- The CV tailoring skill writes to the application folder first, then copies to the root.
- `layout.html` reads from this root file plus `content_base.yaml`.
- Never edit the root file directly. Edit the one in the application folder, then re-copy.

## Workflows

Detailed workflows for CV tailoring and cover letter writing live in `.claude/skills/`:

- `.claude/skills/cv-tailoring/SKILL.md`: the CV tailoring workflow (strategy → YAML).
- `.claude/skills/cover-letter/SKILL.md`: cover letter writing, builds on an existing application's strategy and tailored CV.

Claude Code auto-loads the relevant skill based on the task.