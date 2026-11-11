# Dados e Indicadores de Clima e Ambiente para a Saúde

Livro técnico em Quarto sobre dados e indicadores aplicáveis à vigilância, ao planejamento e à gestão pública. O projeto produz uma versão digital responsiva e um PDF de 160 × 230 mm preparado para revisão editorial.

A identidade visual “Território, evidência e cuidado” integra capa colorida, miolo em cinza e web. A direção de arte e as regras de composição estão no [guia editorial](docs/guia-editorial.md). A capa frontal é gerada com `make cover`; fontes e ilustrações são mantidas no próprio projeto.

Consulte a [prova visual reunida](_output/proofs/identidade-visual.pdf) e o [registro das verificações](docs/relatorio-identidade-visual.md).

O público principal inclui profissionais de secretarias de saúde, vigilância em saúde ambiental, epidemiologia, planejamento, pesquisa e ensino em saúde coletiva.

## Estado do projeto

Esta é a versão editorial 0.9.0, preparada para revisão completa. Os 25 capítulos estão organizados em quatro partes; 64 fichas de indicadores consolidados e 52 fontes com cadastro detalhado estão reunidas na Parte IV; e as referências citadas estão configuradas no estilo ABNT.

Comece pelo [guia de revisão](docs/guia-de-revisao.md) e consulte o [relatório da versão](docs/relatorio-versao-para-revisao.md).

## Estrutura

- Arquivo `_quarto.yml`: metadados centrais e configuração compartilhada.
- Arquivos `_quarto-web.yml` e `_quarto-print.yml`: ordem do livro e configuração de cada saída.
- Diretório `chapters/`: 25 capítulos organizados em quatro partes; a Parte I termina com “Análise de situação de saúde e decisão pública”, no capítulo 6. As pastas correspondem às partes e os prefixos dos arquivos, de `01` a `25`, acompanham a ordem dos perfis Quarto. Os endereços HTML anteriores redirecionam para os atuais.
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

- Git LFS para obter os PDFs completos do livro. Após clonar, execute `git lfs install` e `git lfs pull`.
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

## Edição preliminar no GitHub Pages

A edição pública em <https://rfsaldanha.github.io/dicas/> apresenta as partes I e II
(capítulos 1–12), os elementos iniciais, o glossário, as referências e os dois
apêndices. As partes III e IV e os catálogos ficam fora do site; suas remissões
permanecem como texto, sem links. O repositório público continua contendo a obra
completa, inclusive seus fontes e PDF.

```sh
make preliminar
make serve-preliminar
```

A prévia fica em <http://127.0.0.1:8000/> (`PORT=8001` permite escolher outra
porta). `make preliminar` copia os fontes para um diretório temporário, sem
saídas anteriores nem caches, executa `quarto render --profile preliminar` e
valida as páginas, os redirecionamentos, a busca, as âncoras e os recursos locais.
Somente depois copia o resultado para `_output/preliminar/`, que não é
versionado. Uma falha de compilação ou validação preserva a última prévia válida.
Para repetir somente a validação, execute `make validate-preliminar`.
Os testes de regressão rodam com `python3 scripts/test_preliminar.py` após a
compilação e também são executados pelo workflow antes da publicação.

O perfil `preliminar` é independente: não o combine com `web` ou `print`, pois
o Quarto pode reunir as listas de capítulos. Os comandos existentes continuam
compilando as quatro partes. Para publicar, use **Actions → Publicar edição
preliminar → Run workflow → main**. O workflow compila os fontes daquele commit,
valida o resultado e publica apenas `_output/preliminar/`. Pushes e pull requests
não acionam a publicação; execuções selecionadas em outras branches não publicam.

Na configuração inicial do repositório, selecione visibilidade **Public** e,
em **Settings → Pages → Build and deployment → Source**, **GitHub Actions**.
O workflow usa o ambiente `github-pages`; suas regras devem permitir a branch
`main`. A alteração de visibilidade torna também as partes III e IV e o histórico
do repositório acessíveis no GitHub, embora esses capítulos não integrem o Pages.

Requisitos adicionais dessa compilação: Python 3.10 ou superior (somente
biblioteca padrão). O workflow fixa Quarto 1.10.18 e R 4.3.3 e instala `yaml`;
não precisa baixar o PDF completo via Git LFS.

## Adicionar um capítulo

1. Crie o `.qmd` no diretório da parte correspondente, com prefixo numérico de dois dígitos igual à sua posição no livro.
2. Use um título de nível 1 e um identificador estável.
3. Acrescente o caminho à parte correta em `_quarto-web.yml` e `_quarto-print.yml`, conforme as saídas em que o capítulo deve aparecer.
4. Ao alterar a ordem, ajuste os prefixos, os vínculos das fichas e as referências aos arquivos; declare os endereços HTML anteriores em `aliases` para preservar os links. Atualize a matriz editorial e execute `make`.

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
