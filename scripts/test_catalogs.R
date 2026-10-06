#!/usr/bin/env Rscript

# Testa a geração em uma cópia temporária, sem tocar nos dados do livro.
main <- function() {
  script_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  script_path <- sub("^--file=", "", script_arg[[1L]])
  root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
  fixture <- tempfile("dicas-catalogs-")
  dir.create(fixture)
  on.exit(unlink(fixture, recursive = TRUE), add = TRUE)
  check <- function(ok, message) {
    if (!isTRUE(ok)) stop(message, call. = FALSE)
  }
  for (path in c("scripts/build_catalogs.R", "_quarto-web.yml", "_quarto-print.yml",
                 "indicators/data", "sources/data", "chapters", "backmatter", "scripts/validate_book_structure.R")) {
    target <- file.path(fixture, path)
    dir.create(dirname(target), recursive = TRUE, showWarnings = FALSE)
    source <- file.path(root, path)
    check(file.copy(source, dirname(target), recursive = dir.exists(source)),
          paste("Falha ao preparar", path))
  }
  run <- function(success = TRUE) {
    output <- suppressWarnings(system2(
      file.path(R.home("bin"), "Rscript"),
      shQuote(file.path(fixture, "scripts/build_catalogs.R")),
      stdout = TRUE, stderr = TRUE
    ))
    status <- attr(output, "status")
    ok <- is.null(status) || status == 0L
    check(identical(ok, success), paste(output, collapse = "\n"))
  }
  snapshot <- function() {
    files <- sort(c(
      list.files(file.path(fixture, "indicators/includes"), full.names = TRUE),
      file.path(fixture, "indicators", c("generated-index-alphabetical.qmd", "generated-list.qmd")),
      list.files(file.path(fixture, "sources/generated"), full.names = TRUE)
    ))
    data.frame(path = files, hash = unname(tools::md5sum(files)),
               mtime = as.numeric(file.info(files)$mtime), stringsAsFactors = FALSE)
  }

  run()
  source(file.path(root, "scripts/validate_book_structure.R"))
  validate_book_structure(fixture)
  initial <- snapshot()
  check(nrow(initial) == 66L, "A geração inicial deve produzir 62 fichas e quatro catálogos.")
  # Datas antigas tornam uma regravação detectável mesmo em discos de baixa resolução temporal.
  Sys.setFileTime(initial$path, as.POSIXct("2001-01-01", tz = "UTC"))
  before <- snapshot()
  run()
  check(identical(before, snapshot()), "Conteúdo idêntico foi regravado: hashes e datas devem ser preservados.")

  input <- sort(list.files(file.path(fixture, "indicators/data"), full.names = TRUE))[1L]
  document <- yaml::read_yaml(input)
  grouped <- !is.null(document$indicators)
  entry <- if (grouped) document$indicators[[1L]] else document
  entry$titulo_resumido <- paste0(entry$titulo_resumido, " — teste de atualização")
  if (grouped) document$indicators[[1L]] <- entry else document <- entry
  yaml::write_yaml(document, input)
  run()
  after <- snapshot()
  changed <- after$hash != before$hash
  expected <- file.path(fixture, "indicators", c(
    paste0("includes/", tolower(entry$codigo), ".qmd"),
    "generated-index-alphabetical.qmd", "generated-list.qmd"
  ))
  check(setequal(after$path[changed], expected), "A edição de uma ficha deve atualizar apenas ela e os dois índices de indicadores.")
  check(identical(before[!changed, ], after[!changed, ]), "Arquivos não afetados pela edição foram regravados.")

  unlink(expected[1L])
  run()
  restored <- snapshot()
  check(identical(after$hash, restored$hash), "Uma ficha ausente não foi regenerada corretamente.")
  retained <- after$path != expected[1L]
  check(identical(after[retained, ], restored[retained, ]), "A reposição de uma ficha regravou outros arquivos.")

  valid_destination <- entry$capitulo_fichas
  for (invalid in c(entry$capitulo, "chapters/part-4/ausente.qmd",
                    "chapters/part-4/16-fichas-temperatura-condicoes-termicas.qmd")) {
    entry$capitulo_fichas <- invalid
    if (grouped) document$indicators[[1L]] <- entry else document <- entry
    yaml::write_yaml(document, input)
    run(success = FALSE)
    check(identical(restored, snapshot()), "Destino inválido alterou os arquivos gerados.")
  }
  entry$capitulo_fichas <- valid_destination
  entry$codigo <- "codigo-invalido"
  if (grouped) document$indicators[[1L]] <- entry else document <- entry
  yaml::write_yaml(document, input)
  run(success = FALSE)
  check(identical(restored, snapshot()), "Dados inválidos alteraram os arquivos gerados.")
  message("Catálogos: geração inicial, preservação de datas, atualização seletiva, reposição e validação verificadas.")
}

main()
