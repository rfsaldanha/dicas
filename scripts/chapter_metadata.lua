-- Identidade editorial derivada das fontes, sem números ou títulos duplicados.
local M = {}
local directory = debug.getinfo(1, 'S').source:sub(2):match('^(.*[/\\])') or './'
local root = directory .. '../'

function M.paths(profile)
  local paths = {}
  for line in io.lines(root .. profile) do
    local path = line:match('^%s*%-%s*(chapters/[^%s]+%.qmd)%s*$')
    if path then paths[#paths + 1] = path end
  end
  return paths
end

function M.chapters()
  local chapters = {}
  for number, path in ipairs(M.paths('_quarto-web.yml')) do
    for line in io.lines(root .. path) do
      local title, id = line:match('^# (.-)%s+{#(sec%-[%w%-]+)')
      if id then
        chapters[id] = { title = title, number = number, path = path }
        break
      end
    end
  end
  return chapters
end

return M
