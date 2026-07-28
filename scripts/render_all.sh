#!/bin/sh
set -eu

quarto render --profile web
quarto render --profile print
Rscript scripts/validate_project.R

