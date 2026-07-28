.PHONY: all web print validate catalogs clean

all: web print validate

web:
	quarto render --profile web

print:
	quarto render --profile print

validate:
	Rscript scripts/validate_project.R

catalogs:
	Rscript scripts/build_catalogs.R

clean:
	rm -rf _output .quarto
