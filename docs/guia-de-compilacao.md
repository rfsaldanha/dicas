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

Os montadores das 31 artes dos capítulos 1 a 5 usam `scripts/render_figure.py` para exportar as composições: Chromium carrega as aquarelas e as fontes WOFF2 incorporadas no SVG; ImageMagick produz o PNG de 8 bits em escala de cinza. A exportação verifica a decodificação das imagens e o carregamento das fontes antes de substituir o PNG. Esse caminho evita exportações do Inkscape que omitem a imagem incorporada ou substituem a fonte.

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

A revisão urbana abrange as 31 aquarelas: oito na primeira etapa e outras 23 na segunda. Os originais e prompts anteriores ficam preservados; os montadores selecionam `v2`, exceto CAP1-01, que usa `v3` porque já possuía duas versões. As revisões mantêm os identificadores, os nomes dos SVGs e dos PNGs de impressão. Conferir também a resolução efetiva do original em cada recorte: aumentar a largura do PNG exportado não aumenta o detalhe disponível na aquarela.

Nas cenas de trabalho interno, a presença urbana aparece principalmente nas vistas das janelas. Instrumentos em áreas abertas, estados dos equipamentos, documentos sem dados, vinhetas vazias e relações conceituais devem permanecer coerentes. Os mapas empíricos e diagramas técnicos seguem suas próprias fontes e métodos.

### Renderização do livro

O pré-render executa `scripts/build_catalogs.R`. Esse script lê YAML, valida campos e códigos e gera páginas e índices. Em seguida, o Quarto compõe o livro. A validação completa deve ser executada após as duas saídas existirem. Renderizar os perfis em sequência: eles compartilham artefatos intermediários do Quarto.

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
