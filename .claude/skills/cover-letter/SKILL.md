---
name: cover-letter
description: Writes a tailored cover letter for a specific job application, in Antonio's voice, by SELECTING pre-written paragraphs from letter_base.yaml (never improvising prose). Use this skill whenever the user wants to write a cover letter, draft a motivation letter, or generate cover_letter.md inside an applications/ folder. Triggers on phrases like "write the cover letter", "draft a cover letter for this job", or when the user points to an application folder with a job_description.md.
---

# Cover Letter

This skill builds a letter by **selecting** pre-written paragraphs from `letter_base.yaml` and supplying three short per-job sentences. It does NOT write a letter from scratch. That rule exists because free-written letters went wrong: see `letter_base.yaml` for the voice rules and the reasons behind each of them.

The relationship is exactly the CV's: `letter_base.yaml` is the letter's `content_base.yaml`, its `blocks` are the letter's `presets.yaml`, an application's `letter.yaml` is its `selection.yaml`, and `system/check_letter.py` is its `select_cv.py`.

## The four-paragraph shape, which never changes

1. **Opening: Antonio's profile.** Where he comes from and what he is aiming at, angled to the job family. Comes verbatim from `openings` in `letter_base.yaml`. The last sentence is the per-job `hook`, naming the employer and saying what makes it the right place.
2. **and 3. Two experience paragraphs.** Each comes verbatim from `experiences`: what he did, and what it taught him. The last sentence of each is the per-job `relevance` sentence, tying that learning to THIS job. That link is the point of the paragraph and is never omitted.
4. **Closing.** Opens with the per-job `closing_reason` (what this employer is), then a verbatim `closings` line about where he wants to take his work. Never an ask, never a discovery framing.

## Workflow

1. Read `job_description.md`, the folder's `strategy.md` and `selection.yaml` (so the letter and the CV point the same way), and `letter_base.yaml` in full.
2. **Pick the block that matches the CV preset**, so the letter and the CV are built from the same direction. If the CV `extends: data-built-environment`, the letter normally does too.
3. Decide whether the block's two default paragraphs are the right ones for this posting. Override `paragraphs` with other ids when the job clearly calls for a different pair. Two paragraphs, three at the very most.
4. Write `applications/<bucket>/<folder>/letter.yaml`: `extends`, `company`, `role`, `hook`, `relevance` (one sentence per paragraph), `closing_reason`. Every `relevance_prompt` in `letter_base.yaml` says what its sentence has to do.
5. Render and validate in one step:

   ```bash
   python system/make_letter.py <application-folder>
   ```

   It writes `cover_letter.md` and then runs the checker. If it fails, fix the sentences in `letter.yaml`, or the prose in `letter_base.yaml` if the problem is in a reusable paragraph. Do not hand-edit `cover_letter.md`: it is generated and will be overwritten.
6. Render the PDFs with `python system/make_pdfs.py` (needs `active_application.txt` pointing at the folder). This step is not optional: a `cover_letter.md` with no `cover_letter.pdf` next to it is an unfinished application.

## Per-application notes from Antonio

If Antonio gives two or three raw sentences about why THIS company (a specific hook, a personal connection), that is the best material there is: work it into the `hook` and the `closing_reason` rather than writing a generic one. If no genuine, non-generic hook can be found in the posting or the company, ask him for one instead of inventing enthusiasm.

## When nothing in the library fits

If a posting genuinely needs an angle no `experiences` entry covers, that is an **authoring** task, not a tailoring one. Write the new paragraph into `letter_base.yaml` with a new id, following the voice rules at the top of that file, and flag to Antonio that the library grew so he can review the new paragraph. Never smuggle new prose into `letter.yaml`: only `hook`, `relevance` and `closing_reason` are written per job, and each is one sentence.

## Rules

- **No free prose in an application folder.** `hook`, `relevance` and `closing_reason` are the only per-job sentences, and they are single sentences.
- Reusable paragraphs must stand alone. They are combined in different orders, so none may refer back to another.
- Never frame Antonio's career as a transition, and never write anything that diminishes him. Both are checked mechanically and both are in `letter_base.yaml`'s banned lists.
- Spanish for roles in Spain (`language: es`); the CV stays in English.
- The checker is a floor, not a guarantee. It catches mechanical tells, not empty sentences. Read the output before calling a letter done.
- All writing rules in `CLAUDE.md` apply.
