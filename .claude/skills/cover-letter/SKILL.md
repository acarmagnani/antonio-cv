---
name: cover-letter
description: Writes a tailored cover letter for a specific job application, in Antonio's voice, based on cover_letter_base.md. Use this skill whenever the user wants to write a cover letter, draft a motivation letter, or generate cover_letter.md inside an applications/ folder. Triggers on phrases like "write the cover letter", "draft a cover letter for this job", or when the user points to an application folder with a job_description.md.
---

# Cover Letter

This skill writes a tailored cover letter by following `cover_letter_base.md` (the voice,
structure, and rules anchor) and filling it for a specific job. The base is to the cover
letter what content_base.yaml is to the CV: the reference every letter is written to match.

## Inputs

- `cover_letter_base.md` at the repo root — THE anchor. Its voice, four-paragraph
  architecture, tailoring instructions, and banned-phrases list govern the output.
- `applications/YYYY-MM-company-role/job_description.md` — what the role actually needs.
- `content_base.yaml` — source for the experiences, skills, and numbers to cite (verbatim
  facts; you may phrase them naturally in the letter, but never invent).
- `applications/YYYY-MM-company-role/strategy.md` and `content_tailored.yaml`, if present —
  keep the letter consistent with how the CV was positioned for this role.
- Any per-application notes from Antonio (why this company, a hook). These are gold; if he
  gave none and a genuine company hook isn't clear, ask him for one or two sentences.

## Workflow

1. Read `cover_letter_base.md` in full, then the job description and content_base.
2. **Find the throughline** — the single idea the role is really about, that every
   paragraph points back to (see the base's instructions for examples).
3. Write the letter by following the base's architecture exactly:
   - Opening: throughline + the two or three most relevant of Antonio's fields, tied to
     something specific about this company/role.
   - Anchor paragraph: the one experience from content_base that best fits, developed
     concretely, then abstracted to the quality the role demands.
   - Supporting paragraph: one or two more experiences with concrete detail, ending on a
     sentence that ties back to the throughline.
   - Close: one line on the company's profile and where Antonio wants to go. End there.
4. Obey the base's rules: ~300-350 words, one page, no banned phrases, name specific
   tools/methods the job asks for that Antonio has, do not re-narrate the CV.

Write it in one shot; Antonio will iterate directly. Match the base voice closely.

## Output

Save as `applications/YYYY-MM-company-role/cover_letter.md` (plain prose, including the
greeting and, if the base uses one, the sign-off). Make sure `active_application.txt`
points at this folder, then tell Antonio to run `python system/make_cover_pdf.py` to get
`cover_letter.pdf`.

## Rules

All writing rules in `CLAUDE.md` apply. If a genuine, non-generic company hook is missing
and can't be inferred, ask Antonio rather than inventing enthusiasm.
