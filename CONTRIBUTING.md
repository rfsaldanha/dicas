# Como contribuir

## Convenções

- Use nomes de arquivos em minúsculas, sem espaços e com hífens.
- Mantenha um título de nível 1 por capítulo.
- Preserve identificadores de seções publicados.
- Escreva em português brasileiro e defina siglas na primeira ocorrência.
- Não publique marcadores `TODO`; verifique a informação em fonte oficial ou referência adequada e, quando ela não for documentada, registre claramente “não informado” e a limitação.

## Fichas e fontes

Fichas são editadas em `indicators/data/`, nunca diretamente em `indicators/includes/`, que é gerado e incorporado ao capítulo temático indicado em cada registro. Códigos devem ser únicos. Toda fonte citada por ID precisa existir em `sources/data/sources.yml`.

Registros de fonte devem distinguir instituição, sistema, produto e versão. Não transforme previsão, projeção, reanálise ou estimativa em observação por simplificação textual.

## Referências

- Use BibTeX em `references.bib`.
- Inclua somente obras consultadas.
- Prefira identificadores persistentes e documentos institucionais.
- Não use uma página de busca como referência final.
- Revise autoria institucional, data, título e data de acesso.

## Imagens e tabelas

Toda imagem precisa de legenda, fonte, autoria, licença, texto alternativo e arquivo com resolução adequada. Não são aceitas imagens geradas por inteligência artificial.

Reserve “tabela” para dados predominantemente numéricos e “quadro” para sínteses textuais. Inclua unidade, período, território e notas metodológicas. Confira tabelas no celular e no PDF.

## Revisão

Revise clareza, coerência terminológica, unidades, casas decimais, datas, siglas, limitações e incerteza. Afirmações causais exigem evidência e desenho compatíveis.

## Commits e pull requests

Faça commits pequenos, com mensagem no imperativo e escopo reconhecível. Antes de abrir um pull request:

- [ ] execute `make`;
- [ ] confira `git diff --check`;
- [ ] revise o HTML e o PDF;
- [ ] confirme que não há fonte ou referência inventada;
- [ ] confirme que arquivos gerados correspondem aos metadados;
- [ ] descreva decisões editoriais e tarefas pendentes;
- [ ] não inclua credenciais, dados sensíveis ou arquivos sem licença.
