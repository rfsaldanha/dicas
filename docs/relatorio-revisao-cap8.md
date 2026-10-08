# Revisão do capítulo 8

Registro de 8 de outubro de 2026.

As saídas desta revisão estão em [`_output/revisao-cap8`](../_output/revisao-cap8/):
[HTML do capítulo](../_output/revisao-cap8/web/chapters/part-2/08-precipitacao-secas-eventos-hidrologicos.html)
e [PDF do livro](../_output/revisao-cap8/print/dados-indicadores-clima-ambiente-saude.pdf).
Os arquivos editáveis do capítulo e das figuras permanecem nas pastas usuais do projeto.

## Entrega editorial

O [capítulo revisado](../chapters/part-2/08-precipitacao-secas-eventos-hidrologicos.qmd)
mantém nove seções principais, amplia as três subseções de precipitação e apresenta
sete subseções sobre os caminhos até a saúde. A seção de síntese foi suprimida.
A introdução distingue fenômeno, exposição, consequências e desastre, articulando
chuva habitual e extremos a água, vetores, alimentos, ar, saúde mental e cuidado.

O texto contém 34 referências bibliográficas distintas e 139 remissões Quarto a
capítulos, fichas e apêndices. O quadro de indicadores inclui as sete fichas,
com PRCPTOT. Não foram criadas fichas nem séries calculadas nesta revisão. As
regras operacionais de ERA5-Land, CHIRPS, SPI-3, períodos-base, lacunas, viradas de
ano e agregação espacial foram conferidas com as fichas existentes.

Foram incorporadas nove fontes, incluindo o [estudo brasileiro de Lowe et al.](https://researchonline.lshtm.ac.uk/id/eprint/4660590/1/2021_lowe_LancetPlanHealth.pdf)
e o [plano de seca e estiagem do Ministério da Saúde de 2026](https://www.gov.br/saude/pt-br/centrais-de-conteudo/publicacoes/svsa/vigilancia-ambiental/plano-de-contingencia-seca-e-estiagem.pdf/@@download/file).
As demais adições abordam SPEI, saúde mental após inundações, leptospirose,
movimentos de massa, ameaças e alertas do Cemaden e acumulação ERA5-Land.
O endereço da referência da OMS sobre seca foi corrigido. Páginas sem data de
publicação informada conservam a data de acesso, sem atribuição de ano presumido.
O crédito sobre métodos de pesquisa em emergências foi alinhado à edição de 2022.

## Figuras e navegação

Foram entregues 20 SVGs coloridos e 20 PNGs de impressão em cinza: 11 composições
com aquarelas e 9 diagramas vetoriais. A distribuição é uma figura na introdução,
nove nas seções principais e dez nas subseções. Todas são chamadas no texto,
têm legenda, texto alternativo, crédito e indicação de fonte. A lista de figuras
foi atualizada; os dois quadros numerados conservaram seus identificadores.

As aquarelas foram produzidas com a skill imagegen, a partir da referência visual
do projeto e das composições da série. Os textos e as setas permanecem editáveis
nos SVGs. Originais, prompts, dimensões, hashes, referências e procedimentos estão
no [registro de produção](../assets/figures/arte-cap8-manifest.json) e no
[gerador das composições](../scripts/build_cap8_art.py). As cenas são hipotéticas
e os diagramas são conceituais; não representam observações quantitativas.

Os identificadores `fig-cadeia-hidrometeorologica` e `fig-processos-hidrologicos`
foram preservados. A segunda figura foi posicionada na seção de inundações,
alagamentos e enxurradas. O endereço antigo do capítulo, as sete âncoras de
compatibilidade e os retornos das sete fichas ao contexto foram mantidos.
O HTML permite ampliar as figuras por clique.

## Verificações

| Verificação | Resultado |
|---|---|
| Estrutura editorial | Nove seções, dez subseções e ausência de síntese |
| Cobertura visual | Vinte figuras, uma por trecho; arquivos e metadados íntegros |
| Navegação | Destinos HTML, âncoras antigas e retornos das fichas conferidos |
| Referências cruzadas | Sem remissões não resolvidas no capítulo |
| Citações | Todas as chaves presentes na bibliografia; nenhuma chave duplicada |
| Rótulos SVG | Nenhum texto fora da prancha ou dos painéis verificados |
| Navegador | Desktop 1440 × 1000 e celular 390 × 844; temas claro e escuro |
| Figuras e quadros em tela | 80 provas de figuras e 8 de quadros; sem transbordamento horizontal da página |
| Interação | Navegação Rx1day–capítulo e abertura/fechamento da ampliação conferidos |
| Impressão | Vinte figuras presentes; cinza, fontes incorporadas e imagens acima de 300 ppi |
| Composição | Páginas do capítulo inspecionadas, incluindo quadros, créditos e figuras em escala de leitura |
| Validação da edição isolada | Catálogos, estrutura do livro, links internos, apêndices, testes da Parte III e pré-voo aprovados |

A compilação completa foi executada sequencialmente: HTML, PDF e
`Rscript scripts/validate_project.R`. O verificador específico é
[`scripts/check_cap8.py`](../scripts/check_cap8.py), também integrado ao validador
do projeto. As provas e os registros estão em
[`_output/proofs/revisao-cap8`](../_output/proofs/revisao-cap8/).

## Impressão e reprodução

O PDF entregue tem 748 páginas. formato 160 × 230 mm e 107.111.506 bytes. O capítulo 8 ocupa as páginas 231–264. As vinte imagens do capítulo têm resolução efetiva mínima de 586.2 ppi no PDF; os originais das aquarelas mantêm ao menos 455,3 ppi para a largura máxima declarada.

A primeira compilação ultrapassou o limite de 150 MB do projeto. Foi incorporada
uma [etapa de compressão sem perda](../scripts/optimize_pdf.py) antes do pré-voo.
Ela usa predição PNG nos fluxos das imagens em cinza, sem reduzir resolução nem
alterar pixels. Confere novamente texto, paginação, sumário, quantidade de links
e hashes dos pixels decodificados antes de substituir o PDF. Alterações
concorrentes no arquivo cancelam a substituição.

As dependências opcionais e o uso de `DICAS_PYTHON` estão no
[guia de compilação](guia-de-compilacao.md) e em
[`requirements-print.txt`](../requirements-print.txt).

## Observações de verificação

Houve revisões e compilações simultâneas de outros capítulos. Uma versão completa
passou na validação; durante o ajuste bibliográfico final, novas edições dos
capítulos 11 e 12 passaram a conter referências a figuras ainda não incluídas.
Isso bloqueou a compilação compartilhada. Para concluir esta entrega, a edição
em `_output/revisao-cap8` foi compilada em uma cópia independente, usando nesses
dois capítulos as versões completas do commit
`7e3ff51159c81635db3929b26a45176aa373b0aa`, inclusive suas entradas nas listas de
figuras e quadros. As demais alterações disponíveis no momento da cópia foram
mantidas. Nenhum arquivo de trabalho das revisões paralelas foi revertido.

O novo teste específico da revisão do capítulo 12 foi excluído somente do
acionamento na cópia isolada, porque exige a estrutura e as figuras ainda em
produção. Permaneceram ativos os testes gerais do livro e os verificadores das
revisões incluídas. O validador do projeto de trabalho foi preservado.

`compilacao-isolada.json` registra essa composição. Os hashes em
`arquivos-verificados.json` identificam precisamente os arquivos conferidos.
A atualização das saídas compartilhadas do projeto depende da conclusão das
revisões concorrentes; a edição isolada contém a revisão final do capítulo 8.

O `pdfinfo` 24.02.0 emite o aviso `Suspects object is wrong type (boolean)` para
`/Suspects false`. A [implementação do Poppler consultada](https://skia.googlesource.com/third_party/poppler/%2B/bb547a3ccbcd1b2965708542981cd7e9cf46d3bf/poppler/Catalog.cc)
mostra que esse ramo reporta o booleano falso como erro. O pré-voo, a extração de
texto e a rasterização passaram. Não se removeu a marcação de acessibilidade do PDF.

A conferência de impressão foi digital, com provas a 150 dpi e inspeção em
escala equivalente a 100% a 96 dpi; não foi feita prova física em gráfica.
