#!/usr/bin/env Rscript

# Valida os metadados estruturados e gera páginas/índices consumidos pelo livro.
# Dependência deliberadamente única: pacote CRAN `yaml`.

script_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
script_path <- if (length(script_arg)) sub("^--file=", "", script_arg[[1L]]) else "scripts/build_catalogs.R"
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)

fail <- function(...) stop(paste0(...), call. = FALSE)
write_utf8 <- function(lines, path) {
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  writeLines(lines, path, useBytes = TRUE)
}
as_text <- function(value, fallback = "Não se aplica.") {
  if (is.null(value) || !length(value) || identical(value, "")) fallback else as.character(value)
}
as_list <- function(value) {
  if (is.null(value) || !length(value)) character() else as.character(unlist(value, use.names = FALSE))
}
md_list <- function(value) {
  items <- as_list(value)
  if (!length(items)) return("- Não se aplica.")
  paste0("- ", items)
}
yaml_files <- sort(list.files(
  file.path(root, "indicators", "data"),
  pattern = "\\.ya?ml$",
  full.names = TRUE
))

if (!requireNamespace("yaml", quietly = TRUE)) {
  fail("O pacote R 'yaml' é necessário. Instale-o com install.packages('yaml').")
}
if (!length(yaml_files)) fail("Nenhuma ficha encontrada em indicators/data.")

required_indicator <- c(
  "codigo", "denominacao", "tema", "definicao", "objetivo", "interpretacao",
  "usos", "limitacoes", "dimensoes", "metodo_calculo", "formula",
  "unidade_medida", "unidade_territorial", "resolucao_temporal",
  "fontes_primarias", "disponibilidade", "qualidade_incerteza",
  "comparabilidade", "relacao_saude", "aplicacao_gestao"
)

indicators <- lapply(yaml_files, yaml::read_yaml)
names(indicators) <- basename(yaml_files)
for (name in names(indicators)) {
  missing <- setdiff(required_indicator, names(indicators[[name]]))
  if (length(missing)) {
    fail("Campos obrigatórios ausentes em ", name, ": ", paste(missing, collapse = ", "), ".")
  }
}
codes <- vapply(indicators, function(x) as.character(x$codigo), character(1L))
if (anyDuplicated(codes)) fail("Códigos duplicados: ", paste(unique(codes[duplicated(codes)]), collapse = ", "), ".")
if (any(!grepl("^[A-Z]{3}-[A-Z]{2,3}-[0-9]{2}$", codes))) {
  fail("Código fora do padrão em: ", paste(names(indicators)[!grepl("^[A-Z]{3}-[A-Z]{2,3}-[0-9]{2}$", codes)], collapse = ", "), ".")
}

source_path <- file.path(root, "sources", "data", "sources.yml")
sources <- yaml::read_yaml(source_path)
required_source <- c(
  "id", "nome", "instituicao", "descricao", "temas", "variaveis",
  "cobertura_geografica", "resolucao_espacial", "resolucao_temporal",
  "periodo_disponivel", "atualizacao", "acesso", "url", "limitacoes",
  "ultima_verificacao", "indicadores"
)
for (i in seq_along(sources)) {
  missing <- setdiff(required_source, names(sources[[i]]))
  if (length(missing)) {
    fail("Campos obrigatórios ausentes na fonte ", i, ": ", paste(missing, collapse = ", "), ".")
  }
}
source_ids <- vapply(sources, function(x) as.character(x$id), character(1L))
if (anyDuplicated(source_ids)) fail("IDs de fontes duplicados.")
source_by_id <- setNames(sources, source_ids)

declared_source_ids <- unique(unlist(lapply(indicators, function(x) {
  c(as_list(x$fontes_primarias), as_list(x$fontes_secundarias))
}), use.names = FALSE))
unknown_sources <- setdiff(declared_source_ids, source_ids)
if (length(unknown_sources)) {
  fail("Fontes citadas nas fichas sem cadastro: ", paste(unknown_sources, collapse = ", "), ".")
}

field <- function(label, value) {
  c(paste0("**", label, ".**"), "", as_text(value), "")
}

for (indicator in indicators) {
  slug <- tolower(as.character(indicator$codigo))
  page <- c(
    paste0("# ", indicator$denominacao, " {#sec-", slug, " .unnumbered}"),
    "",
    "::: {.indicator-card}",
    paste0("**Código:** ", indicator$codigo, "  "),
    paste0("**Tema:** ", indicator$tema, "  "),
    paste0("**Dimensão:** ", paste(as_list(indicator$dimensoes), collapse = "; "), "  "),
    paste0("**Disponibilidade:** ", paste0("[", as_list(indicator$disponibilidade), "]{.availability}", collapse = " ")),
    ":::",
    "",
    "## Conceituação {.unnumbered}",
    "",
    as_text(indicator$definicao),
    "",
    "## Objetivo {.unnumbered}",
    "",
    as_text(indicator$objetivo),
    "",
    "## Interpretação {.unnumbered}",
    "",
    as_text(indicator$interpretacao),
    "",
    "## Usos {.unnumbered}",
    "",
    md_list(indicator$usos),
    "",
    "## Limitações {.unnumbered}",
    "",
    md_list(indicator$limitacoes),
    "",
    "## Método de cálculo {.unnumbered}",
    "",
    as_text(indicator$metodo_calculo),
    "",
    "$$",
    as_text(indicator$formula),
    "$$",
    "",
    "::: {.indicator-card}",
    field("Numerador", indicator$numerador),
    field("Denominador", indicator$denominador),
    field("Unidade de medida", indicator$unidade_medida),
    field("Categorias para análise", indicator$categorias_analise),
    field("Unidade territorial", indicator$unidade_territorial),
    field("Resolução espacial original", indicator$resolucao_espacial_original),
    field("Resolução temporal", indicator$resolucao_temporal),
    field("Período de referência", indicator$periodo_referencia),
    field("Limiar ou valor de referência", indicator$limiar_referencia),
    ":::",
    "",
    "## Fontes e disponibilidade {.unnumbered}",
    "",
    paste0(
      "**Fonte primária:** ",
      paste(vapply(as_list(indicator$fontes_primarias), function(id) source_by_id[[id]]$nome, character(1L)), collapse = "; "),
      "."
    ),
    "",
    paste0(
      "**Fonte secundária:** ",
      paste(vapply(as_list(indicator$fontes_secundarias), function(id) source_by_id[[id]]$nome, character(1L)), collapse = "; "),
      "."
    ),
    "",
    field("Instituição responsável", indicator$instituicao_responsavel),
    field("Cobertura geográfica", indicator$cobertura_geografica),
    field("Período disponível", indicator$periodo_disponivel),
    field("Periodicidade de atualização", indicator$periodicidade_atualizacao),
    field("Forma de acesso", indicator$forma_acesso),
    field("URL ou identificador persistente", indicator$url_persistente),
    field("Formato dos arquivos", indicator$formatos),
    field("Necessidade de processamento", indicator$necessidade_processamento),
    "## Qualidade, comparação e saúde {.unnumbered}",
    "",
    field("Qualidade e incerteza", indicator$qualidade_incerteza),
    field("Possibilidade de comparação", indicator$comparabilidade),
    field("Relação com desfechos de saúde", indicator$relacao_saude),
    field("Defasagens temporais relevantes", indicator$defasagens_temporais),
    field("Aplicação na gestão", indicator$aplicacao_gestao),
    field("Observações", indicator$observacoes),
    "## Referências {.unnumbered}",
    "",
    if (length(as_list(indicator$referencias))) md_list(indicator$referencias) else "Nenhuma referência incluída nesta versão demonstrativa. TODO: revisão bibliográfica."
  )
  write_utf8(page, file.path(root, "indicators", "pages", paste0(slug, ".qmd")))
}

indicator_rows <- vapply(indicators, function(x) {
  slug <- tolower(as.character(x$codigo))
  paste0(
    "| [", x$codigo, "](../indicators/pages/", slug, ".qmd) | ",
    x$denominacao, " | ", x$tema, " | ",
    paste(as_list(x$dimensoes), collapse = "; "), " | ",
    paste(as_list(x$disponibilidade), collapse = "; "), " |"
  )
}, character(1L))
indicator_index <- c(
  "<!-- Arquivo gerado por scripts/build_catalogs.R. -->",
  "",
  "| Código | Indicador | Tema | Dimensão | Disponibilidade |",
  "|---|---|---|---|---|",
  indicator_rows
)
write_utf8(indicator_index, file.path(root, "indicators", "generated-index.qmd"))

source_rows <- vapply(sources, function(x) {
  target <- as.character(x$url)
  linked_name <- if (grepl("^https?://", target)) paste0("[", x$nome, "](", target, ")") else x$nome
  paste0(
    "| ", linked_name, " | ", x$instituicao, " | ",
    paste(as_list(x$temas), collapse = "; "), " | ",
    as.character(x$ultima_verificacao), " |"
  )
}, character(1L))
source_index <- c(
  "<!-- Arquivo gerado por scripts/build_catalogs.R. -->",
  "",
  "| Fonte | Instituição | Temas | Verificação |",
  "|---|---|---|---|",
  source_rows
)
write_utf8(source_index, file.path(root, "sources", "generated", "index.qmd"))

source_cards <- unlist(lapply(sources, function(x) {
  c(
    paste0("### ", x$nome, " {#", x$id, "}"),
    "",
    as_text(x$descricao),
    "",
    paste0("**Instituição:** ", x$instituicao, "  "),
    paste0("**Temas:** ", paste(as_list(x$temas), collapse = "; "), "  "),
    paste0("**Cobertura:** ", x$cobertura_geografica, "  "),
    paste0("**Resolução espacial:** ", x$resolucao_espacial, "  "),
    paste0("**Resolução temporal:** ", x$resolucao_temporal, "  "),
    paste0("**Período:** ", x$periodo_disponivel, "  "),
    paste0("**Atualização:** ", x$atualizacao, "  "),
    paste0("**Acesso:** ", x$acesso, "  "),
    paste0("**URL:** ", if (grepl("^https?://", x$url)) paste0("<", x$url, ">") else x$url, "  "),
    paste0("**API:** ", as_text(x$api, "TODO: verificar."), "  "),
    paste0("**Formatos:** ", paste(as_list(x$formatos), collapse = "; "), "  "),
    paste0("**Licença:** ", as_text(x$licenca, "TODO: verificar."), "  "),
    paste0("**Cadastro:** ", as_text(x$cadastro, "TODO: verificar."), "  "),
    paste0("**Custos:** ", as_text(x$custos, "TODO: verificar."), "  "),
    paste0("**Limitações:** ", x$limitacoes, "  "),
    paste0("**Última verificação:** ", x$ultima_verificacao),
    ""
  )
}), use.names = FALSE)
write_utf8(
  c("<!-- Arquivo gerado por scripts/build_catalogs.R. -->", "", source_cards),
  file.path(root, "sources", "generated", "cards.qmd")
)

message(
  "Catálogos validados e gerados: ", length(indicators), " fichas; ",
  length(sources), " fontes."
)
