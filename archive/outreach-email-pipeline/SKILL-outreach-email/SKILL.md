---
name: outreach-email
description: Writes the short email to the person named as the contact in a job posting, by SELECTING pre-written prose from email_base.yaml (never improvising). Runs automatically at the end of every application whose posting carries a contact address, and can be run alone with "escreve o email", "manda um email pro contato da vaga", or when Antonio points at an application folder and a person to write to.
---

# Outreach Email

This skill writes the email Antonio sends to the person a posting names as its contact. It builds it by **selecting** pre-written prose from `email_base.yaml` and supplying two short per-job clauses. It does NOT write an email from scratch, for the same reason the cover letter does not: improvised prose drifts into short punchy sentences, jargon and hedging, and Antonio has to send it back.

The architecture is the letter's, one level smaller: `email_base.yaml` is the email's `content_base.yaml`, its `blocks` mirror the three CV presets, an application's `email.yaml` is its `selection.yaml`, and `system/check_email.py` is its `select_cv.py`.

## When an email is written at all

Only when the posting itself names a person and an address. That is what makes the email invited rather than cold, and it is the whole justification for sending it.

- Address in the posting: write the email. This is automatic, part of finishing the application, not something to ask about.
- No address in the posting: no email, no `email.yaml`, and say nothing about it. Do not hunt for an address on LinkedIn or guess a corporate pattern.
- A department address at the employer itself (`peopleandculture@`, `hr@`, a named team inbox): write it, using an opening tagged `team` and `contact` set to the team name, which switches the greeting to `greeting_team`. It is worth less than a named person, but at a company small enough for a note to get forwarded it is worth the two minutes. Say plainly in the report that it is an inbox, not a person.
- A recruitment agency, or a pure application funnel (`jobs@`, `careers@`, an applicant-tracking address): no email. Nobody reads those for anything but processing.
- Spain: `email_base.yaml` is English-only for now. For a role in Spain, skip the email and tell Antonio the Spanish prose does not exist yet.

## The three-paragraph shape, which never changes

1. **Opening, one sentence.** What he applied to, and why this email is not cold: either the posting's own invitation to ask questions, or a person inside the company. Verbatim from `openings`.
2. **The case.** Opens with the per-job `attention` clause completing "What caught my attention in the posting is ...", closed by a verbatim `bridge` sentence. Then one or two experiences, verbatim from `experiences`. Two is the normal number and three is never allowed.
3. **Close, one sentence.** Verbatim from `closings`, ending in the per-job `closing_tail`. It states openness to a conversation. Never a question, never a request for a meeting, never an ask.

## What gets written per job, and it is only two clauses

- `attention`: the thing in the posting that is genuinely his. It has to be a real phrase from the responsibilities, not a summary of the company. This clause is what connects both experiences to the role, which is why the experiences themselves do not each need their own link.
- `closing_tail`: completes "... could be useful ...". Use the posting's own words for what the team owns.

`relevance` exists as an optional per-experience clause, keyed by experience id, but it is the exception. Use it only when the two experiences pull in visibly different directions and `attention` cannot cover both. Every clause added costs words the email does not have.

## Workflow

1. Read `job_description.md` (for the contact, the address and the phrase that becomes `attention`), the folder's `strategy.md` and `letter.yaml` (so the email, the letter and the CV point one way), and `email_base.yaml` in full.
2. **Pick the block that matches the CV preset.** If the CV `extends: data-built-environment`, so does the email.
3. Decide whether the block's default experience pair is right. Override `experiences` when the posting clearly calls for a different pair. The pair should be the two threads `strategy.md` already leads with, in shorter form.
4. Write `applications/<bucket>/<folder>/email.yaml`: `extends`, `to`, `contact`, `company`, `role`, optional `team`, `attention`, `closing_tail`, plus `referral` and a referral opening if there genuinely is one.
5. Render and validate in one step:

   ```bash
   python system/make_email.py <application-folder>
   ```

   It writes `outreach_email.md` and runs the checker. If it fails, fix `email.yaml`, or `email_base.yaml` if the problem is in reusable prose. Never hand-edit `outreach_email.md`: it is generated and will be overwritten.

There is no PDF. The email is copied out of the markdown file and sent.

## Referrals

A referral is the single most valuable thing an email can carry, and the single easiest thing to overclaim.

- Use `opening.applied.referral.v1` and a `referral` field naming the person and their title, only when someone inside the company is genuinely how the vacancy reached him.
- The phrasing is "which I came across through X". Never "X referred me", unless X actually put his name forward for THIS vacancy. The recipient can check it in one message, so the weaker true claim beats the stronger false one.
- If a referral is in play, remind Antonio to give the person a heads-up before he sends it. Not a request, just a warning so they are not caught out.
- The renderer refuses a referral opening with no `referral` field, and a `referral` field with no referral opening.

## Rules

- **No free prose in an application folder.** `attention`, `closing_tail` and the optional `relevance` are the only per-job text, and each is one clause.
- **Never mention the gap.** The email is three paragraphs, and spending one of them on the reason to say no is a waste of the email. The gap belongs in `strategy.md`, where it is Antonio's to know.
- **Never a question.** A question invites a one-line answer that closes the thread, and a question about a gap hands over the rejection. The checker rejects any "?" in the body.
- Never frame his career as a transition, never anything self-diminishing. Same bans as the letter, inherited from `letter_base.yaml`.
- If a posting genuinely needs an angle no `experiences` entry covers, that is an **authoring** task: add it to `email_base.yaml` with a new id, following the voice rules at the top of that file, and tell Antonio the library grew.
- All writing rules in `CLAUDE.md` apply.
