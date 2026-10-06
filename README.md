# Dados e Indicadores de Clima e Ambiente para a Saúde

Livro técnico em Quarto sobre dados e indicadores aplicáveis à vigilância, ao planejamento e à gestão pública. O projeto produz uma versão digital responsiva e um PDF de 160 × 230 mm preparado para revisão editorial.

A identidade visual “Território, evidência e cuidado” integra capa colorida, miolo em cinza e web. A direção de arte e as regras de composição estão no [guia editorial](docs/guia-editorial.md). A capa frontal é gerada com `make cover`; fontes e ilustrações são mantidas no próprio projeto.

Consulte a [prova visual reunida](_output/proofs/identidade-visual.pdf) e o [registro das verificações](docs/relatorio-identidade-visual.md).

O público principal inclui profissionais de secretarias de saúde, vigilância em saúde ambiental, epidemiologia, planejamento, pesquisa e ensino em saúde coletiva.

## Estado do projeto

Esta é a versão editorial 0.9.0, preparada para revisão completa. Os 24 capítulos estão organizados em quatro partes; 62 fichas de indicadores consolidados e 29 fontes com cadastro detalhado estão reunidas na Parte IV; e as referências citadas estão configuradas no estilo ABNT.

Comece pelo [guia de revisão](docs/guia-de-revisao.md) e consulte o [relatório da versão](docs/relatorio-versao-para-revisao.md).

## Estrutura

- Arquivo `_quarto.yml`: metadados centrais e configuração compartilhada.
- Arquivos `_quarto-web.yml` e `_quarto-print.yml`: ordem do livro e configuração de cada saída.
- Diretório `chapters/`: 24 capítulos organizados em quatro partes; a Parte I termina com “Do indicador à decisão pública”, no capítulo 6. Os caminhos históricos são preservados, e os perfis Quarto definem a organização editorial.
- Diretórios `frontmatter/` e `backmatter/`: elementos pré e pós-textuais compartilhados.
- Diretório `frontmatter/`: fonte única dos elementos pré-textuais das duas edições.
- Diretório `indicators/data/`: fichas estruturadas em YAML.
- Arquivo `sources/data/sources.yml`: catálogo estruturado de fontes.
- Diretório `scripts/`: geração, compilação e validação.
- Diretórios `styles/` e `_extensions/dicas-print/`: identidade web e composição impressa.
- Diretório `docs/`: decisões arquiteturais e guias.
- Diretório `_output/web/`: site compilado.
- Arquivo `_output/print/dados-indicadores-clima-ambiente-saude.pdf`: PDF compilado.

## Requisitos

- Quarto 1.9.17 ou superior; a versão foi validada com 1.10.18.
- R; a versão foi validada com R 4.6.1.
- Pacote R `yaml`;
- Poppler (`pdfinfo`, `pdftotext` e `pdffonts`) para o pré-voo do PDF.

Instale a única dependência R, se necessário:

```r
install.packages("yaml")
```

Não foi criado `renv.lock` nesta etapa porque há uma única dependência leve. A adoção de `renv` deve ser reavaliada quando análises executáveis forem incorporadas.

## Compilação

```sh
quarto render
quarto render --profile web
quarto render --profile print
```

`quarto render` usa o perfil web por padrão. Para compilar e validar tudo:

```sh
make
```

## Adicionar um capítulo

1. Crie o `.qmd` no diretório da parte correspondente.
2. Use um título de nível 1 e um identificador estável.
3. Acrescente o caminho à parte correta em `_quarto-web.yml` e `_quarto-print.yml`, conforme as saídas em que o capítulo deve aparecer.
4. Atualize a matriz editorial e execute `make`.

## Adicionar uma ficha

1. Copie `indicators/templates/ficha.yml` para `indicators/data/`.
2. Adote um código único no padrão `AAA-BBB-00`.
3. Preencha todos os campos com informação verificada; quando um recurso não documentar uma característica, registre explicitamente “não informado” e a limitação correspondente.
4. Cadastre todas as fontes referenciadas.
5. Execute `make catalogs`; a página e os índices serão regenerados.
6. Indique `capitulo` (contexto nas partes II/III) e `capitulo_fichas` (destino na Parte IV), incorpore o arquivo gerado ao capítulo de fichas e acrescente a remissão no capítulo de contexto.

## Adicionar uma fonte

Acrescente um item a `sources/data/sources.yml`, usando `sources/data/source-template.yml` como guia. Registre a data de verificação e separe características por produto quando uma instituição mantiver conjuntos distintos.

## Bibliografia

Inclua em `references.bib` apenas referências verificadas e cite-as nos arquivos `.qmd`. O validador interrompe a execução quando encontra citação sem entrada BibTeX.

## Validação

```sh
Rscript scripts/build_catalogs.R
Rscript scripts/validate_project.R
sh scripts/check_pdf.sh
```

Detalhes estão em `docs/guia-de-compilacao.md`. As contribuições seguem `CONTRIBUTING.md`.

## Licença

O repositório e os arquivos autorais usam a GNU General Public License, versão 3. Recursos e dados de terceiros mantêm suas licenças e termos próprios, registrados quando aplicável.
