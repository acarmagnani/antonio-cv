# Outreach email pipeline, PARKED 2026-09-06

Nothing here runs. Antonio decided he wants to think about outreach emails properly before automating them, so the whole thing was moved out of the working tree. It is kept intact because it works and was tested, not because it is in use.

**The rule that was removed, and must stay removed until he says otherwise:** an application does NOT produce an email just because the posting carries an address. No email is written automatically, ever. If he wants one he will ask for it.

## What is here

- `email_base.yaml`: the source of truth for email prose, built like `letter_base.yaml`. `openings` (including a `team` variant for a department inbox and a `referral` variant), `bridges`, `experiences` (12, every claim traceable to `content_base.yaml`), `closings`, and `blocks` mirroring the three CV presets. Each experience can carry a `text_second`, the same fact pre-written to follow another experience, which must be time-neutral.
- `make_email.py`: renders an application's `email.yaml` into `outreach_email.md` and validates it. Expects to sit in `system/`.
- `check_email.py`: the validator. Inherits banned phrases and patterns from `letter_base.yaml`, adds email-only bans, a hard three-paragraph shape, a 110-200 word body, and rejects any question mark. Imports `split_sentences` and `words` from `system/check_letter.py`, so it expects to sit in `system/` too.
- `SKILL-outreach-email/SKILL.md`: the workflow skill. Was at `.claude/skills/outreach-email/`.

## How to revive it

1. `mv archive/outreach-email-pipeline/email_base.yaml .`
2. `mv archive/outreach-email-pipeline/{make_email.py,check_email.py} system/`
3. `mv archive/outreach-email-pipeline/SKILL-outreach-email .claude/skills/outreach-email`
4. Put the file-structure entries back in `CLAUDE.md` and the commands back in `notes/prompts.md`.
5. Decide deliberately whether it runs automatically or only on request. It was automatic for one day and that is the part he wanted stopped, so the default on revival should be on request only.

## Two emails were written before it was parked

Both are hand-approved and live outside this folder, unaffected:

- Novo Nordisk, to Gábor Máté Farkas, with the Fábio Aspis referral. The draft to send is in `notes/todos.md` under "SEND TO NOVO NORDISK (GÁBOR)", and the context is in `notes/outreach/2026-09-novo-nordisk.md`.
- Cadeler, to `peopleandculture@cadeler.com`. Never sent, not kept. It was only a test of the pipeline.

## What the test surfaced, worth remembering if this comes back

- A department inbox at the employer (`peopleandculture@`) is not the same as a recruitment agency or an ATS `careers@`. The first is worth writing to, the second is not.
- Two experiences were missing from the library on the first real use (`exp.ramboll.market-study`, `exp.sweco.commercial-and-counterparts`). A prose library seeded from one example will always be short; expect to author on the first few uses.
- A `text_second` that opens with a back-reference ("That combination", "Before that") breaks when the pairing changes. Same class of bug as the "At Sweco I also worked" line that had to be fixed in `letter_base.yaml`.
