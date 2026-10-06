# Guia de compilação

## Ambiente validado

- Quarto 1.10.18;
- R 4.6.1;
- Pacote R `yaml`;
- Typst 0.15.1, distribuído com o Quarto usado;
- Poppler com `pdfinfo`, `pdftotext` e `pdffonts`.

## Comandos

Versão web padrão:

```sh
quarto render
```

Perfis explícitos:

```sh
quarto render --profile web
quarto render --profile print
make cover
```

Fluxo completo:

```sh
make
```

Somente catálogos ou validação:

```sh
make catalogs
make validate
```

## Saídas

- Arquivo `_output/web/index.html`;
- Arquivo `_output/web/search.json`;
- Arquivo `_output/print/dados-indicadores-clima-ambiente-saude.pdf`.
- Arquivo `_output/cover/capa.pdf`: capa frontal colorida, separada do miolo; composição editável em `assets/cover/capa.typ`.

## Ordem da compilação

### Recomposição das ilustrações em aquarela

Os montadores das artes dos capítulos 1 a 5 usam `scripts/render_figure.py` para exportar as composições: Chromium carrega as aquarelas e as fontes WOFF2 incorporadas no SVG; ImageMagick produz o PNG de 8 bits em escala de cinza. A exportação verifica a decodificação das imagens e o carregamento das fontes antes de substituir o PNG. Esse caminho evita exportações do Inkscape que omitem a imagem incorporada ou substituem a fonte.

Em um ambiente virtual Python, instalar `Pillow` e `playwright`, além do ImageMagick (`magick` no PATH). Usar `python -m playwright install chromium` para preparar o navegador. Alternativamente, com Google Chrome instalado, definir `DICAS_BROWSER_CHANNEL=chrome` no ambiente das chamadas abaixo.

```sh
python scripts/build_cap1_art.py
python scripts/build_cap1_trajectories.py
python scripts/build_cap1_heat_exposure.py
python scripts/build_cap1_remaining_art.py 04
python scripts/build_cap1_remaining_art.py 05
python scripts/build_cap1_remaining_art.py 06
python scripts/build_cap2_art.py 01
python scripts/build_cap2_art.py 02
python scripts/build_cap2_art.py 03
python scripts/build_cap2_art.py 04
python scripts/build_cap2_art.py 05
python scripts/build_cap2_art.py 06
python scripts/build_cap2_art.py 07
python scripts/build_cap3_art.py
python scripts/build_cap4_art.py
python scripts/build_cap5_art.py
```

A revisão urbana abrange as 31 aquarelas: oito na primeira etapa e outras 23 na segunda. Os originais e prompts anteriores ficam preservados; os montadores selecionam `v2`, exceto CAP1-01 e CAP4-01, que usam `v3`. As revisões mantêm os identificadores, os nomes dos SVGs e dos PNGs de impressão. Conferir também a resolução efetiva do original em cada recorte: aumentar a largura do PNG exportado não aumenta o detalhe disponível na aquarela.

No capítulo 4, CAP4-01 usa a vista vertical `v3`, com os originais anteriores preservados. CAP4-08 e CAP4-09 reutilizam essa aquarela em pranchas espaciais; CAP4-10 e CAP4-11 são vetoriais e dispensam raster incorporado. O montador lê o tipo de composição no manifesto. A tabela de fusos horários registra a versão IANA e as conversões em `data-raw/figures/conversoes-utc-cap4.json`; `python3 scripts/check_cap4_timezones.py` confere os valores publicados e casos de transição sazonal, também durante `make validate`.

Nas cenas de trabalho interno, a presença urbana aparece principalmente nas vistas das janelas. Instrumentos em áreas abertas, estados dos equipamentos, documentos sem dados, vinhetas vazias e relações conceituais devem permanecer coerentes. Os mapas empíricos e diagramas técnicos seguem suas próprias fontes e métodos.

### Revisão visual do capítulo 3

A revisão das figuras de transformação temporal, acesso ao parque, unidades de observação e análise e risco por calor é recomposta por `python scripts/build_cap3_art.py 02 03 07 08`. Os nomes de produção não determinam a numeração editorial: essas artes ocupam as posições 3.2, 3.3, 3.7 e 3.8 na organização atual.

CAP3-02 conserva a aquarela `v2`, usa recortes individuais e acrescenta um calendário vetorial com símbolos distintos para critério atendido, não atendido e dado ausente. CAP3-03 usa `v4`, com parque privado verde e entorno urbano predominantemente cinza, quase sem arborização. CAP3-07 e CAP3-08 usam `v3`, respectivamente com três vistas do mesmo bairro e cinco cenas de calor intenso. As versões anteriores e todos os prompts permanecem preservados; o manifesto registra os originais ativos, dimensões, hashes e histórico.

Conferir os quatro SVGs na web e os PNGs em cinza no PDF: alinhamento das seis etapas, calendário e lacuna, acesso restrito ao parque, correspondência da estação com a vista territorial e exposição de pessoas ao sol sem cobertura. As dimensões completas dos novos originais são usadas nas figuras do parque e das unidades; os recortes da prancha de calor respeitam os limites individuais das vinhetas. A resolução efetiva deve ser verificada sobre esses originais, além do pré-voo dos PNGs exportados.

### Figuras da revisão do capítulo 1

As seis novas figuras (CAP1-07 a CAP1-12) são recompostas por `python scripts/build_cap1_revision.py`, no mesmo ambiente Python das demais artes. Os originais, os três prompts de aquarela e a proveniência estão em `assets/figures`; o manifesto é `arte-cap1-revisao-manifest.json`. O código acrescenta os rótulos editáveis e exporta as versões em cinza.

Quadrantes, curvas e Venn são exclusivamente vetoriais e usam `export_print(..., require_raster=False)`. As aquarelas mantêm a exigência de raster válido, padrão do exportador. Execute `python scripts/test_render_figure.py` para conferir a opção vetorial e a preservação da saída quando a imagem incorporada é inválida. As chamadas aceitam `DICAS_BROWSER_CHANNEL=chrome`.

A composição sobre desigualdades usa 90% da largura na impressão para preservar pelo menos 300 ppi efetivos no original, antes da rasterização. As curvas de impacto são uma elaboração didática sobre os horizontes de Freitas et al. (2014): sua Figura 1 contém blocos temporais, sem curvas ou dados quantitativos.

### Vinhetas de abertura dos capítulos 1 a 6

Executar `sh scripts/build_chapter_opening.sh` para preparar WebP colorido e PNG em cinza para os seis capítulos, ou passar os números desejados, como `sh scripts/build_chapter_opening.sh 1 2 3 4 5`. O montador seleciona as aquarelas sem sufixo `-turner`: `v3` no capítulo 1, `v1` no 2 e `v2` nos capítulos 3 a 5. O capítulo 6 mantém `cap6-indicador-decisao-turner-v2.png`. As versões Turner dos capítulos 1 a 5 estão arquivadas e não são usadas na montagem. O índice de arquivos ativos e históricos está em `assets/openings/README.md`.

A composição de 2400 × 600 pixels remove apenas margens verticais de papel, previamente conferidas, e acrescenta respiro lateral. O script lê as dimensões reais dos originais; não redimensiona a pintura nem amplia artificialmente seu detalhe. A resolução efetiva é de 508 ppi a 120 mm de largura, ou aproximadamente 521 ppi na coluna de 117 mm do miolo. Originais, prompts e créditos por capítulo ficam preservados no diretório da arte. `credits.json` documenta o capítulo 1; os créditos sem `-turner` documentam os capítulos 2 a 5. O capítulo 6 usa `cap6-indicador-decisao-turner.credits.json`.

O parcial `includes/chapter-opening/title-block.html` é ativado no YAML de cada um dos seis capítulos, pelos campos `chapter-opening.image` e `chapter-opening.alt`. Na web, a vinheta fica entre breadcrumb e título. O modelo Typst consulta um mapa de títulos, imagens e descrições e mantém a vinheta abaixo do título, no mesmo bloco indivisível. Conferir as aberturas em desktop e celular nos dois temas, e a paginação e a versão em cinza no PDF. As vinhetas não devem alterar a numeração ou a lista de figuras.

### Renderização do livro

O pré-render executa `scripts/build_catalogs.R`. Esse script lê YAML, valida campos e códigos e gera páginas e índices. Em seguida, o Quarto compõe o livro. A validação completa deve ser executada após as duas saídas existirem. Renderizar os perfis em sequência: eles compartilham artefatos intermediários do Quarto.

Na prévia, o pré-render também pode ser executado ao renderizar uma página individual. O gerador compara o conteúdo antes de gravar: fichas e índices inalterados conservam suas datas de modificação, para não invalidar outras páginas sem necessidade. A mensagem `Catálogos validados` informa quantos arquivos foram efetivamente atualizados; `0 arquivo(s) atualizado(s)` é esperado quando os dados não mudaram. Para verificar esse comportamento, executar `Rscript scripts/test_catalogs.R`. O teste também confere os vínculos entre contexto e fichas e rejeita destinos incorretos antes de gravar saídas. `scripts/validate_book_structure.R` verifica as quatro partes, os 24 capítulos, as 64 fichas, as 52 fontes, os índices e as âncoras de compatibilidade. A validação integral inclui essa conferência sobre o HTML, e o pré-voo do PDF verifica as aberturas das partes e a numeração contínua dos capítulos.

As fontes OTF e WOFF2, acompanhadas de suas licenças, estão em `assets/fonts`. O projeto usa Libertinus Serif e Source Sans 3 sem depender de instalação global ou de um serviço de fontes web. A capa é uma composição frontal de apresentação: lombada, contracapa e sangria de produção serão dimensionadas no fechamento gráfico.

O modelo de impressão é local. A entrelinha do texto corrido é de 14 pt; o fim de cada seção possui uma marca invisível para identificar páginas vazias após repaginação. O complemento do último caderno calcula automaticamente quantas páginas faltam para o múltiplo de quatro.

## Solução de problemas

- Pacote `yaml` ausente: execute `install.packages("yaml")`.

- PDF ausente: confira se o perfil `print` foi usado e se a extensão `_extensions/dicas-print/` está presente.

- Fonte indisponível: confira `assets/fonts` e a configuração `font-paths` do perfil de impressão. Não substituir uma família sem revisar a paginação.

- Link interno quebrado: use caminhos relativos ao arquivo `.qmd`; execute `make validate`.

- Página de ficha desatualizada: edite o YAML, nunca o `.qmd` gerado, e execute `make catalogs`.

## Limpeza

```sh
make clean
```

O alvo remove somente `_output` e `.quarto`, que são artefatos regeneráveis. Não remove dados, capítulos ou metadados.

### Apêndice B: estações meteorológicas e qualidade do ar

Os exemplos locais e seus originais ficam em `data-raw/estacoes`. Para conferir ou reconstruir as tabelas e figuras:

```sh
python3 scripts/build_estacoes_data.py --check
python3 scripts/build_estacoes_data.py
DICAS_BROWSER_CHANNEL=chrome python3 scripts/build_estacoes_art.py
```

O primeiro script requer Python e Poppler (`pdftotext`). O montador usa Pillow, Matplotlib e Playwright com Chrome/Chromium, além do ImageMagick. O exportador aceita `magick` (ImageMagick 7) ou `convert` (ImageMagick 6). As versões web são SVGs com fontes e imagens incorporadas; as versões de impressão são PNGs em cinza. Os gráficos mantêm texto editável no SVG e são refeitos exclusivamente dos CSV conferidos. Metadados, prompts e créditos constam no manifesto `estacoes-manifest.json`.

Na implementação, as dependências foram isoladas em `/tmp/dicas-estacoes-env`, com Playwright 1.63.0, Pillow 12.3.0, Matplotlib 3.11.2 e PyMuPDF 1.28.2 (este último somente para revisão do PDF). Esse ambiente temporário não é requisito permanente do projeto.

O filtro `figure_metadata.lua` identifica os dois apêndices pelo título, acrescenta as letras A/B na impressão e configura a numeração das figuras, tabelas e equações. Remissões dos capítulos ao apêndice usam links ao arquivo Quarto, pois seus headings são deliberadamente não numerados no PDF. A edição HTML usa a identificação alfabética nativa do Quarto.

A revisão operacional da Parte III também é verificada por `python3 scripts/test_part_iii.py` (requer PyYAML). O teste confere a resposta real arquivada do SIDRA, pesos, códigos, fronteiras etárias, janela semanal, não resposta, modelos vazios e códigos retirados. Ele integra `validate_project.R`; os casos de fronteira são entradas técnicas de teste, não dados de estabelecimentos.
