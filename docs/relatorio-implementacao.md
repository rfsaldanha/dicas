# Relatório de implementação

## Entrega consolidada

O repositório contém um Quarto Book completo com 14 capítulos em quatro partes, elementos pré e pós-textuais, 62 fichas integradas aos capítulos, 25 fontes cadastradas, bibliografia, identidade web, formato Typst e validadores.

Os capítulos apresentam fundamentos, fenômenos climáticos e ambientais, impactos sobre a saúde e a saúde pública, indicadores consolidados e aplicações na gestão. A seleção técnica é refletida diretamente na exposição de cada fenômeno e nas fichas integradas ao capítulo correspondente.

## Arquivos principais

- Arquivos `_quarto.yml`, `_quarto-web.yml` e `_quarto-print.yml`;
- 14 capítulos em `chapters/`;
- Elementos editoriais em `frontmatter/` e `backmatter/`;
- Metadados das fichas em `indicators/data/`;
- Trechos gerados em `indicators/includes/`;
- 25 fontes em `sources/data/sources.yml`;
- Referências em `references.bib`;
- Saídas em `_output/web/` e `_output/print/`.

O arquivo não rastreado `prompt.txt` pertence ao usuário e permanece fora da entrega.

## Decisões

- Árvore única para HTML e PDF;
- Fichas integradas por fenômeno;
- Somente indicadores com especificação verificável;
- Preferência por aplicações em saúde pública;
- Separação entre perigo, exposição, vulnerabilidade, efeito e resposta;
- Fontes, produtos e plataformas tipificados separadamente;
- Citações autor-data e bibliografia em estilo ABNT;
- Frameboxes numerados para ilustrações ainda pendentes de arte final.

## Compilação e validação

```sh
quarto render --profile web
quarto render --profile print
Rscript scripts/validate_project.R
```

O PDF validado possui formato 155 × 230 mm, paginação dentro da faixa editorial de 400–500 páginas, fontes incorporadas e referências cruzadas resolvidas. O validador também confere 14 capítulos, 62 fichas, arquivos HTML, busca, links e âncoras.

## Estado editorial

O conteúdo está preparado para revisão técnica, textual, bibliográfica, visual e de acessibilidade. A produção de ilustrações originais assinaladas nos capítulos é a única lacuna deliberadamente mantida no corpo da obra.
