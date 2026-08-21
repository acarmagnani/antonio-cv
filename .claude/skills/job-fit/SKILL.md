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
    needs sponsorship post-Brexit), Spanish fluent, and the DIRECTION, which changed in 2026-08:
    real estate first, real estate + data second, ESG + data as the fallback. Do not treat these
    as co-equal any more, and do not treat green certification (BREEAM/LEED/DGNB) as a target.
  - **Compensation** and **Realistic odds by role family** — read both. They are the difference
    between a useful verdict and a polite one.
  - **Ambitions** — the professional he wants to become (the "future" axis).
  - **Journey** — his background arc.
- If his ambitions or a key constraint are not clear from `notes/context.md`, ask one short
  question rather than guessing (and offer to record the answer in that file).

## Judge honestly

- Real fit, not flattery. Name the genuine matches AND the real gaps (missing must-haves, wrong
  level, a credential he lacks such as BREEAM, a tool he does not have such as Presto).
- **Eligibility is often decisive.** EU roles are clean (Italian passport, Spanish); UK roles
  need sponsorship; always check that first. But **location itself is now his least important
  criterion**: he will relocate anywhere in the EU and would return to Brazil. Do not down-rank a
  good real estate role for being outside Copenhagen.
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
- **Anchor the odds in `notes/context.md` -> "Realistic odds by role family".** Valuation and
  advisory, proptech pricing, research and development analyst roles are genuinely winnable;
  investment/acquisitions analyst seats at the big funds are not, with the CV as it stands.
  The decisive gap for real estate roles is no transaction experience and no DCF/waterfall
  modelling, so a posting that runs a modelling test is a long shot today. Say so.

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

## If Antonio says go

Hand off, keeping chatter minimal:
1. **cv-tailoring** skill — select ids from `content_base.yaml`, run `select_cv.py`, point
   `active_application.txt`.
2. **cover-letter** skill — journey-led storytelling per `cover_letter_base.md`; Spanish for
   roles in Spain, CV in English.
3. Render PDFs (`make_cv_pdf.py`, `make_cover_pdf.py`).
