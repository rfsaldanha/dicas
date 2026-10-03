# Guia editorial

## Língua e tom

Use português brasileiro, linguagem acessível e tecnicamente precisa. Prefira frases diretas, parágrafos com uma ideia principal e verbos que explicitem a ação. Defina siglas na primeira ocorrência de cada capítulo, inclusive em quadros e legendas, e mantenha a grafia institucional oficial.

Inicie com letra maiúscula cada item de lista numerada ou com marcadores, inclusive quando os itens formarem uma continuação sintática da frase introdutória.

## Maiúsculas, unidades e números

- Use maiúscula em nomes próprios e denominações oficiais, não para dar ênfase.
- Adote unidades do Sistema Internacional e um espaço entre valor e unidade: `35 °C`, `10 µg/m³`.
- Informe unidade em cabeçalhos, eixos, fichas e métodos.
- Use vírgula decimal no texto em português.
- Defina casas decimais conforme precisão da fonte e finalidade; não acrescente precisão aparente.
- Escreva datas como `28 de julho de 2026`; em metadados, use `2026-07-28`.

## Instituições e fontes

Na primeira ocorrência, use nome por extenso e sigla. Diferencie instituição, sistema, programa, portal e conjunto de dados. Registre versão, coleção, rodada, cenário e data de acesso quando aplicável.

## Fórmulas

Apresente fórmula, símbolos, unidade, numerador, denominador e regras de inclusão. Explique em linguagem corrente o que a operação representa. Não use fórmula para encobrir decisão conceitual ou classificação arbitrária.

## Dado, variável, índice e indicador

- Dado é registro ou valor.
- Variável é característica que assume valores.
- Índice é transformação ou síntese.
- Indicador vincula medida, objetivo, método e interpretação.

Não chame uma variável de indicador sem declarar finalidade e leitura. Não use “índice” e “indicador” como sinônimos automáticos.

## Limitações e incerteza

Toda ficha deve registrar limitações de cobertura, medição, suporte, atualização e interpretação. Indique fonte de incerteza e sua consequência prática. Evite o enunciado vazio “os dados podem conter erros”.

Diferencie:

- Observação;
- Estimativa;
- Interpolação;
- Modelagem;
- Reanálise;
- Previsão;
- Projeção.

## Clima e causalidade

Mudança climática altera distribuições, probabilidades e contextos de risco, mas a ocorrência de um evento isolado não autoriza atribuição automática. Afirmações de atribuição exigem método e evidência específicos.

Do mesmo modo, coexistência espacial ou temporal entre exposição e desfecho não demonstra causalidade. Use “associado” somente quando houver análise compatível; use “pode afetar” quando descrever mecanismo sustentado; declare limites.

## Boxes

Use a taxonomia:

- Conceito-chave: definição central;
- Boa prática: recomendação aplicável;
- Atenção: risco de erro ou interpretação;
- Nota técnica: detalhe necessário.

Boxes não substituem desenvolvimento do texto.

## Ênfase tipográfica

Use negrito apenas quando houver uma função editorial que não possa ser expressa pela estrutura do documento. Não o empregue para destacar palavras ou frases no texto corrido. Prefira títulos para agrupamentos, listas de definições para pares entre termos e significados e callouts para conceitos centrais.

Nos callouts, use a rubrica correspondente à taxonomia acima. Conceitos e definições centrais devem aparecer, de preferência, em callouts intitulados “Conceito-chave” ou “Conceito-chave: assunto”.

## Identidade visual: Território, evidência e cuidado

A obra adota a linguagem de um atlas de campo em saúde pública: tipografia de livro, espaço branco, filetes finos e aquarelas que relacionam condições ambientais, território e cuidado. Capa e web usam cor; o miolo permanece monocromático, no formato de 160 × 230 mm, com margens de 25 mm internas, 18 mm externas, 20 mm superiores e 22 mm inferiores.

### Paleta

| Cor | Código web e capa | Uso |
|---|---|---|
| Branco de papel | `#FFFFFF` | Fundo de leitura e continuidade das bordas das aquarelas |
| Grafite esverdeado | `#303B36` | Texto e títulos |
| Verde de vegetação | `#536B50` | Identidade, capa, links e navegação |
| Azul acinzentado | `#597482` | Conceitos e destaques secundários |
| Terracota | `#AE6B50` | Filetes e chamadas de atenção |
| Areia clara | `#F3F0E8` | Navegação e superfícies auxiliares |

Usar branco como superfície predominante. A textura pertence às ilustrações, sem aplicação atrás do texto. A cor deve acompanhar uma rubrica, um rótulo ou uma forma; não pode ser a única distinção. Tons de atenção em texto usam a variante mais escura `#985739`. No modo escuro, usar fundo `#202823`, texto `#EEEAE1`, verde `#B8C9AE`, azul `#B2C7D0` e terracota `#E1B296`; as aquarelas continuam sobre branco, sem inversão ou filtros.

### Tipografia e hierarquia

| Elemento | Impressão | Web |
|---|---|---|
| Texto corrido | Libertinus Serif, 10,5 pt, entrelinha de 14 pt | Libertinus Serif, 19 px, entrelinha de 1,6 |
| Título de capítulo | Libertinus Serif, 25 pt | Libertinus Serif, 2,25 rem; 2 rem em tela estreita |
| Seções | Libertinus Serif, 15 pt | Libertinus Serif, 1,65 rem |
| Rubricas, campos e navegação | Source Sans 3 | Source Sans 3 |
| Legendas e tabelas | 9 pt | 0,95 rem |
| Fonte da figura | Source Sans 3, 8,5 pt | Source Sans 3, 0,85 rem |

As fontes estão incorporadas ao projeto em `assets/fonts`, com versões, licenças e hashes registrados. A edição web serve WOFF2 localmente; a impressão usa OTF. Os SVGs da série de aquarelas contêm sua própria fonte, pois uma imagem SVG externa não herda a tipografia da página HTML.

Na impressão, colocar a rubrica “CAPÍTULO” e o número acima do título. Na web, manter número e título na mesma linha tipográfica, formando um único cabeçalho; o número não deve aparecer isolado. Aberturas de parte usam algarismo romano, título e um filete de 0,5 pt, com espaço generoso. Os cabeçalhos correntes são discretos e as páginas deliberadamente vazias não recebem fólio.

### Capa e abertura web

A capa frontal usa fundo branco, título verde alinhado à esquerda em três linhas — “Dados e Indicadores”, “de Clima e Ambiente”, “para a Saúde” — em Libertinus Serif 28 pt, entrelinha de 32 pt. A cena contínua ocupa a metade inferior; o autor aparece no rodapé em Source Sans 3, 11 pt. A composição editável está em `assets/cover/capa.typ`; prompt, referência, ferramenta e intervenções da ilustração constam no mesmo diretório. A largura de uso da arte é 128 mm, equivalente a 304,8 ppi no original de 1536 pixels.

A página inicial retoma título, autoria e cena da capa. A coluna de leitura usa 672 px no grid nativo do Quarto, aproximadamente 76 caracteres na tipografia adotada; links no texto são sublinhados e controles têm foco visível. Figuras usam `column-page-right` apenas na web: ocupam também a margem direita, com recolhimento automático do índice lateral nas regiões de sobreposição. As legendas permanecem abaixo da figura. No celular, as figuras retornam à largura disponível; fórmulas e tabelas extensas podem rolar dentro da coluna.

### Fichas, quadros e figuras

Fichas usam cabeçalho com filete, código e metadados bem localizados, rótulos em Source Sans 3 e blocos separados por espaço. Usar fundos muito claros e evitar molduras pesadas. Boxes mantêm a rubrica explícita — Conceito-chave, Boa prática, Atenção ou Nota técnica — também no miolo em cinza.

Tabelas estatísticas usam filetes horizontais; quadros textuais mantêm grade fechada com cabeçalho leve. Figuras têm legendas alinhadas à esquerda e notas de fonte separadas. As conexões dos diagramas são finas e regulares; espessuras, tracejados e caixas com significado conceitual devem ser preservados. Não enquadrar as bordas orgânicas das aquarelas com molduras adicionais.

### Prova visual

Conferir capa, abertura de parte, abertura de capítulo, figura e ficha extensa em tamanho real; revisar também a página inicial e uma ficha em desktop e celular, nos dois temas. Verificar incorporação das fontes, entrelinha efetiva, contraste, foco de teclado, rolagem das fórmulas e tabelas, referências cruzadas e ausência de fólio nas páginas vazias. O fechamento do miolo em múltiplos de quatro páginas é automático.

## Recursos visuais

Toda figura deve ter função, legenda, fonte, autoria, licença e texto alternativo. Elementos generativos de IA podem ser usados quando forem adequados à função editorial, desde que recebam direção de arte, revisão humana e tratamento coerente com o padrão técnico da obra, sem aparência genérica ou artificiosamente produzida. Não usar imagem meramente decorativa. Tabelas devem permanecer legíveis no celular e no miolo de 160 × 230 mm.

Gráficos e mapas devem usar dados reais e rastreáveis, nunca valores simulados apresentados como observação. Devem informar fonte, período, unidade, tratamento aplicado e, sempre que possível, ser produzidos por código versionado a partir da fonte original ou de um repositório institucional do autor.

Na etapa de planejamento de arte, marcar o local com um comentário HTML no QMD (`<!-- ... -->`), contendo finalidade, prompt completo, instruções de montagem e legenda proposta. Usar marcadores de produção como `ARTE CAP1-01`, sem atribuir identificadores `fig-` a imagens ainda não produzidas. Os comentários ficam junto aos trechos nos originais e não devem aparecer no conteúdo renderizado do site ou do PDF nem nas listas de figuras.

Ao incorporar a arte aprovada, atribuir identificador `fig-` apenas às figuras novas e acrescentar sua referência no texto, legenda, fonte, autoria, licença e texto alternativo. Nos redesenhos, preservar o identificador existente e a integridade das relações conceituais. A numeração acompanha a ordem das figuras; na revisão do capítulo 1, a ilustração de tempo, clima e ambiente passa a abrir a sequência. Códigos de produção como CAP1-07 não são números editoriais.

### Direção de arte: aquarela, grafite e nanquim

Ilustração editorial em aquarela tradicional translúcida, combinada com traços finos e espontâneos de lápis grafite e nanquim. Contornos parcialmente abertos, hachuras leves e marcas discretas de rascunho. Textura sutil de papel aquarela, pigmentação irregular e transições suaves. Paleta de verdes naturais, azuis acinzentados, ocres e terracota, com saturação moderada. Preservar áreas de papel branco e bordas irregulares que se dissolvem no fundo. Pessoas com proporções naturais e diversidade de tons de pele. Linguagem visual madura, acolhedora e adequada à divulgação científica para adultos.

A referência visual da série foi fornecida pelo autor e está preservada em `assets/references/aquarela-grafite-nanquim.png`. Usá-la em todas as gerações para manter o tratamento de luz, pigmentos, contornos e figuras humanas.

| Elemento | Padrão para toda a série |
|---|---|
| Traço | Traços finos e espontâneos de grafite e nanquim; contornos parcialmente abertos, hachuras leves e marcas discretas de rascunho |
| Água e infraestrutura | Azuis acinzentados, com pigmentação irregular e transições suaves |
| Vegetação e proteção | Verdes naturais, com variação de pigmentos e saturação moderada |
| Calor e pressão ambiental | Ocres e terracota, com saturação moderada |
| Perspectiva | Levemente elevada nas cenas; frontal nos esquemas abstratos |
| Pessoas | Proporções naturais, diversidade de tons de pele, idades e condições de vida; dignidade e ausência de caricaturas |
| Composição | Poucos elementos por vinheta, margens generosas e espaços previstos para textos e conexões |
| Tipografia e conexões | Rótulos e setas acrescentados como elementos editáveis, com a tipografia do livro |
| Escala de cinza | Formas, posição, hachuras e contraste sustentam as distinções também sem cor |

Manter mãos, dedos, braços e pernas anatomicamente coerentes, com proporções naturais, articulações plausíveis e continuidade entre os segmentos. Evitar dedos extras ou fundidos, membros duplicados, torções impossíveis e mãos ou pés disformes. Preferir gestos simples e poses claras, respeitando a perspectiva, as oclusões e as características de cada personagem.

A paleta é uma convenção editorial qualitativa. Cores, intensidades de aguada, tamanhos de personagens e larguras de caminhos não representam magnitudes observadas. Gráficos e mapas construídos com dados mantêm escalas, geometrias, símbolos e legendas tecnicamente adequados; a aquarela pode compor elementos de apoio, sem deformar a informação.

### Prompts e continuidade entre capítulos

Representar a diversidade dos territórios brasileiros ao longo da série: áreas rurais, pequenas cidades, periferias e bairros urbanos densos. Nas cenas urbanas, integrar edifícios residenciais e comerciais, construções de diferentes portes, calçadas, vias pavimentadas, serviços e áreas verdes aos planos principais, com presença legível no tamanho de publicação. Distribuir contextos urbanos entre situações de exposição e de proteção, evitando associar automaticamente prédios a risco ou paisagens rurais a condições favoráveis. Preservar a função científica de cada figura e o espaço necessário aos rótulos; as paisagens permanecem hipotéticas.

Em cenas internas, usar as vistas das janelas e a arquitetura dos serviços para situar o contexto urbano, preservando o foco em pessoas, instrumentos e documentos. Manter áreas abertas ao redor das estações meteorológicas. Não acrescentar construções que possam ser interpretadas como contagens de estabelecimentos, nem alterar o estado de equipamentos, amostras e registros para acomodar a paisagem.

Nas revisões de paisagem, preservar o original e seu prompt e salvar a nova arte e o prompt efetivamente utilizado em arquivos versionados. Atualizar a fonte nos montadores e manifestos, os créditos e os textos alternativos, mantendo os identificadores e os nomes das composições publicadas. Conferir a correspondência entre vistas do mesmo bairro e reutilizar o mesmo raster nos painéis que comparam suportes, escalas ou zoneamentos.

Cada prompt deve conter o padrão visual completo, seguido de função conceitual, composição, proporção e elementos obrigatórios da cena. Os prompts das aquarelas do capítulo 1 usam o mesmo parágrafo de direção de arte. Manter esse parágrafo idêntico nas próximas solicitações e alterar apenas a parte específica de cada imagem. Diagramas exclusivamente vetoriais dispensam geração de aquarela, mantendo tipografia, paleta e acessibilidade.

Anexar `assets/references/aquarela-grafite-nanquim.png` como referência de estilo às solicitações. Quando uma arte existente servir também de referência de conteúdo ou disposição, identificar separadamente o papel de cada imagem. Conferir lado a lado paleta, peso do traço, textura, perspectiva, simplificação dos personagens e densidade de elementos. A constância da série depende da referência visual e da revisão, além do texto do prompt.

Gerar as cenas sem palavras ou números e reservar áreas para os rótulos. Compor setas, textos e legendas na diagramação, conferindo cada relação com o texto científico. Distinguir ilustração conceitual de observação empírica; identificar territórios hipotéticos e propostas conceituais em desenvolvimento quando aplicável.

Na arte final, verificar legibilidade no miolo de 160 × 230 mm e em tela estreita, além da versão em escala de cinza. Exportar o arquivo raster com resolução efetiva mínima de 300 pontos por polegada no tamanho de uso; uma arte com 120 mm de largura requer pelo menos 1.418 pixels nessa dimensão. Preservar também o original de maior resolução e a composição com rótulos editáveis. Registrar ferramenta, versão quando disponível, prompt, imagem de referência, intervenções humanas e condições de uso para completar os créditos da figura.
