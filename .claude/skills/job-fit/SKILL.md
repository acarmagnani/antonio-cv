---
name: job-fit
description: Gives a short, honest go/no-go verdict on whether Antonio should apply to a specific job — whether it is worth applying, his realistic chance of getting it, and how well it serves the professional he wants to become. Use whenever Antonio pastes or points to a job posting and asks what you think, e.g. "o que você acha dessa vaga", "vale a pena aplicar?", "should I apply to this?", "essa vaga faz sentido pra mim?". Produces a compact synthesis, never a long essay.
---

# Job Fit

A fast, honest read on a single job posting for Antonio. He sends many of these, often in fresh
chats, and wants a SHORT synthesis he can skim, not a wall of text. Give him a clear verdict,
his odds, and whether the role moves him toward the career he wants.

## Read first (briefly)

- The **job posting** he pasted or pointed to.
- `content_base.yaml` (his real experience and skills) and the "About Antonio" section of
  `CLAUDE.md`.
- `notes/context.md` — the versioned personal context (travels with the repo across machines):
  - **Job search 2026** — work eligibility (Italian / EU citizen, so no visa in the EU/EEA; UK
    needs sponsorship post-Brexit), Spanish fluent, and the **two-horizon direction**. Read that
    part carefully: real estate is where he wants to END UP, but in the short term he is applying
    widely and willingly to ESG, sustainability, consulting, energy, infrastructure and
    computational/circular-economy roles. The ranking is a destination, never a filter.
  - **Compensation** and **Realistic odds by role family** — read both. They are the difference
    between a useful verdict and a polite one. Note that his odds are HIGHEST in the adjacent
    families, not the target one.
  - **Ambitions** — the professional he wants to become (the "future" axis).
  - **Journey** — his background arc.
- If his ambitions or a key constraint are not clear from `notes/context.md`, ask one short
  question rather than guessing (and offer to record the answer in that file).

## Judge honestly

- Real fit, not flattery. Name the genuine matches AND the real gaps (missing must-haves, wrong
  level, a credential he lacks such as BREEAM, a tool he does not have such as Presto).
- **Eligibility is often decisive.** EU roles are clean (Italian passport, Spanish); UK roles
  need sponsorship; always check that first. On location, he is searching **Europe only at this
  stage**: Nordics first, then London, then Spain and Italy, which are as far as he would move
  today. Do not down-rank a good role for being outside Copenhagen, and do not surface Brazil,
  the US or Asia as current options; those are a later horizon.
- **Level. Always state the direction explicitly: below, at, or above his level, and by how much.**
  Benchmark against what he actually has: roughly 4.5 years total including internships and the
  trainee role, of which ~18 months titled "Architect" (Isay Weinfeld), most recent title "Project
  Assistant", no line management, no project P&L ownership. A "Lead"/"Senior"/"Head" title asking
  for team leadership and budget responsibility is several steps above him; say so plainly.
  Analyst and other entry/junior roles are fine when they are a genuine entry rung into his target
  field; do not treat "junior" as a negative. He has finished studying, so internships are not
  relevant. Separate the two failure modes: too senior is a timing problem that fixes itself,
  wrong direction does not.
- **Realistic odds.** Weigh must-have gaps, level, eligibility, and how competitive he would be.
  Do not inflate; a clear skip should be called a skip.
- **Compensation is a real criterion for him, not a taboo.** Say a line about it unprompted when
  it changes the verdict: whether the role is on a path with bonus and carry or only a salary
  band, and how the local market compares. Recalibrate to the LOCAL market (not his Nordic
  salary) and say the data is noisy. A well-aimed role that structurally caps low (green
  certification, pure ESG reporting) deserves that stated plainly.
- **Anchor the odds in `notes/context.md` -> "Realistic odds by role family".** On-target:
  valuation and advisory, proptech pricing, research and development analyst are winnable;
  investment/acquisitions seats at the big funds are not, with the CV as it stands, because the
  decisive gap is no transaction experience and no DCF/waterfall modelling. Adjacent (ESG and
  sustainability consulting, climate risk, energy, circular economy): he is a strong candidate,
  not a stretch.
- **Do NOT recommend skipping a solid role just because it is not real estate.** Right now he
  wants to be working, and an adjacent seat he can move within is a real route to the target.
  Reserve "Pula" for: not eligible, several levels above him, or a role that would genuinely
  trap him with no way out. When a role is adjacent rather than on-target, say so in **Futuro**
  and name the path from it toward real estate, instead of discouraging the application.

## Output — SHORT, in Portuguese (his language)

Six compact lines, skimmable, no preamble, roughly this shape:

**Veredito:** Aplica / Talvez / Pula, <meia linha do porquê>
**Encaixe:** <principais matches; gaps reais> (1-2 linhas)
**Senioridade:** Abaixo / No nível / Acima, <quantos degraus e o que a vaga pede que ele não tem> (1 linha)
**Chance de entrar:** Baixa / Média / Alta, <por quê: elegibilidade, nível, gaps decisivos> (1 linha)
**Futuro:** <serve às ambições dele? desenvolve o profissional que ele quer ser? tem teto de dinheiro ou caminho pra bônus/carry?> (1-2 linhas)
**Bottom line:** <1 linha, a recomendação>

Never skip **Senioridade**, including when the match is good ("No nível" is useful information).
Keep the whole thing under ~170 words. No headers beyond these labels, no long analysis.

## Two phases, always in this order, never interleaved

This is the part that has gone wrong before: sometimes the verdict and the application
came out together, sometimes the application came first, sometimes the PDFs were never
rendered. The sequence below is fixed.

**Phase 1, the verdict, on its own.** Read the posting, `content_base.yaml` and
`notes/context.md`, then write the six lines as ordinary text **before making a single
tool call**. Text written before a tool call is shown to Antonio immediately, so this is
what makes the verdict arrive first rather than buried under a wall of file writing.
Reading files to reach the verdict is fine; writing anything is not.

**Phase 2, only if the verdict is "Aplica".** Having written the verdict, continue in the
same turn and build the whole package. Do not ask for confirmation: "Aplica" is the
confirmation, and Antonio has said explicitly that he prefers it this way.

- **"Pula"**: stop after the verdict. Write nothing, create no folder.
- **"Talvez"**: stop after the verdict, say plainly which way you lean, and ask the single
  yes/no question. This is the only case that waits.
- **"Aplica"**: build it.

## Building the package, when the verdict is "Aplica"

In this order, finishing each step before starting the next:

1. Choose the bucket (`target/` or `wide/`), create
   `applications/<bucket>/YYYY-MM-company-role/`, and write `job_description.md` from the
   posting Antonio pasted.
2. **cv-tailoring** skill: write `selection.yaml` (normally `extends:` a preset plus a few
   ids), run `python system/select_cv.py <folder>` until it prints OK, and write the folder
   into `active_application.txt`.
3. Write `strategy.md`: the positioning line, the profile chosen, the two threads to lead
   with, and the honest gap.
4. **cover-letter** skill: write `letter.yaml` and run
   `python system/make_letter.py <folder>` until it passes.
5. `python system/make_pdfs.py`. This is not optional and it is not the step to skip when
   the turn is getting long. An application without `cv.pdf` and `cover_letter.pdf` is not
   finished.
6. Report in a few short bullets: what was created, where it is, what was special about the
   CV delta, and anything Antonio has to do by hand (a deadline, a referral to warn, a
   field the form asks for that the pipeline cannot fill).

**No outreach emails.** An address in the posting is not a reason to write one. The email
pipeline is parked in `archive/outreach-email-pipeline/` and nothing is written to a contact
unless Antonio asks for it in so many words.

If a referral is in play, say so in the verdict and let it change the verdict. A person
inside the company is often the difference between "Talvez" and "Aplica".
