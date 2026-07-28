#!/usr/bin/env Rscript

script_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
script_path <- if (length(script_arg)) sub("^--file=", "", script_arg[[1L]]) else "scripts/validate_project.R"
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
setwd(root)

fail <- function(...) stop(paste0(...), call. = FALSE)
check_file <- function(path) {
  if (!file.exists(path) || file.info(path)$size == 0) fail("Arquivo ausente ou vazio: ", path)
}

catalog_status <- system2("Rscript", "scripts/build_catalogs.R")
if (catalog_status != 0L) fail("Falha na validação dos catálogos.")

chapter_files <- sort(list.files("chapters", pattern = "\\.qmd$", recursive = TRUE, full.names = TRUE))
if (length(chapter_files) != 14L) {
  fail("Esperados 14 capítulos em chapters/; encontrados ", length(chapter_files), ".")
}

required <- c(
  "_quarto.yml", "_quarto-web.yml", "_quarto-print.yml", "index.qmd",
  "README.md", "CONTRIBUTING.md", "references.bib",
  "frontmatter/folha-rosto.qmd", "frontmatter/ficha-tecnica.qmd",
  "frontmatter/apresentacao.qmd", "frontmatter/prefacio.qmd",
  "frontmatter/agradecimentos.qmd", "frontmatter/siglas.qmd",
  "frontmatter/sumario.qmd", "frontmatter/como-usar.qmd",
  "backmatter/glossario.qmd", "backmatter/referencias.qmd",
  "backmatter/indice-indicadores.qmd", "backmatter/indice-fontes.qmd",
  "backmatter/indice-instituicoes.qmd", "backmatter/apendice-metodologico.qmd",
  "backmatter/lista-fichas.qmd", "backmatter/lista-tabelas.qmd",
  "backmatter/lista-figuras.qmd",
  "docs/diagnostico-repositorios.md", "docs/arquitetura.md",
  "docs/arquitetura-fichas.md", "docs/guia-editorial.md",
  "docs/guia-de-compilacao.md", "docs/fontes-de-dados.md",
  "docs/relatorio-implementacao.md"
)
invisible(lapply(required, check_file))

config <- readLines("_quarto.yml", warn = FALSE, encoding = "UTF-8")
book_paths <- trimws(sub("^[[:space:]]*-[[:space:]]+", "", grep(
  "^[[:space:]]*-[[:space:]]+.*\\.qmd[[:space:]]*$", config, value = TRUE
)))
missing_book <- book_paths[!file.exists(book_paths)]
if (length(missing_book)) fail("Arquivo listado no livro ausente: ", paste(missing_book, collapse = ", "))

qmd_files <- list.files(".", pattern = "\\.qmd$", recursive = TRUE, full.names = TRUE)
source_text <- paste(vapply(qmd_files, function(path) {
  paste(readLines(path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
}, character(1L)), collapse = "\n")

citations <- regmatches(
  source_text,
  gregexpr("(?<![[:alnum:]_.+-])@[[:alnum:]][[:alnum:]_.:-]*", source_text, perl = TRUE)
)[[1L]]
if (length(citations) && !identical(citations, "-1")) {
  citations <- substring(citations, 2L)
  citations <- citations[!grepl("^(sec|fig|tbl|qua|eq|lst)-", citations)]
} else {
  citations <- character()
}
bib <- readLines("references.bib", warn = FALSE, encoding = "UTF-8")
bib_lines <- grep("^[[:space:]]*@[[:alpha:]]+[[:space:]]*\\{", bib, value = TRUE)
bib_keys <- sub(
  "^[[:space:]]*@[[:alpha:]]+[[:space:]]*\\{[[:space:]]*([^,[:space:]]+).*$",
  "\\1", bib_lines, perl = TRUE
)
missing_citations <- setdiff(unique(citations), bib_keys)
if (length(missing_citations)) {
  fail("Citações sem entrada bibliográfica: ", paste(missing_citations, collapse = ", "))
}

html_root <- "_output/web"
pdf <- "_output/print/dados-indicadores-clima-ambiente-saude.pdf"
check_file(file.path(html_root, "index.html"))
check_file(file.path(html_root, "search.json"))
check_file(pdf)

html_files <- list.files(html_root, pattern = "\\.html$", recursive = TRUE, full.names = TRUE)
broken <- character()
for (path in html_files) {
  html <- paste(readLines(path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
  hrefs <- regmatches(html, gregexpr('href="[^"]+"', html, perl = TRUE))[[1L]]
  if (!length(hrefs) || identical(hrefs, "-1")) next
  hrefs <- substring(hrefs, 7L, nchar(hrefs) - 1L)
  local <- hrefs[
    !grepl("^(https?:|mailto:|tel:|javascript:|#|/)", hrefs) &
      !grepl("^data:", hrefs)
  ]
  local <- sub("[?#].*$", "", local)
  local <- local[nzchar(local)]
  for (target in unique(local)) {
    resolved <- file.path(dirname(path), utils::URLdecode(target))
    if (!file.exists(resolved)) broken <- c(broken, paste0(path, " -> ", target))
  }
}
if (length(broken)) {
  fail("Links internos quebrados no HTML:\n", paste(unique(broken), collapse = "\n"))
}

pdf_status <- system2("sh", c("scripts/check_pdf.sh", pdf))
if (pdf_status != 0L) fail("O pré-voo do PDF falhou.")

message(
  "Projeto validado: 14 capítulos; 3 fichas; HTML com ",
  length(html_files), " páginas; PDF presente."
)

