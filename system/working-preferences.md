# Working preferences

How Antonio wants Claude to work on this repo. This file exists for the same reason as
`context.md`: these rules were previously held only in Claude Code's local memory, which is
stored per-machine and per-path and does NOT travel with the repo. Anything durable belongs
here instead, so it survives a new machine or a fresh clone.

Consolidated 2026-07-29 from the Claude memory of two machines.

---

## Language

Antonio writes in Brazilian Portuguese (he calls Claude "Cláudio"). Reply in Portuguese unless
he switches to English.

Outputs keep their own target language regardless: **CVs are always in English**, and cover
letters follow the role's country (Spanish for roles in Spain, per `cover_letter_base.md`).

## CV length

Lean slightly toward more content rather than trimming aggressively. A slightly long CV beats a
slightly short one. Aim for roughly 3 to 4 bullets per experience block (not 1 to 2) and 2 to 3
projects, as long as the material is genuinely relevant. This is a mild bias, not licence to
include everything.

**Why:** comparing the CBRE valuation CV (19 bullets, 2 projects) against the Cushman & Wakefield
project-monitor CV (23 bullets, 3 projects) for two similar real estate roles, the CBRE one read
noticeably thinner to Antonio. Part of that gap was legitimate, since the CBRE posting was
narrower, but he still wants the default nudged toward fuller CVs.

**How to apply:** when a role block would shrink to 1 or 2 bullets under strict relevance
filtering, look again in `content_base.yaml` for a defensible verbatim bullet that broadens
coverage before finalizing. This is about which bullets get selected, never how they are phrased.
The selection-only rule stays intact.

## Do not re-tailor submitted applications

Once an application has been submitted, its folder is frozen. Do not edit, re-tailor, re-sync, or
regenerate PDFs for it.

**Why:** the work is already sent, so touching it is wasted effort. When `content_base.yaml`
changes, older `content_tailored.yaml` files go stale and `verify_cv.py` will flag them. That is
expected. Ignore it, and only run the verifier against the folder being worked on.

**Status note:** as of 2026-07-29 the Jacobs, Arup and Octave folders were confirmed submitted.
The submission status of the 2026-07 batch (Arcadis, CBRE, Clikalia, Cushman & Wakefield, EY
sustainability data analytics, KPMG, Zurich, EY-Parthenon) was never recorded. Ask Antonio before
assuming any of them is still editable.

## Job discovery is the bottleneck, not tailoring

Antonio considers the tailoring workflow itself to be working well. His real time cost is *finding*
postings, manually searching LinkedIn by location and keyword.

He asked (2026-07-27) whether Claude could log into LinkedIn and search on his behalf. It cannot,
and it should not: no authenticated browser tool is available here, and automating a logged-in
LinkedIn session risks his account under LinkedIn's User Agreement. He does not want auto-apply
either, since application links are often off-platform.

**How to apply:** prefer low-cost alternatives. Antonio sets up native LinkedIn saved-search and
job-alert emails for his recurring keyword and location combinations, then pastes a batch of links
in one go. Claude runs the `job-fit` skill across the batch for cheap go/no-go triage, and only
then builds folders for the ones he greenlights. For named companies, public career pages can be
checked directly with WebFetch or WebSearch, no login and no ToS problem.

## Multiple machines

Antonio works on this repo from more than one machine, so commits made on one may not be present
on another, and the local view can be stale or actively shifting.

**How to apply:** run `git fetch` before summarizing project status, and re-run `git status`
immediately before staging rather than trusting a snapshot from earlier in the conversation. Verify
with `git rev-parse HEAD origin/main` rather than assuming `origin/main` resolves, since a missing
tracking ref fails silently when stderr is suppressed.

**Why:** this bit twice. On 2026-07-10 the repo claimed to be up to date while sitting a commit
behind a stale fetch. On 2026-07-29 the repo was inside a cloud-synced folder and the `.git`
directory itself changed mid-session, so files that were untracked at the start of the conversation
had silently become committed by the time of the push.
