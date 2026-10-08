#!/bin/sh
set -eu
"${DICAS_PYTHON:-python3}" scripts/optimize_pdf.py "$@"
