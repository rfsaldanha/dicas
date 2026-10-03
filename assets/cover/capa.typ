// Capa frontal de apresentação: sem lombada ou sangria de produção.
// Compilar na raiz: quarto typst compile --root . --font-path assets/fonts \
//   assets/cover/capa.typ _output/cover/capa.pdf
#let book = yaml("../../_quarto.yml").book
#set document(title: book.title, author: book.author)
#set page(width: 160mm, height: 230mm, margin: 0mm, fill: white)
#set text(font: "Libertinus Serif", fill: rgb("#536b50"), size: 28pt,
  top-edge: 0.75em, bottom-edge: 0.25em, weight: "regular", lang: "pt")
#set par(justify: false, leading: 4pt)
#place(top + left, dx: 18mm, dy: 28mm)[
  #block(width: 124mm)[
    Dados e Indicadores \
    de Clima e Ambiente \
    para a Saúde
  ]
]
// 1536 px a 128 mm: resolução efetiva de 304,8 ppi, sem reamostragem.
#place(top + left, dx: 16mm, dy: 100mm)[
  #image("territorio-e-cuidado-v1.png", width: 128mm,
    alt: "Profissional de saúde conversa com uma moradora idosa e um familiar à sombra de uma árvore; ao fundo, moradias, unidade de saúde, vegetação e um rio.")
]
#place(bottom + left, dx: 18mm, dy: -21mm)[
  #text(font: "Source Sans 3", size: 11pt, fill: rgb("#303b36"), book.author)
]
