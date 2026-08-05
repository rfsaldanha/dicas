-- Acrescenta a declaração editorial comum aos diagramas autorais.
-- Os textos alternativos permanecem junto de cada diagrama, pois descrevem
-- relações específicas; fonte, autoria e licença são comuns à série.

function CodeBlock(block)
  if block.classes:includes("mermaid") then
    local note = pandoc.Span(
      pandoc.Inlines("Fonte e autoria: elaboração própria. Licença: a mesma dos textos autorais da obra."),
      pandoc.Attr("", { "figure-source" })
    )
    return { block, pandoc.Para({ note }) }
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
