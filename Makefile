.PHONY: all web print validate links figures-real catalogs clean

all: web print validate

web:
	quarto render --profile web

print:
	quarto render --profile print

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
