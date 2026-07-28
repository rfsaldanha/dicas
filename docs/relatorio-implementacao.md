# Relatório de implementação

## Entrega consolidada

O repositório contém um Quarto Book completo com 14 capítulos em quatro partes, elementos pré e pós-textuais, 62 fichas integradas aos capítulos, 25 fontes cadastradas, bibliografia, identidade web, formato Typst e validadores.

Os capítulos apresentam fundamentos, fenômenos climáticos e ambientais, impactos sobre a saúde e a saúde pública, indicadores consolidados e aplicações na gestão. A seleção técnica é refletida diretamente na exposição de cada fenômeno e nas fichas integradas ao capítulo correspondente.

## Arquivos principais

- `_quarto.yml`, `_quarto-web.yml` e `_quarto-print.yml`;
- 14 capítulos em `chapters/`;
- elementos editoriais em `frontmatter/` e `backmatter/`;
- metadados das fichas em `indicators/data/`;
- trechos gerados em `indicators/includes/`;
- 25 fontes em `sources/data/sources.yml`;
- referências em `references.bib`;
- saídas em `_output/web/` e `_output/print/`.

O arquivo não rastreado `prompt.txt` pertence ao usuário e permanece fora da entrega.

## Decisões

- árvore única para HTML e PDF;
- fichas integradas por fenômeno;
- somente indicadores com especificação verificável;
- preferência por aplicações em saúde pública;
- separação entre perigo, exposição, vulnerabilidade, efeito e resposta;
- fontes, produtos e plataformas tipificados separadamente;
- citações autor-data e bibliografia em estilo ABNT;
- indicações de nova arte marcadas como `visual-needed`.

## Compilação e validação

```sh
quarto render --profile web
quarto render --profile print
Rscript scripts/validate_project.R
```

O PDF validado possui formato 155 × 230 mm, paginação dentro da faixa editorial de 400–500 páginas, fontes incorporadas e referências cruzadas resolvidas. O validador também confere 14 capítulos, 62 fichas, arquivos HTML, busca, links e âncoras.

## Estado editorial

O conteúdo está preparado para revisão técnica, textual, bibliográfica, visual e de acessibilidade. A produção de ilustrações originais assinaladas nos capítulos é a única lacuna deliberadamente mantida no corpo da obra.
