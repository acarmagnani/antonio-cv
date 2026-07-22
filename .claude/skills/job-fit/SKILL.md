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
- `system/context.md` — the versioned personal context (travels with the repo across machines):
  - **Job search 2026** — work eligibility (Italian / EU citizen, so no visa in the EU/EEA; UK
    needs sponsorship post-Brexit), Spanish fluent, contract timing, the two open directions.
  - **Ambitions** — the professional he wants to become (the "future" axis).
  - **Journey** — his background arc.
- If his ambitions or a key constraint are not clear from `system/context.md`, ask one short
  question rather than guessing (and offer to record the answer in that file).

## Judge honestly

- Real fit, not flattery. Name the genuine matches AND the real gaps (missing must-haves, wrong
  level, a credential he lacks such as BREEAM, a tool he does not have such as Presto).
- **Eligibility is often decisive.** EU roles are clean (Italian passport, Spanish); UK roles
  need sponsorship; always check the geography first.
- **Level.** Is it a proper step, or junior / graduate / intern / short fixed-term? He is not
  interested in junior or temporary roles.
- **Realistic odds.** Weigh must-have gaps, level, eligibility, and how competitive he would be.
  Do not inflate; a clear skip should be called a skip.
- **Salary**, only if he asks: recalibrate to the LOCAL market (not his Nordic salary), and say
  the data is noisy.

## Output — SHORT, in Portuguese (his language)

Five compact lines, skimmable, no preamble, roughly this shape:

**Veredito:** Aplica / Talvez / Pula, <meia linha do porquê>
**Encaixe:** <principais matches; gaps reais> (1-2 linhas)
**Chance de entrar:** Baixa / Média / Alta, <por quê: elegibilidade, nível, gaps decisivos> (1 linha)
**Futuro:** <serve às ambições dele? geografia faz sentido? desenvolve o profissional que ele quer ser?> (1-2 linhas)
**Bottom line:** <1 linha, a recomendação>

Keep the whole thing under ~150 words. No headers beyond these labels, no long analysis.

## If Antonio says go

Hand off, keeping chatter minimal:
1. **cv-tailoring** skill — select verbatim from `content_base.yaml`, run `verify_cv.py`, point
   `active_application.txt`.
2. **cover-letter** skill — journey-led storytelling per `cover_letter_base.md`; Spanish for
   roles in Spain, CV in English.
3. Render PDFs (`make_cv_pdf.py`, `make_cover_pdf.py`).
