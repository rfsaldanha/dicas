#!/bin/sh
set -eu

quarto render --profile web
quarto render --profile print
make cover
Rscript scripts/validate_project.R
