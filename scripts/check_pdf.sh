#!/bin/sh
set -eu

pdf=${1:-_output/print/dados-indicadores-clima-ambiente-saude.pdf}

if [ ! -s "$pdf" ]; then
  printf 'PDF ausente ou vazio: %s\n' "$pdf" >&2
  exit 1
fi

if command -v pdfinfo >/dev/null 2>&1; then
  pages=$(pdfinfo "$pdf" | sed -n 's/^Pages:[[:space:]]*//p')
  size=$(pdfinfo "$pdf" | sed -n 's/^Page size:[[:space:]]*//p')
  compact=$(printf '%s' "$size" | tr -d ' ')
  case "$compact" in
    439.37x651.968pts*|439.37x651.969pts*) ;;
    *)
      printf 'Formato inesperado: %s (esperado: 155 × 230 mm)\n' "$size" >&2
      exit 1
      ;;
  esac
  printf 'PDF: %s páginas; %s\n' "$pages" "$size"
  if [ "$pages" -lt 400 ] || [ "$pages" -gt 500 ]; then
    printf 'Aviso: a paginação está fora da faixa editorial de 400–500 páginas.\n'
  fi
fi

if command -v pdffonts >/dev/null 2>&1; then
  if ! pdffonts "$pdf" | tail -n +3 | awk 'NF && $6 != "yes" { exit 1 }'; then
    printf 'Há fontes não incorporadas no PDF.\n' >&2
    exit 1
  fi
  printf 'Fontes incorporadas: sim\n'
fi

if command -v pdftotext >/dev/null 2>&1; then
  text_file=$(mktemp)
  trap 'rm -f "$text_file"' EXIT HUP INT TERM
  pdftotext -layout "$pdf" "$text_file"
  for title in "Ficha técnica" "Apresentação" "Lista de siglas" "Sumário" \
    "Dados, variáveis, índices e" "Temperatura e condições" \
    "Temperatura máxima diária" "Título resumido" "Responsabilidade gerencial" \
    "Análise descritiva do indicador" "Tipo de registro" \
    "Referências" "Índice de fontes de dados"; do
    if ! grep -F "$title" "$text_file" >/dev/null; then
      printf 'Elemento esperado ausente no PDF: %s\n' "$title" >&2
      exit 1
    fi
  done
  if grep -E '@(sec|fig|tbl|qua)-[[:alnum:]_.:-]+|[?][?]' "$text_file" >/dev/null; then
    printf 'Referência cruzada não resolvida localizada no PDF.\n' >&2
    exit 1
  fi
fi

printf 'Pré-voo do PDF concluído.\n'
