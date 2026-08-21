---
name: reference-intake
description: Files a job posting or a LinkedIn profile into reference/ as a long-term aspiration reference (not an application). Use whenever Antonio pastes a posting or a LinkedIn PDF and frames it as "onde eu quero chegar", "vaga referência", "perfil que eu quero espelhar", "guarda isso como referência", or points at reference/. Gives a brief keep/skip verdict and WAITS for Antonio's go before writing anything. Then files a descriptive file: short summary plus the raw text. Never writes analysis, never speculates.
---

# Reference intake

Antonio keeps an archive of where he wants to get to: roles he does not yet have the seniority for, and people whose careers he wants to mirror. This skill decides whether something belongs in that archive and files it.

This is NOT the `job-fit` skill. Job-fit answers "should I apply now". This one answers "is this worth keeping as a picture of the future", and the answer to "can he get it today" is usually no, by design.

## Step 1 — brief verdict, then STOP

Read `notes/context.md` ("Ambitions", "Journey") to judge direction. Do not re-read the whole repo for this.

Decide the bucket:

- **`north-star`** — the exact professional Antonio wants to become. The bullseye. Real estate / ESG / data / strategy in the built environment, upstream analytical work. Level is irrelevant here: a role he could never get today is exactly the point.
- **`adjacent`** — same universe, genuinely interesting, but not the mira: a neighbouring domain, a role that is mostly right with one wrong half, a career worth studying without wanting to copy it.
- **skip** — off-target. The folder is curated, not a dump. Execution-level architecture, pure software engineering with no built-environment angle, and generic corporate roles do not belong. Say no plainly; a skip is a useful answer, not a failure.

Output exactly this shape, in Portuguese, and NOTHING else. Under 80 words. No preamble, no headers beyond these labels.

```
**Veredito:** Guardar em `north-star` / Guardar em `adjacent` / Não guardar, <meia linha do porquê>
**O que é:** <1 linha: que vaga é essa, ou quem é essa pessoa>
**Por quê:** <1 a 2 linhas: o que aqui é a direção que ele quer. Se for `adjacent`, diga na mesma linha o que faz não ser o alvo exato>

Guardo?
```

**Then stop and wait.** Write no file, create no folder, run no tool. He answers with a go, a no, or a correction of the bucket. Only his go moves you to step 2. If he corrects the bucket, take his word and do not argue it.

## Step 2 — write the file

Templates live in `reference/README.md`. Follow them exactly.

- Roles: `reference/roles/<bucket>/empresa-cargo.md`
- People: `reference/people/nome-sobrenome.md`
- Raw PDFs, if he sends one worth keeping: `reference/sources/`

The file has two parts and only two parts:

1. **Frontmatter + `## Resumo`** — 4 to 6 bullets so he can skim what this is without reading the full text. For a role: what it is, what the person does, the concrete asks (tools, certifications, languages), what stands out. For a person: where they are now, career length, the arc from start to now, education, certifications, tools that recur.
2. **The raw text, pasted.** The posting as it came. For a person: `## Experiência`, `## Formação`, `## Licenças e certificações`, straight from the LinkedIn.

`why_reference` is Antonio's line, not yours. If he said why when he pasted it, use his words. If he did not, write the plainest one-line reason from the content itself, and do not editorialise.

## The two hard rules

**Never speculate.** If the posting does not state years of experience, delete the `years_experience` line. If seniority is not stated, delete `seniority`. Same for location, source, anything. An absent field is correct; an inferred field is a lie that will pollute the analysis later. The `## Resumo` only reorganises what is written in the source, it never adds.

**Never analyse.** No gaps, no "what Antonio would need", no action plan, no comparison to his CV, not inside the file and not in the chat reply. He will ask for that separately, later, across the whole folder at once. After he says go, filing is a one-line reply: where you put it. The verdict was already given in step 1, do not repeat it.

## Formatting

Markdown files in this repo are NOT hard-wrapped. Write each paragraph and each bullet as one single long line and let the editor wrap it. Do not insert newlines to keep lines under 80/100 characters.
