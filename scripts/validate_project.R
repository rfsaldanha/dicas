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
if (length(chapter_files) != 25L) {
  fail("Esperados 25 capítulos em chapters/; encontrados ", length(chapter_files), ".")
}

required <- c(
  "_quarto.yml", "_quarto-web.yml", "_quarto-print.yml", "index.qmd",
  "README.md", "CONTRIBUTING.md", "references.bib",
  "frontmatter/ficha-tecnica.qmd", "frontmatter/bem-vindo.qmd", "includes/bem-vindo.qmd",
  "frontmatter/apresentacao.qmd", "frontmatter/prefacio.qmd",
  "frontmatter/agradecimentos.qmd", "frontmatter/siglas.qmd",
  "frontmatter/sumario.qmd", "frontmatter/como-usar.qmd",
  "backmatter/referencias.qmd", "backmatter/glossario.qmd",
  "backmatter/indice-indicadores.qmd", "backmatter/indice-fontes.qmd",
  "backmatter/indice-instituicoes.qmd", "backmatter/apendice-metodologico.qmd",
  "backmatter/apendice-estacoes.qmd", "scripts/build_estacoes_data.py",
  "scripts/build_estacoes_art.py", "assets/figures/estacoes-manifest.json",
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
  "assets/figures/arte-cap1-03-v3.png",
  "assets/figures/arte-cap1-03-v3.prompt.txt",
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
chapter_four_manifest <- yaml::read_yaml("assets/figures/arte-cap4-manifest.json")
chapter_four_art <- vapply(chapter_four_manifest, function(a) paste0(a$number, "-", a$slug), character(1L))
chapter_four_ids <- vapply(chapter_four_manifest, function(a) a$id, character(1L))
if (length(chapter_four_art) != 11L) fail("Esperadas onze composições no manifesto do capítulo 4.")
required <- c(required, "scripts/build_cap4_art.py", "scripts/cap4_panels.py",
  "scripts/check_cap4_timezones.py", "data-raw/figures/conversoes-utc-cap4.json",
  "assets/figures/arte-cap4-manifest.json",
  unlist(lapply(chapter_four_manifest, function(a) {
    paste0("assets/figures/", unlist(a[c("svg", "print", "prompt", "source", "source_prompt", "refinement_prompt")]))
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
chapter_six_manifest <- yaml::read_yaml("assets/figures/arte-cap6-manifest.json")
chapter_six_art <- vapply(chapter_six_manifest, function(a) a$svg, character(1L))
chapter_six_ids <- vapply(chapter_six_manifest, function(a) a$id, character(1L))
required <- c(required, "scripts/build_cap6_art.py", "assets/figures/arte-cap6-manifest.json",
  unlist(lapply(chapter_six_manifest, function(a) {
    paste0("assets/figures/", unlist(a[c("svg", "print", "prompt", "source")]))
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
# Os capítulos 11 e 12 usam composições SVG; permanecem quatro Mermaid na Parte III.
if (length(mermaid_blocks) != 4L) {
  fail("Esperados 4 diagramas Mermaid; encontrados ", length(mermaid_blocks), ".")
}
missing_alt <- mermaid_blocks[!grepl("(?m)^%%\\| fig-alt:", mermaid_blocks, perl = TRUE)]
if (length(missing_alt)) fail("Há diagrama Mermaid sem texto alternativo.")

framebox_lines <- grep("::: \\{\\.framebox\\}", source_text, value = TRUE)
if (length(framebox_lines)) {
  fail("Há placeholders de arte remanescentes nos capítulos.")
}

chapter_seven_manifest <- yaml::read_yaml("assets/figures/arte-cap7-manifest.json")
chapter_seven_art <- vapply(chapter_seven_manifest, function(a) a$svg, character(1L))
chapter_nine_manifest <- yaml::read_yaml("assets/figures/arte-cap9-manifest.json")
if (length(chapter_nine_manifest) != 11L) fail("O capítulo 9 deve ter onze figuras no manifesto.")
chapter_nine_art <- vapply(chapter_nine_manifest, function(a) a$svg, character(1L))
illustration_paths <- c(
  paste0("assets/figures/", chapter_nine_art),
  paste0("assets/figures/", chapter_seven_art),
  paste0("assets/figures/", chapter_six_art),
  paste0("assets/figures/arte-cap5-", chapter_five_art, ".svg"),
  paste0("assets/figures/arte-cap4-", chapter_four_art, ".svg"),
  paste0("assets/figures/arte-cap3-", chapter_three_art, ".svg"),
  "assets/figures/mudanca-suporte.svg",
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
# Uma citação narrativa pode terminar em ponto de frase; preserve chaves
# existentes e remova essa pontuação somente quando a chave resultante existe.
citations <- vapply(citations, function(key) {
  candidate <- sub("[.]+$", "", key)
  if (!(key %in% bib_keys) && candidate %in% bib_keys) candidate else key
}, character(1L))
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
if (!grepl("CLI-TEM-01", search_index, fixed = TRUE) ||
    !grepl("17-fichas-temperatura-condicoes-termicas.html#sec-cli-tem-01", search_index, fixed = TRUE)) {
  fail("A ficha CLI-TEM-01 não foi localizada no índice de busca.")
}

html_files <- list.files(html_root, pattern = "\\.html$", recursive = TRUE, full.names = TRUE)
chapter_one_html <- paste(readLines(
  file.path(html_root, "chapters/part-1/01-clima-ambiente-saude.html"),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
chapter_one_source <- paste(readLines(
  "chapters/part-1/01-clima-ambiente-saude.qmd", warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
chapter_one_ids <- c(
  "fig-tempo-clima-ambiente", "fig-cadeia-risco", "fig-quadrantes-impacto",
  "fig-curvas-impacto-desastres", "fig-trajetorias-inundacao", "fig-venn-risco",
  "fig-caracterizacao-perigo", "fig-exposicao-calor-dia", "fig-medida-exposicao-dose",
  "fig-territorios-contraste", "fig-desigualdades-risco", "fig-justica-ambiental-climatica"
)
chapter_one_assets <- c(
  "07-tempo-clima-ambiente", "01-diagrama", "08-quadrantes", "09-curvas-impacto",
  "02-trajetorias", "10-venn-risco", "11-perigos", "03-exposicao", "04-dose",
  "05-territorios", "12-desigualdades", "06-justica"
)
figure_list <- paste(readLines("backmatter/lista-figuras.qmd", warn = FALSE, encoding = "UTF-8"), collapse = "\n")
for (i in seq_along(chapter_one_ids)) {
  id <- chapter_one_ids[[i]]
  asset <- paste0("arte-cap1-", chapter_one_assets[[i]])
  for (extension in c(".svg", "-print.png")) check_file(paste0("assets/figures/", asset, extension))
  check_file(paste0(html_root, "/assets/figures/", asset, ".svg"))
  if (!grepl(paste0('id="', id, '"'), chapter_one_html, fixed = TRUE) ||
      !grepl(paste0("Figura&nbsp;1.", i, ":"), chapter_one_html, fixed = TRUE) ||
      !grepl(paste0("@", id), chapter_one_source, fixed = TRUE) ||
      !grepl(paste0("@", id), figure_list, fixed = TRUE)) {
    fail("Figura do capítulo 1 ausente, sem chamada ou com numeração incorreta: ", id)
  }
}
# A figura consolidada segue o parágrafo inicial e substitui o quadro separado.
section <- strsplit(chapter_one_source, "### Efeitos diretos, indiretos e trajetórias no tempo", fixed = TRUE)[[1L]][[2L]]
section <- sub("(?s)<!--.*?-->", "", section, perl = TRUE)
paragraphs <- strsplit(trimws(section), "\n\n", fixed = TRUE)[[1L]]
if (!grepl("fig-quadrantes-impacto", paragraphs[[3L]], fixed = TRUE) ||
    grepl("qua-trajetorias-impacto", chapter_one_source, fixed = TRUE) ||
    grepl("qua-trajetorias-impacto", chapter_one_html, fixed = TRUE) ||
    any(grepl("qua-trajetorias-impacto",
              readLines("backmatter/lista-tabelas.qmd", warn = FALSE, encoding = "UTF-8"),
              fixed = TRUE))) {
  fail("A figura de quadrantes deve consolidar os exemplos e substituir o antigo Quadro 1.3.")
}
chapter_two_html <- paste(readLines(
  file.path(html_root, "chapters/part-1/02-mudanca-climatica-resposta-sus.html"),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
# A arte 07-grades integra o capítulo 3; o inventário de produção permanece completo.
chapter_two_display_art <- chapter_two_art[chapter_two_art != "07-grades"]
for (i in seq_along(chapter_two_display_art)) {
  art <- paste0("arte-cap2-", chapter_two_display_art[[i]], ".svg")
  check_file(file.path(html_root, "assets/figures", art))
  image_pattern <- paste0('<img[^>]+src="[^"]*', sub("[.]svg$", "[.]svg", art), '"')
  if (!grepl(image_pattern, chapter_two_html, perl = TRUE)) {
    fail("A aquarela da Figura 2.", i, " não foi incorporada ao capítulo 2.")
  }
}
if (grepl('id="sec-grades-planejamento-sus"', chapter_two_html, fixed = TRUE) ||
    grepl('id="fig-dados-grade-sus"', chapter_two_html, fixed = TRUE)) {
  fail("A seção sobre dados em grade ou sua figura ainda está no capítulo 2.")
}
chapter_three_path <- "chapters/part-1/03-dados-variaveis-indices-indicadores.qmd"
chapter_three_source <- paste(readLines(chapter_three_path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
chapter_three_html <- paste(readLines(
  file.path(html_root, sub("[.]qmd$", ".html", chapter_three_path)),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
figure_list <- paste(readLines("backmatter/lista-figuras.qmd", warn = FALSE, encoding = "UTF-8"), collapse = "\n")
# A arte 05-ficha está no capítulo 5; CAP2-07 ocupa a posição 3.4.
# Os nomes de produção permanecem independentes da ordem editorial.
chapter_three_order <- which(chapter_three_ids != "fig-ficha-ripsa-livro")
chapter_three_display_ids <- append(
  chapter_three_ids[chapter_three_order], "fig-dados-grade-sus", after = 3L
)
chapter_three_display_art <- append(
  paste0("arte-cap3-", chapter_three_art[chapter_three_order], ".svg"),
  "arte-cap2-07-grades.svg", after = 3L
)
for (i in seq_along(chapter_three_display_ids)) {
  art <- chapter_three_display_art[[i]]
  id <- chapter_three_display_ids[[i]]
  check_file(file.path(html_root, "assets/figures", art))
  caption_pattern <- paste0('(?s)<figcaption[^>]+id="', id, '-caption-[^"]+"[^>]*>.*?</figcaption>')
  caption <- regmatches(chapter_three_html, regexpr(caption_pattern, chapter_three_html, perl = TRUE))
  image_pattern <- paste0('<img[^>]+src="[^"]*', sub("[.]svg$", "[.]svg", art), '"')
  if (!grepl(paste0('id="', id, '"'), chapter_three_html, fixed = TRUE) ||
      length(caption) != 1L ||
      !grepl(paste0("Figura&nbsp;3.", i, ":"), caption, fixed = TRUE) ||
      !grepl(image_pattern, chapter_three_html, perl = TRUE)) {
    fail("Figura do capítulo 3 ausente ou com numeração incorreta: ", id)
  }
  if (!grepl(paste0("@", id), chapter_three_source, fixed = TRUE) ||
      !grepl(paste0("@", id), figure_list, fixed = TRUE)) {
    fail("Figura do capítulo 3 sem chamada ou ausente da lista: ", id)
  }
}
if (!grepl('<section id="sec-grades-planejamento-sus"[^>]*data-number="3[.]2[.]5"',
           chapter_three_html, perl = TRUE)) {
  fail("A seção sobre dados em grade não ocupa a posição 3.2.5.")
}
if (grepl("ARTE CAP[23]-", gsub("(?s)<!--.*?-->", "", chapter_three_html, perl = TRUE))) {
  fail("Instruções de produção do capítulo 3 aparecem no conteúdo renderizado.")
}

chapter_four_path <- "chapters/part-1/04-espaco-tempo-qualidade.qmd"
chapter_four_source <- paste(readLines(chapter_four_path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
chapter_four_html <- paste(readLines(
  file.path(html_root, sub("[.]qmd$", ".html", chapter_four_path)),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
# As composições têm códigos de produção; a numeração segue a ordem no texto.
chapter_four_numbers <- c(1L, 5L, 6L, 7L, 10L, 11L, 12L, 2L, 4L, 8L, 9L)
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
    !grepl("Figura&nbsp;4.3:", chapter_four_html, fixed = TRUE)) {
  fail("O mapa empírico do capítulo 4 está ausente ou foi renumerado incorretamente.")
}
for (a in chapter_four_manifest) {
  svg <- paste(readLines(file.path("assets/figures", a$svg), warn = FALSE), collapse = "\n")
  raster <- is.null(a$kind) || a$kind != "vector"
  if (grepl("<image ", svg, fixed = TRUE) != raster) {
    fail("Tipo de composição e presença de aquarela divergentes: ", a$svg)
  }
}
figure_count <- lengths(regmatches(chapter_four_source,
  gregexpr("(?m)^!\\[.*?\\]\\([^\n]+\\)\\{#fig-", chapter_four_source, perl = TRUE)))
if (figure_count != 12L) fail("O capítulo 4 deve incorporar doze figuras.")
if (!grepl('id="tbl-conversoes-utc"', chapter_four_html, fixed = TRUE) ||
    !grepl("@tbl-conversoes-utc", paste(readLines("backmatter/lista-tabelas.qmd"), collapse="\n"), fixed=TRUE)) {
  fail("Tabela de UTC ausente do capítulo ou da lista.")
}
if (system2("python3", "scripts/check_cap4_timezones.py") != 0L) fail("Conversões de UTC inconsistentes.")
if (grepl("ARTE CAP4-", gsub("(?s)<!--.*?-->", "", chapter_four_html, perl = TRUE), fixed = TRUE)) {
  fail("Instruções de produção do capítulo 4 aparecem no conteúdo renderizado.")
}

chapter_five_path <- "chapters/part-1/05-fontes-fichas.qmd"
chapter_five_source <- paste(readLines(chapter_five_path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
chapter_five_html <- paste(readLines(
  file.path(html_root, sub("[.]qmd$", ".html", chapter_five_path)),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
chapter_five_assets <- append(paste0("arte-cap5-", chapter_five_art, ".svg"), "arte-cap3-05-ficha.svg", after = 2L)
chapter_five_display_ids <- append(chapter_five_ids, "fig-ficha-ripsa-livro", after = 2L)
for (i in seq_along(chapter_five_assets)) {
  art <- chapter_five_assets[[i]]
  id <- chapter_five_display_ids[[i]]
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

chapter_six_path <- "chapters/part-1/06-indicador-decisao.qmd"
chapter_six_source <- paste(readLines(chapter_six_path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
chapter_six_html <- paste(readLines(
  file.path(html_root, sub("[.]qmd$", ".html", chapter_six_path)),
  warn = FALSE, encoding = "UTF-8"
), collapse = "\n")
for (i in seq_along(chapter_six_art)) {
  art <- chapter_six_art[[i]]
  id <- chapter_six_ids[[i]]
  check_file(file.path(html_root, "assets/figures", art))
  if (!grepl(paste0('id="', id, '"'), chapter_six_html, fixed = TRUE) ||
      !grepl(paste0("Figura&nbsp;6.", i, ":"), chapter_six_html, fixed = TRUE) ||
      !grepl(paste0("@", id), chapter_six_source, fixed = TRUE) ||
      !grepl(paste0("@", id), figure_list, fixed = TRUE)) {
    fail("Figura do capítulo 6 ausente, sem chamada ou com numeração incorreta: ", id)
  }
}
if (grepl("ARTE CAP6-", gsub("(?s)<!--.*?-->", "", chapter_six_html, perl = TRUE), fixed = TRUE)) {
  fail("Instruções de produção do capítulo 6 aparecem no conteúdo renderizado.")
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
    if (grepl('id="bibliography"|id="toc-bibliography"', html)) {
      fail("Cabeçalho automático de bibliografia fora da página central: ", path)
    }
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

# O apêndice B publica observações reais: conferir derivados contra os originais.
if (system2("python3", c("scripts/build_estacoes_data.py", "--check")) != 0L) {
  fail("Os exemplos observados do apêndice B divergem dos arquivos oficiais preservados.")
}
appendix_html <- paste(readLines("_output/web/backmatter/apendice-estacoes.html", warn = FALSE), collapse = "\n")
appendix_art <- yaml::read_yaml("assets/figures/estacoes-manifest.json")
if (length(appendix_art) != 7L) fail("Esperadas sete figuras no apêndice B.")
for (a in appendix_art) {
  check_file(file.path("assets/figures", a$svg))
  check_file(file.path("assets/figures", a$print))
  if (!grepl(a$svg, appendix_html, fixed = TRUE)) fail("Figura ausente no HTML do apêndice B: ", a$svg)
}
for (profile in c("_quarto-web.yml", "_quarto-print.yml")) {
  config <- yaml::read_yaml(profile)
  if (!identical(unlist(config$book$appendices), c("backmatter/apendice-metodologico.qmd", "backmatter/apendice-estacoes.qmd"))) {
    fail("Ordem dos apêndices A/B incorreta: ", profile)
  }
}

if (system2("python3", "scripts/test_part_iii.py") != 0L) {
  fail("Falha nos testes de aceite da especificação da Parte III.")
}

source("scripts/validate_book_structure.R")
validate_book_structure(root, rendered = TRUE)
if (system2("python3", "scripts/check_book_refs.py") != 0L) {
  fail("Falha na validação das remissões automáticas.")
}
if (system2("python3", c("scripts/check_cap7.py", "--rendered")) != 0L) {
  fail("Integração editorial do capítulo 7 inválida.")
}

if (system2("python3", c("scripts/check_cap8.py", "--rendered")) != 0L) {
  fail("Integração editorial do capítulo 8 inválida.")
}

if (system2("python3", c("scripts/check_cap10.py", "--rendered")) != 0L) {
  fail("Integração editorial do capítulo 10 inválida.")
}

if (system2("python3", c("scripts/check_cap12.py", "--rendered")) != 0L) {
  fail("Falha na integração editorial do capítulo 12.")
}

if (system2("python3", c("scripts/check_cap16.py", "--rendered")) != 0L) {
  fail("Falha na integração das ilustrações do capítulo 16.")
}

indicator_count <- length(list.files("indicators/includes", pattern = "\\.qmd$"))
message(
  "Projeto validado: quatro partes; 25 capítulos; ", indicator_count, " fichas; HTML com ",
  length(html_files), " páginas; links e âncoras íntegros; PDF presente."
)

if (system2("python3", c("scripts/check_cap11.py", "--rendered")) != 0L) {
  fail("Falha na integração editorial do capítulo 11.")
}
