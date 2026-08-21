# Guia rápido (pra mim)

## O que eu edito
- **content_base.yaml** — TODO o meu conteúdo (perfis + experiências). É o único arquivo de conteúdo que eu mexo.
  - Cada experiência tem `points` (fatos). Cada point tem `variants` (versões da mesma frase, com tags de setor).
  - Projetos, educação e skills também ficam aqui e são **fixos** (iguais em todo CV).
- **cover_letter_base.md** — a base/voz das cover letters (o "content_base" das cartas). Edito aqui pra mudar o estilo de todas as futuras.
- **cv.pdf / cover_letter.pdf** — os documentos gerados. É o que eu abro pra ver o resultado.

## Nova candidatura (passo a passo)
1. Crio a pasta `applications/AAAA-MM-empresa-cargo/`
2. Colo o anúncio da vaga num `job_description.md` dentro dela
3. Peço pro Claude: **"tailora meu CV pra essa vaga"**
   - Ele seleciona os bullets relevantes (só os ids, sem copiar texto), escreve o `selection.yaml`,
     roda o verificador e aponta o `active_application.txt` pra essa pasta.
4. (Opcional) Peço: **"escreve a cover letter pra essa vaga"**, e passo 2-3 frases sobre por que essa empresa.
   Ele escreve o `cover_letter.md` seguindo o `cover_letter_base.md`.
5. Rodo `python system/make_cv_pdf.py` (CV) e `python system/make_cover_pdf.py` (carta), e abro os PDFs.

## Comandos
- **Gerar o PDF do CV:** `python system/make_cv_pdf.py`
- **Gerar o PDF da cover letter:** `python system/make_cover_pdf.py`
- **Ver o CV completo (sem tailoring):** esvazio o `active_application.txt` e rodo o make_cv_pdf.

## Regras de ouro
- No tailoring o Claude **só seleciona**: a pasta da candidatura guarda apenas ids, nunca texto de CV. O validador (`system/select_cv.py`) confere que todo id existe.
- Se eu quiser mudar o texto de um bullet, mudo no **content_base.yaml** (a fonte da verdade). Muda em todos os CVs de uma vez.
- Para gerar os PDFs da candidatura ativa: `python system/make_pdfs.py`.

## Pastas
- **applications/** — uma pasta por vaga.
- **system/** — a maquinaria (scripts, template, CSS). Não preciso mexer.
- **archive/** — rascunhos, backups e material antigo. Pode ignorar.
- **CLAUDE.md** — instruções pro Claude (não é pra mim).
