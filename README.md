# Dados e Indicadores de Clima e Ambiente para a Saúde

Livro técnico em Quarto sobre dados e indicadores aplicáveis à vigilância, ao planejamento e à gestão pública. O projeto produz uma versão digital responsiva e um PDF de 160 × 230 mm preparado para revisão editorial.

O público principal inclui profissionais de secretarias de saúde, vigilância em saúde ambiental, epidemiologia, planejamento, pesquisa e ensino em saúde coletiva.

## Estado do projeto

Esta é a versão editorial 0.9.0, preparada para revisão completa. Os 14 capítulos estão escritos; 62 fichas de indicadores consolidados estão integradas aos capítulos; 25 fontes possuem cadastro detalhado; e as referências citadas estão configuradas no estilo ABNT. As indicações de arte original permanecem marcadas no próprio texto.

Comece pelo [guia de revisão](docs/guia-de-revisao.md) e consulte o [relatório da versão](docs/relatorio-versao-para-revisao.md).

## Estrutura

- `_quarto.yml`: metadados centrais e configuração compartilhada.
- `_quarto-web.yml` e `_quarto-print.yml`: ordem do livro e configuração de cada saída.
- `chapters/`: 14 capítulos organizados em quatro partes.
- `frontmatter/` e `backmatter/`: elementos pré e pós-textuais compartilhados.
- `print/pretextuais.typ`: pré-textuais próprios da edição impressa.
- `indicators/data/`: fichas estruturadas em YAML.
- `sources/data/sources.yml`: catálogo estruturado de fontes.
- `scripts/`: geração, compilação e validação.
- `styles/` e `_extensions/dicas-print/`: identidade web e composição impressa.
- `docs/`: decisões arquiteturais e guias.
- `_output/web/`: site compilado.
- `_output/print/dados-indicadores-clima-ambiente-saude.pdf`: PDF compilado.

## Requisitos

- Quarto 1.8 ou superior; a versão foi validada com 1.10.18.
- R; a versão foi validada com R 4.6.1.
- pacote R `yaml`;
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
6. Integre o arquivo gerado ao capítulo temático correspondente.

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
