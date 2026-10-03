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
  height: 0.5pt,
  fill: luma(90),
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
  return pandoc.RawInline("typst", '#text(font: "Source Sans 3", weight: "semibold")[' .. label .. "]")
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
  fill: luma(249),
  stroke: (top: 0.4pt + luma(160), bottom: 0.4pt + luma(160)),
)[
  #set par(first-line-indent: 0pt, spacing: 0.45em, justify: false)
]] .. body .. [[
]
]]
  return pandoc.RawBlock("typst", rendered)
end

local function framebox(div)
  if not quarto.doc.is_format("typst") or not has_class(div, "framebox") then
    return nil
  end

  local body = pandoc.write(pandoc.Pandoc(div.content), "typst")
  local rendered = [[
#block(
  width: 100%,
  breakable: false,
  inset: (x: 10pt, y: 9pt),
  fill: rgb("#fafafa"),
  stroke: (top: 0.5pt + luma(90), bottom: 0.5pt + luma(90)),
)[
  #set text(size: 9pt)
  #set par(first-line-indent: 0pt, spacing: 0.5em, justify: false)
]] .. body .. [[
]
]]
  return pandoc.RawBlock("typst", rendered)
end

local function section_end(header)
  if not quarto.doc.is_format("typst") or header.level ~= 1 then
    return nil
  end
  return {pandoc.RawBlock("typst", '#metadata("dicas-section-end")'), header}
end

return {
  { Span = field_label },
  { Header = ficha_title },
  { Header = section_end },
  { Div = function(div)
      return indicator_card(div) or framebox(div)
    end },
}
