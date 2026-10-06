# Invariantes editoriais compartilhadas pela validação do livro e pelos testes.
validate_book_structure <- function(root = ".", rendered = FALSE) {
  check <- function(ok, message) {
    if (!isTRUE(ok)) stop(message, call. = FALSE)
  }
  read_text <- function(path) paste(readLines(file.path(root, path), warn = FALSE, encoding = "UTF-8"), collapse = "\n")
  configs <- lapply(c("_quarto-web.yml", "_quarto-print.yml"), function(p) yaml::read_yaml(file.path(root, p)))
  parts <- lapply(configs, function(config) Filter(function(x) is.list(x) && !is.null(x$part), config$book$chapters))
  expected_parts <- c("Parte I — Fundamentos e métodos", "Parte II — Dados e indicadores temáticos",
    "Parte III — Indicadores integrados de clima, ambiente e saúde", "Parte IV — Fichas de indicadores e fontes de dados")
  for (i in seq_along(configs)) {
    check(identical(vapply(parts[[i]], `[[`, character(1L), "part"), expected_parts), "O livro deve conter as quatro partes aprovadas.")
    check(identical(vapply(parts[[i]][1:3], function(x) length(x$chapters), integer(1L)), c(6L, 6L, 3L)), "Ordem ou quantidade de capítulos das partes I–III incorreta.")
    last_part <- unlist(parts[[i]][[4]]$chapters, use.names = FALSE)
    check(length(last_part) == 12L && identical(last_part[c(1, 2, 12)], c("backmatter/lista-fichas.qmd", "backmatter/indice-indicadores.qmd", "backmatter/indice-fontes.qmd")), "Índices e catálogo devem abrir e encerrar a Parte IV.")
    top <- unlist(Filter(is.character, configs[[i]]$book$chapters), use.names = FALSE)
    sequence <- c("frontmatter/siglas.qmd", "backmatter/lista-figuras.qmd", "backmatter/lista-tabelas.qmd", "frontmatter/sumario.qmd")
    pos <- match(sequence, top)
    check(!anyNA(pos) && all(diff(pos) == 1L), "Listas de figuras e quadros devem ficar entre siglas e sumário.")
    check(identical(tail(top, 2L), c("backmatter/glossario.qmd", "backmatter/referencias.qmd")), "Glossário e referências devem ser entradas independentes ao final.")
    check(identical(tail(configs[[i]]$book$chapters, 2L), as.list(c("backmatter/glossario.qmd", "backmatter/referencias.qmd"))), "Glossário e referências devem ficar após a Parte IV.")
    check(identical(unlist(configs[[i]]$book$appendices), c("backmatter/apendice-metodologico.qmd", "backmatter/apendice-estacoes.qmd")), "Ordem dos apêndices A/B incorreta.")
  }
  check(identical(parts[[1]], parts[[2]]), "As partes devem ter a mesma composição nas duas edições.")
  paths <- unlist(lapply(parts[[1]], `[[`, "chapters"), use.names = FALSE)
  chapter_paths <- paths[startsWith(paths, "chapters/")]
  check(length(chapter_paths) == 24L && !anyDuplicated(chapter_paths), "Esperados 24 capítulos únicos.")
  context_paths <- chapter_paths[7:15]
  card_paths <- chapter_paths[16:24]
  documents <- lapply(sort(list.files(file.path(root, "indicators/data"), pattern = "\\.yml$", full.names = TRUE)), yaml::read_yaml)
  indicators <- unlist(lapply(documents, function(x) if (is.null(x$indicators)) list(x) else x$indicators), recursive = FALSE)
  codes <- vapply(indicators, `[[`, character(1L), "codigo")
  check(length(codes) == 62L && !anyDuplicated(codes), "Esperadas 62 fichas com códigos únicos.")
  check(length(yaml::read_yaml(file.path(root, "sources/data/sources.yml"))) == 29L, "Esperadas 29 fontes cadastradas.")
  included <- unlist(lapply(card_paths, function(path) {
    text <- read_text(path)
    check(grepl("(?m)^# Fichas — ", text, perl = TRUE), paste("Título de capítulo de fichas inválido:", path))
    hits <- regmatches(text, gregexpr("indicators/includes/[a-z0-9-]+\\.qmd", text))[[1L]]
    sub("\\.qmd$", "", sub("indicators/includes/", "", hits))
  }), use.names = FALSE)
  check(length(included) == length(codes) && !anyDuplicated(included) && setequal(included, tolower(codes)), "Fichas ausentes ou duplicadas nos capítulos da Parte IV.")
  for (path in context_paths) {
    check(!grepl("include .*indicators/includes/", read_text(path)), paste("Ficha completa ainda incorporada ao capítulo de contexto:", path))
  }
  expected_counts <- c(21L, 6L, 4L, 6L, 4L, 4L, 3L, 7L, 7L)
  counts <- tabulate(match(vapply(indicators, `[[`, character(1L), "capitulo_fichas"), card_paths), nbins = 9L)
  check(identical(counts, expected_counts), "Distribuição temática das fichas incorreta.")
  for (x in indicators) {
    slug <- tolower(x$codigo)
    index <- match(x$capitulo, context_paths)
    check(!is.na(index) && identical(x$capitulo_fichas, card_paths[index]), paste("Contexto e destino incompatíveis:", x$codigo))
    context <- read_text(x$capitulo)
    check(grepl(paste0('`<span id="sec-', slug, '"></span>`{=html}'), context, fixed = TRUE), paste("Âncora de compatibilidade ausente:", x$codigo))
    target <- paste0(x$capitulo_fichas, "#sec-", slug)
    check(grepl(target, context, fixed = TRUE), paste("Remissão à ficha ausente:", x$codigo))
    rows <- grep("^\\|", strsplit(context, "\n", fixed = TRUE)[[1L]], value = TRUE)
    check(any(grepl(target, rows, fixed = TRUE)), paste("Ficha ausente do quadro de orientação:", x$codigo))
    ficha <- read_text(paste0("indicators/includes/", slug, ".qmd"))
    check(grepl(paste0("](../../", x$capitulo, "#sec-"), ficha, fixed = TRUE), paste("Retorno ao contexto ausente:", x$codigo))
    check(grepl(paste0("includes/", slug, ".qmd"), read_text(x$capitulo_fichas), fixed = TRUE), paste("Ficha incorporada em destino incorreto:", x$codigo))
    if (rendered) {
      context_html <- read_text(file.path("_output/web", sub("qmd$", "html", x$capitulo)))
      card_html <- read_text(file.path("_output/web", sub("qmd$", "html", x$capitulo_fichas)))
      check(grepl(paste0('id="sec-', slug, '"'), context_html, fixed = TRUE), paste("Link antigo não preservado:", x$codigo))
      check(grepl(paste0('id="sec-', slug, '"'), card_html, fixed = TRUE), paste("Ficha ausente do HTML:", x$codigo))
      check(!grepl('class="ficha-title', context_html, fixed = TRUE), paste("Ficha completa publicada no contexto:", x$codigo))
    }
  }
  index_lines <- strsplit(read_text("indicators/generated-index-alphabetical.qmd"), "\n", fixed = TRUE)[[1L]]
  index_rows <- grep("^\\| .* \\| \\[?[A-Z]{3}-[A-Z]{2,3}-[0-9]{2}", index_lines, value = TRUE)
  titles <- vapply(strsplit(index_rows, " | ", fixed = TRUE), function(x) sub("^\\| ", "", x[1]), character(1L))
  short <- vapply(indicators, `[[`, character(1L), "titulo_resumido")
  check(identical(titles, rep(short[order(tolower(short), method = "shell")], 2L)), "Índice deve usar títulos resumidos na mesma ordem em HTML e PDF.")
  check(grepl("include indice-instituicoes.qmd", read_text("backmatter/indice-fontes.qmd"), fixed = TRUE), "Instituições devem integrar o catálogo de fontes.")
  if (rendered) {
    home <- read_text("_output/web/index.html")
    check(!grepl("Elementos pós-textuais", home, fixed = TRUE), "A antiga parte ainda aparece na navegação.")
    check(!grepl('href="./backmatter/indice-instituicoes.html"', home, fixed = TRUE), "Instituições ainda aparecem como página independente.")
  }
  invisible(TRUE)
}
