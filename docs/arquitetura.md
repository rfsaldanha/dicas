# Arquitetura do projeto

## Decisões

O identificador `dicas` foi mantido: não havia arquivo, pacote ou configuração conflitante no repositório inicial. O título aparece uma única vez em `_quarto.yml` e é consumido pelas duas saídas.

Os 24 capítulos e os elementos pré-textuais em QMD são compartilhados entre as duas saídas. A extensão Typst acrescenta apenas folha de rosto, verso editorial, paginação e composição gráfica próprias da edição impressa.

A organização editorial tem quatro partes: fundamentos, métodos e decisão em saúde (capítulos 1–6), fenômenos e indicadores de clima e ambiente (7–12), exposição, vulnerabilidade, efeitos e resposta em saúde (13–15) e fichas de indicadores e fontes de dados (16–24). “Análise de situação de saúde e decisão pública” encerra a Parte I como capítulo 6. Seu caminho é `chapters/part-1/06-indicador-decisao.qmd`. As pastas correspondem às partes e os prefixos dos arquivos, de `01` a `24`, acompanham a ordem definida nos perfis Quarto.

## Perfis

- Arquivo `_quarto.yml`: metadados, referências cruzadas e pré-render.
- Arquivo `_quarto-web.yml`: ordem completa da edição digital, HTML, tema, CSS e diretório `_output/web`.
- Arquivo `_quarto-print.yml`: ordem específica da edição impressa, formato `dicas-print-typst`, tipografia e diretório `_output/print`.

O perfil web é padrão, portanto `quarto render` produz o site. `quarto render --profile print` produz somente o PDF.

## Diretórios

Os capítulos vivem em `chapters/part-*`; pré e pós-textuais ficam separados. Fichas e fontes distinguem dados autoritativos (`data/`) de artefatos gerados (`includes/` e `generated/`). A extensão Typst local fica versionada em `_extensions/dicas-print/`.

Os capítulos renomeados declaram os endereços HTML anteriores em `aliases`. O Quarto gera redirecionamentos que preservam os fragmentos dos links; os identificadores de seções, figuras, quadros e fichas permanecem estáveis. Os códigos de produção das ilustrações continuam independentes da numeração editorial das figuras, conforme o guia editorial.

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

A versão online começa por Bem-vindo, Agradecimentos, Prefácio do autor e Lista de siglas, seguidos imediatamente da Parte I. No PDF, a folha de rosto e os créditos são seguidos pela Ficha técnica e pelo Sumário; depois vem a mesma sequência de leitura. Apresentação, Como utilizar este livro e as listas de figuras e de quadros e tabelas foram retirados das duas saídas, com os arquivos-fonte preservados para consulta e validações internas. Ficha técnica e Sumário são exclusivos do PDF. O texto de Bem-vindo é compartilhado por um include; a página inicial permanece exclusiva da web e vazia na impressão, enquanto uma página própria posiciona Bem-vindo após o Sumário. A navegação lateral e os índices de seções dos capítulos permanecem na web. A Parte IV começa pela lista de fichas por código e pelo índice alfabético, reúne os capítulos 16–24 e termina com o catálogo de fontes, que incorpora a relação de instituições. Glossário e referências são entradas independentes após essa parte, seguidos dos apêndices metodológico (A) e sobre estações meteorológicas e de qualidade do ar (B). Não há uma parte formal de elementos pós-textuais. O apêndice usa identificação alfabética; a bibliografia única reúne todas as obras citadas, inclusive nos apêndices, sob o título “Referências”, antes deles. A impressão usa `citeproc: true` para respeitar a posição de `#refs`. A ordem nas configurações define a numeração editorial, e o validador confere sua correspondência com os nomes e as pastas dos arquivos.

## Publicação

`_output/web` pode ser publicado por GitHub Pages. Antes disso, confirmar URL canônica, repositório público, política de versões, analytics e domínio.
