# LinkedIn — notes

Why `profile.md` says what it says. Source material in this folder: exports of Antonio's
profile (page, experience, education) and Daniel Ferrara Bilesky's profile, used as a
reference for structure and tone, not for career direction.

---

## The register: LinkedIn is not the CV

This is the thing to get right before anything else, and the first draft of `profile.md` got
it wrong by pulling straight from `content_base.yaml`.

The CV is **project-level**. It proves things: named clients, named studies, the Azerbaijan
field mission, the Nordzucker tool, the critical raw materials study. It is read by someone who
already has a specific job in mind and is checking evidence against it.

LinkedIn is **role-level**. For each job it answers two questions: what was the role, and what
did he generally do in it. It is read by someone who does not yet know who he is, scanning to
decide whether to keep reading. A named field mission is noise at that altitude.

Check this against Daniel, which is the tell. His About runs 205 words and names **zero**
projects and **zero** clients. It is entirely categories of capability: "the data
infrastructure, dashboards, and automation tools", "bespoke plugins and automation tools for
AEC firms". Even his side practice, which is real client work, stays generic. The specificity
lives in his experience bullets and stops there.

So: About stays at capability level. Experience bullets stay at role level, two to four each,
with a specific thing only when that thing *was* the job (the Isay staircase plugin qualifies,
because making workflows easier is what he did there). Everything else specific goes to the
Projects section, which is the part of LinkedIn built to hold it.

---

## What Daniel does that is worth copying

**1. The headline is a claim plus a proof stack, in three slots.**

```
Data Analyst & Software Developer | Business Analytics · Process automation | Airbus · The Royal Danish Academy · BIG
```

`[what I am] | [what I do] | [where I have done it]`. The third slot is a credibility stack,
not a list of current employers, which is why BIG is still there five years after he left.
The first slot is a job title someone actually recruits for.

**2. The About has a shape, not just content.**

Hook (one sentence of identity plus what excites him) → "By day" (the current job, the stack,
then a reframe of what he actually cares about) → "On the side" (the parallel practice) →
the through-line that ties both halves together → "Based in Copenhagen."

The through-line is the load-bearing part. "I find the bottleneck, build the solution, and
make it disappear into the workflow" is what makes two unrelated jobs read as one person with
a direction, rather than a scattered CV. That is exactly the problem Antonio has, split across
ESG, real estate, and computation.

**3. Numbers as parameters, not as decoration.**

"multi-billion euro portfolio", "~24 hrs/week to near zero", "4B+ USD/year across 3M+ parts",
"million-part portfolio". They set the scale and the stakes. None of them are achievements in
themselves, they are the context that makes the achievement mean something.

**4. Skills tagged per role.** Every position carries chips ("Automation, Data Analysis and 3
more"). This is what recruiter search actually indexes.

**5. Education entries carry real research**, not just degree names. His thesis and his CNN
segmentation project get full paragraphs under the education entry.

## What Daniel does that is worth avoiding

- **The Featured section contradicts the headline.** It is four render posts from 2019-2021
  with twenty hashtags each, under a Data Analyst headline. Featured is the second thing a
  recruiter scrolls past, and his is arguing he is an architect.
- **Unfalsifiable claims mixed in with the good numbers.** "resulting in a reduction in
  construction waste and a decrease in carbon emissions", "increasing customer satisfaction"
  (twice, no evidence). Copy the number discipline, not the unmeasured claims.
- **The Companies section repeats the same two roles** already listed in Experience.
- **29 skills including "Problem Solving".** Dilutes the ones that matter.

---

## What is wrong with Antonio's profile right now

Ranked by cost.

**1. Sweco reads "Feb 2026 - Present". It ended 2026-07-31.**
Factually wrong, and it contradicts the "Open to work" banner sitting a few pixels above it.
Fix first, everything else can wait.

**2. The About is two sentences and 30 words.**

> Interested in using data-driven tools to make workflows smarter and urban development more
> thoughtful. For more about me & my work, visit antoniocarmagnani.com

It states an interest and then points elsewhere. No proof, no scale, no keywords, no
direction. This is the single biggest lever on the profile: it is the one field where he
controls the whole narrative, and right now it is a placeholder. It is also the field the
"low key demais" instinct is describing.

**3. The headline names a field, not a role, and matches no search.**

> Architecture and computation @ Sweco @ RoyalDanishAcademy

Three problems. It only fills slot three of Daniel's structure. "Architecture and computation"
is not a phrase any recruiter types. And it is now partly false, since neither Sweco nor the
degree is ongoing.

Cross-check against `notes/job_search_keywords.md`, the list of what recruiters actually
search: DGNB, LCA, embodied carbon, CSRD, EU Taxonomy, double materiality, climate risk,
sustainability consultant, ESG, GIS, Python, real estate analyst, BREEAM. **None of them
appear in his headline or his About.** He is invisible to every search he built that file for.

**4. Bullets describe activity, not role.**

Current: `- Built geospatial project databases in QGIS.` That is a task, not an answer to
what the job was. The fix is not more detail, it is a higher altitude: what was the role, what
did he generally do there, and one number where the number describes the scope of the role
rather than a single deliverable. "15+ feasibility studies for developer clients" is
role-scope. "A field mission across Baku's water supply system" is not, however good it looks
on the CV.

**5. Acronym-only writing.** "HRIAs, double materiality" appears, but not "Human Rights Impact
Assessment". Recruiters search the expanded term at least as often as the acronym. Write both,
once each.

**6. Education is undersold.** A master's thesis, the Venice Biennale with CITA / GXN / 3XN,
a top 2% ML competition finish, an embodied carbon toolkit built with a startup. Almost none
of it is on the profile. Daniel, with a thinner research record, wrote three paragraphs about
his.

**7. No Projects section**, and LinkedIn is literally showing the prompt to add one.

**8. No skills tagged on any role**, and no Featured section.

---

## Things that are working, keep them

- **The posts perform.** Three posts at 1,827 / 1,968 / 1,956 impressions against 682
  followers is a strong ratio, better than the follower count suggests. Posting is a real
  channel for him, not a chore.
- **Chronology and structure are clean.** All seven roles present, dates consistent, Isay
  Weinfeld correctly split into Architect and Intern under one company entry.
- **The website link is already there.** Keep it, and add it to Featured as well.
- **Location and contact info are complete.**

---

## Why two variants instead of one

Antonio's two target tracks (ESG + data, real estate + data) do not compress into one honest
headline without turning to mush. So `profile.md` carries two complete top-of-profile sets and
he swaps the top layer to match wherever the openings are that month. Everything underneath,
experience, education, projects, the full skills list, is shared and never changes.

The asymmetry matters: real estate leading makes room for ESG underneath, but ESG leading
crowds real estate out. So Variant B carries all three strands and Variant A carries two.
Denmark right now is almost entirely the ESG track, which is why A is the one to run first.

Swapping costs about two minutes (headline, About, three pinned skills, bullet order in one or
two roles). Do not swap more than every few weeks: LinkedIn notifies the network on profile
edits, and churn reads as indecision.

---

## Flags to resolve

**Vizu dates conflict.** LinkedIn says `Jan 2021 – Jun 2022`. `content_base.yaml` says
`2022-02 – 2022-10`, which is byte-for-byte identical to the OSPA entry above it and looks
like a copy-paste error in the YAML. The CV and the LinkedIn disagreeing on an 18-month
co-founder role is the kind of thing an interviewer notices. Confirm the real dates and fix
whichever is wrong.

**"IFDK" in `content_base.yaml`.** Listed among development banks alongside the World Bank,
EBRD, KfW and EIB, but it is not a development bank anyone recognizes. Possibly IFU or IFC.
Dropped from the LinkedIn text until confirmed.

**Isay Weinfeld date split.** LinkedIn splits Architect (Jan 2024 – Aug 2024) and Intern
(Feb 2023 – Jan 2024). `content_base.yaml` has one Architect role, Feb 2023 – Aug 2024. The
LinkedIn version is the more precise one; consider bringing it back into the YAML.

---

## Maintenance

This folder is part of the CV system, not separate from it. When a bullet changes in
`content_base.yaml`, it should change here too. When a role ends, the end date changes here
first, since LinkedIn is the version strangers read.
