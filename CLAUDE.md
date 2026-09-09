# CV & Cover Letter Project

This repository holds Antonio Carmagnani's CV content and a workflow for producing tailored CVs and cover letters for specific job applications.


## About Antonio

Antonio is an architect by training (Bachelor's Degree in Architecture and Urbanism, Mackenzie São Paulo) with a Master's Degree in Architecture Computation at The Royal Danish Academy. His background spans four domains that can be framed in different combinations depending on the role:

- **Real estate development** — feasibility studies, financial modeling, zoning analysis (OSPA, Itaú-Unibanco, Isay Weinfeld)
- **ESG and sustainability consulting** — Human Rights Impact Assessments, CSRD/double materiality, supply chain due diligence (Ramboll), infrastructure project work (Sweco)
- **Computational design and data** — Python, GIS, parametric modeling, machine learning (academic projects, Isay Weinfeld)
- **Architecture practice** — BIM, Revit, Grasshopper, project documentation (Isay Weinfeld, Felipe Hess)

He is based in Copenhagen and applying across real estate, consulting, ESG, and computational/data-adjacent fields. As of 2026-08 he has a clear long-term target, **real estate** (investment, valuation, development, research), with sustainability and data as differentiators inside that seat rather than as the job itself. In the short term he still applies widely and willingly across ESG, sustainability, consulting, energy and computational roles: the target is a destination, not a filter on what to apply to. `notes/context.md` holds the full picture. Each CV is still tailored to present a coherent, job-specific purpose, drawing from the relevant parts of his background rather than defaulting to one framing.

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

### Roles are never dropped (decided 2026-08-31)

All seven roles appear in every CV. Antonio's history is his history, and a CV that hides a job raises a question in the reader's head that a bullet count never does. This overrides the earlier guidance that whole roles could be omitted for focus.

Emphasis comes from bullets, not from absence: a role that serves this job keeps four or five, a role that does not keeps one or two, and the "anchor" point marks the lead bullet for a role, so it is the natural single line when a role is trimmed to the bone. If a role feels like it fights the positioning, cut it to one bullet and pick the variant that fights least.

### Bullet style

- Preserve concrete details: tool names, numbers, specific outputs. Keep client/project names only where Antonio is sure of them.
- Bullets should convey analysis, decision support, or delivery, not just activity.
- Translate one-off decorative anecdotes into the transferable skill they demonstrate, rather than describing the specific item.

### Profile summary

Profiles are **pre-written variants** in content_base.yaml, selected verbatim by tag match. They must do a different job than the rest of the CV: convey who Antonio is professionally and his direction for this kind of role. Antonio's preferred voice opens impersonally ("Experience in..."), names his master's focus, lists a few hands-on skills, and ends with a "Motivated by..." line. No "professional / consultant / practitioner" self-labels.

## File structure

- **content_base.yaml**:         Source of truth, and the ONLY place CV text lives. Every role, profile, variant and project carries a stable `id` (e.g. `ramboll.critical-raw-materials-study.v1`) that presets and applications reference. `profiles` (tagged profile variants), `experience` (7 roles, each with a stable `id` and a list of `points` with tagged phrasing `variants`), `projects`, and STATIC `education`, `skills`. Adding a bullet means adding an id to it.
- **letter_base.yaml**:          Source of truth for cover letters, and the ONLY place letter prose lives. Same architecture as the CV: `openings`, `experiences` (each carrying what he did and what it taught him) and `closings` all carry stable ids, and `blocks` holds a finished letter per job family: three mirroring the CV presets, plus `architecture-technical` for the technical architecture seats inside the data block (facade and envelope, materials, computational design in practice), which pairs with the `data-built-environment` CV. Only three short sentences are written per job (`hook`, `relevance`, `closing_reason`). The voice rules and the banned lists live at the top of the file. Editing it is AUTHORING, done with Antonio; per-application work is selection only.
- **notes/**:                    Reference notes Antonio READS. Plain markdown, no machinery.
  - **context.md**:              Personal context (work eligibility, ambitions, career arc). Read by the job-fit skill; edit it when timing, eligibility, or direction changes.
  - **job_search_keywords.md**:  Search terms and geography rules for the daily LinkedIn pass.
  - **skills_gaps.md**:          What his real applications ask for that he has and lacks. Rebuilt from `applications/*/job_description.md`, never from market research.
  - **prompts.md**:              Antonio's own cheat-sheet of which skill to type for which task. Keep it tiny; update it when a skill is added or renamed.
  - **outreach/**:               Source material for cold emails and warm intros, one file per company (e.g. `2026-08-arkitema-cowi.md`): the contacts, why the contact is worth making, and the raw postings behind it. The email drafts themselves live in `todos.md`; this folder holds the reference so a later session can rewrite a draft without the context being gone.
  - **leads/**:                  Output of a careers-site sweep, one file per company and date (e.g. `2026-08-ey-luxembourg.md`). Stage 1 of the pipeline: every posting worth applying to, with its title and link, plus what was cut and why (language requirement, level, direction). No job-fit and no CV work happens here, that is stage 2 against `applications/`.
- **system/**:                   Machinery only. Scripts, template, CSS. Antonio does not edit these.
- **presets.yaml**:              The three CV blocks Antonio actually applies with (`real-estate-investment`, `esg-built-environment`, `data-built-environment`), derived from the real postings in `applications/`. A preset is a finished CV for a FAMILY of jobs: profile, which roles appear, bullets, projects, skill groups. Roles always render reverse-chronologically; that is fixed and not configurable. Ids only, no text. Each block deliberately DROPS the roles that point elsewhere, which is the whole point: a CV should read as one direction, not as a list of everything. An application normally just extends a block and records the delta. A fourth block, `general`, sits alongside them and is NOT for applying: it is the deliberately undirected CV for mentorship and career programmes, networking and speculative uploads, where there is no posting to point at.
- **system/select_cv.py**:       Validator. Resolves a folder's `selection.yaml` (including `extends` / `add` / `drop`) against `presets.yaml` and `content_base.yaml`: every id must exist, no id repeated, no two bullets from the same point. Roles with no bullets are reported as deliberately omitted, not as a problem. `--preview` prints the resolved CV as text, `--preset <name>` inspects a block directly, `--list-presets` lists them, and `--usage` prints which block uses which `content_base.yaml` entry (and what nothing reaches). Run `python system/select_cv.py <folder>` after tailoring.
- **system/verify_cv.py**:       LEGACY. Verbatim checker for old applications that still have a `content_tailored.yaml`. Not used for new ones.
- **system/show_blocks.py**:     Writes each preset block out as a readable CV to `preset_previews/cv_<block>.md`, one file per block, each bullet tagged with its id. Holds ONLY the CV (header, profile, experience, education, projects, skills), no commentary, so it reads like the real thing. The fast, always-fresh way to judge whether a block points one direction: edit `content_base.yaml`, re-run, reread. Generated, never edited by hand.
- **system/make_preset_pdfs.py**: Renders every block in `presets.yaml` to `preset_previews/cv_<block>.pdf` so a whole block can be read side by side with `content_base.yaml`. Never touches `active_application.txt`, so it is safe to run mid-application. Output is gitignored and regenerated each run.
- **system/make_letter.py**:     Renders an application's `letter.yaml` into `cover_letter.md` by resolving ids against `letter_base.yaml`, then validates it. The letter equivalent of `select_cv.py`. `cover_letter.md` is GENERATED; never hand-edit it.
- **system/check_letter.py**:    Validator for a rendered letter. Rejects banned phrases, career-transition framing, anything self-diminishing, em dashes, paragraphs ending on a short sentence used as a beat, and length outside range. Warns on short sentences for a human read. A floor, not a guarantee.
- **system/make_reference_docx.py**: Renders a reference letter to `.docx` for the referee to sign or edit: `python system/make_reference_docx.py reference_letters/<person>`. The `.md` is the source of truth, the `.docx` is generated. Formatting mirrors the cover letters; the letter must fit one page.
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
- **letter.yaml**:               Written by Claude during the cover letter step. Ids plus three per-job sentences (`hook`, `relevance`, `closing_reason`). No free prose.
- **cover_letter.md**:           GENERATED from `letter.yaml` by `system/make_letter.py`. Do not edit by hand. Older applications have a hand-written one; those are legacy.
- **system/**:                   All machinery (scripts, template, CSS). Not edited by hand.
- **No outreach emails.** An email address in a posting is not a reason to write to it. The email pipeline was built and then parked in `archive/outreach-email-pipeline/`; nothing writes to a contact unless Antonio explicitly asks for it.
- **archive/**:                  Old drafts, backups, and source material (e.g. content_base.draft.yaml, sections_SWECO). Safe to ignore.
- **linkedin/**:                 LinkedIn profile, kept in sync with the CV. `profile.md` is the paste-ready content, with two swappable top-of-profile variants (ESG-forward and real-estate-forward) plus shared per-role and per-education text, projects and skills; `notes.md` holds the reasoning and open flags. Source PDFs (Antonio's profile export, plus a reference profile) live alongside them. Same truthfulness rule as the CV: every claim traces to `content_base.yaml`.
- **reference/**:                Long-horizon aspiration archive. NOT for applying. `roles/north-star/` (the exact role Antonio wants to become) and `roles/adjacent/` (same direction, interesting, not the bullseye); `people/` (LinkedIn profiles he wants to mirror); `sources/` (raw PDFs). Purely descriptive files, no analysis inside them: the gap analysis is generated FROM this folder later. Domain is a frontmatter tag (`real-estate`, `esg`, `data`, `computational`, `strategy`), never a folder. File templates live in `reference/README.md`; the intake workflow is the `reference-intake` skill.
- **reference_letters/**:        Reference letters. `strategy.md` at the top holds the rules that apply to every letter (the umbrella principle, the four-paragraph shape, the voice, the truthfulness constraints, the process); read it first and do not repeat it per person. `messages.md` holds the message that goes with each draft when it is sent. One folder per person Antonio asks a reference letter from (e.g. `tereza-kramlova/`), holding `strategy.md` and `reference_letter.md`. Each referee covers ONE umbrella, the job family the shared work actually evidences, stated explicitly in the letter; a second referee covers a different one. `strategy.md` is the brief (who they are, what was done together, which facts are confirmed and which are not, the shape of the letter) and holds everything Antonio recounted; the letter itself uses only what serves the umbrella. Drafted for the referee to sign or edit, so nothing goes in that Antonio cannot defend and nothing is attributed to them that they did not supervise.
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

### The sequence, which is fixed

When Antonio pastes a posting, the work happens in two phases and never interleaved.

**Phase 1: the verdict alone.** Read the posting and judge it. Write the six job-fit lines as plain text BEFORE making any tool call, so the verdict reaches him first instead of arriving under a pile of file writes. Reading to reach the verdict is fine; writing is not.

**Phase 2: only if the verdict is "Aplica".** Continue in the same turn and build the whole package, without asking for confirmation. "Pula" stops at the verdict. "Talvez" stops at the verdict, states which way you lean, and asks the one yes/no question.

The package is built in this order, each step finished before the next starts: folder and `job_description.md`, then `selection.yaml` validated with `select_cv.py` and `active_application.txt` pointed at it, then `strategy.md`, then `letter.yaml` rendered with `make_letter.py`, then `python system/make_pdfs.py`. The PDF step is never skipped: a folder with a `cover_letter.md` and no `cover_letter.pdf` is an unfinished application.

Detailed workflows for CV tailoring and cover letter writing live in `.claude/skills/`:

- `.claude/skills/cv-tailoring/SKILL.md`: the CV tailoring workflow (read job description → select variant ids → write selection.yaml → run select_cv.py → point active_application.txt).
- `.claude/skills/skills-gaps/SKILL.md`: rebuilds `notes/skills_gaps.md` by counting what the postings in `applications/target/` ask for. Run occasionally, not per application.
- `.claude/skills/cover-letter/SKILL.md`: cover letter writing by SELECTION from `letter_base.yaml` (never free prose), then `python system/make_letter.py <folder>` to render and validate, and `python system/make_pdfs.py` for the PDF.
- `.claude/skills/reference-intake/SKILL.md`: files a posting or LinkedIn profile into `reference/` as a long-term aspiration reference. Verdict first (`north-star` / `adjacent` / skip), then a short summary plus the raw text. Never speculates, never analyses.

Claude Code auto-loads the relevant skill based on the task.
