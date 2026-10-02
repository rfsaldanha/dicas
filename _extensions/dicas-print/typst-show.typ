#import "@preview/orange-book:0.7.1": book

// O sumário deste projeto já ocupa uma posição editorial explícita entre os
// elementos pré-textuais. Suprime apenas o sumário automático do modelo.
#show outline: it => if it.title == auto { none } else { it }

// Verso da folha de rosto, com créditos editoriais e área reservada para
// a ficha catalográfica. Os campos ainda não atribuídos permanecem explícitos.
#let copyright-page = [
  #set text(size: 9pt)
  #set par(first-line-indent: 0pt, leading: 0.35em, spacing: 0.6em)

  #block(width: 100%)[
    #grid(
      columns: (38mm, 1fr),
      column-gutter: 4mm,
      row-gutter: 2mm,
      align: (left + top, left + top),
      [*Direitos autorais*], [© 2026 Raphael de Freitas Saldanha],
      [*Créditos editoriais*], [Raphael de Freitas Saldanha],
      [*Editora*], [Edição do autor],
      [*ISBN*], [Não atribuído],
      [*Impressão*], [UICLAP],
    )

    #v(6mm)

    Esta publicação e seu código-fonte estão disponíveis em
    #link("https://github.com/rfsaldanha/dicas")[github.com/rfsaldanha/dicas].
    Os arquivos autorais seguem a licença GNU General Public License, versão 3;
    fontes de terceiros mantêm suas licenças próprias.

    #v(6mm)

    #block(
      width: 100%,
      height: 80mm,
      inset: 0mm,
      stroke: 0.6pt + black,
    )[]

    #v(2mm)

    #set text(size: 8pt)
    #align(center)[Espaço reservado para a ficha catalográfica]
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
      Edição do autor\
      2026]
    ]
  }
})

// Aberturas de parte: composição própria, em escala de cinza, com forte
// contraste entre o algarismo romano, a rubrica editorial e o título. A
// identificação parte do título gerado pelo Quarto, preservando o elemento
// heading original para o sumário e para a navegação interna do PDF.
#let dicas-part-counter = counter("dicas-part-counter")

#let dicas-is-part-title(body) = {
  let value = content-to-string(body)
  value.starts-with("Parte ") or value == "Elementos pós-textuais"
}

#let dicas-is-list-title(body) = {
  let value = content-to-string(body)
  value == "Lista de figuras"
}

#let dicas-part-opening(it) = {
  pagebreak(to: "odd")
  dicas-part-counter.step()

  context {
    let full-title = content-to-string(it.body)
    let short-title = if full-title.starts-with("Parte ") {
      full-title.replace(
        regex("^Parte\s+[IVXLCDM]+\s+[-–—]+\s+"),
        "",
      )
    } else {
      full-title
    }
    let part-number = dicas-part-counter.get().first()
    let roman = numbering("I", part-number)

    set par(justify: false, first-line-indent: 0pt, leading: 0.66em)

    block(width: 100%, height: 100%, breakable: false)[
      #place(top + left, dy: 10mm)[
        #block(width: 100%)[
          #grid(
            columns: (5mm, 1fr, auto),
            column-gutter: 5mm,
            align: (left + top, left + bottom, right + top),
            rect(width: 5mm, height: 34mm, fill: black),
            [
              #text(size: 9pt, weight: "bold", tracking: 0.16em)[PARTE]
              #v(2mm)
              #line(length: 32mm, stroke: 0.7pt + black)
            ],
            text(size: 62pt, weight: "bold", fill: luma(205), roman),
          )
        ]
      ]

      #place(top + left, dy: 57mm)[
        #block(
          width: 100%,
          inset: (top: 8mm),
          stroke: (top: 1.4pt + black),
        )[
          #text(size: 25pt, weight: "bold", short-title)
        ]
      ]

      #place(bottom + left, dy: -4mm)[
        #block(
          width: 100%,
          inset: (top: 4mm),
          stroke: (top: 0.5pt + black),
        )[
          #grid(
            columns: (1fr, auto),
            column-gutter: 6mm,
            align: (left + horizon, right + horizon),
            text(size: 7.5pt, tracking: 0.06em)[
              DADOS E INDICADORES DE CLIMA E AMBIENTE PARA A SAÚDE
            ],
            text(size: 8pt, weight: "bold")[PARTE #roman],
          )
        ]
      ]
    ]
  }
}

#let dicas-book = book.with(
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

#show: body => dicas-book(body)

// O Orange Book usa "1." nos títulos de capítulo. Nas remissões, o ponto
// pertence à frase, não ao número: evita "Capítulo 6.." sem mudar os títulos.
#show ref: it => {
  if it.element != none and it.element.func() == heading and it.element.level == 1 {
    show regex("\\.$$"): none
    it
  } else {
    it
  }
}

// O modelo trata as partes como títulos de nível 1 sem numeração. Esta regra
// substitui apenas essas cinco aberturas; os demais títulos continuam sendo
// compostos normalmente pelo Orange Book.
#show heading.where(level: 1, numbering: none): it => {
  let value = content-to-string(it.body)
  if value == "Apêndices" {
    none
  } else if dicas-is-part-title(it.body) {
    dicas-part-opening(it)
  } else {
    it
  }
}


// Fólios e títulos correntes seguem o padrão do volume de referência:
// abertura no rodapé; demais páginas no cabeçalho, junto ao título corrente.
// A relação corresponde aos versos vazios da prova final e deve ser revista se
// o miolo for repaginado; o conteúdo dessas páginas permanece deliberadamente
// sem cabeçalho e sem fólio.
#let dicas-intentional-blank-pages = (
  132, 246, 346, 348, 370, 408, 446, 466, 468, 476, 498,
)

#set page(
  header: context {
    set text(size: 9pt)
    let page-number = counter(page).at(here()).first()
    let chapter-headings = query(heading.where(level: 1))
    let chapter-opening = chapter-headings.any(
      it => it.location().page() == page-number
    )
    let part-opening = chapter-headings.any(
      it => it.location().page() == page-number and dicas-is-part-title(it.body)
    )
    let intentional-blank = dicas-intentional-blank-pages.contains(page-number)
    let after-part-opening = chapter-headings.any(
      it => it.location().page() + 1 == page-number and dicas-is-part-title(it.body)
    )
    let textual-headings = chapter-headings.filter(it => it.body == [Clima, ambiente e saúde pública])
    let textual-start = if textual-headings == () {
      1
    } else {
      textual-headings.first().location().page()
    }

    if page-number >= textual-start and not chapter-opening and not after-part-opening and not intentional-blank {
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
        let running-title = if calc.odd(page-number) and sections-before != () and not dicas-is-list-title(current-chapter.body) {
          sections-before.last().body
        } else {
          current-chapter.body
        }
        // O título integral permanece no texto; abreviação apenas no cabeçalho.
        let running-title = if running-title == [O que os dados permitem concluir: correlação, causalidade e atribuição] {
          [Correlação, causalidade e atribuição]
        } else {
          running-title
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
    let part-opening = chapter-headings.any(
      it => it.location().page() == page-number and dicas-is-part-title(it.body)
    )
    let intentional-blank = dicas-intentional-blank-pages.contains(page-number)
    let textual-headings = chapter-headings.filter(it => it.body == [Clima, ambiente e saúde pública])
    let textual-start = if textual-headings == () {
      1
    } else {
      textual-headings.first().location().page()
    }
    if page-number >= textual-start and chapter-opening and not part-opening and not intentional-blank {
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
#show table: set text(size: 9pt, hyphenate: false)
#show table: set par(spacing: 0.5em, justify: false)
#show bibliography: set par(spacing: 0.8em)
#set bibliography(title: [Referências])
#show link: set text(hyphenate: false)

// Citações diretas em bloco: composição consistente com o miolo técnico.
#show quote.where(block: true): it => block(inset: (left: 4cm), above: 0.8em, below: 0.8em)[
  #set text(size: 9.5pt)
  #set par(first-line-indent: 0pt, leading: 0.55em, spacing: 0.65em)
  #it.body
]
