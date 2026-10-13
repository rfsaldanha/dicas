-- Acrescenta a declaração editorial comum aos diagramas autorais.
-- Os textos alternativos permanecem junto de cada diagrama, pois descrevem
-- relações específicas; fonte, autoria e licença são comuns à série.

local function print_source_note(value)
  -- Preserva os nós Cite até a passagem do citeproc. Converter o conteúdo
  -- em string aqui expõe chaves bibliográficas como referências Typst.
  local content = pandoc.Inlines({ pandoc.RawInline(
    "typst",
    "#block(above: 2pt, below: 5pt)[" ..
      "#set text(font: \"Source Sans 3\", size: 8.5pt, fill: luma(55)); " ..
      "#set par(first-line-indent: 0pt, leading: 0.25em, spacing: 0pt); "
  ) })
  content:extend(type(value) == "string" and pandoc.Inlines(value) or value)
  content:insert(pandoc.RawInline("typst", "]"))
  return pandoc.Para(content)
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
    return print_source_note(span.content)
  end
end

local in_print_appendix = false
local appendix_titles = {
  ["Apêndice metodológico"] = { letter = "A", title = "Apêndice A — Apêndice metodológico" },
  ["Estações meteorológicas e de qualidade do ar"] = { letter = "B", title = "Apêndice B — Estações meteorológicas e de qualidade do ar" }
}

function Header(header)
  if not quarto.doc.is_format("typst") then
    return
  end
  local title = pandoc.utils.stringify(header.content)
  local appendix = header.level == 1 and appendix_titles[title] or nil
  if appendix then
    in_print_appendix = true
    header.content = pandoc.Inlines(appendix.title)
    header.classes:insert("unnumbered")
    -- Os contadores de imagem e tabela são reiniciados pelo template a cada H1.
    -- A letra do apêndice deve substituir o último número de capítulo também
    -- nas referências, sem transformar B em um novo capítulo numérico.
    local prefix = appendix.letter
    local setup = '#set figure(numbering: n => "' .. prefix .. '." + str(n))\n' ..
      '#set math.equation(numbering: n => "(' .. prefix .. '." + str(n) + ")")'
    return { pandoc.RawBlock("typst", setup), header }
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

-- Mantém a imagem, a legenda e o crédito juntos nas pranchas do apêndice.
function Div(div)
  if quarto.doc.is_format("typst") and div.classes:includes("figure-with-source") then
    local blocks = pandoc.List({ pandoc.RawBlock("typst", "#block(breakable: false)[") })
    blocks:extend(div.content)
    blocks:insert(pandoc.RawBlock("typst", "]"))
    return blocks
  end
end
