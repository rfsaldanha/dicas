#!/bin/sh
set -eu

pdf=${1:-_output/print/dados-indicadores-clima-ambiente-saude.pdf}

if [ ! -s "$pdf" ]; then
  printf 'PDF ausente ou vazio: %s\n' "$pdf" >&2
  exit 1
fi

bytes=$(wc -c < "$pdf" | tr -d ' ')
if [ "$bytes" -gt 150000000 ]; then
  printf 'PDF excede o limite de 150 MB da UICLAP: %s bytes\n' "$bytes" >&2
  exit 1
fi

if command -v pdfinfo >/dev/null 2>&1; then
  pages=$(pdfinfo "$pdf" | sed -n 's/^Pages:[[:space:]]*//p')
  size=$(pdfinfo "$pdf" | sed -n 's/^Page size:[[:space:]]*//p')
  compact=$(printf '%s' "$size" | tr -d ' ')
  case "$compact" in
    453.543x651.968pts*|453.543x651.969pts*) ;;
    *)
      printf 'Formato inesperado: %s (esperado: 160 × 230 mm)\n' "$size" >&2
      exit 1
      ;;
  esac
  if [ "$pages" -lt 4 ] || [ "$pages" -gt 1000 ]; then
    printf 'Quantidade de páginas fora do intervalo aceito pela UICLAP: %s\n' "$pages" >&2
    exit 1
  fi
  remainder=$((pages % 4))
  if [ "$remainder" -ne 0 ]; then
    printf 'O miolo não fecha em cadernos de quatro páginas: %s páginas.\n' "$pages" >&2
    exit 1
  fi
  printf 'PDF UICLAP: %s páginas; %s; %s bytes\n' "$pages" "$size" "$bytes"
fi

if command -v pdffonts >/dev/null 2>&1; then
  if ! pdffonts "$pdf" | tail -n +3 | awk 'NF && $(NF-4) != "yes" { exit 1 }'; then
    printf 'Há fontes não incorporadas no PDF.\n' >&2
    exit 1
  fi
  printf 'Fontes incorporadas: sim\n'
fi

if command -v pdfimages >/dev/null 2>&1; then
  image_list=$(mktemp)
  trap 'rm -f "$image_list"' EXIT HUP INT TERM
  pdfimages -list "$pdf" > "$image_list"
  if ! tail -n +3 "$image_list" | awk '
    NF && $6 != "gray" && $6 != "mono" { exit 1 }
  '; then
    printf 'O PDF contém imagens raster coloridas; o miolo deve permanecer em escala de cinza.\n' >&2
    exit 1
  fi
  if ! tail -n +3 "$image_list" | awk '
    NF && ($13 < 300 || $14 < 300) { exit 1 }
  '; then
    printf 'O PDF contém imagem raster abaixo de 300 ppi.\n' >&2
    exit 1
  fi
  printf 'Imagens raster: escala de cinza e resolução mínima de 300 ppi.\n'
fi

if command -v pdftotext >/dev/null 2>&1; then
  text_file=$(mktemp)
  trap 'rm -f "$text_file" ${image_list:-}' EXIT HUP INT TERM
  pdftotext -layout "$pdf" "$text_file"
  for title in "Agradecimentos" "Apresentação" "Prefácio do autor" \
    "Lista de siglas" "Sumário" "Como utilizar este livro" \
    "Dados, variáveis, índices e" "Temperatura e condições" \
    "Temperatura máxima diária" "Título resumido" "Responsabilidade gerencial" \
    "Análise descritiva do indicador" "Tipo de registro" \
    "Referências" "Catálogo de fontes de dados"; do
    if ! grep -F "$title" "$text_file" >/dev/null; then
      printf 'Elemento esperado ausente no PDF: %s\n' "$title" >&2
      exit 1
    fi
  done
  if grep -E '@(sec|fig|tbl|qua)-[[:alnum:]_.:-]+|[?][?]' "$text_file" >/dev/null; then
    printf 'Referência cruzada não resolvida localizada no PDF.\n' >&2
    exit 1
  fi
  if grep -E '^[[:space:]]*Bibliografia[[:space:]]*$' "$text_file" >/dev/null; then
    printf 'Título bibliográfico duplicado ou incorreto localizado no PDF: Bibliografia.\n' >&2
    exit 1
  fi
  if ! grep -F "Quadro A.1" "$text_file" >/dev/null; then
    printf 'Numeração do quadro do apêndice não foi convertida para A.1.\n' >&2
    exit 1
  fi
  if ! grep -F "WORLD WIDE WEB CONSORTIUM. Data on the Web Best Practices." "$text_file" >/dev/null; then
    printf 'A seção Referências não contém uma entrada bibliográfica esperada.\n' >&2
    exit 1
  fi
fi

printf 'Pré-voo do miolo para a UICLAP concluído.\n'
