#!/usr/bin/env Rscript

# Valida os metadados estruturados e gera páginas/índices consumidos pelo livro.
# Dependência deliberadamente única: pacote CRAN `yaml`.

script_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
script_path <- if (length(script_arg)) sub("^--file=", "", script_arg[[1L]]) else "scripts/build_catalogs.R"
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)

fail <- function(...) stop(paste0(...), call. = FALSE)
updated_files <- 0L
generated_paths <- character()
write_utf8 <- function(lines, path) {
  generated_paths <<- c(generated_paths, path)
  # A prévia acompanha também os includes. Regravar conteúdo idêntico muda
  # as datas das dependências e pode provocar renderizações desnecessárias.
  content <- charToRaw(paste0(paste0(enc2utf8(lines), "\n"), collapse = ""))
  if (file.exists(path)) {
    previous <- readBin(path, "raw", n = file.info(path)$size)
    if (identical(previous, content)) return(invisible(FALSE))
  }
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  writeBin(content, path)
  updated_files <<- updated_files + 1L
  invisible(TRUE)
}
as_text <- function(value, fallback = "Não se aplica.") {
  if (is.null(value) || !length(value) || identical(value, "")) fallback else as.character(value)
}
as_list <- function(value) {
  if (is.null(value) || !length(value)) character() else as.character(unlist(value, use.names = FALSE))
}
uppercase_initial <- function(value) {
  paste0(toupper(substr(value, 1L, 1L)), substring(value, 2L))
}
source_entries <- function(value, indicator_code = "") {
  if (is.null(value) || !length(value)) {
    fail("A ficha ", indicator_code, " não declara fontes_dados.")
  }
  lapply(value, function(entry) {
    if (!is.list(entry) || is.null(entry$id) || is.null(entry$papel)) {
      fail("Cada item de fontes_dados deve conter id e papel na ficha ", indicator_code, ".")
    }
    list(id = as.character(entry$id), papel = as.character(entry$papel))
  })
}
md_list <- function(value) {
  items <- uppercase_initial(as_list(value))
  if (!length(items)) return("- Não se aplica.")
  paste0("- ", items)
}
yaml_files <- sort(list.files(
  file.path(root, "indicators", "data"),
  pattern = "\\.ya?ml$",
  full.names = TRUE
))

source_path <- file.path(root, "sources", "data", "sources.yml")

# Na renderização parcial, reaproveita apenas uma geração concluída cujas
# entradas E saídas continuam idênticas. A compilação integral e a chamada
# manual sempre validam os dados. Hashes detectam também alterações que
# preservam a data do arquivo, como restaurações de cópias de segurança.
input_paths <- c(
  file.path(root, "scripts/build_catalogs.R"),
  file.path(root, c("_quarto-web.yml", "_quarto-print.yml")),
  yaml_files, source_path,
  sort(list.files(file.path(root, "chapters"), pattern = "\\.qmd$",
                  recursive = TRUE, full.names = TRUE))
)
input_hashes <- tools::md5sum(input_paths)
cache_path <- file.path(root, ".quarto", "catalogs.rds")
incremental <- "--incremental" %in% commandArgs(trailingOnly = TRUE) &&
  Sys.getenv("QUARTO_PROJECT_RENDER_ALL") != "1"
if (incremental && file.exists(cache_path)) {
  cache <- tryCatch(readRDS(cache_path), error = function(e) NULL)
  if (is.list(cache) && !anyNA(input_hashes) &&
      identical(cache$inputs, input_hashes) &&
      is.character(cache$outputs) && length(cache$outputs) > 0L &&
      length(names(cache$outputs)) == length(cache$outputs) &&
      all(file.exists(names(cache$outputs))) &&
      identical(cache$outputs, tools::md5sum(names(cache$outputs)))) {
    quit(save = "no", status = 0L)
  }
}

if (!requireNamespace("yaml", quietly = TRUE)) {
  fail("O pacote R 'yaml' é necessário. Instale-o com install.packages('yaml').")
}
if (!length(yaml_files)) fail("Nenhuma ficha encontrada em indicators/data.")

required_indicator <- c(
  "codigo", "titulo_completo", "titulo_resumido", "conceito", "interpretacao",
  "usos", "limitacoes", "fontes_dados", "formula_calculo", "metodo_calculo",
  "variaveis_categorias_analise", "granularidade", "periodicidade_atualizacao",
  "responsabilidade_gerencial", "notas", "analise_descritiva",
  "tema", "objetivo", "dimensoes", "unidade_medida", "unidade_territorial",
  "resolucao_temporal", "disponibilidade", "qualidade_incerteza",
  "comparabilidade", "relacao_saude", "aplicacao_gestao",
  "capitulo", "capitulo_fichas", "referencia_metodologica", "numerador", "denominador",
  "resolucao_espacial_original", "periodo_referencia", "limiar_referencia",
  "cobertura_geografica", "periodo_disponivel", "forma_acesso",
  "url_persistente", "formatos", "necessidade_processamento",
  "defasagens_temporais", "referencias"
)

# Protocolos versionados usam os campos da ficha sobre os valores comuns.
# Preserva a leitura dos catálogos legados fora do escopo desta revisão.
indicator_documents <- lapply(yaml_files, function(path) {
  document <- yaml::read_yaml(path)
  entries <- if (!is.null(document$indicators)) document$indicators else list(document)
  if (any(vapply(entries, function(x) !is.null(x$protocolo_versao), logical(1L)))) {
    document <- yaml::read_yaml(path, merge.precedence = "override")
  }
  document
})
indicators <- unlist(lapply(seq_along(indicator_documents), function(i) {
  document <- indicator_documents[[i]]
  entries <- if (!is.null(document$indicators)) document$indicators else list(document)
  names(entries) <- paste0(basename(yaml_files[[i]]), "#", seq_along(entries))
  entries
}), recursive = FALSE)
for (name in names(indicators)) {
  missing <- setdiff(required_indicator, names(indicators[[name]]))
  if (length(missing)) {
    fail("Campos obrigatórios ausentes em ", name, ": ", paste(missing, collapse = ", "), ".")
  }
  indicator <- indicators[[name]]
  if (!is.null(indicator$protocolo_versao)) {
    operational <- c("situacao_calculo", "dependencia_dados_locais", "automacao",
                     "condicoes_automacao", "evidencia_verificacao", "detalhe_verificacao")
    missing <- setdiff(operational, names(indicator))
    if (length(missing)) fail("Protocolo incompleto em ", indicator$codigo, ": ", paste(missing, collapse = ", "))
    labels <- c(abertos = "Calculável com dados abertos",
                centralizados = "Calculável com dados locais centralizados",
                locais = "Depende de dados locais")
    if (!indicator$situacao_calculo %in% names(labels)) fail("Situação inválida em ", indicator$codigo)
    if (!identical(as_list(indicator$disponibilidade), unname(labels[indicator$situacao_calculo]))) {
      fail("Rótulo incompatível com a situação em ", indicator$codigo)
    }
    if (!indicator$automacao %in% c("Viável", "Condicionada", "Não demonstrada")) fail("Automação inválida em ", indicator$codigo)
    if (!indicator$evidencia_verificacao %in% c("Documentação verificada", "Acesso testado", "Acesso e cálculo testados")) fail("Evidência inválida em ", indicator$codigo)
  }
  source_entries(indicators[[name]]$fontes_dados, indicators[[name]]$codigo)
}
codes <- vapply(indicators, function(x) as.character(x$codigo), character(1L))
if (anyDuplicated(codes)) fail("Códigos duplicados: ", paste(unique(codes[duplicated(codes)]), collapse = ", "), ".")
if (any(!grepl("^[A-Z]{3}-[A-Z]{2,3}-[0-9]{2}$", codes))) {
  fail("Código fora do padrão em: ", paste(names(indicators)[!grepl("^[A-Z]{3}-[A-Z]{2,3}-[0-9]{2}$", codes)], collapse = ", "), ".")
}

sources <- yaml::read_yaml(source_path)
required_source <- c(
  "id", "tipo_registro", "nome", "instituicao", "descricao", "recursos_relacionados",
  "temas", "variaveis",
  "cobertura_geografica", "resolucao_espacial", "resolucao_temporal",
  "periodo_disponivel", "atualizacao", "acesso", "url", "limitacoes",
  "ultima_verificacao", "indicadores", "api", "formatos", "licenca",
  "cadastro", "custos"
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
source_types <- c(
  "instituição", "unidade institucional", "programa", "sistema de informação",
  "plataforma", "base de dados", "produto", "serviço", "cadastro provisório"
)
invalid_source_types <- vapply(
  sources,
  function(x) !as.character(x$tipo_registro) %in% source_types,
  logical(1L)
)
if (any(invalid_source_types)) {
  fail(
    "Tipo de registro inválido em: ",
    paste(source_ids[invalid_source_types], collapse = ", "), "."
  )
}

declared_source_ids <- unique(unlist(lapply(indicators, function(x) {
  vapply(source_entries(x$fontes_dados, x$codigo), function(entry) entry$id, character(1L))
}), use.names = FALSE))
unknown_sources <- setdiff(declared_source_ids, source_ids)
if (length(unknown_sources)) {
  fail("Fontes citadas nas fichas sem cadastro: ", paste(unknown_sources, collapse = ", "), ".")
}

# A ordem editorial vem dos perfis; os prefixos dos arquivos acompanham essa ordem.
configured_chapters <- function(profile) {
  config <- yaml::read_yaml(file.path(root, profile))
  paths <- unlist(lapply(config$book$chapters, function(entry) {
    if (is.character(entry)) entry else if (!is.null(entry$chapters)) unlist(entry$chapters) else entry$href
  }), use.names = FALSE)
  paths[grepl("^chapters/", paths)]
}
chapter_paths <- configured_chapters("_quarto-web.yml")
if (!identical(chapter_paths, configured_chapters("_quarto-print.yml"))) {
  fail("A ordem dos capítulos difere entre web e impressão.")
}
chapter_numbers <- setNames(seq_along(chapter_paths), chapter_paths)

chapter_info <- function(path) {
  full_path <- file.path(root, path)
  if (!file.exists(full_path)) fail("Capítulo não encontrado: ", path)
  heading <- grep("^# ", readLines(full_path, warn = FALSE, encoding = "UTF-8"), value = TRUE)
  if (length(heading) != 1L || !grepl("\\{#sec-", heading)) {
    fail("Capítulo sem título e identificador estável: ", path)
  }
  list(title = sub(" \\{.*$", "", sub("^# ", "", heading)),
       anchor = sub(".*\\{#([^ }]+).*", "\\1", heading))
}
chapter_metadata <- setNames(lapply(chapter_paths, chapter_info), chapter_paths)
for (indicator in indicators) {
  context <- as.character(indicator$capitulo)
  target <- as.character(indicator$capitulo_fichas)
  if (!context %in% chapter_paths || !target %in% chapter_paths ||
      !grepl("^chapters/part-[23]/", context) || !grepl("^chapters/part-4/", target) ||
      !startsWith(chapter_metadata[[target]]$title, "Fichas — ") ||
      unname(chapter_numbers[target]) != unname(chapter_numbers[context]) + 9L) {
    fail("Vínculo de contexto/fichas inválido para ", indicator$codigo, ".")
  }
}

field <- function(label, value) {
  c(paste0("[", label, ".]{.field-label} ", as_text(value)), "")
}

for (indicator in indicators) {
  slug <- tolower(as.character(indicator$codigo))
  context <- chapter_metadata[[as.character(indicator$capitulo)]]
  entries <- source_entries(indicator$fontes_dados, indicator$codigo)
  source_lines <- vapply(entries, function(entry) {
    paste0(
      "- ", source_by_id[[entry$id]]$nome, " — ", entry$papel,
      " ([cadastro](../../backmatter/indice-fontes.qmd#", entry$id, "))"
    )
  }, character(1L))
  ficha <- c(
    paste0("## Ficha do indicador: ", indicator$titulo_completo, " {#sec-", slug, " .ficha-title}"),
    "",
    "::: {.indicator-card}",
    paste0("[Código:]{.field-label} ", indicator$codigo, " \\"),
    paste0("[Título resumido:]{.field-label} ", indicator$titulo_resumido, " \\"),
    paste0("[Tema:]{.field-label} ", indicator$tema, " \\"),
    paste0("[Dimensão:]{.field-label} ", paste(as_list(indicator$dimensoes), collapse = "; "), " \\"),
    paste0("[Disponibilidade:]{.field-label} ", paste0("[", as_list(indicator$disponibilidade), "]{.availability}", collapse = " ")),
    ":::",
    "",
    paste0("Contexto e interpretação: [", context$title, "](../../",
           indicator$capitulo, "#", context$anchor, ")."),
    "",
    "### Identificação e fundamento",
    "",
    field("Base de consolidação", indicator$referencia_metodologica),
    "::: {.callout-note icon=false title=\"Conceito-chave\"}",
    as_text(indicator$conceito),
    ":::",
    "",
    "### Objetivo",
    "",
    as_text(indicator$objetivo),
    "",
    "### Interpretação",
    "",
    as_text(indicator$interpretacao),
    "",
    "### Usos",
    "",
    md_list(indicator$usos),
    "",
    "### Limitações",
    "",
    md_list(indicator$limitacoes),
    "",
    "### Fontes de dados",
    "",
    source_lines,
    "",
    "### Método de cálculo",
    "",
    as_text(indicator$metodo_calculo),
    "",
    "$$",
    trimws(as_text(indicator$formula_calculo), which = "right"),
    "$$",
    "",
    "::: {.indicator-card}",
    field("Numerador", indicator$numerador),
    field("Denominador", indicator$denominador),
    field("Unidade de medida", indicator$unidade_medida),
    field("Variáveis e categorias de análise", indicator$variaveis_categorias_analise),
    field("Granularidade", indicator$granularidade),
    field("Periodicidade de atualização", indicator$periodicidade_atualizacao),
    field("Responsabilidade gerencial", indicator$responsabilidade_gerencial),
    field("Notas", indicator$notas),
    field("Análise descritiva do indicador", indicator$analise_descritiva),
    ":::",
    "",
    "### Campos complementares para clima, ambiente e saúde",
    "",
    "::: {.indicator-card}",
    field("Unidade territorial", indicator$unidade_territorial),
    field("Resolução espacial original", indicator$resolucao_espacial_original),
    field("Resolução temporal", indicator$resolucao_temporal),
    field("Período de referência", indicator$periodo_referencia),
    field("Limiar ou valor de referência", indicator$limiar_referencia),
    ":::",
    "",
    "### Disponibilidade e acesso",
    "",
    if (!is.null(indicator$protocolo_versao)) c(
      field("Protocolo verificado em", indicator$protocolo_versao),
      field("Dependência de dados locais", indicator$dependencia_dados_locais),
      field("Automação", indicator$automacao),
      field("Requisitos para o cálculo", indicator$condicoes_automacao),
      field("Nível de evidência", indicator$evidencia_verificacao),
      field("Alcance da verificação", indicator$detalhe_verificacao)
    ),
    field("Cobertura geográfica", indicator$cobertura_geografica),
    field("Período disponível", indicator$periodo_disponivel),
    field("Periodicidade de atualização", indicator$periodicidade_atualizacao),
    field("Forma de acesso", indicator$forma_acesso),
    field("URL ou identificador persistente", indicator$url_persistente),
    field("Formato dos arquivos", indicator$formatos),
    field("Necessidade de processamento", indicator$necessidade_processamento),
    "### Qualidade, comparação e saúde",
    "",
    field("Qualidade e incerteza", indicator$qualidade_incerteza),
    field("Possibilidade de comparação", indicator$comparabilidade),
    field("Relação com desfechos de saúde", indicator$relacao_saude),
    field("Defasagens temporais relevantes", indicator$defasagens_temporais),
    field("Aplicação na gestão", indicator$aplicacao_gestao),
    "### Referências metodológicas",
    "",
    md_list(indicator$referencias)
  )
  ficha <- sub(
    "^### (.+)",
    "### \\1 {.unnumbered .ficha-section}",
    ficha
  )
  write_utf8(ficha, file.path(root, "indicators", "includes", paste0(slug, ".qmd")))
}

indicator_page_ref <- function(x) {
  paste0("`#ref(<sec-", tolower(x$codigo), ">, form: \"page\", supplement: none)`{=typst}")
}
chapter_link <- function(path) {
  paste0("[cap. ", unname(chapter_numbers[path]), "](../", path, ")")
}
indicator_row_html <- function(x, kind) {
  link <- paste0("[", x$codigo, "](../", x$capitulo_fichas, "#sec-", tolower(x$codigo), ")")
  if (kind == "index") {
    paste0("| ", x$titulo_resumido, " | ", link, " | ", x$tema, " |")
  } else {
    paste0("| ", link, " | ", x$titulo_resumido, " | ", chapter_link(x$capitulo),
           " | ", chapter_link(x$capitulo_fichas), " |")
  }
}
indicator_row_print <- function(x, kind) {
  if (kind == "index") {
    paste0("| ", x$titulo_resumido, " | ", x$codigo, " | ", indicator_page_ref(x), " |")
  } else {
    paste0("| ", x$codigo, " | ", x$titulo_resumido, " | ",
           unname(chapter_numbers[x$capitulo]), " | ",
           unname(chapter_numbers[x$capitulo_fichas]), " | ", indicator_page_ref(x), " |")
  }
}
short_titles <- vapply(indicators, function(x) as.character(x$titulo_resumido), character(1L))
short_title_order <- order(tolower(short_titles), method = "shell")
code_order <- order(codes, method = "radix")

indicator_document <- function(entries, kind = c("index", "list")) {
  kind <- match.arg(kind)
  html_header <- if (kind == "index") {
    c("| Indicador | Código | Tema |", "|---|---|---|")
  } else {
    c("| Código | Indicador | Contexto | Fichas |", "|---|---|---|---|")
  }
  print_header <- if (kind == "index") {
    c("| Indicador | Código | Página |", "|---|---|---|")
  } else {
    c("| Código | Indicador | Contexto | Fichas | Página |", "|---|---|---|---|---|")
  }
  c(
    "<!-- Arquivo gerado por scripts/build_catalogs.R. -->", "",
    "::: {.content-visible .quadro-grid when-format=\"html\"}",
    html_header, vapply(entries, indicator_row_html, character(1L), kind = kind), ":::", "",
    "::: {.content-visible .quadro-grid when-format=\"typst\"}",
    print_header, vapply(entries, indicator_row_print, character(1L), kind = kind), ":::"
  )
}
write_utf8(
  indicator_document(indicators[short_title_order], "index"),
  file.path(root, "indicators", "generated-index-alphabetical.qmd")
)
write_utf8(
  indicator_document(indicators[code_order], "list"),
  file.path(root, "indicators", "generated-list.qmd")
)

source_rows <- vapply(sources, function(x) {
  target <- as.character(x$url)
  linked_name <- if (grepl("^https?://", target)) paste0("[", x$nome, "](", target, ")") else x$nome
  paste0(
    "| ", linked_name, " | ", x$tipo_registro, " | ", x$instituicao, " | ",
    paste(as_list(x$temas), collapse = "; "), " | ",
    as.character(x$ultima_verificacao), " |"
  )
}, character(1L))
source_rows_print <- vapply(sources, function(x) {
  paste0(
    "| ", x$nome, " | ", x$tipo_registro, " | ", x$instituicao, " |"
  )
}, character(1L))
source_index <- c(
  "<!-- Arquivo gerado por scripts/build_catalogs.R. -->",
  "",
  "::: {.content-visible .quadro-grid when-format=\"html\"}",
  "| Fonte | Tipo de registro | Instituição responsável | Temas | Verificação |",
  "|---|---|---|---|---|",
  source_rows,
  ":::",
  "",
  "::: {.content-visible .quadro-grid when-format=\"typst\"}",
  "| Fonte | Tipo de registro | Instituição responsável |",
  "|---|---|---|",
  source_rows_print,
  ":::"
)
write_utf8(source_index, file.path(root, "sources", "generated", "index.qmd"))

source_cards <- unlist(lapply(sources, function(x) {
  c(
    paste0("### ", x$nome, " {#", x$id, "}"),
    "",
    as_text(x$descricao),
    "",
    paste0("[Tipo de registro:]{.field-label} ", x$tipo_registro, " \\"),
    paste0("[Instituição:]{.field-label} ", x$instituicao, " \\"),
    paste0("[Recursos relacionados:]{.field-label} ", paste(as_list(x$recursos_relacionados), collapse = "; "), " \\"),
    paste0("[Temas:]{.field-label} ", paste(as_list(x$temas), collapse = "; "), " \\"),
    paste0("[Cobertura:]{.field-label} ", x$cobertura_geografica, " \\"),
    paste0("[Resolução espacial:]{.field-label} ", x$resolucao_espacial, " \\"),
    paste0("[Resolução temporal:]{.field-label} ", x$resolucao_temporal, " \\"),
    paste0("[Período:]{.field-label} ", x$periodo_disponivel, " \\"),
    paste0("[Atualização:]{.field-label} ", x$atualizacao, " \\"),
    paste0("[Acesso:]{.field-label} ", x$acesso, " \\"),
    paste0("[URL:]{.field-label} ", if (grepl("^https?://", x$url)) paste0("<", x$url, ">") else x$url, " \\"),
    paste0("[API:]{.field-label} ", as_text(x$api, "Não informada para este recurso."), " \\"),
    paste0("[Formatos:]{.field-label} ", paste(as_list(x$formatos), collapse = "; "), " \\"),
    paste0("[Licença:]{.field-label} ", as_text(x$licenca, "Não informada para este recurso."), " \\"),
    paste0("[Cadastro:]{.field-label} ", as_text(x$cadastro, "Não informado para este recurso."), " \\"),
    paste0("[Custos:]{.field-label} ", as_text(x$custos, "Não informados para este recurso."), " \\"),
    paste0("[Limitações:]{.field-label} ", x$limitacoes, " \\"),
    paste0("[Última verificação:]{.field-label} ", x$ultima_verificacao),
    ""
  )
}), use.names = FALSE)
write_utf8(
  c("<!-- Arquivo gerado por scripts/build_catalogs.R. -->", "", source_cards),
  file.path(root, "sources", "generated", "cards.qmd")
)

dir.create(dirname(cache_path), recursive = TRUE, showWarnings = FALSE)
saveRDS(list(inputs = input_hashes, outputs = tools::md5sum(generated_paths)), cache_path)

message(
  "Catálogos validados: ", length(indicators), " fichas; ",
  length(sources), " fontes; ", updated_files, " arquivo(s) atualizado(s)."
)
