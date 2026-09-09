# O que eu escrevo pra cada coisa

Chat novo por tarefa. A barra na primeira mensagem tira a ambiguidade.

- **Ver se vale aplicar numa vaga:** 
    `/job-fit` + cola a vaga
- **Criar a application (CV + carta + PDFs):** 
    `/cv-tailoring` + cola a vaga
- **Guardar uma vaga ou pessoa como referência de longo prazo:** 
    `/reference-intake` + cola a vaga ou o LinkedIn
- **Atualizar o que as vagas pedem que eu tenho e não tenho:** 
    `/skills-gaps`
- **Só a carta, numa application que já existe:** 
    `/cover-letter` + nome da pasta

## Comandos no terminal

- `python system/show_blocks.py`: escreve os 3 blocos em `preset_previews/cv_<bloco>.md`
- `python system/make_preset_pdfs.py`: os 3 blocos em PDF
- `python system/make_pdfs.py`: CV + carta da application ativa
- `python system/make_cv_pdf.py`: só o CV da application ativa
- `python system/select_cv.py <pasta> --preview`: valida uma application
- `python system/select_cv.py --usage`: que tópico vai pra cada bloco
- `python system/select_cv.py --list-presets`: lista os blocos
- `python system/make_letter.py <pasta>`: gera a carta a partir do `letter.yaml` e valida
- `python system/check_letter.py <pasta>`: só valida uma carta já escrita

Notas:

- `/cv-tailoring` já faz a carta e os PDFs junto. Não preciso chamar `/cover-letter` depois.
- `/job-fit` manda o veredito primeiro, sozinho. Se for "Aplica", ele já continua e monta a application inteira sem perguntar. Se for "Pula", para no veredito. Se for "Talvez", para e pergunta.
- Emails para contactos das vagas estão desligados. O pipeline está parado em `archive/outreach-email-pipeline/` e ele não escreve nenhum a não ser que eu peça.
- Se eu tenho referência dentro da empresa, falo logo na primeira mensagem: muda o veredito e muda o que ele escreve.
- Depois da primeira mensagem com barra, pode ir colando mais coisa direto que ele continua no mesmo modo.
- Qualquer outra coisa (mexer no `content_base.yaml`, LinkedIn, arrumar um arquivo, uma dúvida): escrevo normal, sem barra.
