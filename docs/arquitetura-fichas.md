# Arquitetura das fichas de indicadores

## Solução escolhida

Cada conjunto de fichas é mantido em YAML em `indicators/data/`. O script `scripts/build_catalogs.R` valida os registros, resolve IDs de fontes, produz trechos Quarto em `indicators/includes/` e atualiza os índices. Os trechos são incorporados ao capítulo do fenômeno, e não publicados como capítulos autônomos.

Essa abordagem foi escolhida porque:

- Mantém revisão campo a campo;
- Gera HTML e PDF com o mesmo conteúdo;
- Permite filtros futuros por tema, dimensão, fonte e disponibilidade;
- Evita um filtro Lua complexo;
- Torna códigos e campos obrigatórios validáveis;
- Preserva páginas legíveis e vinculáveis.

CSV foi descartado porque textos longos, listas e fórmulas ficam frágeis. Metadados apenas no cabeçalho `.qmd` misturariam dado estruturado e apresentação. Um banco ou ambiente Python seria desproporcional.

## Código

O padrão é `AAA-BBB-00`, com prefixos de domínio e medida. Códigos publicados não devem ser reutilizados. Renomear exige redirecionamento editorial.

## Dimensões

Valores aceitos editorialmente: perigo, exposição, vulnerabilidade, efeito sobre a saúde, capacidade de resposta, adaptação e resiliência. Mais de um valor é permitido quando a justificativa estiver na definição e no método.

## Disponibilidade

Use somente:

- Disponível para consulta;
- Disponível para download;
- Cálculo simples;
- Requer geoprocessamento;
- Requer modelagem;
- Sem produção regular.

O selo indica esforço de obtenção, não qualidade.

## Fluxo

1. Copiar `indicators/templates/ficha.yml`.
2. Preencher todos os campos.
3. Cadastrar as fontes por ID em `sources/data/sources.yml`.
4. Adicionar referências verificadas a `references.bib`.
5. Executar `make catalogs`.
6. Revisar a página gerada em HTML e PDF.
7. Incluir o trecho gerado no capítulo temático correspondente.

Arquivos em `indicators/includes/` são gerados e não devem ser editados manualmente.

## Núcleo RIPSA 2026

A estrutura obrigatória acompanha os 16 campos da Ficha de Qualificação do Indicador (FQI) descritos na terceira edição de *Indicadores Básicos para a Saúde no Brasil*:

1. Código da RIPSA;
2. Título completo;
3. Título resumido;
4. Conceito;
5. Interpretação;
6. Usos;
7. Limitações;
8. Fontes de dados;
9. Fórmula de cálculo;
10. Método de cálculo;
11. Variáveis e categorias de análise;
12. Granularidade;
13. Periodicidade de atualização;
14. Responsabilidade gerencial;
15. Notas;
16. Análise descritiva do indicador.

Os códigos deste livro têm taxonomia própria e não devem ser confundidos com códigos oficiais da RIPSA. “Código da RIPSA” é, aqui, implementado como o identificador editorial do indicador, mantendo a mesma função de identificação sem alegar inclusão no portfólio da Rede.

O campo de análise descritiva informa quais distribuições, estratos, verificações de cobertura, qualidade e incerteza devem acompanhar o indicador. Resultados empíricos dependentes de um território e período não são inventados.

## Extensões para clima, ambiente e saúde

O YAML acrescenta objetivo, tema, dimensões analíticas, unidade territorial, resolução espacial original, resolução temporal, período e limiar de referência, disponibilidade, acesso, processamento, qualidade e incerteza, comparabilidade, relação com desfechos de saúde, defasagens temporais e aplicação na gestão.

“Granularidade” e “resolução espacial original” não são sinônimos. A primeira registra a desagregação máxima recomendada do indicador; a segunda registra o suporte nativo do dado antes de qualquer agregação.

`fontes_dados` é uma lista estruturada com `id` e `papel`. O ID resolve um cadastro em `sources/data/sources.yml`; o papel distingue, por exemplo, observação primária de fonte secundária modelada.

## Tipos de registros de fontes

Cada registro de fonte declara um único `tipo_registro`: instituição, unidade institucional, programa, sistema de informação, plataforma, base de dados, produto, serviço ou cadastro provisório. Bases, produtos, painéis e APIs associados aparecem separadamente em `recursos_relacionados` e `api`.

Essa separação evita atribuir a uma instituição características que pertencem a um produto específico, ou tratar uma interface de consulta como se fosse a base de origem.

## Catálogo da edição

A versão 0.9.0 contém 62 fichas integradas. O catálogo cobre temperatura e ondas de calor, precipitação e seca, qualidade do ar e fumaça, água e saneamento, vegetação e ambiente urbano, desastres, vulnerabilidade, efeitos em saúde e resiliência do sistema de saúde. Cada ficha declara a referência metodológica que sustenta sua definição.
