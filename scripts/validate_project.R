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
if (length(chapter_files) != 15L) {
  fail("Esperados 15 capítulos em chapters/; encontrados ", length(chapter_files), ".")
}

required <- c(
  "_quarto.yml", "_quarto-web.yml", "_quarto-print.yml", "index.qmd",
  "README.md", "CONTRIBUTING.md", "references.bib",
  "frontmatter/ficha-tecnica.qmd",
  "frontmatter/apresentacao.qmd", "frontmatter/prefacio.qmd",
  "frontmatter/agradecimentos.qmd", "frontmatter/siglas.qmd",
  "frontmatter/sumario.qmd", "frontmatter/como-usar.qmd",
  "backmatter/referencias.qmd", "backmatter/glossario.qmd",
  "backmatter/indice-indicadores.qmd", "backmatter/indice-fontes.qmd",
  "backmatter/indice-instituicoes.qmd", "backmatter/apendice-metodologico.qmd",
  "backmatter/lista-fichas.qmd", "backmatter/lista-tabelas.qmd",
  "backmatter/lista-figuras.qmd", "indicators/generated-index-alphabetical.qmd",
  "indicators/generated-list.qmd", "scripts/figure_metadata.lua",
  "assets/figures/arte-cap1-01-v1.png",
  "assets/figures/arte-cap1-01-v2.png",
  "assets/references/aquarela-grafite-nanquim.png",
  "assets/figures/arte-cap1-01-diagrama.svg",
  "assets/figures/arte-cap1-01-diagrama-print.png",
  "scripts/build_cap1_art.py",
  "assets/figures/arte-cap1-02-v1.png",
  "assets/figures/arte-cap1-02-v1.prompt.txt",
  "assets/figures/arte-cap1-02-trajetorias.svg",
  "assets/figures/arte-cap1-02-trajetorias-print.png",
  "scripts/build_cap1_trajectories.py",
  "assets/figures/arte-cap1-03-v1.png",
  "assets/figures/arte-cap1-03-v1.prompt.txt",
  "assets/figures/arte-cap1-03-exposicao.svg",
  "assets/figures/arte-cap1-03-exposicao-print.png",
  "scripts/build_cap1_heat_exposure.py",
  "scripts/build_cap1_remaining_art.py",
  "assets/figures/arte-cap1-04-v1.png",
  "assets/figures/arte-cap1-04-v1.prompt.txt",
  "assets/figures/arte-cap1-04-dose.svg",
  "assets/figures/arte-cap1-04-dose-print.png",
  "assets/figures/arte-cap1-05-v1.png",
  "assets/figures/arte-cap1-05-v1.prompt.txt",
  "assets/figures/arte-cap1-05-territorios.svg",
  "assets/figures/arte-cap1-05-territorios-print.png",
  "assets/figures/arte-cap1-06-v1.png",
  "assets/figures/arte-cap1-06-v1.prompt.txt",
  "assets/figures/arte-cap1-06-justica.svg",
  "assets/figures/arte-cap1-06-justica-print.png",
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
chapter_two_art <- c(
  "01-referencias", "02-cascatas", "07-grades", "03-atendimento",
  "04-adaptacao", "05-horizontes", "06-indicadores"
)
urban_art <- c(
  paste0("1-", sprintf("%02d", 2:6)),
  paste0("2-", sprintf("%02d", 1:7)),
  paste0("3-", sprintf("%02d", 1:8)),
  paste0("4-", sprintf("%02d", 1:7)),
  paste0("5-", sprintf("%02d", 1:3))
)
required <- c(required, "scripts/render_figure.py",
  "assets/figures/arte-cap1-01-v3.png",
  "assets/figures/arte-cap1-01-v3.prompt.txt",
  "assets/figures/arte-cap4-02-v2-refinamento.prompt.txt",
  paste0("assets/figures/arte-cap", urban_art, "-v2.png"),
  paste0("assets/figures/arte-cap", urban_art, "-v2.prompt.txt"))
required <- c(required, "scripts/build_cap2_art.py", unlist(lapply(chapter_two_art, function(art) {
  number <- substr(art, 1L, 2L)
  paste0("assets/figures/arte-cap2-", c(
    paste0(number, "-v1.png"), paste0(number, "-v1.prompt.txt"),
    paste0(art, ".svg"), paste0(art, "-print.png")
  ))
}), use.names = FALSE))
chapter_three_art <- c(
  "01-cadeia", "02-tempo", "03-proxy", "04-indice",
  "05-ficha", "06-denominador", "07-unidades", "08-risco"
)
chapter_three_ids <- c(
  "fig-cadeia-representacao", "fig-escala-temporal", "fig-proxy-limites",
  "fig-indice-componentes", "fig-ficha-ripsa-livro", "fig-numerador-denominador",
  "fig-observacao-analise-populacao", "fig-indicadores-cadeia-risco"
)
required <- c(required, "scripts/build_cap3_art.py", "assets/figures/arte-cap3-manifest.json",
  unlist(lapply(chapter_three_art, function(art) {
    number <- substr(art, 1L, 2L)
    paste0("assets/figures/arte-cap3-", c(
      paste0(number, "-v1.png"), paste0(number, "-v1.prompt.txt"),
      paste0(art, ".svg"), paste0(art, "-print.png")
    ))
  }), use.names = FALSE))
chapter_four_art <- c(
  "01-suporte", "02-zoneamento", "03-tempos", "04-previsao",
  "05-qualidade", "06-ausencias", "07-interpretacao"
)
chapter_four_ids <- c(
  "fig-suporte-localizacao", "fig-escala-zoneamento", "fig-tempos-dado",
  "fig-tempos-previsao", "fig-qualidade-uso", "fig-ausencia-zero",
  "fig-compatibilizacao-inferencia"
)
required <- c(required, "scripts/build_cap4_art.py", "assets/figures/arte-cap4-manifest.json",
  unlist(lapply(chapter_four_art, function(art) {
    number <- substr(art, 1L, 2L)
    paste0("assets/figures/arte-cap4-", c(
      paste0(number, "-v1.png"), paste0(number, "-v1.prompt.txt"),
      paste0(art, ".svg"), paste0(art, "-print.png")
    ))
  }), use.names = FALSE))
chapter_five_art <- c("01-identificacao", "02-selecao", "03-proveniencia")
chapter_five_ids <- c("fig-identificacao-fonte", "fig-selecao-fontes", "fig-proveniencia")
required <- c(required, "scripts/build_cap5_art.py", "assets/figures/arte-cap5-manifest.json",
  unlist(lapply(chapter_five_art, function(art) {
    number <- substr(art, 1L, 2L)
    paste0("assets/figures/arte-cap5-", c(
      paste0(number, "-v1.png"), paste0(number, "-v1.prompt.txt"),
      paste0(art, ".svg"), paste0(art, "-print.png")
    ))
  }), use.names = FALSE))
invisible(lapply(required, check_file))

obsolete <- c(
  "frontmatter/folha-rosto.qmd",
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
if (length(mermaid_blocks) != 17L) {
  fail("Esperados 17 diagramas Mermaid; encontrados ", length(mermaid_blocks), ".")
}
missing_alt <- mermaid_blocks[!grepl("(?m)^%%\\| fig-alt:", mermaid_blocks, perl = TRUE)]
if (length(missing_alt)) fail("Há diagrama Mermaid sem texto alternativo.")

framebox_lines <- grep("::: \\{\\.framebox\\}", source_text, value = TRUE)
if (length(framebox_lines)) {
  fail("Há placeholders de arte remanescentes nos capítulos.")
}

illustration_paths <- c(
  paste0("assets/figures/arte-cap5-", chapter_five_art, ".svg"),
  paste0("assets/figures/arte-cap4-", chapter_four_art, ".svg"),
  paste0("assets/figures/arte-cap3-", chapter_three_art, ".svg"),
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

real_map_metadata <- yaml::read_yaml("data-raw/figures/mudanca-suporte-rj.yml")
if (any(!is.finite(real_map$area_km2)) || any(real_map$area_km2 < 0) ||
    any(!is.finite(real_map$population)) || any(real_map$population < 0)) {
  fail("Ponderadores inválidos no exemplo real de mudança de suporte.")
}
recomputed <- c(
  weighted.mean(real_map$temperature_c, real_map$area_km2),
  weighted.mean(real_map$temperature_c, real_map$population),
  max(real_map$temperature_c)
)
documented <- unlist(real_map_metadata[c(
  "area_weighted_mean_c", "population_weighted_mean_c", "territorial_maximum_c"
)])
if (length(documented) != 3L || any(abs(recomputed - documented) > 1e-4)) {
  fail("Resultados documentados não correspondem aos dados do exemplo real.")
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

if (anyDuplicated(bib_keys)) fail("Há chaves duplicadas na bibliografia.")
for (profile in c("_quarto-web.yml", "_quarto-print.yml")) {
  profile_text <- readLines(profile, warn = FALSE, encoding = "UTF-8")
  refs_line <- grep("backmatter/referencias.qmd", profile_text, fixed = TRUE)
  appendix_line <- grep("^[[:space:]]*appendices:", profile_text)
  if (length(refs_line) != 1L || length(appendix_line) != 1L || refs_line >= appendix_line) {
    fail("Referências devem aparecer uma vez, antes dos apêndices: ", profile)
  }
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
chapter_one_html <- paste(readLines(
  file.path(html_root, "chapters/part-1/01-clima-ambiente-saude.html"),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
if (!grepl('<img[^>]+src="[^"]*arte-cap1-01-diagrama[.]svg"', chapter_one_html, perl = TRUE)) {
  fail("A aquarela da Figura 1.1 não foi incorporada ao capítulo 1.")
}
if (!grepl('<img[^>]+src="[^"]*arte-cap1-02-trajetorias[.]svg"', chapter_one_html, perl = TRUE)) {
  fail("A aquarela da Figura 1.2 não foi incorporada ao capítulo 1.")
}
if (!grepl('<img[^>]+src="[^"]*arte-cap1-03-exposicao[.]svg"', chapter_one_html, perl = TRUE)) {
  fail("A aquarela da Figura 1.3 não foi incorporada ao capítulo 1.")
}
if (!grepl('<img[^>]+src="[^"]*arte-cap1-04-dose[.]svg"', chapter_one_html, perl = TRUE)) {
  fail("A aquarela da Figura 1.4 não foi incorporada ao capítulo 1.")
}
if (!grepl('<img[^>]+src="[^"]*arte-cap1-05-territorios[.]svg"', chapter_one_html, perl = TRUE)) {
  fail("A aquarela da Figura 1.5 não foi incorporada ao capítulo 1.")
}
if (!grepl('<img[^>]+src="[^"]*arte-cap1-06-justica[.]svg"', chapter_one_html, perl = TRUE)) {
  fail("A aquarela da Figura 1.6 não foi incorporada ao capítulo 1.")
}
chapter_two_html <- paste(readLines(
  file.path(html_root, "chapters/part-1/01b-mudanca-climatica-resposta-sus.html"),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
for (i in seq_along(chapter_two_art)) {
  art <- paste0("arte-cap2-", chapter_two_art[[i]], ".svg")
  check_file(file.path(html_root, "assets/figures", art))
  image_pattern <- paste0('<img[^>]+src="[^"]*', sub("[.]svg$", "[.]svg", art), '"')
  if (!grepl(image_pattern, chapter_two_html, perl = TRUE)) {
    fail("A aquarela da Figura 2.", i, " não foi incorporada ao capítulo 2.")
  }
}
chapter_three_path <- "chapters/part-1/02-dados-variaveis-indices-indicadores.qmd"
chapter_three_source <- paste(readLines(chapter_three_path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
chapter_three_html <- paste(readLines(
  file.path(html_root, sub("[.]qmd$", ".html", chapter_three_path)),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
figure_list <- paste(readLines("backmatter/lista-figuras.qmd", warn = FALSE, encoding = "UTF-8"), collapse = "\n")
# A arte 05-ficha foi transferida ao capítulo 5, preservando o arquivo original.
for (i in which(chapter_three_ids != "fig-ficha-ripsa-livro")) {
  figure_number <- if (i > 5L) i - 1L else i
  art <- paste0("arte-cap3-", chapter_three_art[[i]], ".svg")
  id <- chapter_three_ids[[i]]
  check_file(file.path(html_root, "assets/figures", art))
  if (!grepl(paste0('id="', id, '"'), chapter_three_html, fixed = TRUE) ||
      !grepl(paste0("Figura&nbsp;3.", figure_number, ":"), chapter_three_html, fixed = TRUE)) {
    fail("Figura do capítulo 3 ausente ou com numeração incorreta: ", id)
  }
  if (!grepl(paste0("@", id), chapter_three_source, fixed = TRUE) ||
      !grepl(paste0("@", id), figure_list, fixed = TRUE)) {
    fail("Figura do capítulo 3 sem chamada ou ausente da lista: ", id)
  }
}
if (grepl("ARTE CAP3-", gsub("(?s)<!--.*?-->", "", chapter_three_html, perl = TRUE), fixed = TRUE)) {
  fail("Instruções de produção do capítulo 3 aparecem no conteúdo renderizado.")
}

chapter_four_path <- "chapters/part-1/03-espaco-tempo-qualidade.qmd"
chapter_four_source <- paste(readLines(chapter_four_path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
chapter_four_html <- paste(readLines(
  file.path(html_root, sub("[.]qmd$", ".html", chapter_four_path)),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
# O mapa empírico permanece na posição 4.2, entre as duas primeiras artes.
chapter_four_numbers <- c(1L, 3L, 4L, 5L, 6L, 7L, 8L)
for (i in seq_along(chapter_four_art)) {
  art <- paste0("arte-cap4-", chapter_four_art[[i]], ".svg")
  id <- chapter_four_ids[[i]]
  check_file(file.path(html_root, "assets/figures", art))
  if (!grepl(paste0('id="', id, '"'), chapter_four_html, fixed = TRUE) ||
      !grepl(paste0("Figura&nbsp;4.", chapter_four_numbers[[i]], ":"), chapter_four_html, fixed = TRUE)) {
    fail("Figura do capítulo 4 ausente ou com numeração incorreta: ", id)
  }
  if (!grepl(paste0("@", id), chapter_four_source, fixed = TRUE) ||
      !grepl(paste0("@", id), figure_list, fixed = TRUE)) {
    fail("Figura do capítulo 4 sem chamada ou ausente da lista: ", id)
  }
}
if (!grepl('id="fig-mudanca-suporte"', chapter_four_html, fixed = TRUE) ||
    !grepl("Figura&nbsp;4.2:", chapter_four_html, fixed = TRUE)) {
  fail("O mapa empírico do capítulo 4 está ausente ou foi renumerado incorretamente.")
}
if (grepl("ARTE CAP4-", gsub("(?s)<!--.*?-->", "", chapter_four_html, perl = TRUE), fixed = TRUE)) {
  fail("Instruções de produção do capítulo 4 aparecem no conteúdo renderizado.")
}

chapter_five_path <- "chapters/part-1/04-fontes-fichas.qmd"
chapter_five_source <- paste(readLines(chapter_five_path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
chapter_five_html <- paste(readLines(
  file.path(html_root, sub("[.]qmd$", ".html", chapter_five_path)),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
chapter_five_assets <- c(paste0("arte-cap5-", chapter_five_art, ".svg"), "arte-cap3-05-ficha.svg")
for (i in seq_along(chapter_five_assets)) {
  art <- chapter_five_assets[[i]]
  id <- c(chapter_five_ids, "fig-ficha-ripsa-livro")[[i]]
  check_file(file.path(html_root, "assets/figures", art))
  if (!grepl(paste0('id="', id, '"'), chapter_five_html, fixed = TRUE) ||
      !grepl(paste0("Figura&nbsp;5.", i, ":"), chapter_five_html, fixed = TRUE) ||
      !grepl(paste0("@", id), chapter_five_source, fixed = TRUE) ||
      !grepl(paste0("@", id), figure_list, fixed = TRUE)) {
    fail("Figura do capítulo 5 ausente, sem chamada ou com numeração incorreta: ", id)
  }
}
for (id in c("sec-ficha-ripsa", "qua-campos-fqi-ripsa", "fig-ficha-ripsa-livro")) {
  if (grepl(paste0("{#", id), chapter_three_source, fixed = TRUE) ||
      !grepl(paste0('id="', id, '"'), chapter_five_html, fixed = TRUE)) {
    fail("Transferência da seção RIPSA incompleta: ", id)
  }
}
if (grepl("ARTE CAP5-", gsub("(?s)<!--.*?-->", "", chapter_five_html, perl = TRUE), fixed = TRUE)) {
  fail("Instruções de produção do capítulo 5 aparecem no conteúdo renderizado.")
}

references_html_path <- file.path(html_root, "backmatter/referencias.html")
check_file(references_html_path)
references_html <- paste(readLines(references_html_path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
missing_entries <- unique(citations)[!vapply(unique(citations), function(key) {
  grepl(paste0('id="ref-', key, '"'), references_html, fixed = TRUE)
}, logical(1L))]
if (length(missing_entries)) fail("Obras citadas ausentes da bibliografia central: ", paste(missing_entries, collapse = ", "))

broken <- character()
broken_anchors <- character()
unresolved_html <- character()
for (path in html_files) {
  html <- paste(readLines(path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
  if (!identical(path, references_html_path)) {
    refs_tags <- regmatches(html, gregexpr('<div[^>]*id="refs"[^>]*>', html, perl = TRUE))[[1L]]
    if (length(refs_tags) && !identical(refs_tags, "-1") && any(!grepl("display: none", refs_tags, fixed = TRUE))) {
      fail("Bibliografia visível fora da página central: ", path)
    }
  }
  # Scripts da galeria contêm templates de links; não são âncoras do documento.
  link_html <- gsub("(?is)<script\\b[^>]*>.*?</script\\s*>", "", html, perl = TRUE)
  link_html <- gsub("(?s)<!--.*?-->", "", link_html, perl = TRUE)
  hrefs <- regmatches(link_html, gregexpr('href="[^"]+"', link_html, perl = TRUE))[[1L]]
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
  "Projeto validado: 15 capítulos; ", indicator_count, " fichas; HTML com ",
  length(html_files), " páginas; links e âncoras íntegros; PDF presente."
)
