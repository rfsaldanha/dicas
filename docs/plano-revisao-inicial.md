# Plano de conferência da versão inicial consolidada

> Registro de uma etapa anterior. A organização vigente em quatro partes está documentada em [Arquitetura do projeto](arquitetura.md); as contagens e verificações abaixo descrevem aquela etapa.

> Documento histórico da fase 0.1.0. O plano foi concluído e é mantido apenas para rastreabilidade; o estado atual está descrito em `docs/relatorio-versao-para-revisao.md`.

## Objetivo

Preparar o protótipo existente para uma revisão editorial confiável, preservando a arquitetura de uma única árvore de conteúdo para HTML e PDF. Esta etapa não amplia o livro nem substitui os marcadores editoriais por texto genérico.

## Estado de partida

- Último commit analisado: `ef4b4b5` — protótipo funcional inicial.
- Estrutura: quatro partes, 14 capítulos, três fichas demonstrativas e catálogo com 14 registros.
- Saídas existentes: livro web e PDF de 160 × 230 mm.
- Arquivo preexistente fora do escopo: `prompt.txt`, não rastreado e preservado.
- Repositórios de referência: somente leitura; nenhuma alteração será realizada.

## Conferência editorial

1. Comparar a ordem e as subseções dos 14 capítulos com o escopo aprovado.
2. Identificar sobreposições entre temperatura e ilha de calor, eventos hidrológicos e desastres, exposição e efeitos, capacidade de resposta e aplicação.
3. Confirmar que capítulos não desenvolvidos contêm somente:
   - Descrição breve do escopo;
   - Estrutura de seções;
   - Indicadores planejados;
   - Tarefas `TODO` explícitas.
4. Revisar a página inicial e os capítulos-modelo sem iniciar a redação integral da obra.

## Conferência de fichas e fontes

1. Mapear os campos das fichas às dimensões documentais da RIPSA e às extensões necessárias para clima e ambiente.
2. Conferir definição, interpretação, cálculo, limitações, aplicação, suporte espacial e temporal, disponibilidade e incerteza.
3. Verificar coerência entre YAML, página gerada, índice e fonte relacionada.
4. Classificar cada registro do catálogo por natureza: instituição, sistema, plataforma, base, produto, painel ou serviço/API.
5. Manter como `TODO` toda característica não verificada.

## Inspeção da versão web

Serão examinadas:

- Página inicial;
- Barra lateral, sumário e busca;
- Capítulo conceitual;
- Capítulo temático;
- Ficha de indicador;
- Índice de indicadores;
- Índice e registros de fontes;
- Tabelas, links e referências cruzadas;
- Larguras representativas de celular, tablet e computador.

Evidências: capturas de tela, inspeção do HTML gerado e validação automática de links locais.

## Inspeção do PDF

Serão examinadas:

- Folha de rosto e páginas pré-textuais;
- Sumário;
- Abertura de partes e capítulos;
- Páginas pares e ímpares;
- Cabeçalhos, fólios, margens e tipografia;
- Capítulo com tabela e callout;
- Fichas completas e suas quebras;
- Referências e índices;
- Páginas em branco;
- Elementos fora da mancha, linhas isoladas e cortes.

Evidências: `pdfinfo`, `pdffonts`, `pdftotext`, conversão de páginas em imagem e auditoria geométrica.

## Critérios para correção

Serão corrigidos erros que prejudiquem a revisão, como duplicação estrutural, rótulos ambíguos, campos ausentes, links inválidos, tabelas ilegíveis, conteúdo cortado e páginas iniciais incoerentes. Capa, ISBN, ficha catalográfica, fechamento tipográfico e conteúdo completo permanecem fora desta etapa.

## Validação final

Executar, nesta ordem:

```sh
Rscript scripts/build_catalogs.R
quarto render
quarto render --profile web
quarto render --profile print
make
Rscript scripts/validate_project.R
sh scripts/check_pdf.sh
```

O relatório final registrará comandos, evidências, páginas examinadas, limitações e decisões editoriais pendentes. O trabalho não será commitado nem publicado.
