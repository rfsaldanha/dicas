-- Use []{.chapter-title-ref target="sec-..."} para títulos que acompanham @sec.
local directory = PANDOC_SCRIPT_FILE:match('^(.*[/\\])') or './'
local chapters = dofile(directory .. 'chapter_metadata.lua').chapters()

function Span(span)
  if not span.classes:includes('chapter-title-ref') then return end
  local id = span.attributes.target
  local chapter = chapters[id]
  if not chapter then error('Título de capítulo sem destino: ' .. tostring(id)) end
  return pandoc.Inlines(chapter.title)
end
