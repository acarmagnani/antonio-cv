# CV & Cover Letter Project

This repository holds Antonio Carmagnani's CV content and a workflow for producing tailored CVs and cover letters for specific job applications.


## About Antonio

Antonio is an architect by training (B.Arch., Mackenzie São Paulo) with a M.Arch. in Architecture Computation at The Royal Danish Academy. His background spans four domains that can be framed in different combinations depending on the role:

- **Real estate development** — feasibility studies, financial modeling, zoning analysis (OSPA, Itaú-Unibanco, Isay Weinfeld)
- **ESG and sustainability consulting** — Human Rights Impact Assessments, CSRD/double materiality, supply chain due diligence (Ramboll), infrastructure project work (Sweco)
- **Computational design and data** — Python, GIS, parametric modeling, machine learning (academic projects, Isay Weinfeld)
- **Architecture practice** — BIM, Revit, Grasshopper, project documentation (Isay Weinfeld, Felipe Hess)

He is based in Copenhagen and applying across real estate, consulting, ESG, and computational/data-adjacent fields. As of 2026-08 he HAS a priority: **real estate first** (investment, valuation, development, research), with sustainability and data as differentiators inside that seat rather than as the job itself; real-estate-plus-data second; ESG-plus-data as the fallback. `notes/context.md` holds the full picture, including compensation as an explicit criterion and which role families are realistically winnable. Each CV is still tailored to present a coherent, job-specific purpose, drawing from the relevant parts of his background rather than defaulting to one framing.

**Important**: The goal of each tailored CV is to look like its purpose is aligned with the specific job — not scattered across all his interests. Inclusion decisions should be deliberate. Not every experience and not every bullet belongs in every CV.

## Writing rules

There are two distinct phases, with different rules:

- **Authoring** `content_base.yaml` (done with Antonio, occasionally): writing his full history as `points` with tagged phrasing `variants`. Rephrasing, emphasis-shifting, and tasteful oversell live here.
- **Tailoring** a CV for a job (per application): pure SELECTION of existing text. No rewriting.

### Truthfulness

- Never invent experiences, roles, responsibilities, or outcomes that are not in content_base.yaml.
- During **tailoring**, no CV text is written at all: an application folder holds only a list of **ids** pointing into content_base.yaml, resolved at render time. Rewording is impossible by construction. `select_cv.py` validates the ids.
- During **authoring**, rephrasing to shift emphasis is expected: the same fact can have multiple tagged variants (e.g. an ESG framing and a PropTech framing). Tasteful oversell is wanted (strong verbs, best-angle framing), but every claim must be defensible in an interview. Never fabricate tools, clients, or metrics.
- If the job description calls for something Antonio genuinely hasn't done, flag the gap and ask. Do not stretch to cover it.
- Avoid em dashes. Use commas, periods, or parentheses instead.

### Markdown formatting (every file in this repo)

Do NOT hard-wrap markdown. Write each paragraph and each bullet as one single long line and let the editor soft-wrap it. Antonio reads these with word-wrap on, so manual newlines inside a paragraph only fragment the text for him. This applies to every `.md` here: notes, skills, strategy files, cover letters, README.

### Reverse-chronological, always

The CV renders roles in reverse-chronological order, full stop. There is no way to reorder them and none should be added. Emphasis comes from which roles appear and how many bullets each keeps, never from moving a role up the page.

### Roles are droppable

An "anchor" point marks the lead bullet for a role, NOT a bullet that must appear in every CV. A tailored CV is expected to omit whole roles: Antonio's own read of his CV is that his career looks scattered (bank, then architecture, then ESG, then infrastructure), and the fix is that each CV shows only the roles that serve its direction. Watch the timeline when cutting, since a weak role may still earn one line by closing a gap.

### Bullet style

- Preserve concrete details: tool names, numbers, specific outputs. Keep client/project names only where Antonio is sure of them.
- Bullets should convey analysis, decision support, or delivery, not just activity.
- Translate one-off decorative anecdotes into the transferable skill they demonstrate, rather than describing the specific item.

### Profile summary

Profiles are **pre-written variants** in content_base.yaml, selected verbatim by tag match. They must do a different job than the rest of the CV: convey who Antonio is professionally and his direction for this kind of role. Antonio's preferred voice opens impersonally ("Experience in..."), names his M.Arch focus, lists a few hands-on skills, and ends with a "Motivated by..." line. No "professional / consultant / practitioner" self-labels.

## File structure

- **content_base.yaml**:         Source of truth, and the ONLY place CV text lives. Every role, profile, variant and project carries a stable `id` (e.g. `ramboll.critical-raw-materials-study.v1`) that presets and applications reference. `profiles` (tagged profile variants), `experience` (7 roles, each with a stable `id` and a list of `points` with tagged phrasing `variants`), `projects`, and STATIC `education`, `skills`. Adding a bullet means adding an id to it.
- **cover_letter_base.md**:      Base/voice anchor for cover letters (the content_base of letters). Antonio edits it; the cover-letter skill writes each letter to match its voice, architecture, and banned-phrases list.
- **notes/**:                    Reference notes Antonio READS. Plain markdown, no machinery.
  - **context.md**:              Personal context (work eligibility, ambitions, career arc). Read by the job-fit skill; edit it when timing, eligibility, or direction changes.
  - **job_search_keywords.md**:  Search terms and geography rules for the daily LinkedIn pass.
  - **skills_gaps.md**:          What his real applications ask for that he has and lacks. Rebuilt from `applications/*/job_description.md`, never from market research.
  - **prompts.md**:              Antonio's own cheat-sheet of which skill to type for which task. Keep it tiny; update it when a skill is added or renamed.
- **system/**:                   Machinery only. Scripts, template, CSS. Antonio does not edit these.
- **presets.yaml**:              The three CV blocks Antonio actually applies with (`real-estate-investment`, `esg-built-environment`, `data-built-environment`), derived from the real postings in `applications/`. A preset is a finished CV for a FAMILY of jobs: profile, which roles appear, bullets, projects, skill groups. Roles always render reverse-chronologically; that is fixed and not configurable. Ids only, no text. Each block deliberately DROPS the roles that point elsewhere, which is the whole point: a CV should read as one direction, not as a list of everything. An application normally just extends a block and records the delta.
- **system/select_cv.py**:       Validator. Resolves a folder's `selection.yaml` (including `extends` / `add` / `drop`) against `presets.yaml` and `content_base.yaml`: every id must exist, no id repeated, no two bullets from the same point. Roles with no bullets are reported as deliberately omitted, not as a problem. `--preview` prints the resolved CV as text, `--preset <name>` inspects a block directly, `--list-presets` lists them, and `--usage` prints which block uses which `content_base.yaml` entry (and what nothing reaches). Run `python system/select_cv.py <folder>` after tailoring.
- **system/verify_cv.py**:       LEGACY. Verbatim checker for old applications that still have a `content_tailored.yaml`. Not used for new ones.
- **system/show_blocks.py**:     Writes each preset block out as a readable CV to `preset_previews/cv_<block>.md`, one file per block, each bullet tagged with its id. Holds ONLY the CV (header, profile, experience, education, projects, skills), no commentary, so it reads like the real thing. The fast, always-fresh way to judge whether a block points one direction: edit `content_base.yaml`, re-run, reread. Generated, never edited by hand.
- **system/make_preset_pdfs.py**: Renders every block in `presets.yaml` to `preset_previews/cv_<block>.pdf` so a whole block can be read side by side with `content_base.yaml`. Never touches `active_application.txt`, so it is safe to run mid-application. Output is gitignored and regenerated each run.
- **system/make_pdfs.py**:       One command for the active application: validates the selection, then renders `cv.pdf` and `cover_letter.pdf`. Normal way to produce output.
- **system/make_cv_pdf.py**:        Render the active CV to `cv.pdf` via a local server + headless Chrome. Run `python system/make_cv_pdf.py` (works in any shell). `system/make_cv_pdf.sh` is the Git Bash equivalent.
- **system/make_cover_pdf.py**:  Render the active application's `cover_letter.md` to `cover_letter.pdf` (same headless-Chrome approach).
- **active_application.txt**:    Pointer file at root. Just the application folder name. Written by the tailoring skill. Empty/absent renders the base CV. Not committed to git.
- **system/templates/cv.html**:  Renders the CV. Experience + profile come from the tailored file (via the pointer); projects/education/skills always come from content_base.yaml.
- **system/assets/**:            CV and cover letter CSS.
- **applications/target/YYYY-MM-company-role/**:  Applications aligned with what Antonio wants to become, at his level. ONLY these feed the skills-gap analysis.
- **applications/wide/YYYY-MM-company-role/**:    Everything else: above his level, wrong direction, or a long shot he is trying anyway. Never counted in the analysis.
- A `job_description.md` whose first line contains `not-a-posting` is a brief we wrote, not employer text. It renders normally but is excluded from requirement counts.
- **job_description.md**:        Pasted from the job posting.
- **selection.yaml**:            Written by Claude during tailoring. Ids only, no CV text. Usually just `extends:` a preset plus `add:` / `drop:` of a few ids, so the file records what was special about this job. The full form (`profile`, `roles`, `bullets`, `projects`, `skills`) is for a job that fits no block. Education is always static from content_base.yaml.
- **content_tailored.yaml**:     LEGACY format (full text copied in). Present in applications made before the id-based selection. Still renders; do not create new ones.
- **strategy.md**:               Short positioning note written during tailoring; used by the cover-letter skill.
- **cover_letter.md**:           Optional. Cover letter for this application.
- **system/**:                   All machinery (scripts, template, CSS). Not edited by hand.
- **archive/**:                  Old drafts, backups, and source material (e.g. content_base.draft.yaml, sections_SWECO). Safe to ignore.
- **linkedin/**:                 LinkedIn profile, kept in sync with the CV. `profile.md` is the paste-ready content, with two swappable top-of-profile variants (ESG-forward and real-estate-forward) plus shared per-role and per-education text, projects and skills; `notes.md` holds the reasoning and open flags. Source PDFs (Antonio's profile export, plus a reference profile) live alongside them. Same truthfulness rule as the CV: every claim traces to `content_base.yaml`.
- **reference/**:                Long-horizon aspiration archive. NOT for applying. `roles/north-star/` (the exact role Antonio wants to become) and `roles/adjacent/` (same direction, interesting, not the bullseye); `people/` (LinkedIn profiles he wants to mirror); `sources/` (raw PDFs). Purely descriptive files, no analysis inside them: the gap analysis is generated FROM this folder later. Domain is a frontmatter tag (`real-estate`, `esg`, `data`, `computational`, `strategy`), never a folder. File templates live in `reference/README.md`; the intake workflow is the `reference-intake` skill.
- **README.md**:                 Antonio's own quick-start guide.
- **.claude/skills/**:           Claude Code skills for CV tailoring and cover letters.

### Application folder naming

- Format: `target/YYYY-MM-company-role` or `wide/YYYY-MM-company-role`, lowercase, hyphens for spaces.
- `active_application.txt` holds the path WITH the bucket, e.g. `target/2026-08-cbre-energy-analyst`.
- Choosing the bucket is a judgement made once, at tailoring time, so the analysis never has to re-derive it.

### How rendering works

- `templates/cv.html` reads `active_application.txt` to find the active application folder, then loads its `selection.yaml`, expands any `extends` against `presets.yaml`, and resolves the ids against `content_base.yaml` (falling back to a legacy `content_tailored.yaml` if there is no selection file).
- Education always renders from `content_base.yaml` (static). Skills come from `content_base.yaml` too, but the selection or preset chooses which groups appear and in what order. Projects are selected per job (the base renders all projects when there is no tailored file).
- If the pointer is missing or empty, it renders the base CV directly, flattening each experience point to its first variant (a full "master" view).
- To switch which application is rendered, update `active_application.txt` (the tailoring skill does this).
- Generate the PDFs with `python system/make_pdfs.py` (validates, then outputs `cv.pdf` and `cover_letter.pdf`).

## Workflows

Detailed workflows for CV tailoring and cover letter writing live in `.claude/skills/`:

- `.claude/skills/cv-tailoring/SKILL.md`: the CV tailoring workflow (read job description → select variant ids → write selection.yaml → run select_cv.py → point active_application.txt).
- `.claude/skills/skills-gaps/SKILL.md`: rebuilds `notes/skills_gaps.md` by counting what the postings in `applications/target/` ask for. Run occasionally, not per application.
- `.claude/skills/cover-letter/SKILL.md`: cover letter writing; writes each letter to match `cover_letter_base.md`, then render with `python system/make_cover_pdf.py`.
- `.claude/skills/reference-intake/SKILL.md`: files a posting or LinkedIn profile into `reference/` as a long-term aspiration reference. Verdict first (`north-star` / `adjacent` / skip), then a short summary plus the raw text. Never speculates, never analyses.

Claude Code auto-loads the relevant skill based on the task.
