# reference/ — onde eu quero chegar

Esta pasta não tem nada a ver com aplicar para vagas. É um arquivo de referências de longo prazo: vagas que eu ainda não tenho senioridade para pegar, e pessoas cuja carreira eu gostaria de espelhar.

`applications/` = o que eu estou aplicando agora. `reference/` = o profissional que eu quero ser daqui a alguns anos.

Por enquanto o objetivo é **só popular**. Nada de análise, gap, plano de ação ou insight dentro dos arquivos. Cada arquivo é um resumo curto no topo (pra eu bater o olho e entender o que é) e o texto cru colado embaixo. A análise vem depois, e vai ser gerada A PARTIR daqui.

**Não especular.** Se a vaga não diz quantos anos de experiência pede, o campo simplesmente não existe no arquivo. Nada de estimativa, nada de "provavelmente". O resumo só reorganiza o que está escrito no texto original.

## Estrutura

```
reference/
  roles/
    north-star/   a vaga / o profissional que eu MAIS quero ser. O alvo exato.
    adjacent/     mesma direção, interessante, mas não é a mira: sênior demais,
                  domínio vizinho, ou "legal mas não é bem isso".
  people/         perfis de LinkedIn de gente que eu admiro e quero espelhar.
  sources/        PDFs crus (export de LinkedIn, print da vaga). Opcional.
```

Chamei de `roles/` e não `applications/` de propósito, para não confundir com a pasta `applications/`, que tem máquina em volta (`selection.yaml`, `active_application.txt`, scripts). Aqui não roda nada, é só leitura.

**Domínio não vira pasta, vira tag.** Real estate, ESG, data e computational se cruzam o tempo todo, e uma referência boa costuma ser duas coisas ao mesmo tempo. Dividir em pastas por domínio ia me obrigar a escolher uma. Então o eixo das pastas é só "quão perto do alvo", e o domínio fica no campo `domain` do frontmatter, que aceita mais de um.

Valores de `domain`: `real-estate`, `esg`, `data`, `computational`, `strategy`.

## Como entra coisa nova

Eu colo uma vaga ou mando um PDF de LinkedIn no chat com `/reference-intake`. Vem um veredito curto (guardar em qual balde, ou não guardar) e nada é escrito até eu dar o OK. Esta pasta é curada, não é um dump.

## Nomes de arquivo

- Vagas: `empresa-cargo.md` (ex: `hines-investment-associate.md`). Sem data no nome, a data fica no frontmatter: estas referências não expiram como uma vaga aberta expira.
- Pessoas: `nome-sobrenome.md`.

## Template — vaga (`roles/`)

Campos do frontmatter que a vaga não menciona: apagar a linha inteira. Só `company`, `title`, `bucket`, `domain` e `seen` são obrigatórios.

```markdown
---
type: role
company:
title:
location:
seniority:          # só se a vaga disser: analyst | associate | mid | senior | lead | director
years_experience:   # só se a vaga disser, ex: "5-8"
domain: []          # real-estate | esg | data | computational | strategy
bucket:             # north-star | adjacent
seen: YYYY-MM-DD
why_reference:      # uma linha, minha, sobre por que guardei
---

## Resumo

- 4 a 6 bullets: o que é a vaga, o que a pessoa faz, o que pede de mais concreto (ferramentas, certificações, idiomas), o que salta aos olhos.

## Job opening

<texto da vaga colado como veio>
```

## Template — pessoa (`people/`)

```markdown
---
type: person
name:
current_title:
current_company:
location:
domain: []
seen: YYYY-MM-DD
source:             # link do LinkedIn
why_reference:      # uma linha, minha, sobre o que eu quero espelhar
---

## Resumo

- 4 a 6 bullets: onde está hoje, quantos anos de carreira, o arco (de onde veio até onde chegou), formação, certificações, ferramentas que aparecem.

## Experiência

<colado do LinkedIn>

## Formação

<colado do LinkedIn>

## Licenças e certificações

<colado do LinkedIn>
```
