# Arquitetura das fichas de indicadores

## Solução escolhida

Cada conjunto de fichas é mantido em YAML em `indicators/data/`. O script `scripts/build_catalogs.R` valida os registros, resolve IDs de fontes, produz trechos Quarto em `indicators/includes/` e atualiza os índices. Os trechos são incorporados aos nove capítulos de fichas da Parte IV, numerados de 16 a 24. O campo `capitulo` identifica o capítulo de contexto nas partes II/III; `capitulo_fichas` identifica o destino da ficha. Ambos são obrigatórios. Os identificadores `sec-<código>` pertencem às fichas; os antigos destinos mantêm âncoras HTML junto das remissões, sem duplicar identificadores na impressão.

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
7. Incluir o trecho gerado no capítulo de fichas da Parte IV e referenciá-lo no capítulo de contexto.

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

## Protocolo de cálculo da Parte II

As 52 fichas da Parte II (45 revisadas e sete inclusões) usam `protocolo_versao`, `situacao_calculo`, `dependencia_dados_locais`, `automacao`, `condicoes_automacao`, `evidencia_verificacao` e `detalhe_verificacao`. O gerador valida esses campos e imprime a distinção entre disponibilidade, dependência local e alcance do teste.

- Dados abertos (`abertos`): calculável com produtos abertos especificados, observados ou modelados; pode exigir cadastro gratuito.
- Dados locais centralizados (`centralizados`): depende de medições locais já reunidas em uma base pública; a cobertura continua limitada à rede.
- Dados locais (`locais`): depende de levantamento ou registro local não demonstrado em uma base nacional suficiente.

A evidência distingue documentação, acesso e acesso com cálculo testado. Um teste parcial deve declarar seu alcance; nenhum rótulo afirma que a série nacional já foi produzida. Nas fichas versionadas, campos individuais prevalecem sobre valores comuns herdados do YAML.

## Tipos de registros de fontes

Cada registro de fonte declara um único `tipo_registro`: instituição, unidade institucional, programa, sistema de informação, plataforma, base de dados, produto, serviço ou cadastro provisório. Bases, produtos, painéis e APIs associados aparecem separadamente em `recursos_relacionados` e `api`.

Essa separação evita atribuir a uma instituição características que pertencem a um produto específico, ou tratar uma interface de consulta como se fosse a base de origem.

## Catálogo da edição

A versão 0.9.0 contém 64 fichas na Parte IV e 52 fontes cadastradas. O catálogo cobre temperatura e ondas de calor, precipitação e seca, qualidade do ar e fumaça, água e saneamento, vegetação e ambiente urbano, desastres, vulnerabilidade, efeitos em saúde e resiliência do sistema de saúde. Cada ficha declara a referência metodológica que sustenta sua definição.

A revisão da Parte III (protocolo 2026-10-06) mantém 12 fichas operacionais: duas de vulnerabilidade/habitação, três de saúde e sete de resposta. Os sete códigos retirados ou substituídos permanecem reservados, com notas nos destinos antigos da Parte IV. `indicators/protocols/parte-iii.yml` registra os grupos e parâmetros; os CSVs de universo/avaliação estão vazios e o CSV OMS contém apenas pesos oficiais normalizados. Os capítulos 22–24 incorporam os componentes do IVS, os pesos etários e o dicionário local. Os cálculos de séries serão implementados em outro repositório.

A evidência empírica desta revisão está em `data-raw/parte-iii/verificacao.json`: consulta SIDRA 9933, Rio de Janeiro, 2022, com resposta original e checksum. As demais fichas tiveram conferência documental; não foram produzidas séries SIM/SIH, valores eSPAR ou avaliações locais. A tabela populacional `popsvs2024br.def` foi identificada na página oficial do Ministério, mas as tentativas de acesso direto expiraram. A ficha exige denominadores publicados, inclusive as faixas 80–84/85+ para padronização; não autoriza reconstruí-los quando ausentes.
