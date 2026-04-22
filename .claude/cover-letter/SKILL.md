---
name: cover-letter
description: Writes a tailored cover letter for a specific job application, building on the application's strategy.md and content_tailored.yaml. Use this skill whenever the user wants to write a cover letter, draft a motivation letter, or generate cover_letter.md inside an applications/ folder. Triggers on phrases like "write the cover letter", "draft a cover letter for this job", or when the user points to an application folder that already has a tailored CV.
---

# Cover Letter

This skill produces a tailored cover letter for a specific job application. It assumes the CV has already been tailored for the same application (i.e., `content_tailored.yaml` and `strategy.md` exist in the application folder). If they don't, ask the user to run the cv-tailoring skill first.

## Inputs

- `applications/YYYY-MM-company-role/job_description.md`
- `applications/YYYY-MM-company-role/strategy.md`
- `applications/YYYY-MM-company-role/content_tailored.yaml`
- `content_base.yaml` at the repo root (for additional context not in the tailored CV)

The tailored YAML is the source of truth for what Antonio is presenting for this role. The cover letter must stay consistent with it (same positioning, same emphasis, no contradictions).

## Workflow

Write `cover_letter.md` in the same application folder in one shot. No review checkpoint. Antonio will edit directly.

## Shape

Approximately 350 words, single page. Full prose, no bullet lists. Markdown format with no header block (Antonio will add his own formatting when exporting).

### Paragraph 1: Opening

How the opening frames the letter depends on the job. Pick the strongest of:

- Why this specific role genuinely fits what Antonio is trying to do next.
- A specific hook: a project, background element, or angle that's directly relevant.
- A brief reference to the company's work, only if the job description or public context makes the connection genuinely strong. Do not force it.

Avoid generic openers that could appear on any cover letter for any job. If the opening sentence doesn't tell the reader something specific about Antonio or this role, rewrite it.

### Paragraphs 2 and 3: Body

This is where most cover letters fail by restating the CV. Do not do that.

The body's job is to explain why Antonio is a fit, not what Antonio has done. The CV lists the what. The cover letter connects the what to the specific needs of this role.

Approach:
- Pick one or two threads from `strategy.md` and `content_tailored.yaml` that most directly address the role. Go deeper on those.
- Where useful, name a specific project, outcome, or method. 
- Do not walk through roles chronologically. Do not summarize multiple experiences shallowly. One or two proof points developed well beats four mentioned in passing.
- If there's a natural opportunity to acknowledge the company's work or direction in one sentence, take it. If there isn't, skip it. Forced flattery reads as worse than no flattery.

### Paragraph 4: Closing

Short. Three to four sentences. It should tie back to why this role and this company specifically, and express interest in continuing the conversation without boilerplate or restating the opening.

## Rules

All writing rules in `CLAUDE.md` apply: truthfulness, banned phrases, no em dashes, tone.

## What to reference from other files

- `strategy.md`: shared positioning between the CV and cover letter. The cover letter must be consistent with the Positioning line and Profile bullets.
- `content_tailored.yaml`: source for specific projects, tools, outcomes. When naming something concrete, pull from here.
- `job_description.md`: source for what the role actually requires. Match real requirements, not imagined ones.
- `content_base.yaml`: use only if context beyond the tailored CV is genuinely needed. Prefer the tailored file.

## Output

Save as `applications/YYYY-MM-company-role/cover_letter.md`. Do not copy anywhere else. Unlike the CV, the cover letter doesn't feed into a render pipeline.

Tell the user the cover letter is ready to review.