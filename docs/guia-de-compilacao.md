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

## Prévia para edição e leitura

Para editar com renderização automática:

```sh
quarto preview --profile web
```

O preview pode recompor uma página na primeira visita da sessão, mesmo que seu HTML já exista. Para uma revisão de leitura sem essa espera, compile a web uma vez e sirva os arquivos prontos:

```sh
make web
make serve
```

Abra <http://localhost:8000>. Se a web já estiver atualizada, basta `make serve`.
Se a porta estiver ocupada, use `make serve PORT=8001` e abra <http://localhost:8001>.
Esse servidor é local e não recompila alterações: execute `make web` novamente
quando quiser incorporar edições. Encerre com `Ctrl+C`.

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

### Vinhetas de abertura dos capítulos 1 a 12

Executar `sh scripts/build_chapter_opening.sh` para preparar WebP colorido e PNG em cinza para os doze capítulos, ou passar os números desejados, como `sh scripts/build_chapter_opening.sh 6 7 8 9 10 11 12`. O montador usa ImageMagick 7 (`magick`) ou ImageMagick 6 (`convert` e `identify`). Seleciona as aquarelas sem sufixo `-turner`: `v3` no capítulo 1, `v1` no 2, `v2` nos capítulos 3 a 5 e `v1` nos capítulos 6 a 12. As experiências Turner dos capítulos 1 a 6 estão arquivadas. O índice de arquivos ativos e históricos está em `assets/openings/README.md`.

A composição de 2400 × 600 pixels remove apenas margens verticais de papel, previamente conferidas, e acrescenta respiro lateral. O script lê as dimensões reais dos originais; não redimensiona a pintura nem amplia artificialmente seu detalhe. A resolução efetiva é de 508 ppi a 120 mm de largura, ou aproximadamente 521 ppi na coluna de 117 mm do miolo. Originais, prompts e créditos por capítulo ficam preservados no diretório da arte. `credits.json` documenta o capítulo 1; os arquivos `<nome-base>.credits.json`, sem `-turner`, documentam os capítulos 2 a 12.

O parcial `includes/chapter-opening/title-block.html` é ativado no YAML de cada capítulo pelos campos `chapter-opening.image` e `chapter-opening.alt`. Na web, a vinheta fica entre breadcrumb e título. O modelo Typst consulta um mapa de títulos editoriais atuais, imagens e descrições e mantém a vinheta abaixo do título, no mesmo bloco indivisível. Conferir as aberturas em desktop e celular nos dois temas, e a paginação e a versão em cinza no PDF. As vinhetas não devem alterar a numeração ou a lista de figuras.

### Renderização do livro

O pré-render executa `Rscript scripts/build_catalogs.R --incremental`. Esse script lê YAML, valida campos e códigos e gera páginas e índices. Em seguida, o Quarto compõe o livro. A validação completa deve ser executada após as duas saídas existirem. Renderizar os perfis em sequência: eles compartilham artefatos intermediários do Quarto. Ao retirar páginas de um perfil, remover também os HTML antigos correspondentes de `_output/web` antes da compilação; a validação estrutural rejeita páginas retiradas que permaneçam na saída, na navegação ou na busca. Os arquivos-fonte das páginas retiradas são preservados.

Na prévia e nas renderizações parciais, o gerador verifica os hashes das entradas e das saídas e encerra sem mensagem quando nada mudou. O cache fica em `.quarto/catalogs.rds` e inclui os YAMLs de indicadores e fontes, os dois perfis, os capítulos e o próprio gerador. Mudanças nesses arquivos, saídas ausentes ou alteradas e cache ausente ou corrompido provocam nova validação e geração. A compilação integral (`QUARTO_PROJECT_RENDER_ALL=1`) e `make catalogs` sempre validam os dados. O gerador compara o conteúdo antes de gravar: fichas e índices inalterados conservam suas datas de modificação. A mensagem `Catálogos validados` aparece somente quando a validação é executada. Para verificar o cache, sua invalidação, a atualização seletiva e a rejeição de dados e destinos inválidos, executar `Rscript scripts/test_catalogs.R`. `scripts/validate_book_structure.R` verifica as quatro partes, os 25 capítulos, a sequência de prefixos `01`–`25` e suas pastas, as 64 fichas, as 52 fontes, os índices e as âncoras de compatibilidade. No HTML, também confere os números dos capítulos e os redirecionamentos dos endereços anteriores. A validação integral inclui essa conferência sobre o HTML, e o pré-voo do PDF verifica as aberturas das partes e a numeração contínua dos capítulos.

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

### Figuras da revisão do capítulo 7

Recompor as 17 figuras com `DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap7_art.py`,
no ambiente de arte descrito acima. O montador aceita os códigos 00 a 16 para
recomposição seletiva. São dez aquarelas e sete esquemas vetoriais: os originais,
prompts, fontes e créditos estão em `assets/figures/arte-cap7-manifest.json`.
As cenas são conceituais e não contêm observações empíricas. Os identificadores das
figuras de ar/superfície e índices biometeorológicos foram preservados.

CAP7-13 mostra o abrigo de Stevenson fechado e uma vista didática aberta;
CAP7-14 mostra o termômetro infravermelho sem contato dirigido à testa.
CAP7-15 compara a vista superior de uma área hipotética com sua representação LST
em cores falsas; CAP7-16 distingue limiar absoluto, percentil e anomalia.
Recompor essas adições com `python scripts/build_cap7_art.py 13 14 15 16`.
Os códigos de produção não determinam a ordem editorial. O verificador associa
figuras e seções pelos identificadores e aceita várias figuras por seção,
mantendo as 23 âncoras existentes.

A exportação utiliza fontes incorporadas, SVG colorido e PNG de 8 bits em cinza.
O manifesto registra dimensões, hashes e resolução efetiva conservadora dos
originais. Conferir especialmente as distinções entre observação e índice, as
regras de persistência, as exceções de agregação e o ciclo de gestão.

Executar `python3 scripts/check_cap7.py --rendered` após a renderização para
conferir figuras por seção, citações, links, âncoras legadas e arquivos gráficos.
Essa verificação integra `make validate`. As 23 fichas conservam seus protocolos;
a seção 7.12 reúne os destinos de navegação e compatibilidade.

### Figuras da revisão do capítulo 8

`DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap8_art.py` recompõe as 20 figuras de precipitação, seca e eventos hidrológicos no ambiente com Pillow e Playwright. O montador aceita números de produção para exportação seletiva, como `03 12`. Onze pranchas incorporam aquarelas produzidas com `image_gen`; nove são exclusivamente vetoriais. Os originais, prompts efetivamente enviados, composições SVG e variantes em cinza ficam em `assets/figures`, com proveniência em `arte-cap8-manifest.json`.

A cobertura inclui introdução, nove seções e dez subseções. Os identificadores `fig-cadeia-hidrometeorologica` e `fig-processos-hidrologicos` e as sete âncoras antigas das fichas foram preservados. Execute `python3 scripts/check_cap8.py` para validar cobertura, citações, remissões, arquivos e resolução dos originais. Depois da renderização web, `python3 scripts/check_cap8.py --rendered` confere também links HTML, destinos das fichas, retornos e redirecionamento. Essa verificação integra `scripts/validate_project.R`.

As cenas são hipotéticas; o calendário de persistência é apenas um esquema da regra, sem medições. Conferir em especial os quatro processos hidrológicos, a diferenciação entre CDD e SPI-3 e a ordem distinta de agregação dos seis índices anuais e do SPI-3. As provas visuais da revisão ficam em `_output/proofs/revisao-cap8/`.

### Figuras da revisão do capítulo 10

Recompor as 14 figuras com `DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap10_art.py`,
no ambiente de arte descrito acima. O montador aceita os códigos 00 a 13.
São sete aquarelas e sete esquemas vetoriais; originais, prompts, fontes e créditos
constam em `assets/figures/arte-cap10-manifest.json`. As composições conservam
rótulos editáveis, fontes incorporadas, SVG colorido e PNG de 8 bits em cinza.
O manifesto registra dimensões, hashes e resolução efetiva conservadora dos originais.
Os PNGs têm 1800 px de largura, equivalentes a 381 ppi em 120 mm; os originais
das aquarelas conservam pelo menos 375 ppi nessa largura.

Executar `python3 scripts/check_cap10.py --rendered` após a renderização para
verificar as figuras da introdução, das nove seções e das quatro subseções,
as citações, os destinos das fichas e as nove âncoras legadas. Essa conferência
integra `make validate`. Os protocolos das fichas e o recorte SINISA 2025,
referência 2024, permanecem preservados. As figuras são conceituais, sem dados
observados; formas e rótulos mantêm as distinções na edição em cinza.

### Figuras da revisão do capítulo 9

Recompor as 11 figuras com `DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap9_art.py`,
no ambiente de arte descrito acima. O montador aceita os códigos 00 a 10 para
recomposição seletiva. São sete aquarelas e quatro esquemas vetoriais; fontes,
originais, prompts, dimensões, hashes e créditos constam de
`assets/figures/arte-cap9-manifest.json`.

O código acrescenta rótulos e relações editáveis, incorpora fontes e exporta SVG
colorido e PNG de 8 bits em cinza. As cenas são conceituais, sem dados observados.
As exportações têm 1600 px nas aquarelas e 1800 px nos esquemas, preservando
mais de 300 ppi a 120 mm e reduzindo o peso do PDF. A arte de monitoramento usa a versão v2, com tomadas de ar afastadas da vegetação;
a versão v1 permanece no histórico. A figura de fogo reutiliza o mesmo recorte
nos painéis de ocorrência e detecção, com grade meramente ilustrativa.

Conferir as 11 figuras na introdução, nas oito seções e nas duas subseções de
poluentes; ausência da síntese; remissões às fichas e aos capítulos relacionados;
e preservação das cinco âncoras legadas. Os identificadores `fig-cadeia-ar-saude`
e `fig-fumaca-exposicao` foram mantidos. Os protocolos operacionais das fichas não
foram alterados. Renderizar web e impressão em sequência e executar `make validate`.

### Compressão sem perda do miolo

O perfil de impressão executa `scripts/optimize_pdf.py` antes do pré-voo. Quando o
PDF ultrapassa 140 MB, recomprime os fluxos das imagens em cinza usando predição
PNG, conservando os pixels, as dimensões, a resolução e o perfil de cor. O limite
final continua sendo 150 MB. Texto, páginas, sumário, quantidade de links e hashes
dos pixels decodificados são conferidos antes de substituir a saída. Uma mudança
concorrente no PDF cancela a substituição.

Para PDFs que precisem dessa etapa, instale as dependências opcionais em um
ambiente Python e indique seu executável à compilação:

```sh
python3 -m venv /tmp/dicas-print-env
/tmp/dicas-print-env/bin/python -m pip install -r requirements-print.txt
DICAS_PYTHON=/tmp/dicas-print-env/bin/python quarto render --profile print
```

A variável `DICAS_PYTHON` também pode ser usada com `make print` ou
`scripts/render_all.sh`. Não há redução de resolução nem conversão para JPEG.


### Revisão do capítulo 12: eventos severos e desastres

O capítulo possui dez figuras: cinco composições com aquarela (00, 01, 03, 04 e 05) e cinco esquemas vetoriais (02, 06, 07, 08 e 09). Reproduzir com `DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap12_art.py`, no ambiente com Pillow e Playwright descrito acima. O exportador usa ImageMagick para os PNGs de impressão em cinza de 8 bits.

Os originais produzidos com `image_gen`, os prompts efetivamente utilizados e o manifesto `arte-cap12-manifest.json` ficam em `assets/figures`. O manifesto registra a referência visual, as dimensões e os hashes dos originais e a resolução mínima conservadora a 120 mm. Textos, setas e relações são editáveis nos SVGs. As paisagens são hipotéticas e não representam contagens ou resultados empíricos. Os identificadores `fig-risco-desastre` e `fig-linha-tempo-desastre` permanecem preservados.

Executar `python3 scripts/check_cap12.py` antes da renderização e acrescentar `--rendered` depois da compilação web. A verificação integra `make validate` e confere figuras, acessibilidade, citações, links e quatro âncoras de compatibilidade com as fichas. Na web, o capítulo habilita ampliação por lightbox; em tela estreita, as duas tabelas usam rolagem horizontal com largura mínima para preservar a leitura das colunas. As fichas e a edição do Atlas mantêm seus protocolos. Conferir também todas as figuras em desktop e celular, nos dois temas, e no PDF em tamanho real; provas da revisão ficam em `_output/proofs/revisao-cap12`. Renderizar os perfis web e print sequencialmente.

### Figuras da revisão do capítulo 11

Recompor as nove figuras com `DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap11_art.py`, no ambiente com Pillow e Playwright descrito acima. O montador aceita códigos de 00 a 08 para seleção. Seis figuras incorporam aquarelas produzidas com `image_gen`; três são vetoriais. Originais, prompts, SVGs com fontes e rótulos editáveis, PNGs em cinza e proveniência ficam em `assets/figures`, com manifesto `arte-cap11-manifest.json`. As cenas são conceituais, sem dados observados.

Executar `python3 scripts/check_cap11.py` antes da renderização e `python3 scripts/check_cap11.py --rendered` depois da web. A segunda verificação integra `make validate`. São conferidos oito seções, nove figuras, seis aquarelas, bibliografia, remissões, quatro âncoras legadas, redirecionamento e retorno das fichas. Os identificadores `fig-terra-saude` e `fig-camadas-urbanas` foram preservados. Conferir também as versões colorida e em cinza, a resolução efetiva dos originais e a distinção entre 300 m lineares e 400 m caminháveis. As provas visuais ficam em `_output/proofs/revisao-cap11/`.


### Figuras do capítulo 16: comunicação de risco

Recompor as oito figuras com `DICAS_BROWSER_CHANNEL=chrome python scripts/build_cap16_art.py`, no ambiente com Pillow e Playwright descrito acima. O montador aceita os códigos `01` a `08` para exportação seletiva. Cinco aquarelas foram produzidas com a ferramenta integrada `image_gen`; os outros três diagramas são vetoriais. Os originais, os prompts completos, os SVGs editáveis, os PNGs em cinza e o manifesto `arte-cap16-manifest.json` ficam em `assets/figures`. CAP16-07 utiliza a versão `v2`, com a anterior preservada. Os oito comentários `ARTE CAP16-01` a `ARTE CAP16-08`, no capítulo, documentam finalidade, composição, rótulos, fontes, legenda e texto alternativo.

As composições incorporam Source Sans 3, mantêm texto e setas editáveis e usam largura de 117 mm na impressão. Os PNGs têm 1800 px, cerca de 391 ppi nessa largura; as aquarelas preservam aproximadamente 341 ppi efetivos nos originais. As cenas são hipotéticas e não apresentam dados observados. A imagem de sinos é genérica e não reconstitui um episódio histórico. O manifesto registra hashes, dimensões, referência de estilo e histórico de edição.

Executar `python3 scripts/check_cap16.py` antes da renderização e acrescentar `--rendered` depois da web; a segunda verificação integra `make validate`. Conferir também todas as figuras no celular e no PDF em tamanho real, a numeração 16.1–16.8, o contraste em cinza, os três quadros e a permanência de arte, legenda e fonte na mesma página. As figuras possuem textos alternativos e ampliação por lightbox na web. Os fluxos de escuta e de falha do apoio devem manter explícitos os responsáveis, as devolutivas e o acompanhamento das demandas não atendidas.
