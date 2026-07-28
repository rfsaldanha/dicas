# Relatório da versão para revisão editorial

## Identificação

- Versão editorial: 0.1.0 — revisão inicial.
- Data de consolidação: 28 de julho de 2026.
- Árvore de conteúdo: uma única fonte Quarto para HTML e PDF.
- Artefatos: `_output/web/index.html` e `_output/print/dados-indicadores-clima-ambiente-saude.pdf`.

## Escopo consolidado

A versão contém 14 capítulos em quatro partes. Os capítulos 2 e 5 estão desenvolvidos como modelos. Os demais contêm somente descrição breve, limite editorial, tópicos, indicadores previstos quando aplicável e tarefas explícitas.

| Capítulo | Estado | Fronteira principal |
|---|---|---|
| 1. Clima, ambiente e saúde pública | estrutura | vocabulário e caminhos conceituais, sem repetir métodos |
| 2. Dados, variáveis, índices e indicadores | desenvolvido | fundamentos da mensuração e da decisão |
| 3. Espaço, tempo e qualidade | estrutura | tratamento transversal, sem métodos temáticos |
| 4. Fontes e fichas | estrutura estabilizada | documentação da fonte e arquitetura das fichas |
| 5. Temperatura e condições térmicas | desenvolvido | mensuração térmica; uso da terra fica no capítulo 9 |
| 6. Precipitação e hidrologia | estrutura | processos físicos; registros de desastre ficam no capítulo 10 |
| 7. Qualidade do ar e fumaça | estrutura + ficha | concentração e exposição; uso da terra e efeitos ficam fora |
| 8. Água e saneamento | estrutura | condição ambiental e serviços; desfechos ficam no capítulo 12 |
| 9. Uso da terra e ambiente urbano | estrutura | determinantes territoriais; mensuração térmica fica no capítulo 5 |
| 10. Eventos severos e desastres | estrutura | registros, danos, resposta e recuperação |
| 11. Exposição e vulnerabilidade | estrutura | condições anteriores ou concomitantes ao efeito |
| 12. Efeitos sobre a saúde | estrutura | desfecho, desenho analítico e inferência |
| 13. Resposta, adaptação e resiliência | estrutura | capacidade mensurável do SUS |
| 14. Indicador e decisão | estrutura | integração em fluxos decisórios, sem nova taxonomia |

Não foram identificadas lacunas estruturais que impeçam a revisão inicial. Permanecem decisões futuras sobre saúde mental, saúde ocupacional, justiça climática e avaliação econômica, que podem ser aprofundadas nos capítulos já previstos sem criar, nesta fase, novas partes.

## Fichas e RIPSA

As fichas `CLI-TEM-01`, `CLI-CAL-01` e `AMB-AR-01` foram comparadas com a terceira edição de *Indicadores Básicos para a Saúde no Brasil* (2026), especialmente a descrição da FQI revista em 2024.

O validador exige os 16 campos do núcleo:

1. código;
2. título completo;
3. título resumido;
4. conceito;
5. interpretação;
6. usos;
7. limitações;
8. fontes de dados;
9. fórmula de cálculo;
10. método de cálculo;
11. variáveis e categorias de análise;
12. granularidade;
13. periodicidade de atualização;
14. responsabilidade gerencial;
15. notas;
16. análise descritiva.

O código local não alega pertencimento ao portfólio oficial da RIPSA. O campo de análise descritiva permanece pendente, com pré-condições explícitas, porque não há série, território, período e visualização validados nesta versão.

As extensões climáticas e ambientais aparecem em bloco separado: resolução espacial original, resolução temporal, período e limiar de referência, disponibilidade e acesso, processamento, qualidade e incerteza, comparabilidade, relação com a saúde, defasagens e aplicação na gestão.

## Cadastro de fontes

Os 14 registros declaram um `tipo_registro` único. A distribuição é:

- três instituições;
- duas unidades institucionais;
- dois programas;
- dois sistemas de informação;
- duas plataformas;
- um produto;
- um serviço;
- um cadastro provisório.

Bases, produtos, painéis e APIs relacionados são descritos separadamente. Campos não confirmados continuam marcados como `TODO`; não foram completados por inferência.

## Auditoria visual do site

Foram inspecionadas a página inicial, o capítulo conceitual, o capítulo de temperatura, uma ficha e o índice de fontes. A inspeção cobriu navegação lateral, sumário local, hierarquia, links, cartões, tabela e contraste.

Foram geradas prévias locais de 1440 px e 390 px. A folha de estilos contém tratamento específico abaixo de 620 px, com cartões em uma coluna e tabelas com rolagem horizontal. A miniatura de 390 px do Quick Look reduz o canvas em vez de emular integralmente um navegador móvel; por isso, a interação responsiva final deve ser confirmada também no navegador usado pela equipe editorial.

A busca está habilitada, `search.json` é gerado e as páginas de capítulos, fichas e índices estão presentes no índice. A execução interativa da caixa de busca não integra o pré-voo automatizado.

## Auditoria visual do PDF

O PDF tem formato exato de 155 × 230 mm, fontes incorporadas, margens espelhadas e composição em preto e branco. Foram examinadas páginas de título, sumário, aberturas de partes, capítulos 2 e 5, chamadas, três fichas, índices, tabela de fontes, registros detalhados, apêndice e bibliografia.

Correções feitas durante a auditoria:

- data de título estabilizada em 2026-07-28;
- subtítulo encurtado para evitar hifenização isolada na página de título;
- chamadas convertidas de cores semânticas para cinza;
- rótulos e valores das fichas mantidos no mesmo parágrafo;
- títulos de segundo nível configurados para acompanhar o conteúdo seguinte;
- índices impressos reduzidos a colunas compatíveis com o miolo.

As partes e os capítulos começam em páginas ímpares. Os versos automáticos mantêm apenas o fólio; essa é uma decisão provisória a revisar no fechamento gráfico. O PDF permanece muito abaixo da meta final de 400–500 páginas porque esta entrega não contém o livro completo.

## Validação técnica

O fluxo de validação cobre:

- geração e validação de três fichas e 14 fontes;
- presença e ordem dos 14 capítulos;
- chaves bibliográficas citadas;
- arquivos HTML, links locais e âncoras;
- referências cruzadas não resolvidas;
- presença do índice de busca;
- tamanho do PDF, incorporação de fontes e elementos editoriais esperados.

Comandos de aceite:

```sh
quarto render
quarto render --profile web
quarto render --profile print
make
Rscript scripts/validate_project.R
git diff --check
```

## Pendências deliberadas

- desenvolvimento dos 12 capítulos estruturais;
- revisão bibliográfica das fichas e capítulos;
- seleção territorial da rede de qualidade do ar;
- confirmação de períodos, licenças, formatos, custos, cadastros e APIs;
- validação de limiares e normas vigentes;
- séries e análises descritivas;
- capa final, ISBN, ficha catalográfica e créditos institucionais definitivos;
- fechamento tipográfico e paginação final.

Essas pendências estão visíveis e não impedem a revisão da arquitetura, dos capítulos-modelo, das fichas ou do sistema de fontes.
