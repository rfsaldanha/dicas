# Vinhetas de abertura

As aberturas dos capítulos editoriais 1 a 12 usam aquarelas com cores suaves, grafite e nanquim delicados e bordas dissolvidas no papel branco. Todas são paisagens brasileiras hipotéticas sem pessoas, geradas pela ferramenta integrada `image_gen`. A abertura aprovada do capítulo 1 orienta a identidade visual da série.

| Capítulo | Nome-base ativo | Versão |
|---|---|---|
| 1 — Clima, ambiente e saúde pública | `cap1-clima-ambiente-saude` | `v3` |
| 2 — Mudança climática, planejamento e resposta do SUS | `cap2-planejamento-resposta-sus` | `v1` |
| 3 — Dados, variáveis, índices e indicadores | `cap3-dados-indicadores` | `v2` |
| 4 — Integração de dados: espaço, tempo e qualidade | `cap4-espaco-tempo-qualidade` | `v2` |
| 5 — Seleção de fontes e qualificação de indicadores | `cap5-fontes-fichas` | `v2` |
| 6 — Análise de situação de saúde e decisão pública | `cap6-indicador-decisao` | `v1` |
| 7 — Temperatura e condições térmicas | `cap7-temperatura-condicoes-termicas` | `v1` |
| 8 — Precipitação, secas, inundações e deslizamentos | `cap8-precipitacao-secas-eventos-hidrologicos` | `v1` |
| 9 — Qualidade do ar, queimadas e fumaça | `cap9-qualidade-ar-queimadas-fumaca` | `v1` |
| 10 — Água, saneamento e higiene | `cap10-agua-saneamento-qualidade-ambiental` | `v1` |
| 11 — Uso e cobertura da terra, vegetação e ambiente urbano | `cap11-uso-cobertura-terra-ambiente-urbano` | `v1` |
| 12 — Eventos meteorológicos severos e desastres | `cap12-eventos-severos-desastres` | `v1` |

O nome-base seguido da versão e de `.png` identifica o original ativo. O prompt correspondente usa a extensão `.prompt.txt`. Os créditos estão em `credits.json` para o capítulo 1 e em `<nome-base>.credits.json` para os capítulos 2 a 12; incluem descrição alternativa, dimensões reais e recorte aplicado.

`sh scripts/build_chapter_opening.sh` prepara a série completa. Para preparar apenas as novas aberturas, usar `sh scripts/build_chapter_opening.sh 6 7 8 9 10 11 12`. O script aceita ImageMagick 7 (`magick`) e 6 (`convert` e `identify`). Exporta `-web.webp` em cor e `-print.png` em cinza, ambos com 2400 × 600 pixels. O processo retira somente papel e acrescenta margens laterais, sem redimensionar a pintura. Na web, a imagem fica entre breadcrumb e título; no PDF, abaixo do título e na mesma página. As vinhetas não têm número, legenda nem entrada na lista de figuras.

As versões com `-turner` dos capítulos 1 a 6 permanecem arquivadas com seus prompts, derivados e créditos. Os capítulos 1 a 5 voltaram às aquarelas originais por preferência do autor. A abertura do capítulo 6 foi reinterpretada na mesma identidade suave, preservando a cidade ribeirinha, a ponte e os equipamentos públicos. O registro inicial do teste está em `cap6-indicador-decisao-turner-teste.credit-history.json`.
