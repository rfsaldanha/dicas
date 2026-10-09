.PHONY: all web serve print cover validate links figures-real catalogs clean

PORT ?= 8000

all: web print cover validate

web:
	quarto render --profile web

serve:
	@test -f _output/web/index.html || { echo "Execute make web antes de make serve."; exit 1; }
	python3 -m http.server $(PORT) --bind 127.0.0.1 --directory _output/web

print:
	quarto render --profile print

cover:
	mkdir -p _output/cover
	quarto typst compile --root . --font-path assets/fonts assets/cover/capa.typ _output/cover/capa.pdf

validate:
	Rscript scripts/validate_project.R

links:
	Rscript scripts/validate_external_links.R

figures-real:
	Rscript scripts/build_real_figures.R

catalogs:
	Rscript scripts/build_catalogs.R

clean:
	rm -rf _output .quarto
