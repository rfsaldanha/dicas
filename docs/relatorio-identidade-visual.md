# Prova da identidade visual

Verificação realizada em 3 de outubro de 2026. A identidade “Território, evidência e cuidado” foi aplicada à capa frontal, ao miolo e à edição web. As regras de manutenção estão no [guia editorial](guia-editorial.md#identidade-visual-território-evidência-e-cuidado).

## Arquivos para revisão

- [Prova reunida](../_output/proofs/identidade-visual.pdf): capa, folha de rosto, abertura de parte, capítulo, figura, ficha extensa e capturas da web.
- [Capa frontal colorida](../_output/cover/capa.pdf), com [composição editável](../assets/cover/capa.typ).
- [Miolo completo](../_output/print/dados-indicadores-clima-ambiente-saude.pdf), em escala de cinza.
- [Página inicial web](../_output/web/index.html).
- [Figura ampliada em desktop](../_output/proofs/web-figura-ampla.png) e [em celular](../_output/proofs/web-figura-celular.png).

## Layout web

A coluna foi ampliada no grid do Quarto para 672 px. A largura efetiva do texto no desktop de 1440 px é 621 px, descontados os espaços do grid. A configuração `fig-column: page-right` permite que as figuras ocupem também a margem direita. A figura de abertura usa 866,5 px nessa tela: cerca de 40% mais largura que o texto. O índice se recolhe nas regiões de sobreposição e a navegação esquerda permanece livre. Trata-se do comportamento nativo descrito na [documentação de layout do Quarto](https://quarto.org/docs/authoring/article-layout.html#overflowing-content).

O número do capítulo permanece integrado à primeira linha do título. No celular, as figuras respeitam a largura disponível; fórmulas e tabelas extensas podem rolar dentro de seus próprios contêineres. As aquarelas mantêm fundo branco nos dois temas.

As 32 páginas foram abertas em Chrome, com larguras de 390 e 1440 px: nenhuma imagem ausente e nenhuma rolagem horizontal da página. Também foram conferidos carregamento das fontes locais, foco visível, número do capítulo e alternância dos temas. Os registros estão em [web-check.json](../_output/proofs/web-check.json) e [layout-check.json](../_output/proofs/layout-check.json).

Os contrastes calculados entre os principais textos e fundos são 11,64:1 para texto claro, 5,85:1 para links claros, 12,59:1 para texto escuro e 8,64:1 para links escuros. Texto secundário e a variante textual de atenção também superam 4,5:1.

## Impressão e capa

O miolo atual tem 528 páginas de 160 × 230 mm, com as margens preservadas. A paginação inclui a organização editorial atual dos capítulos. A folha de rosto é monocromática; a capa colorida é um arquivo separado. Aberturas de parte usam título, rubrica e filete; capítulos usam número discreto acima do título. Fichas mantêm códigos, campos e relações, com rubricas em Source Sans 3 e divisões leves.

O pré-voo confirmou fontes incorporadas, imagens raster em escala de cinza com pelo menos 300 ppi e total de páginas múltiplo de quatro. A distância entre linhas consecutivas de texto corrido foi conferida no PDF em 14 pt. Páginas vazias não recebem cabeçalho ou fólio. As páginas selecionadas do miolo são 1, 19, 21, 26 e 180–183; a ficha CLI-TEM-01 atravessa as quatro últimas páginas da seleção.

A ilustração original da capa foi produzida com a ferramenta integrada `image_gen`, sem reamostragem: 1536 × 1024 pixels, usados a 128 mm de largura, equivalentes a 304,8 ppi. O [prompt](../assets/cover/territorio-e-cuidado-v1.prompt.txt), a [arte](../assets/cover/territorio-e-cuidado-v1.png) e os [créditos](../assets/cover/credits.json) estão preservados. As fontes OTF e WOFF2 acompanham o projeto com suas licenças.

## Validação e limites da prova

`Rscript scripts/validate_project.R` passou: 15 capítulos, 62 fichas, 25 fontes, 32 páginas HTML, links e âncoras íntegros e PDF válido. Os estilos foram inspecionados visualmente em capturas e páginas do PDF; a avaliação do papel e da reprodução física dos tons de cinza requer impressão da prova em tamanho real. A capa ainda é uma composição frontal: lombada, contracapa e sangria de produção serão dimensionadas no fechamento gráfico.
