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
  "frontmatter/ficha-tecnica.qmd",
  "frontmatter/apresentacao.qmd", "frontmatter/prefacio.qmd",
  "frontmatter/agradecimentos.qmd", "frontmatter/siglas.qmd",
  "frontmatter/sumario.qmd", "frontmatter/como-usar.qmd",
  "backmatter/glossario.qmd",
  "backmatter/indice-indicadores.qmd", "backmatter/indice-fontes.qmd",
  "backmatter/indice-instituicoes.qmd", "backmatter/apendice-metodologico.qmd",
  "backmatter/lista-fichas.qmd", "backmatter/lista-tabelas.qmd",
  "backmatter/lista-figuras.qmd", "indicators/generated-index-alphabetical.qmd",
  "indicators/generated-list.qmd", "scripts/figure_metadata.lua",
  "assets/figures/cadeia-representacao.svg",
  "assets/figures/mudanca-suporte.svg",
  "assets/figures/temperatura-ar-superficie.svg",
  "assets/figures/residencia-presenca-exposicao.svg",
  "assets/figures/defasagem-exposicao-desfecho.svg",
  "scripts/build_real_figures.R", "data-raw/figures/README.md",
  "data-raw/figures/mudanca-suporte-rj.csv",
  "data-raw/figures/mudanca-suporte-rj.yml",
  "docs/diagnostico-repositorios.md", "docs/arquitetura.md",
  "docs/arquitetura-fichas.md", "docs/guia-editorial.md",
  "docs/guia-de-compilacao.md", "docs/fontes-de-dados.md",
  "docs/relatorio-implementacao.md", "docs/guia-de-revisao.md",
  "docs/relatorio-versao-para-revisao.md"
)
invisible(lapply(required, check_file))

obsolete <- c(
  "backmatter/referencias.qmd", "frontmatter/folha-rosto.qmd",
  "includes/print-before-body.typ", "print/pretextuais.typ",
  "indicators/generated-index.qmd"
)
present_obsolete <- obsolete[file.exists(obsolete)]
if (length(present_obsolete)) {
  fail("Arquivos obsoletos ainda presentes: ", paste(present_obsolete, collapse = ", "))
}

config <- unlist(lapply(
  c("_quarto-web.yml", "_quarto-print.yml"),
  readLines, warn = FALSE, encoding = "UTF-8"
), use.names = FALSE)
book_paths <- trimws(sub("^[[:space:]]*-[[:space:]]+", "", grep(
  "^[[:space:]]*-[[:space:]]+.*\\.qmd[[:space:]]*$", config, value = TRUE
)))
missing_book <- book_paths[!file.exists(book_paths)]
if (length(missing_book)) fail("Arquivo listado no livro ausente: ", paste(missing_book, collapse = ", "))

qmd_files <- list.files(".", pattern = "\\.qmd$", recursive = TRUE, full.names = TRUE)
markdown_files <- list.files(".", pattern = "\\.(qmd|md)$", recursive = TRUE, full.names = TRUE)
bad_list_items <- unlist(lapply(markdown_files, function(path) {
  lines <- readLines(path, warn = FALSE, encoding = "UTF-8")
  in_fence <- FALSE
  bad <- character()
  for (i in seq_along(lines)) {
    if (grepl("^[[:space:]]*(```|~~~)", lines[[i]], perl = TRUE)) {
      in_fence <- !in_fence
    } else if (
      !in_fence &&
      grepl(
        "^[[:space:]]*(?:[-+*]|[0-9]+[.)])[[:space:]]+(?:\\[[ xX]\\][[:space:]]+)?(?:\\*|_|`|\\[)*[[:lower:]]",
        lines[[i]],
        perl = TRUE
      )
    ) {
      bad <- c(bad, paste0(path, ":", i, ": ", lines[[i]]))
    }
  }
  bad
}), use.names = FALSE)
if (length(bad_list_items)) {
  fail(
    "Itens de lista devem começar com letra maiúscula:\n",
    paste(bad_list_items, collapse = "\n")
  )
}
source_text <- paste(vapply(qmd_files, function(path) {
  paste(readLines(path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
}, character(1L)), collapse = "\n")

mermaid_blocks <- unlist(lapply(chapter_files, function(path) {
  lines <- readLines(path, warn = FALSE, encoding = "UTF-8")
  starts <- which(lines == "```{mermaid}")
  vapply(starts, function(start) {
    relative_end <- which(lines[seq.int(start + 1L, length(lines))] == "```")[[1L]]
    paste(lines[seq.int(start, start + relative_end)], collapse = "\n")
  }, character(1L))
}), use.names = FALSE)
if (length(mermaid_blocks) != 20L) {
  fail("Esperados 20 diagramas Mermaid; encontrados ", length(mermaid_blocks), ".")
}
missing_alt <- mermaid_blocks[!grepl("(?m)^%%\\| fig-alt:", mermaid_blocks, perl = TRUE)]
if (length(missing_alt)) fail("Há diagrama Mermaid sem texto alternativo.")

framebox_lines <- grep("::: \\{\\.framebox\\}", source_text, value = TRUE)
if (length(framebox_lines)) {
  fail("Há placeholders de arte remanescentes nos capítulos.")
}

illustration_paths <- c(
  "assets/figures/cadeia-representacao.svg",
  "assets/figures/mudanca-suporte.svg",
  "assets/figures/temperatura-ar-superficie.svg",
  "assets/figures/residencia-presenca-exposicao.svg",
  "assets/figures/defasagem-exposicao-desfecho.svg"
)
illustration_mentions <- vapply(illustration_paths, function(path) {
  sum(grepl(paste0("../../", path), source_text, fixed = TRUE))
}, integer(1L))
if (any(illustration_mentions != 1L)) {
  fail("Cada ilustração editorial deve ser incorporada exatamente uma vez.")
}
for (path in illustration_paths) {
  svg <- paste(readLines(path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
  if (!grepl("<svg[ >]", svg) || !grepl("<title[ >]", svg) || !grepl("<desc[ >]", svg)) {
    fail("SVG sem estrutura acessível mínima: ", path)
  }
}

real_map <- utils::read.csv(
  "data-raw/figures/mudanca-suporte-rj.csv",
  stringsAsFactors = FALSE,
  encoding = "UTF-8"
)
real_map_required <- c("cell", "temperature_c", "area_km2", "population")
if (!all(real_map_required %in% names(real_map)) || nrow(real_map) < 10L) {
  fail("Dados derivados da figura de mudança de suporte estão incompletos.")
}
if (any(!is.finite(real_map$temperature_c)) ||
    sum(real_map$population, na.rm = TRUE) < 1e6) {
  fail("A figura de mudança de suporte não contém valores reais plausíveis.")
}
if (!grepl("CAMS/ECMWF", source_text, fixed = TRUE) ||
    !grepl("Grade Estatística 2022", source_text, fixed = TRUE)) {
  fail("Fontes do mapa real não foram declaradas no capítulo.")
}

read_table_column <- function(path, column) {
  lines <- readLines(path, warn = FALSE, encoding = "UTF-8")
  rows <- grep("^\\| \\[?[A-Z]{3}-[A-Z]{2,3}-[0-9]{2}", lines, value = TRUE)
  cells <- strsplit(sub("^\\| ", "", rows), " \\| ", fixed = FALSE)
  vapply(cells, function(x) x[[column]], character(1L))
}
alphabetical_all <- read_table_column("indicators/generated-index-alphabetical.qmd", 2L)
alphabetical_titles <- head(alphabetical_all, length(alphabetical_all) / 2L)
if (!identical(alphabetical_titles, sort(alphabetical_titles, method = "shell"))) {
  fail("O catálogo alfabético de indicadores está fora de ordem.")
}
listed_all <- read_table_column("indicators/generated-list.qmd", 1L)
listed_codes <- sub("^\\[([^]]+)\\].*$", "\\1", head(listed_all, length(listed_all) / 2L))
if (!identical(listed_codes, sort(listed_codes, method = "radix"))) {
  fail("A lista de fichas está fora da ordem dos códigos.")
}

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
home_html <- paste(readLines(file.path(html_root, "index.html"), warn = FALSE, encoding = "UTF-8"), collapse = "\n")
search_index <- paste(readLines(file.path(html_root, "search.json"), warn = FALSE, encoding = "UTF-8"), collapse = "\n")
if (!grepl("quarto-search", home_html, fixed = TRUE)) {
  fail("A interface de busca não foi localizada na página inicial.")
}
if (!grepl("Temperatura máxima diária", search_index, fixed = TRUE)) {
  fail("A ficha CLI-TEM-01 não foi localizada no índice de busca.")
}

html_files <- list.files(html_root, pattern = "\\.html$", recursive = TRUE, full.names = TRUE)
broken <- character()
broken_anchors <- character()
unresolved_html <- character()
for (path in html_files) {
  html <- paste(readLines(path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
  hrefs <- regmatches(html, gregexpr('href="[^"]+"', html, perl = TRUE))[[1L]]
  if (!length(hrefs) || identical(hrefs, "-1")) next
  hrefs <- substring(hrefs, 7L, nchar(hrefs) - 1L)
  local <- hrefs[
    !grepl("^(https?:|mailto:|tel:|javascript:|/)", hrefs) &
      !grepl("^data:", hrefs) &
      hrefs != "#"
  ]
  for (target in unique(local)) {
    target_file <- sub("[?#].*$", "", target)
    fragment <- if (grepl("#", target, fixed = TRUE)) sub("^[^#]*#", "", target) else ""
    resolved <- if (nzchar(target_file)) {
      file.path(dirname(path), utils::URLdecode(target_file))
    } else {
      path
    }
    if (!file.exists(resolved)) {
      broken <- c(broken, paste0(path, " -> ", target))
      next
    }
    if (nzchar(fragment) && grepl("\\.html$", resolved, ignore.case = TRUE)) {
      target_html <- paste(readLines(resolved, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
      decoded_fragment <- utils::URLdecode(fragment)
      if (!grepl(paste0('id="', decoded_fragment, '"'), target_html, fixed = TRUE)) {
        broken_anchors <- c(broken_anchors, paste0(path, " -> ", target))
      }
    }
  }
  if (grepl("@(sec|fig|tbl|qua)-[[:alnum:]_.:-]+", html, perl = TRUE)) {
    unresolved_html <- c(unresolved_html, path)
  }
}
if (length(broken)) {
  fail("Links internos quebrados no HTML:\n", paste(unique(broken), collapse = "\n"))
}
if (length(broken_anchors)) {
  fail("Âncoras internas quebradas no HTML:\n", paste(unique(broken_anchors), collapse = "\n"))
}
if (length(unresolved_html)) {
  fail("Referências cruzadas não resolvidas no HTML:\n", paste(unique(unresolved_html), collapse = "\n"))
}

pdf_status <- system2("sh", c("scripts/check_pdf.sh", pdf))
if (pdf_status != 0L) fail("O pré-voo do PDF falhou.")

indicator_count <- length(list.files("indicators/includes", pattern = "\\.qmd$"))
message(
  "Projeto validado: 14 capítulos; ", indicator_count, " fichas; HTML com ",
  length(html_files), " páginas; links e âncoras íntegros; PDF presente."
)
