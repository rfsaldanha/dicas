#!/usr/bin/env Rscript

# Validação deliberadamente separada: depende de rede e pode ser afetada por
# bloqueios temporários, autenticação e limitação de requisições dos provedores.

files <- c(
  "references.bib",
  list.files("chapters", pattern = "\\.qmd$", recursive = TRUE, full.names = TRUE),
  list.files("frontmatter", pattern = "\\.qmd$", full.names = TRUE),
  list.files("backmatter", pattern = "\\.qmd$", full.names = TRUE),
  list.files("indicators/data", pattern = "\\.ya?ml$", full.names = TRUE),
  "sources/data/sources.yml"
)
text <- paste(vapply(files, function(path) {
  paste(readLines(path, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
}, character(1L)), collapse = "\n")
matches <- regmatches(text, gregexpr("https?://[^[:space:]<>\\]{}\\\"']+", text, perl = TRUE))[[1L]]
normalize_url <- function(url) {
  url <- sub("[.,;:]$", "", url)
  while (
    grepl("\\)$", url) &&
      lengths(regmatches(url, gregexpr("\\(", url))) < lengths(regmatches(url, gregexpr("\\)", url)))
  ) {
    url <- sub("\\)$", "", url)
  }
  url
}
urls <- sort(unique(vapply(matches, normalize_url, character(1L))))

check_url <- function(url) {
  result <- system2(
    "curl",
    c("-L", "-sS", "--max-time", "25", "--retry", "1", "-o", "/dev/null", "-w", "%{http_code}", shQuote(url)),
    stdout = TRUE,
    stderr = TRUE
  )
  status <- attr(result, "status")
  code <- suppressWarnings(as.integer(tail(result, 1L)))
  code_text <- ifelse(is.na(code), "erro", as.character(code))
  state <- if (is.null(status) && !is.na(code) && (code < 400L || code %in% c(401L, 403L, 405L, 429L))) {
    "ok"
  } else if (is.na(code) || code == 0L) {
    "indeterminado"
  } else {
    "falha"
  }
  c(url = url, code = code_text, state = state)
}

detected_cores <- parallel::detectCores()
workers <- if (is.na(detected_cores)) 2L else min(8L, detected_cores)
results <- parallel::mclapply(urls, check_url, mc.cores = workers)
indeterminate <- vapply(results, function(x) x[["state"]] == "indeterminado", logical(1L))
if (any(indeterminate)) {
  details <- vapply(results[indeterminate], function(x) paste0(x[["code"]], " ", x[["url"]]), character(1L))
  warning("Links sem resposta conclusiva; verificar manualmente:\n", paste(details, collapse = "\n"), call. = FALSE)
}
failed <- vapply(results, function(x) x[["state"]] == "falha", logical(1L))
if (any(failed)) {
  details <- vapply(results[failed], function(x) paste0(x[["code"]], " ", x[["url"]]), character(1L))
  stop("Links externos sem resposta aceitável:\n", paste(details, collapse = "\n"), call. = FALSE)
}
message("Links externos verificados: ", length(urls), ".")
