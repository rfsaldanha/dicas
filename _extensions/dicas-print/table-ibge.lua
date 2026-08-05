-- Aplica o padrão editorial do projeto de referência: grade fechada nos
-- quadros e três linhas nas tabelas estatísticas, conforme a distinção do IBGE.

local function add_three_line_rule(typst)
  local with_top, top_count = typst:gsub(
    "table%.header%(",
    "table.hline(y: 0, stroke: 0.7pt + black),\n  table.header(",
    1
  )

  if top_count ~= 1 then
    quarto.log.warning("Não foi possível inserir a linha superior de uma tabela.")
    return typst
  end

  local with_header_rule, header_count = with_top:gsub(
    "table%.hline%(%)",
    "table.hline(stroke: 0.7pt + black)",
    1
  )

  if header_count ~= 1 then
    quarto.log.warning("Não foi possível ajustar a linha abaixo do cabeçalho de uma tabela.")
    return typst
  end

  -- pandoc.write pode acrescentar um identificador após #table(...), portanto
  -- localizamos o parêntese que fecha especificamente a chamada de table.
  local table_start, open_pos = with_header_rule:find("#table%(")
  if not table_start then
    quarto.log.warning("Não foi possível localizar a tabela renderizada em Typst.")
    return typst
  end

  local depth = 0
  local in_string = false
  local escaped = false
  local close_pos = nil

  for pos = open_pos, #with_header_rule do
    local char = with_header_rule:sub(pos, pos)
    if in_string then
      if escaped then
        escaped = false
      elseif char == "\\" then
        escaped = true
      elseif char == '"' then
        in_string = false
      end
    elseif char == '"' then
      in_string = true
    elseif char == "(" then
      depth = depth + 1
    elseif char == ")" then
      depth = depth - 1
      if depth == 0 then
        close_pos = pos
        break
      end
    end
  end

  if not close_pos then
    quarto.log.warning("Não foi possível inserir a linha inferior de uma tabela.")
    return typst
  end

  -- Mantém apenas #table(...); o invólucro de figura, legenda e identificador
  -- continua sob responsabilidade do Quarto.
  return with_header_rule:sub(table_start, close_pos - 1)
    .. "  table.hline(stroke: 0.7pt + black),\n"
    .. with_header_rule:sub(close_pos, close_pos)
end

local function add_grid_rule(typst, compact)
  -- Um preenchimento ligeiramente menor reduz quebras causadas por quadros
  -- indivisíveis sem alterar a fonte de 9,5 pt nem comprometer a leitura.
  local table_start = "#table(\n"
    .. "  stroke: 0.35pt + rgb(\"#999999\"),\n"
    .. "  fill: (x, y) => if y == 0 {\n"
    .. "    rgb(\"#dedede\")\n"
    .. "  } else if calc.odd(y) {\n"
    .. "    rgb(\"#f6f6f6\")\n"
    .. "  } else {\n"
    .. "    white\n"
    .. "  },\n"
    .. "  inset: (x: 5pt, y: 3.25pt),"
  if compact then
    table_start = table_start:gsub(
      "inset: %(x: 5pt, y: 3.25pt%)",
      "inset: (x: 4pt, y: 2.625pt)",
      1
    )
  end
  local with_grid, grid_count = typst:gsub(
    "#table%(",
    table_start,
    1
  )

  if grid_count ~= 1 then
    quarto.log.warning("Não foi possível aplicar a grade editorial de um quadro.")
    return typst
  end

  local table_start, open_pos = with_grid:find("#table%(")
  if not table_start then
    return with_grid
  end

  local depth = 0
  local in_string = false
  local escaped = false
  for pos = open_pos, #with_grid do
    local char = with_grid:sub(pos, pos)
    if in_string then
      if escaped then
        escaped = false
      elseif char == "\\" then
        escaped = true
      elseif char == '"' then
        in_string = false
      end
    elseif char == '"' then
      in_string = true
    elseif char == "(" then
      depth = depth + 1
    elseif char == ")" then
      depth = depth - 1
      if depth == 0 then
        return with_grid:sub(table_start, pos)
      end
    end
  end

  quarto.log.warning("Não foi possível localizar o fim da grade de um quadro.")
  return with_grid
end

local function has_class(element, class_name)
  for _, class in ipairs(element.classes or {}) do
    if class == class_name then
      return true
    end
  end
  return false
end

local function normalized_cell_text(cell)
  local text = pandoc.utils.stringify(cell.contents or {}):lower()
  text = text:gsub("^%s+", ""):gsub("%s+$", "")
  return text
end

local function is_summary_table(tbl)
  if #tbl.colspecs ~= 6 then
    return false
  end
  local first_row = tbl.head and tbl.head.rows and tbl.head.rows[1]
  if not first_row or not first_row.cells then
    return false
  end
  local expected = {
    "sigla",
    "nome",
    "ano de criação",
    "unidade de análise",
    "cobertura",
    "disseminação de dados",
  }
  for index, label in ipairs(expected) do
    if not first_row.cells[index] or normalized_cell_text(first_row.cells[index]) ~= label then
      return false
    end
  end
  return true
end

local function apply_quadro_column_widths(tbl)
  -- Quadros comparativos combinam siglas com referências de página na coluna
  -- "Sistema". Por ser um cabeçalho curto, a largura automática do Typst pode
  -- comprimi-la até o texto invadir a célula seguinte. Reservamos 17% para
  -- essa coluna nos quadros de três e quatro colunas e distribuímos o restante
  -- de acordo com sua posição; os demais mantêm o cálculo automático.
  local column_count = #tbl.colspecs
  if column_count ~= 3 and column_count ~= 4 then
    return
  end

  local head = tbl.head
  local first_row = head and head.rows and head.rows[1]
  if not first_row or not first_row.cells then
    return
  end

  local system_column = nil
  for i, cell in ipairs(first_row.cells) do
    if normalized_cell_text(cell) == "sistema" then
      system_column = i
      break
    end
  end
  if not system_column then
    return
  end

  local profiles = {
    [3] = {
      [1] = {0.17, 0.37, 0.46},
      [2] = {0.34, 0.17, 0.49},
      [3] = {0.42, 0.41, 0.17},
    },
    [4] = {
      [1] = {0.17, 0.27, 0.30, 0.26},
      [2] = {0.27, 0.17, 0.27, 0.27},
      [3] = {0.27, 0.25, 0.17, 0.31},
      [4] = {0.29, 0.27, 0.27, 0.17},
    },
  }
  local widths = profiles[column_count][system_column]
  for i, width in ipairs(widths) do
    tbl.colspecs[i] = {tbl.colspecs[i][1], width}
  end
end

local function mark_quadro_tables(div)
  if not ((div.identifier or ""):match("^qua%-") or has_class(div, "quadro-grid")) then
    return nil
  end
  div = div:walk({
    Table = function(tbl)
      if not has_class(tbl, "quadro-grid") then
        tbl.classes:insert("quadro-grid")
      end
      return tbl
    end,
  })
  return div
end

local function render_table(tbl)
  if not quarto.doc.is_format("typst") then
    return nil
  end

  -- No Markdown, AlignDefault corresponde ao alinhamento textual usual à
  -- esquerda. O writer Typst traduzia "auto" como centralizado; tornamos esse
  -- padrão explícito e preservamos alinhamentos declarados, como Ano à direita.
  for i, colspec in ipairs(tbl.colspecs) do
    if colspec[1] == pandoc.AlignDefault then
      tbl.colspecs[i] = {pandoc.AlignLeft, colspec[2]}
    end
  end

  apply_quadro_column_widths(tbl)

  local typst = pandoc.write(pandoc.Pandoc({tbl}), "typst")
  local rendered
  if has_class(tbl, "quadro-grid") then
    rendered = add_grid_rule(typst, is_summary_table(tbl))
  else
    rendered = add_three_line_rule(typst)
  end
  return pandoc.RawBlock("typst", rendered)
end

return {
  { Div = mark_quadro_tables },
  { Table = render_table },
}
