-- Acrescenta a declaração editorial comum aos diagramas autorais.
-- Os textos alternativos permanecem junto de cada diagrama, pois descrevem
-- relações específicas; fonte, autoria e licença são comuns à série.

local function typst_escape(value)
  return value
    :gsub("\\", "\\\\")
    :gsub("#", "\\#")
    :gsub("%[", "\\[")
    :gsub("%]", "\\]")
end

local function print_source_note(value)
  return pandoc.RawBlock(
    "typst",
    "#block(above: 2pt, below: 5pt)[" ..
      "#set text(font: \"Source Sans 3\", size: 8.5pt, fill: luma(55)); " ..
      "#set par(first-line-indent: 0pt, leading: 0.25em, spacing: 0pt); " ..
      typst_escape(value) ..
    "]"
  )
end

function CodeBlock(block)
  if block.classes:includes("mermaid") then
    local value = "Fonte e autoria: elaboração própria. Licença: a mesma dos textos autorais da obra."
    if quarto.doc.is_format("typst") then
      return { block, print_source_note(value) }
    end
    local note = pandoc.Span(pandoc.Inlines(value), pandoc.Attr("", { "figure-source" }))
    return { block, pandoc.Para({ note }) }
  end
end

function Para(para)
  if not quarto.doc.is_format("typst") or #para.content ~= 1 then
    return
  end
  local span = para.content[1]
  if span.t == "Span" and span.classes:includes("figure-source") then
    return print_source_note(pandoc.utils.stringify(span.content))
  end
end

local in_print_appendix = false

function Header(header)
  if not quarto.doc.is_format("typst") then
    return
  end
  local title = pandoc.utils.stringify(header.content)
  if header.level == 1 and (title:match("^Apêndice A") or title == "Apêndice metodológico") then
    in_print_appendix = true
  end
  if in_print_appendix then
    header.classes:insert("unnumbered")
    return header
  end
end

-- Variantes de impressão ficam ao lado da arte colorida. A substituição
-- conserva o identificador e o caminho já normalizado pelo Quarto.
function Image(element)
  local print_src = element.attributes["print-src"]
  local print_width = element.attributes["print-width"]
  if print_src then
    if quarto.doc.is_format("typst") then
      local directory = element.src:match("^(.*[/])") or ""
      element.src = directory .. print_src
      if print_width then
        element.attributes.width = print_width
      end
    end
    element.attributes["print-src"] = nil
    element.attributes["print-width"] = nil
    return element
  end
end
