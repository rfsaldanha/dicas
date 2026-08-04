#import "@preview/orange-book:0.7.1": book

// O sumário deste projeto já ocupa uma posição editorial explícita entre os
// elementos pré-textuais. Suprime apenas o sumário automático do modelo.
#show outline: it => if it.title == auto { none } else { it }

// Verso sintético para a edição de revisão. A ficha técnica completa segue
// no corpo pré-textual do livro.
#let copyright-page = [
  #set text(size: 9pt)
  #set par(first-line-indent: 0pt, leading: 0.35em, spacing: 0.7em)
  #align(center + horizon)[
    #block(width: 96mm)[
      #align(center)[
        *Dados e Indicadores de Clima e Ambiente para a Saúde*

        Guia para vigilância e gestão pública

        #v(4mm)

        © 2026 Raphael de Freitas Saldanha

        Primeira edição — versão para revisão editorial

        #v(4mm)

        Composição editorial com Quarto e Typst.

        Impressão sob demanda: UICLAP.

        Código-fonte e versão digital:

        #link("https://github.com/rfsaldanha/dicas")[github.com/rfsaldanha/dicas]
      ]
    ]
  ]
]

// Callouts em escala de cinza, com a mesma estrutura compacta do projeto de
// referência e sem transportar as cores semânticas do site para o impresso.
#let callout(
  body: [],
  title: "Destaque",
  background_color: rgb("#dddddd"),
  icon: none,
  icon_color: black,
  body_background_color: white,
) = {
  let print_header = rgb("#dddddd")
  let print_stroke = black
  let print_body = white
  block(
    breakable: false,
    fill: print_header,
    stroke: (paint: print_stroke, thickness: 0.5pt, cap: "round"),
    width: 100%,
    radius: 2pt,
    block(
      inset: 1pt,
      width: 100%,
      below: 0pt,
      block(
        fill: print_header,
        width: 100%,
        inset: (x: 8pt, top: 10pt, bottom: 6pt),
      )[#if icon != none [#text(print_stroke, weight: 900)[#icon] ]#title] +
      if body != [] {
        block(
          inset: 1pt,
          width: 100%,
          block(fill: print_body, width: 100%, inset: 8pt)[
            #set par(first-line-indent: 0pt, spacing: 0.5em)
            #body
          ],
        )
      },
    ),
  )
}

// Complementa a folha de rosto sem criar elementos junto à linha de corte.
#set page(background: context {
  let page-number = counter(page).get().first()
  if page-number == 1 {
    place(bottom + center, dy: -18mm)[
      #set text(size: 10.5pt)
      #set par(first-line-indent: 0pt, leading: 0.35em)
      #align(center)[Brasil\
      Versão para revisão editorial\
      2026]
    ]
  }
})

#show: book.with(
$if(title)$
  title: [$title$],
$endif$
$if(subtitle)$
  subtitle: [$subtitle$],
$endif$
$if(by-author)$
  author: "$for(by-author)$$it.name.literal$$sep$, $endfor$",
$endif$
$if(date)$
  date: "$date$",
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
  width: 160mm,
  height: 230mm,
  margin: (
    inside: 25mm,
    outside: 18mm,
    top: 20mm,
    bottom: 22mm,
  ),
  main-color: black,
  copyright: copyright-page,
  supplement-chapter: "Capítulo",
  supplement-part: "Parte",
$if(fontsize)$
  font-size: $fontsize$,
$endif$
  first-line-indent: true,
  heading-style: 1,
  padded-heading-number: false,
$if(toc-depth)$
  outline-depth: $toc-depth$,
$endif$
)

// Fólios e títulos correntes seguem o padrão do volume de referência:
// abertura no rodapé; demais páginas no cabeçalho, junto ao título corrente.
#set page(
  header: context {
    set text(size: 9pt)
    let page-number = counter(page).at(here()).first()
    let chapter-headings = query(heading.where(level: 1))
    let chapter-opening = chapter-headings.any(
      it => it.location().page() == page-number
    )
    let textual-headings = chapter-headings.filter(it => it.body == [Bem-vindo])
    let textual-start = if textual-headings == () {
      1
    } else {
      textual-headings.first().location().page()
    }

    if page-number >= textual-start and not chapter-opening {
      let chapters-before = query(
        selector(heading.where(level: 1)).before(here())
      )
      if chapters-before != () {
        let current-chapter = chapters-before.last()
        let sections-before = query(
          selector(heading.where(level: 2))
            .after(current-chapter.location())
            .before(here())
        )
        let running-title = if calc.odd(page-number) and sections-before != () {
          sections-before.last().body
        } else {
          current-chapter.body
        }

        box(
          width: 100%,
          inset: (bottom: 5pt),
          stroke: (bottom: 0.5pt),
        )[
          #set par(justify: false)
          #if calc.odd(page-number) {
            grid(
              columns: (1fr, auto),
              align: (left + horizon, right + horizon),
              column-gutter: 0.4em,
              text(size: 8.5pt, running-title),
              numbering("1", page-number),
            )
          } else {
            grid(
              columns: (auto, 1fr),
              align: (left + horizon, right + horizon),
              column-gutter: 0.4em,
              numbering("1", page-number),
              align(right, text(size: 8.5pt, weight: "bold", running-title)),
            )
          }
        ]
      }
    }
  },
  footer: context {
    let page-number = counter(page).at(here()).first()
    let chapter-headings = query(heading.where(level: 1))
    let chapter-opening = chapter-headings.any(
      it => it.location().page() == page-number
    )
    let textual-headings = chapter-headings.filter(it => it.body == [Bem-vindo])
    let textual-start = if textual-headings == () {
      1
    } else {
      textual-headings.first().location().page()
    }
    if page-number >= textual-start and chapter-opening {
      align(center, numbering("1", page-number))
    }
  },
)

#set par(spacing: 0.65em)
// Mermaid's SVG serializer emits a lowercase `viewbox` attribute. SVG attribute
// names are case-sensitive, so Typst otherwise ignores the view box and clips
// diagrams to their nominal canvas. Normalize the attribute while embedding the
// SVG and constrain it to the printable text area.
#show image: it => {
  let source = it.source
  if str(source).ends-with(".svg") {
    let svg = read(source)
    let normalized = svg
      .replace("viewbox=", "viewBox=")
      .replace(" width=\"528\"", "", count: 1)
      .replace(" height=\"336\"", "", count: 1)
    let bounds = normalized.match(
      regex("viewBox=\"0 0 ([0-9.]+) ([0-9.]+)\"")
    )
    let ratio = if bounds == none { 1.0 } else {
      float(bounds.captures.at(0)) / float(bounds.captures.at(1))
    }
    if ratio < 0.8 {
      image(
        bytes(normalized),
        format: "svg",
        height: 125mm,
        fit: "contain",
        alt: it.alt,
      )
    } else {
      image(
        bytes(normalized),
        format: "svg",
        width: 100%,
        fit: "contain",
        alt: it.alt,
      )
    }
  } else {
    it
  }
}
#show table: set text(size: 9.5pt, hyphenate: true)
#show table: set par(spacing: 0.5em, justify: false)
#show bibliography: set par(spacing: 0.8em)
#show link: set text(hyphenate: false)
