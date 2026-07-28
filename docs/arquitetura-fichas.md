# Arquitetura das fichas de indicadores

## Solução escolhida

Cada ficha é um YAML em `indicators/data/`. O script `scripts/build_catalogs.R` valida os registros, resolve IDs de fontes, produz páginas Quarto em `indicators/pages/` e atualiza índices.

Essa abordagem foi escolhida porque:

- mantém revisão campo a campo;
- gera HTML e PDF com o mesmo conteúdo;
- permite filtros futuros por tema, dimensão, fonte e disponibilidade;
- evita um filtro Lua complexo;
- torna códigos e campos obrigatórios validáveis;
- preserva páginas legíveis e vinculáveis.

CSV foi descartado porque textos longos, listas e fórmulas ficam frágeis. Metadados apenas no cabeçalho `.qmd` misturariam dado estruturado e apresentação. Um banco ou ambiente Python seria desproporcional.

## Código

O padrão é `AAA-BBB-00`, com prefixos de domínio e medida. Códigos publicados não devem ser reutilizados. Renomear exige redirecionamento editorial.

## Dimensões

Valores aceitos editorialmente: perigo, exposição, vulnerabilidade, efeito sobre a saúde, capacidade de resposta, adaptação e resiliência. Mais de um valor é permitido quando a justificativa estiver na definição e no método.

## Disponibilidade

Use somente:

- disponível para consulta;
- disponível para download;
- cálculo simples;
- requer geoprocessamento;
- requer modelagem;
- sem produção regular.

O selo indica esforço de obtenção, não qualidade.

## Fluxo

1. Copiar `indicators/templates/ficha.yml`.
2. Preencher todos os campos.
3. Cadastrar as fontes por ID em `sources/data/sources.yml`.
4. Adicionar referências verificadas a `references.bib`.
5. Executar `make catalogs`.
6. Revisar a página gerada em HTML e PDF.
7. Incluir a ficha na ordem do livro quando aprovada.

Arquivos em `indicators/pages/` são gerados e não devem ser editados manualmente.

## Fichas demonstrativas

- `CLI-TEM-01`: temperatura máxima diária;
- `CLI-CAL-01`: onda de calor;
- `AMB-AR-01`: concentração média diária de PM2,5.

Os campos metodológicos estão completos no nível de protótipo. Limiares, licenças, períodos e formatos não verificados permanecem como tarefas explícitas.

