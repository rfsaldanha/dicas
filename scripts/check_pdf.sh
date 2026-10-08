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
    NF && $6 != "gray" && $6 != "mono" && !($6 == "icc" && $7 == 1) { exit 1 }
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
  if ! awk '
    /^[[:space:]]*PARTE [IVXLCDM]+[[:space:]]*$/ {
      gsub(/^[[:space:]]*PARTE |[[:space:]]*$/, "")
      parts = parts (parts ? "," : "") $0
    }
    END { exit !(parts == "I,II,III,IV") }
  ' "$text_file"; then
    printf 'As quatro aberturas de parte estão ausentes ou fora de ordem.\n' >&2
    exit 1
  fi
  if ! awk '
    /^[[:space:]]*CAPÍTULO [0-9]+[[:space:]]*$/ {
      gsub(/^[[:space:]]*CAPÍTULO |[[:space:]]*$/, "")
      count++
      if ($0 + 0 != count) invalid = 1
    }
    END { exit !(count == 24 && !invalid) }
  ' "$text_file"; then
    printf 'A numeração dos capítulos deve ir de 1 a 24 no PDF.\n' >&2
    exit 1
  fi
  if grep -E 'Elementos pós-textuais|p[.] página|IV\(p[.]' "$text_file" >/dev/null; then
    printf 'Divisão antiga ou remissão de página malformada no PDF.\n' >&2
    exit 1
  fi
  for title in "Agradecimentos" "Apresentação" "Prefácio do autor" \
    "Lista de siglas" "Sumário" "Como utilizar este livro" \
    "Dados, variáveis" "Temperatura e condições" \
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
  if ! grep -F "Apêndice B — Estações" "$text_file" >/dev/null; then
    printf 'Apêndice B ausente no PDF.\n' >&2
    exit 1
  fi
  for element in "Figura B.1" "Figura B.7" "Tabela B.1" "Tabela B.5"; do
    if ! tr '\302\240' ' ' < "$text_file" | grep -E "$(printf '%s' "$element" | sed 's/ /[[:space:]]+/g')" >/dev/null; then
      printf 'Numeração do apêndice B ausente ou incorreta: %s\n' "$element" >&2
      exit 1
    fi
  done
  # A entrada bibliográfica fica depois dos capítulos e antes do conteúdo do apêndice.
  if ! awk '
    /BARCELLOS, C/ && !reference { reference = NR }
    /Este apêndice reúne um protocolo/ && !appendix { appendix = NR }
    END { exit !(reference && appendix && reference < appendix) }
  ' "$text_file"; then
    printf 'Bibliografia central ausente ou posicionada depois do apêndice.\n' >&2
    exit 1
  fi
  if ! grep -F "WORLD WIDE WEB CONSORTIUM. Data on the Web Best Practices." "$text_file" >/dev/null; then
    printf 'A seção Referências não contém uma entrada bibliográfica esperada.\n' >&2
    exit 1
  fi
fi

printf 'Pré-voo do miolo para a UICLAP concluído.\n'
