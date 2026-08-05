local removed = false

function Header(header)
  if removed or header.level ~= 1 then
    return nil
  end

  local title = pandoc.utils.stringify(header.content)
  if title:match("^%s*$") or title == "Bem-vindo" then
    removed = true
    return {}
  end
end
