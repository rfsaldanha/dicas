-- A página inicial é exclusiva da web, mas o Quarto a coloca no início
-- do documento combinado. Remova somente seu primeiro título vazio/sintético;
-- a página Bem-vindo da impressão é um elemento editorial próprio.
local first_heading = true

function Header(header)
  if not first_heading or header.level ~= 1 then
    return nil
  end

  first_heading = false
  local title = pandoc.utils.stringify(header.content)
  if title:match("^%s*$")
      or title == "Dados e Indicadores de Clima e Ambiente para a Saúde" then
    return {}
  end
end

-- Os links da abertura compartilhada usam a raiz do projeto para funcionar
-- na página inicial e no frontmatter. Na impressão, apontam para o próprio
-- livro ou para a licença publicada, sem depender de arquivos QMD locais.
local welcome_targets = {
  ["/backmatter/lista-fichas.qmd"] = "#lista-de-fichas-por-código-e-capítulo",
  ["/backmatter/indice-fontes.qmd"] = "#catálogo-de-fontes-de-dados",
  ["/LICENSE"] = "https://github.com/rfsaldanha/dicas/blob/main/LICENSE"
}

function Link(link)
  local target = welcome_targets[link.target:gsub("^%./", "/")]
  if target then
    link.target = target
    return link
  end
end
