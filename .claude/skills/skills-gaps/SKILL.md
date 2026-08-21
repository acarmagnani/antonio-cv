---
name: skills-gaps
description: Rebuilds notes/skills_gaps.md by counting what Antonio's real job postings ask for, split into what he has and what he lacks, overall and per geography. Use when he says "atualiza os gaps", "update the skills gap file", "roda a análise das vagas", or after several new applications have accumulated. NOT run on every new application.
---

# Skills Gaps

Rebuilds `notes/skills_gaps.md` from Antonio's own applications. Counts only, no market
research, no outside knowledge of what the industry usually asks for.

Run occasionally, roughly every 5 or 6 new target applications. One extra posting rarely moves
a ranking, so running it per application is waste.

## What counts

- **Only** `applications/target/*/job_description.md`.
- **Skip** any file whose first line contains `not-a-posting`. Those are briefs we wrote, not
  employer text, so they are not evidence.
- Ignore `applications/wide/` entirely. That folder exists so this judgement is already made.

State the resulting base count at the top of the file (e.g. "Base: 8 postings").

## Method

1. List the qualifying folders. Note each one's geography.
2. Read every qualifying `job_description.md` in full.
3. Extract each concrete requirement: named tools, named standards and certifications,
   technical domains, languages. Ignore soft-skill filler ("proactive", "team player") unless a
   posting makes it a hard requirement.
4. For each requirement, decide **have** or **lack** by checking `content_base.yaml`. The test
   is whether a bullet actually evidences it, not whether the word appears in the `skills`
   block. A skill listed with no bullet behind it goes under **lack**, with a note saying it is
   already claimed on the CV. That distinction is the most useful thing in the file.
5. Count how many postings asked for each item. Never estimate; count.
6. Repeat the counts per geography.

## Output format

Overwrite `notes/skills_gaps.md`. Keep it scannable: topic, then the count on the same line,
then company names as a sub-bullet only where they help. Prose only in the final Notes section.

Sections, in this order:

1. **Which applications this is based on** — numbered list with location, then an "Excluded"
   list saying briefly why each was left out.
2. **Have** — descending by count.
3. **Lack** — descending by count.
4. **Certifications** — what he holds (currently none), then each certification named across
   the postings with its count.
5. **By geography** — one subsection per country, each with its own Have and Lack counts, then
   a short "Geography insight" naming where the countries diverge. Bold the divergences.
6. **Notes** — at most four lines. Include anything asked in 0/N that he has anyway, since that
   is a differentiator rather than a gap.

Rules:

- No tables. They render badly and he has said so.
- No cost estimates or course recommendations. Those live in `notes/certifications.md`.
- Do not carry over counts from the previous version. Recount from the files every time.
- Update the "Last rebuilt" date.

## After writing

Tell him what changed versus the previous version, in two or three lines: what moved up, what
moved down, what is new. Do not re-narrate the whole file.
