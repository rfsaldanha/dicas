# Arquitetura do projeto

## Decisões

O identificador `dicas` foi mantido: não havia arquivo, pacote ou configuração conflitante no repositório inicial. O título aparece uma única vez em `_quarto.yml` e é consumido pelas duas saídas.

Os 14 capítulos textuais são compartilhados entre as duas saídas. A edição impressa possui composição própria para agradecimentos, apresentação e prefácio em `print/pretextuais.typ`; os arquivos QMD correspondentes permanecem como fonte da edição web.

## Perfis

- `_quarto.yml`: metadados, referências cruzadas e pré-render.
- `_quarto-web.yml`: ordem completa da edição digital, HTML, tema, CSS e diretório `_output/web`.
- `_quarto-print.yml`: ordem específica da edição impressa, formato `dicas-print-typst`, tipografia e diretório `_output/print`.

O perfil web é padrão, portanto `quarto render` produz o site. `quarto render --profile print` produz somente o PDF.

## Diretórios

Os capítulos vivem em `chapters/part-*`; pré e pós-textuais ficam separados. Fichas e fontes distinguem dados autoritativos (`data/`) de artefatos gerados (`pages/` e `generated/`). A extensão Typst local fica versionada em `_extensions/dicas-print/`.

Diretórios vazios propostos no briefing não foram criados. Figuras, tabelas e dados analíticos deverão surgir quando houver recursos reais com proveniência.

## Impressão

O formato local estende o modelo Typst com folha de rosto, verso editorial, pré-textuais próprios, paginação e pré-voo:

- 160 × 230 mm;
- 25 mm internos e 18 mm externos;
- 20 mm superiores e 22 mm inferiores;
- Libertinus Serif, 10,5 pt;
- capítulos em página ímpar;
- fólio em cabeçalho após as páginas iniciais;
- pré-textuais sem fólio, abertos em páginas ímpares;
- espaço de 80 mm reservado para a ficha catalográfica;
- fechamento do miolo em múltiplo de quatro páginas.

A composição pré-textual segue a arquitetura de `sis_pdf`, adaptada aos conteúdos e metadados disponíveis neste projeto. A ficha catalográfica permanece vazia até a atribuição formal de seus dados.

## Geração e validação

`scripts/build_catalogs.R` valida fichas e fontes, evita códigos duplicados e gera páginas e índices. `scripts/validate_project.R` verifica estrutura, citações, links internos e artefatos. `scripts/check_pdf.sh` confere tamanho, fontes, elementos e marcadores não resolvidos.

## Bibliografia

`references.bib` é a bibliografia única. Não foi copiado um CSL dos projetos anteriores. O estilo autor-data padrão do Citeproc permanece até decisão bibliográfica formal; esta escolha evita incorporar uma versão de estilo sem validação.

## Publicação

`_output/web` pode ser publicado por GitHub Pages. Antes disso, confirmar URL canônica, repositório público, política de versões, analytics e domínio.

