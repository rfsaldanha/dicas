# Relatório da versão para revisão editorial

## Identificação

- Versão editorial: 0.9.0 — revisão completa.
- Data de consolidação: 28 de julho de 2026.
- Conteúdo: 14 capítulos em quatro partes.
- Fichas integradas: 62.
- Fontes cadastradas: 25.
- Artefatos: `_output/web/index.html` e `_output/print/dados-indicadores-clima-ambiente-saude.pdf`.

## Escopo

A Parte I estabelece relações entre clima, ambiente e saúde, conceitos de mensuração, espaço, tempo, qualidade e documentação. A Parte II apresenta temperatura e calor, precipitação e seca, qualidade do ar e fumaça, água e saneamento, uso da terra e ambiente urbano, e desastres. A Parte III integra exposição, vulnerabilidade, efeitos em saúde e resiliência do sistema. A Parte IV converte indicadores em fluxos decisórios e quatro estudos de caso.

Para cada fenômeno, o texto apresenta diretamente os principais indicadores usados em saúde pública. As fichas completas permanecem dentro do capítulo. Não são propostos indicadores genéricos nem uma seção autônoma de fichas.

## Fichas

O catálogo contém indicadores climatológicos do ETCCDI, medidas multiaspecto e biometeorológicas de ondas de calor, indicadores de precipitação e seca, qualidade do ar e fumaça, ODS de água, saneamento, cidades e desastres, medidas de vulnerabilidade, taxas e carga atribuível de saúde e indicadores da OMS para resiliência de sistemas de saúde.

Cada ficha registra conceito, objetivo, interpretação, usos, limitações, fontes, método, fórmula, numerador, denominador, unidade, variáveis, granularidade, território, tempo, referência, acesso, processamento, qualidade, comparabilidade, relação com saúde, defasagens, aplicação gerencial e referências.

## Fontes

Os 25 registros distinguem instituição, unidade institucional, programa, sistema de informação, plataforma, base, produto e serviço. Cobertura, resolução, período, atualização, acesso, API, formatos, licença, cadastro, custos e limitações foram qualificados na documentação oficial disponível em 28 de julho de 2026.

## Bibliografia e referências cruzadas

As obras citadas estão em `references.bib` e são processadas com o estilo `styles/abnt.csl`. O validador interrompe a execução quando encontra chave ausente. Figuras, tabelas, quadros, capítulos, seções, fichas e fontes possuem identificadores estáveis.

## Saídas

O site possui 31 páginas, navegação, busca, fichas incorporadas, fórmulas, diagramas e índices. O PDF utiliza miolo de 155 × 230 mm, fontes incorporadas, margens espelhadas e composição em preto e branco.

Na compilação consolidada de 28 de julho de 2026, o PDF possui 436 páginas e permanece dentro da meta editorial de 400–500 páginas.

## Validação

O fluxo cobre:

- Validação dos 62 indicadores e 25 fontes;
- Presença e ordem dos 14 capítulos;
- Chaves bibliográficas;
- HTML, busca, links e âncoras;
- Referências cruzadas;
- Formato e paginação do PDF;
- Incorporação das fontes;
- Presença de elementos editoriais.

Comandos:

```sh
quarto render --profile web
quarto render --profile print
Rscript scripts/validate_project.R
git diff --check
```

## Indicações de arte

Os únicos marcadores deliberados no corpo do livro são seis blocos `visual-needed`. Eles especificam ilustrações originais sobre cadeia de impactos, processos hidrológicos, fumaça, água e saneamento, território urbano e desastres. A arte deverá ser produzida, licenciada, descrita com texto alternativo e revisada antes da edição pública.
