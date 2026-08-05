local function has_class(element, class_name)
  for _, class in ipairs(element.classes or {}) do
    if class == class_name then
      return true
    end
  end
  return false
end

local function ficha_title(header)
  if not quarto.doc.is_format("typst") or not has_class(header, "ficha-title") then
    return nil
  end

  local marker = pandoc.RawBlock("typst", [[
#v(4mm)
#block(
  width: 100%,
  height: 2pt,
  fill: black,
  sticky: true,
)[]
#v(2mm)
]])
  return {marker, header}
end

local function field_label(span)
  if not quarto.doc.is_format("typst") or not has_class(span, "field-label") then
    return nil
  end

  local label = pandoc.write(
    pandoc.Pandoc({pandoc.Plain(span.content)}),
    "typst"
  ):gsub("^%s+", ""):gsub("%s+$", "")
  return pandoc.RawInline("typst", "#smallcaps[" .. label .. "]")
end

local function indicator_card(div)
  if not quarto.doc.is_format("typst") or not has_class(div, "indicator-card") then
    return nil
  end

  local body = pandoc.write(pandoc.Pandoc(div.content), "typst")
  local rendered = [[
#block(
  width: 100%,
  breakable: true,
  inset: (x: 9pt, y: 7pt),
  fill: rgb("#f4f4f4"),
  stroke: 0.5pt + rgb("#909090"),
  radius: 2pt,
)[
  #set par(first-line-indent: 0pt, spacing: 0.45em, justify: false)
]] .. body .. [[
]
]]
  return pandoc.RawBlock("typst", rendered)
end

return {
  { Span = field_label },
  { Header = ficha_title },
  { Div = indicator_card },
}
