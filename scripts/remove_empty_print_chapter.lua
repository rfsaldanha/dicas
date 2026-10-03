local removed = false

function Header(header)
  if removed or header.level ~= 1 then
    return nil
  end

  local title = pandoc.utils.stringify(header.content)
  if title:match("^%s*$") or title == "Bem-vindo"
      or title == "Dados e Indicadores de Clima e Ambiente para a Saúde" then
    removed = true
    return {}
  end
end
