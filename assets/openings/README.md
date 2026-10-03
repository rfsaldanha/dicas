# Vinhetas de abertura

As aberturas dos capítulos editoriais 1 a 5 usam as aquarelas originais, com cores suaves e traços delicados. O capítulo 6 mantém o teste inspirado em William Turner. Todas são paisagens sem pessoas, geradas pela ferramenta integrada `image_gen`.

| Capítulo | Nome-base ativo | Versão |
|---|---|---|
| 1 — Clima, ambiente e saúde pública | `cap1-clima-ambiente-saude` | `v3` |
| 2 — Mudança climática, planejamento e resposta do SUS | `cap2-planejamento-resposta-sus` | `v1` |
| 3 — Dos dados aos indicadores | `cap3-dados-indicadores` | `v2` |
| 4 — Compatibilizando dados: espaço, tempo e qualidade | `cap4-espaco-tempo-qualidade` | `v2` |
| 5 — Fontes de dados e fichas de indicadores | `cap5-fontes-fichas` | `v2` |
| 6 — Do indicador à decisão pública | `cap6-indicador-decisao-turner` | `v2` |

O nome-base seguido da versão e de `.png` identifica o original ativo. O prompt correspondente usa a extensão `.prompt.txt`. Os créditos estão em `credits.json` para o capítulo 1 e em `<nome-base>.credits.json` para os capítulos 2 a 6.

`sh scripts/build_chapter_opening.sh` prepara `-web.webp` em cor e `-print.png` em cinza, ambos com 2400 × 600 pixels. O processo retira somente papel e acrescenta margens laterais, sem redimensionar a pintura. Na web, a imagem fica entre breadcrumb e título; no PDF, abaixo do título e na mesma página. As vinhetas não têm número, legenda nem entrada na lista de figuras.

As versões com `-turner` dos capítulos 1 a 5 permanecem arquivadas com seus prompts, derivados e créditos. Foram retiradas das aberturas a pedido do autor por apresentarem um tratamento mais dramático que o desejado. O registro inicial do teste do capítulo 6 está em `cap6-indicador-decisao-turner-teste.credit-history.json`.
