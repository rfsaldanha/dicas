# Arquitetura do projeto

## Decisões

O identificador `dicas` foi mantido: não havia arquivo, pacote ou configuração conflitante no repositório inicial. O título aparece uma única vez em `_quarto.yml` e é consumido pelas duas saídas.

Os 24 capítulos e os elementos pré-textuais em QMD são compartilhados entre as duas saídas. A extensão Typst acrescenta apenas folha de rosto, verso editorial, paginação e composição gráfica próprias da edição impressa.

A organização editorial tem quatro partes: fundamentos e métodos (capítulos 1–6), dados e indicadores temáticos (7–12), indicadores integrados de clima, ambiente e saúde (13–15) e fichas de indicadores e fontes de dados (16–24). “Do indicador à decisão pública” encerra a Parte I como capítulo 6. Seu caminho histórico em `chapters/part-4/` é preservado para manter os links; a vinculação às partes e a numeração são definidas nos perfis Quarto.

## Perfis

- Arquivo `_quarto.yml`: metadados, referências cruzadas e pré-render.
- Arquivo `_quarto-web.yml`: ordem completa da edição digital, HTML, tema, CSS e diretório `_output/web`.
- Arquivo `_quarto-print.yml`: ordem específica da edição impressa, formato `dicas-print-typst`, tipografia e diretório `_output/print`.

O perfil web é padrão, portanto `quarto render` produz o site. `quarto render --profile print` produz somente o PDF.

## Diretórios

Os capítulos vivem em `chapters/part-*`; pré e pós-textuais ficam separados. Fichas e fontes distinguem dados autoritativos (`data/`) de artefatos gerados (`pages/` e `generated/`). A extensão Typst local fica versionada em `_extensions/dicas-print/`.

Diretórios vazios propostos no briefing não foram criados. Figuras, tabelas e dados analíticos deverão surgir quando houver recursos reais com proveniência.

## Impressão

O formato local estende o modelo Typst com folha de rosto, verso editorial, paginação e pré-voo:

- 160 × 230 mm;
- 25 mm internos e 18 mm externos;
- 20 mm superiores e 22 mm inferiores;
- Libertinus Serif, 10,5 pt, entrelinha de 14 pt; Source Sans 3 em rubricas e campos;
- Capítulos em página ímpar;
- Fólio em cabeçalho após as páginas iniciais;
- Pré-textuais sem fólio, abertos em páginas ímpares;
- Espaço de 80 mm reservado para a ficha catalográfica;
- Fechamento do miolo em múltiplo de quatro páginas.

A composição usa o modelo Typst local e a identidade “Território, evidência e cuidado”, documentada no guia editorial. Fontes estão versionadas em `assets/fonts`; a folha de rosto é monocromática e a capa frontal colorida é um artefato separado. A ficha catalográfica permanece vazia até a atribuição formal de seus dados. Páginas vazias são reconhecidas por marcas de fim de seção, e o complemento do último caderno é calculado automaticamente.

## Geração e validação

`scripts/build_catalogs.R` valida fichas e fontes, evita códigos duplicados e gera páginas e índices. `scripts/validate_project.R` verifica estrutura, citações, links internos e artefatos. `scripts/check_pdf.sh` confere tamanho, fontes, elementos e marcadores não resolvidos.

## Bibliografia

`references.bib` é a bibliografia única. O estilo local `styles/abnt.csl` aplica o sistema autor-data e contém correções editoriais para datas de páginas web, DOI e pontuação. A saída é validada como configuração do projeto; não se declara conformidade integral com uma edição normativa sem auditoria específica.

As duas saídas usam a mesma ordem editorial. As listas de figuras e de quadros e tabelas ficam entre siglas e sumário. A Parte IV começa pela lista de fichas por código e pelo índice alfabético, reúne os capítulos 16–24 e termina com o catálogo de fontes, que incorpora a relação de instituições. Glossário e referências são entradas independentes após essa parte, seguidos dos apêndices metodológico (A) e sobre estações meteorológicas e de qualidade do ar (B). Não há uma parte formal de elementos pós-textuais. O apêndice usa identificação alfabética; a bibliografia única reúne todas as obras citadas, inclusive nos apêndices, sob o título “Referências”, antes deles. A impressão usa `citeproc: true` para respeitar a posição de `#refs`. Os nomes históricos dos arquivos são preservados; a ordem nas configurações define a numeração editorial.

## Publicação

`_output/web` pode ser publicado por GitHub Pages. Antes disso, confirmar URL canônica, repositório público, política de versões, analytics e domínio.
