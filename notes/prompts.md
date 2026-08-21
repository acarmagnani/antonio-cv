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

Pra olhar os currículos base (os blocos), sem mexer em application nenhuma:

- **Exportar os 3 blocos em PDF pra ler:** 
    `python system/make_preset_pdfs.py` (sai em `preset_previews/`)
- **Ver que tópico do content_base vai pra cada bloco:** 
    `python system/select_cv.py --usage`
- **Listar os blocos:** 
    `python system/select_cv.py --list-presets`

Notas:

- `/cv-tailoring` já faz a carta e os PDFs junto. Não preciso chamar `/cover-letter` depois.
- Depois da primeira mensagem com barra, pode ir colando mais coisa direto que ele continua no mesmo modo.
- Qualquer outra coisa (mexer no `content_base.yaml`, LinkedIn, arrumar um arquivo, uma dúvida): escrevo normal, sem barra.
