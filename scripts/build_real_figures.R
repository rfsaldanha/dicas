#!/usr/bin/env Rscript

required <- c("dplyr", "geobr", "ggplot2", "patchwork", "sf", "terra")
missing <- required[!vapply(required, requireNamespace, logical(1L), quietly = TRUE)]
if (length(missing)) {
  stop("Pacotes R ausentes: ", paste(missing, collapse = ", "), call. = FALSE)
}

root <- normalizePath(".", mustWork = TRUE)
cams_file <- Sys.getenv(
  "DICAS_CAMS_TEMP_FILE",
  unset = file.path(root, "..", "camsdata", "forecast_data", "cams_forecast_temp.nc")
)
if (!file.exists(cams_file)) stop("Arquivo CAMS ausente: ", cams_file, call. = FALSE)

data_dir <- file.path(root, "data-raw", "figures")
asset_file <- file.path(root, "assets", "figures", "mudanca-suporte.svg")
dir.create(data_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(asset_file), recursive = TRUE, showWarnings = FALSE)

lead_hours <- 24L
population_year <- 2022L
temperature_stack <- terra::rast(cams_file)
layer_index <- grep(
  paste0("forecast_period=", lead_hours, "_"),
  names(temperature_stack),
  fixed = TRUE
)[[1L]]
temperature <- temperature_stack[[layer_index]] - 273.15
names(temperature) <- "temperature_c"
reference_time <- as.POSIXct(terra::time(temperature_stack)[[1L]], tz = "UTC")
valid_time <- reference_time + lead_hours * 3600

state <- geobr::read_state(
  year = 2022,
  code_state = 33,
  simplified = FALSE,
  showProgress = FALSE,
  cache = TRUE,
  verbose = FALSE
) |>
  sf::st_make_valid() |>
  sf::st_transform(4326)

temperature_crop <- terra::crop(temperature, terra::vect(state))
temperature_grid <- terra::as.polygons(
  temperature_crop,
  na.rm = TRUE,
  aggregate = FALSE
) |>
  sf::st_as_sf()
temperature_grid$cell <- terra::cellFromXY(
  temperature,
  sf::st_coordinates(suppressWarnings(sf::st_point_on_surface(temperature_grid)))
)
temperature_grid <- sf::st_intersection(temperature_grid, state)

population <- geobr::read_statistical_grid(
  year = population_year,
  code_muni = 33,
  showProgress = FALSE,
  cache = TRUE,
  verbose = FALSE
)
population_points <- sf::st_point_on_surface(population)
population$cell <- terra::cellFromXY(
  temperature,
  sf::st_coordinates(population_points)
)
population_by_cell <- sf::st_drop_geometry(population) |>
  dplyr::filter(!is.na(cell)) |>
  dplyr::group_by(cell) |>
  dplyr::summarise(population = sum(pop_total, na.rm = TRUE), .groups = "drop")

grid_projected <- sf::st_transform(temperature_grid, 31983)
temperature_grid$area_km2 <- as.numeric(sf::st_area(grid_projected)) / 1e6
temperature_grid <- temperature_grid |>
  dplyr::left_join(population_by_cell, by = "cell") |>
  dplyr::mutate(
    population = dplyr::coalesce(population, 0),
    temperature_band = cut(
      temperature_c,
      breaks = c(-Inf, 16, 18, 20, 22, Inf),
      labels = c("até 16", "16 a 18", "18 a 20", "20 a 22", "acima de 22"),
      right = TRUE
    )
  )

area_mean <- stats::weighted.mean(
  temperature_grid$temperature_c,
  temperature_grid$area_km2,
  na.rm = TRUE
)
population_mean <- stats::weighted.mean(
  temperature_grid$temperature_c,
  temperature_grid$population,
  na.rm = TRUE
)
maximum <- max(temperature_grid$temperature_c, na.rm = TRUE)

temperature_plot <- temperature_grid |>
  sf::st_transform(31983) |>
  sf::st_simplify(dTolerance = 500, preserveTopology = TRUE) |>
  sf::st_transform(4326)
state_plot <- state |>
  sf::st_transform(31983) |>
  sf::st_simplify(dTolerance = 500, preserveTopology = TRUE) |>
  sf::st_transform(4326)
centres <- sf::st_point_on_surface(temperature_plot) |>
  dplyr::filter(population > 0)
maximum_cell <- temperature_plot |>
  dplyr::filter(temperature_c == maximum)

base_theme <- ggplot2::theme_void(base_family = "Helvetica", base_size = 11) +
  ggplot2::theme(
    plot.title = ggplot2::element_text(face = "bold", size = 13, colour = "#223039", hjust = 0.5),
    plot.subtitle = ggplot2::element_text(size = 11, colour = "#46555c", hjust = 0.5),
    plot.margin = ggplot2::margin(4, 4, 4, 4),
    legend.position = "bottom",
    legend.title = ggplot2::element_text(face = "bold", size = 11),
    legend.text = ggplot2::element_text(size = 10),
    panel.border = ggplot2::element_rect(colour = "#34454d", fill = NA, linewidth = 0.5)
  )

base_map <- function() {
  ggplot2::ggplot(temperature_plot) +
    ggplot2::geom_sf(ggplot2::aes(fill = temperature_band), colour = "#ffffff", linewidth = 0.35) +
    ggplot2::geom_sf(data = state_plot, fill = NA, colour = "#223039", linewidth = 0.75) +
    ggplot2::scale_fill_manual(
      values = c("#dfe8e7", "#d6d7d2", "#c9bdb6", "#b9877f", "#9a3e38"),
      name = NULL,
      labels = c("≤ 16", "16–18", "18–20", "20–22", "> 22"),
      drop = FALSE
    ) +
    ggplot2::coord_sf(datum = NA, expand = FALSE) +
    base_theme
}

p_area <- base_map() +
  ggplot2::labs(
    title = "Média territorial",
    subtitle = paste0(format(round(area_mean, 1), decimal.mark = ","), " °C")
  )

p_population <- base_map() +
  ggplot2::geom_sf(
    data = centres,
    ggplot2::aes(size = population),
    shape = 21, fill = "#34454d", colour = "#ffffff", alpha = 0.78,
    inherit.aes = FALSE
  ) +
  ggplot2::scale_size_area(max_size = 7, guide = "none") +
  ggplot2::labs(
    title = "Média populacional",
    subtitle = paste0(
      format(round(population_mean, 1), decimal.mark = ","),
      " °C\nCírculos ∝ população ", population_year
    )
  )

p_maximum <- base_map() +
  ggplot2::geom_sf(data = maximum_cell, fill = NA, colour = "#223039", linewidth = 1.4) +
  ggplot2::labs(
    title = "Máximo territorial",
    subtitle = paste0(format(round(maximum, 1), decimal.mark = ","), " °C")
  )

figure_design <- "
AB
CC
"
figure <- (p_area + p_population + p_maximum) +
  patchwork::plot_layout(design = figure_design, guides = "collect") +
  patchwork::plot_annotation(
    title = "Estado do Rio de Janeiro · temperatura do ar a 2 m",
    subtitle = paste0(
      "CAMS, rodada ", format(reference_time, "%d/%m/%Y %H UTC"),
      " · prazo ", lead_hours, " h · grade de 0,4°"
    ),
    theme = ggplot2::theme(
      plot.title = ggplot2::element_text(
        family = "Helvetica", face = "bold", size = 15, colour = "#223039", hjust = 0.5
      ),
      plot.subtitle = ggplot2::element_text(
        family = "Helvetica", size = 11, colour = "#46555c", hjust = 0.5
      )
    )
  ) &
  ggplot2::theme(legend.position = "bottom")

pdftocairo <- Sys.which("pdftocairo")
if (!nzchar(pdftocairo)) stop("pdftocairo não localizado.", call. = FALSE)
temporary_pdf <- tempfile(fileext = ".pdf")
on.exit(unlink(temporary_pdf), add = TRUE)
grDevices::pdf(
  file = temporary_pdf,
  width = 5.1,
  height = 4.8,
  pointsize = 11,
  family = "Helvetica",
  bg = "white",
  onefile = TRUE,
  useDingbats = FALSE,
  paper = "special"
)
print(figure)
grDevices::dev.off()
if (file.exists(asset_file)) unlink(asset_file)
conversion_status <- system2(
  pdftocairo,
  c("-svg", shQuote(temporary_pdf), shQuote(asset_file))
)
if (conversion_status != 0L || !file.exists(asset_file)) {
  stop("Falha na conversão vetorial de PDF para SVG.", call. = FALSE)
}

svg <- readLines(asset_file, warn = FALSE, encoding = "UTF-8")
svg_start <- grep("^<svg ", svg)[[1L]]
svg[[svg_start]] <- sub(
  "<svg ",
  "<svg role=\"img\" aria-labelledby=\"title desc\" ",
  svg[[svg_start]],
  fixed = TRUE
)
accessible <- c(
  "<title id=\"title\">Mudança de suporte aplicada à temperatura do ar no estado do Rio de Janeiro</title>",
  paste0(
    "<desc id=\"desc\">Três mapas usam a mesma previsão CAMS de temperatura do ar. ",
    "O primeiro informa a média pela área territorial, o segundo a média ponderada pela população ",
    "residente do Censo 2022 e o terceiro o máximo territorial.</desc>"
  )
)
svg <- append(svg, accessible, after = svg_start)
writeLines(svg, asset_file, useBytes = TRUE)

derived <- sf::st_drop_geometry(temperature_grid) |>
  dplyr::transmute(
    cell,
    temperature_c = round(temperature_c, 4),
    area_km2 = round(area_km2, 4),
    population
  )
utils::write.csv(
  derived,
  file.path(data_dir, "mudanca-suporte-rj.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

metadata <- c(
  "figure: mudanca-suporte.svg",
  "territory: Estado do Rio de Janeiro",
  paste0("forecast_reference_utc: ", format(reference_time, "%Y-%m-%dT%H:%M:%SZ")),
  paste0("forecast_valid_utc: ", format(valid_time, "%Y-%m-%dT%H:%M:%SZ")),
  paste0("forecast_lead_hours: ", lead_hours),
  "temperature_variable: CAMS 2m temperature",
  "temperature_unit_source: K",
  "temperature_unit_figure: degree Celsius",
  "temperature_grid: 0.4 degree latitude-longitude",
  paste0("population_source: IBGE Statistical Grid ", population_year, " via geobr"),
  "boundary_source: IBGE state mesh 2022 via geobr",
  paste0("area_weighted_mean_c: ", round(area_mean, 4)),
  paste0("population_weighted_mean_c: ", round(population_mean, 4)),
  paste0("territorial_maximum_c: ", round(maximum, 4))
)
writeLines(metadata, file.path(data_dir, "mudanca-suporte-rj.yml"), useBytes = TRUE)

message(
  "Figura real gerada: média territorial ", round(area_mean, 1),
  " °C; média populacional ", round(population_mean, 1),
  " °C; máximo ", round(maximum, 1), " °C."
)
