#!/bin/sh
# Prepara as vinhetas dos capítulos 1 a 12, preservando os originais.
set -eu
cd "$(dirname "$0")/.."

# ImageMagick 7 usa magick; a versão 6 fornece convert e identify.
if command -v magick >/dev/null 2>&1; then
  image_convert() { magick "$@"; }
  image_identify() { magick identify "$@"; }
elif command -v convert >/dev/null 2>&1 && command -v identify >/dev/null 2>&1; then
  image_convert() { convert "$@"; }
  image_identify() { identify "$@"; }
else
  printf 'ImageMagick ausente: instale magick ou convert e identify.\n' >&2
  exit 1
fi

build_opening() {
  target_prefix="assets/openings/$1"
  source_image="${target_prefix}-$2.png"
  crop_top_override=${3:-}
  # As margens verticais foram conferidas visualmente em cada original.
  # Lê dimensões reais: a geração pode variar alguns pixels entre arquivos.
  set -- $(image_identify -format '%w %h' "$source_image")
  source_width=$1
  source_height=$2
  if [ "$source_width" -gt 2400 ] || [ "$source_width" -lt 1418 ] || [ "$source_height" -lt 600 ]; then
    printf 'Dimensões incompatíveis com a montagem sem redimensionamento: %s\n' "$source_image" >&2
    return 1
  fi
  crop_top=${crop_top_override:-$(((source_height - 600) / 2))}
  if [ "$crop_top" -lt 0 ] || [ "$((crop_top + 600))" -gt "$source_height" ]; then
    printf 'Recorte fora do original: %s\n' "$source_image" >&2
    return 1
  fi
  crop_geometry="${source_width}x600+0+${crop_top}"

  # Retira apenas papel acima e abaixo; acrescenta branco nas laterais.
  # Nenhum redimensionamento: a resolução efetiva a 120 mm é de 508 ppi.
  image_convert "$source_image" -crop "$crop_geometry" +repage \
    -background white -gravity center -extent 2400x600 \
    -quality 92 "${target_prefix}-web.webp"

  image_convert "$source_image" -crop "$crop_geometry" +repage \
    -background white -gravity center -extent 2400x600 \
    -alpha remove -alpha off -colorspace Gray -depth 8 \
    -units PixelsPerInch -density 508 -define png:color-type=0 \
    "${target_prefix}-print.png"
  printf 'Vinheta exportada: %s\n' "$target_prefix"
}

# Sem argumentos, recompõe a série completa; números selecionam capítulos.
if [ "$#" -eq 0 ]; then set -- 1 2 3 4 5 6 7 8 9 10 11 12; fi
for chapter in "$@"; do
  case "$chapter" in
    1) build_opening cap1-clima-ambiente-saude v3 ;;
    2) build_opening cap2-planejamento-resposta-sus v1 ;;
    3) build_opening cap3-dados-indicadores v2 ;;
    4) build_opening cap4-espaco-tempo-qualidade v2 ;;
    # Preserva também a borda inferior da aguada do rio.
    5) build_opening cap5-fontes-fichas v2 70 ;;
    6) build_opening cap6-indicador-decisao v1 ;;
    7) build_opening cap7-temperatura-condicoes-termicas v1 ;;
    8) build_opening cap8-precipitacao-secas-eventos-hidrologicos v1 ;;
    9) build_opening cap9-qualidade-ar-queimadas-fumaca v1 ;;
    10) build_opening cap10-agua-saneamento-qualidade-ambiental v1 ;;
    11) build_opening cap11-uso-cobertura-terra-ambiente-urbano v1 ;;
    12) build_opening cap12-eventos-severos-desastres v1 ;;
    *) printf 'Capítulo inválido: %s (use 1 a 12).\n' "$chapter" >&2; exit 1 ;;
  esac
done
