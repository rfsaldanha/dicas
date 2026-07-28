# Arquitetura do projeto

## Decisões

O identificador `dicas` foi mantido: não havia arquivo, pacote ou configuração conflitante no repositório inicial. O título e o subtítulo aparecem uma única vez em `_quarto.yml` e são consumidos pelas duas saídas.

O conteúdo é compartilhado. Não existem cópias web e impressão dos capítulos.

## Perfis

- `_quarto.yml`: metadados, ordem, referências cruzadas e pré-render.
- `_quarto-web.yml`: HTML, tema, CSS e diretório `_output/web`.
- `_quarto-print.yml`: formato `dicas-print-typst`, tipografia e diretório `_output/print`.

O perfil web é padrão, portanto `quarto render` produz o site. `quarto render --profile print` produz somente o PDF.

## Diretórios

Os capítulos vivem em `chapters/part-*`; pré e pós-textuais ficam separados. Fichas e fontes distinguem dados autoritativos (`data/`) de artefatos gerados (`pages/` e `generated/`). A extensão Typst local fica versionada em `_extensions/dicas-print/`.

Diretórios vazios propostos no briefing não foram criados. Figuras, tabelas e dados analíticos deverão surgir quando houver recursos reais com proveniência.

## Impressão

O formato local substitui apenas o parcial de página do Typst:

- 155 × 230 mm;
- 20 mm internos e 15 mm externos;
- 18 mm superiores e 20 mm inferiores;
- Libertinus Serif, 10,5 pt;
- capítulos em página ímpar;
- fólio em cabeçalho após as páginas iniciais.

A solução é deliberadamente menor que a extensão de `sis_pdf`. Recursos como ficha catalográfica composta, índice remissivo, controle avançado de viúvas e órfãs e cadernos múltiplos serão incorporados quando houver conteúdo final.

## Geração e validação

`scripts/build_catalogs.R` valida fichas e fontes, evita códigos duplicados e gera páginas e índices. `scripts/validate_project.R` verifica estrutura, citações, links internos e artefatos. `scripts/check_pdf.sh` confere tamanho, fontes, elementos e marcadores não resolvidos.

## Bibliografia

`references.bib` é a bibliografia única. Não foi copiado um CSL dos projetos anteriores. O estilo autor-data padrão do Citeproc permanece até decisão bibliográfica formal; esta escolha evita incorporar uma versão de estilo sem validação.

## Publicação

`_output/web` pode ser publicado por GitHub Pages. Antes disso, confirmar URL canônica, repositório público, política de versões, analytics e domínio.

