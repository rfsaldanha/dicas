-- As remissões editoriais continuam legíveis na edição parcial, sem links
-- para capítulos ou catálogos que não fazem parte dela.
local omitted_sections = {
  ["sec-exposicao-vulnerabilidade"] = "capítulo 13",
  ["sec-efeitos-saude"] = "capítulo 14",
  ["sec-resposta"] = "capítulo 15",
  ["sec-comunicacao-risco"] = "capítulo 16"
}

function Cite(cite)
  local has_omitted = false
  for _, citation in ipairs(cite.citations) do
    has_omitted = has_omitted or omitted_sections[citation.id] ~= nil
  end
  if not has_omitted then return end

  local result = pandoc.Inlines({})
  local retained = {}
  local function separate()
    if #result > 0 then result:insert(pandoc.Space()) end
  end
  local function flush()
    if #retained > 0 then
      separate()
      result:insert(pandoc.Cite({}, retained))
      retained = {}
    end
  end
  for _, citation in ipairs(cite.citations) do
    local label = omitted_sections[citation.id]
    if label then
      flush()
      separate()
      result:extend(citation.prefix)
      result:insert(pandoc.Str(label))
      result:extend(citation.suffix)
    else
      retained[#retained + 1] = citation
    end
  end
  flush()
  return result
end

function Link(link)
  local target = link.target:gsub("[?#].*$", "")
  if target:match("^%a[%w+.-]*:") or target:match("^//") then
    return
  end
  -- Este endereço antigo pertence ao capítulo 6, atualmente na Parte I.
  if target:match("chapters/part%-4/14%-indicador%-decisao%.html$") then
    return
  end
  if target:match("chapters/part%-[34]/")
      or target:match("backmatter/indice%-fontes%.[%w]+$")
      or target:match("backmatter/indice%-instituicoes%.[%w]+$")
      or target:match("backmatter/indice%-indicadores%.[%w]+$")
      or target:match("backmatter/lista%-fichas%.[%w]+$") then
    return link.content
  end
end
