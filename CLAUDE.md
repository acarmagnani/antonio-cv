# CV & Cover Letter Project

This repository holds Antonio Carmagnani's CV content and a workflow for producing tailored CVs and cover letters for specific job applications.


## About Antonio

Antonio is an architect by training (B.Arch., Mackenzie São Paulo) with a M.Arch. in Architecture Computation at The Royal Danish Academy. His background spans four domains that can be framed in different combinations depending on the role:

- **Real estate development** — feasibility studies, financial modeling, zoning analysis (OSPA, Itaú-Unibanco, Isay Weinfeld)
- **ESG and sustainability consulting** — Human Rights Impact Assessments, CSRD/double materiality, supply chain due diligence (Ramboll), infrastructure project work (Sweco)
- **Computational design and data** — Python, GIS, parametric modeling, machine learning (academic projects, Isay Weinfeld)
- **Architecture practice** — BIM, Revit, Grasshopper, project documentation (Isay Weinfeld, Felipe Hess)

He is based in Copenhagen and applying to roles across consulting, real estate, ESG, and computational/data-adjacent fields. He does not have a fixed target role — the CV should be tailored to present a coherent, job-specific purpose for each application, drawing from the relevant parts of his background rather than defaulting to one framing.

**Important**: The goal of each tailored CV is to look like its purpose is aligned with the specific job — not scattered across all his interests. Inclusion decisions should be deliberate. Not every experience and not every bullet belongs in every CV.

## Writing rules

There are two distinct phases, with different rules:

- **Authoring** `content_base.yaml` (done with Antonio, occasionally): writing his full history as `points` with tagged phrasing `variants`. Rephrasing, emphasis-shifting, and tasteful oversell live here.
- **Tailoring** a CV for a job (per application): pure SELECTION of existing text. No rewriting.

### Truthfulness

- Never invent experiences, roles, responsibilities, or outcomes that are not in content_base.yaml.
- During **tailoring**, bullets and the profile are copied **verbatim** from content_base.yaml. Do not reword them, not even slightly. `verify_cv.py` enforces this.
- During **authoring**, rephrasing to shift emphasis is expected: the same fact can have multiple tagged variants (e.g. an ESG framing and a PropTech framing). Tasteful oversell is wanted (strong verbs, best-angle framing), but every claim must be defensible in an interview. Never fabricate tools, clients, or metrics.
- If the job description calls for something Antonio genuinely hasn't done, flag the gap and ask. Do not stretch to cover it.
- Avoid em dashes. Use commas, periods, or parentheses instead.

### Bullet style

- Preserve concrete details: tool names, numbers, specific outputs. Keep client/project names only where Antonio is sure of them.
- Bullets should convey analysis, decision support, or delivery, not just activity.
- Translate one-off decorative anecdotes into the transferable skill they demonstrate, rather than describing the specific item.

### Profile summary

Profiles are **pre-written variants** in content_base.yaml, selected verbatim by tag match. They must do a different job than the rest of the CV: convey who Antonio is professionally and his direction for this kind of role. Antonio's preferred voice opens impersonally ("Experience in..."), names his M.Arch focus, lists a few hands-on skills, and ends with a "Motivated by..." line. No "professional / consultant / practitioner" self-labels.

## File structure

- **content_base.yaml**:         Source of truth. `profiles` (tagged profile variants), `experience` (7 roles, each a list of `points` with tagged phrasing `variants`), tag-selectable `projects` (tags per whole project), and STATIC `education`, `skills`.
- **cover_letter_base.md**:      Base/voice anchor for cover letters (the content_base of letters). Antonio edits it; the cover-letter skill writes each letter to match its voice, architecture, and banned-phrases list.
- **system/context.md**:         Versioned personal context (work eligibility, ambitions, career arc) that travels with the repo across machines. Read by the job-fit skill; edit it when timing, eligibility, or direction changes.
- **system/verify_cv.py**:       Verifier. Checks a folder's `content_tailored.yaml` against `content_base.yaml`: every bullet and the profile must be verbatim, and no two bullets may come from the same point. Exits non-zero on failure. Run `python system/verify_cv.py <folder>` after tailoring.
- **system/make_cv_pdf.py**:        Render the active CV to `cv.pdf` via a local server + headless Chrome. Run `python system/make_cv_pdf.py` (works in any shell). `system/make_cv_pdf.sh` is the Git Bash equivalent.
- **system/make_cover_pdf.py**:  Render the active application's `cover_letter.md` to `cover_letter.pdf` (same headless-Chrome approach).
- **active_application.txt**:    Pointer file at root. Just the application folder name. Written by the tailoring skill. Empty/absent renders the base CV. Not committed to git.
- **system/templates/cv.html**:  Renders the CV. Experience + profile come from the tailored file (via the pointer); projects/education/skills always come from content_base.yaml.
- **system/assets/**:            CV and cover letter CSS.
- **applications/YYYY-MM-company-role/**: One folder per job application (kebab-case).
- **job_description.md**:        Pasted from the job posting.
- **content_tailored.yaml**:     Written by Claude during tailoring. Contains `profile`, `experience`, and the selected `projects` (verbatim). Education and skills are static from content_base.yaml.
- **strategy.md**:               Short positioning note written during tailoring; used by the cover-letter skill.
- **cover_letter.md**:           Optional. Cover letter for this application.
- **system/**:                   All machinery (scripts, template, CSS). Not edited by hand.
- **archive/**:                  Old drafts, backups, and source material (e.g. content_base.draft.yaml, sections_SWECO). Safe to ignore.
- **README.md**:                 Antonio's own quick-start guide.
- **.claude/skills/**:           Claude Code skills for CV tailoring and cover letters.

### Application folder naming

- Format: `YYYY-MM-company-role`, lowercase, hyphens for spaces.

### How rendering works

- `templates/cv.html` reads `active_application.txt` to find the active application folder, then loads its `content_tailored.yaml` for the profile and experience.
- Education and skills always render from `content_base.yaml` (static). Projects are selected per job (the base renders all projects when there is no tailored file).
- If the pointer is missing or empty, it renders the base CV directly, flattening each experience point to its first variant (a full "master" view).
- To switch which application is rendered, update `active_application.txt` (the tailoring skill does this).
- Generate the PDF with `python system/make_cv_pdf.py` (outputs `cv.pdf`).

## Workflows

Detailed workflows for CV tailoring and cover letter writing live in `.claude/skills/`:

- `.claude/skills/cv-tailoring/SKILL.md`: the CV tailoring workflow (read job description → select variants verbatim → write content_tailored.yaml → run verify_cv.py → point active_application.txt).
- `.claude/skills/cover-letter/SKILL.md`: cover letter writing; writes each letter to match `cover_letter_base.md`, then render with `python system/make_cover_pdf.py`.

Claude Code auto-loads the relevant skill based on the task.