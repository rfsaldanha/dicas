
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

// A rubrica textual distingue o tipo de box também na impressão monocromática.
#let callout(
  body: [],
  title: "Destaque",
  background_color: rgb("#f5f5f5"),
  icon: none,
  icon_color: black,
  body_background_color: white,
) = block(
  breakable: true,
  width: 100%,
  inset: (left: 10pt, right: 9pt, y: 9pt),
  fill: luma(247),
  stroke: (left: 0.8pt + luma(80)),
  above: 10pt,
  below: 10pt,
)[
  #set par(first-line-indent: 0pt, spacing: 0.5em)
  #block(below: 5pt, sticky: true)[
    #text(font: "Source Sans 3", size: 10pt, weight: "semibold", title)
  ]
  #body
]

// Folha de rosto e verso são páginas próprias; a capa colorida é separada.
#let dicas-title-page() = page(margin: 0mm, header: none, footer: none)[
  #place(top + left, dx: 25mm, dy: 30mm)[
    #block(width: 117mm)[
      #set text(font: "Libertinus Serif", size: 25pt, weight: "regular", fill: black)
      #set par(justify: false, leading: 5pt)
      Dados e Indicadores \
      de Clima e Ambiente \
      para a Saúde
      #v(12mm)
      #text(font: "Source Sans 3", size: 11pt)[$for(by-author)$$it.name.literal$$sep$, $endfor$]
    ]
  ]
  #place(bottom + left, dx: 25mm, dy: -24mm)[
    #set text(font: "Source Sans 3", size: 9pt)
    #set par(justify: false, leading: 3pt)
    Brasil · Edição do autor \
    2026
  ]
]

// Aberturas de parte: composição própria, em escala de cinza, com forte
// contraste entre o algarismo romano, a rubrica editorial e o título. A
// identificação parte do título gerado pelo Quarto, preservando o elemento
// heading original para o sumário e para a navegação interna do PDF.
#let dicas-part-counter = counter("dicas-part-counter")

#let dicas-is-part-title(body) = {
  let value = content-to-string(body)
  value.starts-with("Parte ")
}

#let dicas-is-list-title(body) = {
  let value = content-to-string(body)
  value == "Lista de figuras" or value == "Lista de quadros e tabelas"
}

#let dicas-part-opening(it) = {
  pagebreak(to: "odd")
  let full-title = content-to-string(it.body)
  dicas-part-counter.step()
  context {
    let short-title = full-title.replace(regex("^Parte\s+[IVXLCDM]+\s+[-–—]+\s+"), "")
    set par(justify: false, first-line-indent: 0pt, leading: 5pt)
    block(width: 100%, height: 100%, breakable: false)[
      #place(top + left, dy: 30mm)[
        #block(width: 100%)[
          #text(font: "Source Sans 3", size: 10pt, tracking: 0.06em)[
            PARTE #numbering("I", dicas-part-counter.get().first())
          ]
          #v(7mm)
          #line(length: 28mm, stroke: 0.5pt + luma(90))
          #v(8mm)
          #text(font: "Libertinus Serif", size: 25pt, weight: "regular", short-title)
        ]
      ]
      #place(bottom + left, dy: -6mm)[
        #text(font: "Source Sans 3", size: 8pt, fill: luma(70))[
          Dados e Indicadores de Clima e Ambiente para a Saúde
        ]
      ]
    ]
  }
}

// Composição local: uma única camada controla título, entrelinha e aberturas.
#let dicas-book(body) = {
  set document(
    title: "$title$",
    author: "$for(by-author)$$it.name.literal$$sep$, $endfor$",
  )
  set text(font: "Libertinus Serif", size: 10.5pt, fill: black, lang: "pt")
  set par(justify: true, first-line-indent: 1em, leading: 6.125pt, spacing: 0.65em)
  set heading(numbering: "1.1", supplement: "Capítulo")
  set figure(numbering: num => numbering("1.1", counter(heading).get().first(), num))
  set math.equation(numbering: num => numbering("(1.1)", counter(heading).get().first(), num))
  show terms: set par(first-line-indent: 0pt)
  show figure: set align(center)
  show figure: set block(spacing: 10pt)
  show figure.where(caption: none): set figure(outlined: false)
  dicas-title-page()
  page(header: none, footer: none)[#align(bottom, copyright-page)]
  body
}

#show: body => dicas-book(body)

// Nas remissões, o ponto pertence à frase, não ao número do capítulo.
#show ref: it => {
  if it.element != none and it.element.func() == heading and it.element.level == 1 {
    show regex("\\.$$"): none
    it
  } else {
    it
  }
}

// Vinhetas dos capítulos de fundamentos, identificadas pelo título editorial.
#let dicas-chapter-openings = (
  "Do indicador à decisão pública": (
    source: "assets/openings/cap6-indicador-decisao-turner-print.png",
    alt: "Paisagem pictórica de uma cidade brasileira hipotética à margem de um rio, sem pessoas. Uma ponte e vias ribeirinhas conectam bairros e edifícios públicos entre áreas verdes. Luz dourada atravessa a bruma e se reflete na água, em contraste com nuvens azul-acinzentadas e chuva distante.",
  ),
  "Clima, ambiente e saúde pública": (
    source: "assets/openings/cap1-clima-ambiente-saude-print.png",
    alt: "Aquarela panorâmica de um bairro brasileiro hipotético, sem pessoas: casas e prédios, ruas arborizadas, rio com margens vegetadas e ponte, sob sol à esquerda e nuvens de chuva à direita. Uma pequena edificação com rampa integra a paisagem.",
  ),
  "Mudança climática, planejamento e resposta do SUS": (
    source: "assets/openings/cap2-planejamento-resposta-sus-print.png",
    alt: "Paisagem urbana hipotética sem pessoas: unidade de saúde com entrada coberta e rampa, ruas arborizadas, casas e prédios, drenagem, jardim de chuva e reservatório de água, sob nuvens de chuva ao fundo. A infraestrutura remete ao acesso e ao funcionamento dos serviços diante das condições climáticas.",
  ),
  "Dos dados aos indicadores: como representar clima, ambiente e saúde": (
    source: "assets/openings/cap3-dados-indicadores-print.png",
    alt: "Paisagem hipotética sem pessoas: estação meteorológica em amplo terreno de grama baixa, com abrigo ventilado de sensores, pluviômetro e mastro com anemômetro. Ao fundo, curso d’água, vegetação e cidade, com edifícios e árvores afastados dos instrumentos.",
  ),
  "Compatibilizando dados: espaço, tempo e qualidade": (
    source: "assets/openings/cap4-espaco-tempo-qualidade-print.png",
    alt: "Panorama hipotético sem pessoas de uma bacia com encosta arborizada, área agrícola, rio no vale e bairro denso. Pequenos conjuntos de instrumentos ocupam terrenos abertos em cotas distintas, destacando diferenças de relevo, entorno e representatividade das observações.",
  ),
  "Fontes de dados e fichas de indicadores": (
    source: "assets/openings/cap5-fontes-fichas-print.png",
    alt: "Paisagem hipotética sem pessoas de um pequeno núcleo urbano: instalação de monitoramento ambiental, estação meteorológica em gramado aberto, sensor junto ao rio e estabelecimento de saúde integrado às ruas, casas e prédios. A cena remete a diferentes origens dos dados.",
  ),
)

// Mantém os headings originais como destinos de sumário e referências,
// alterando somente sua apresentação. Reinicia os contadores como o modelo.
#show heading: it => {
  let value = content-to-string(it.body)
  if it.level == 1 {
    if value == "Apêndices" { none }
    else if dicas-is-part-title(it.body) { dicas-part-opening(it) }
    else {
      pagebreak(to: "odd")
      counter(figure.where(kind: image)).update(0)
      counter(figure.where(kind: table)).update(0)
      counter(math.equation).update(0)
      let opening = dicas-chapter-openings.at(value, default: none)
      let has-opening = opening != none
      block(width: 100%, above: 8mm, below: if has-opening { 6mm } else { 10mm },
        breakable: not has-opening, sticky: true)[
        #set par(justify: false, first-line-indent: 0pt, leading: 5pt)
        #if it.numbering != none {
          block(below: 5mm)[
            #text(font: "Source Sans 3", size: 9pt, tracking: 0.06em)[
              CAPÍTULO #context counter(heading).display("1")
            ]
          ]
        }
        #text(font: "Libertinus Serif", size: 25pt, weight: "regular", it.body)
        #if has-opening {
          v(3mm)
          image(opening.source, width: 100%, alt: opening.alt)
        }
      ]
    }
  } else {
    block(above: if it.level == 2 { 14pt } else { 10pt }, below: 6pt, sticky: true)[
      #set par(justify: false, first-line-indent: 0pt, leading: 3pt)
      #set text(
        font: if it.level == 2 { "Libertinus Serif" } else { "Source Sans 3" },
        size: if it.level == 2 { 15pt } else { 10.5pt },
        weight: if it.level == 2 { "regular" } else { "semibold" },
      )
      #if it.numbering != none [#context counter(heading).display(it.numbering) #h(0.3em)]
      #it.body
    ]
  }
}

// Marcas invisíveis de fim de seção identificam os versos vazios, mesmo
// depois de uma repaginação. Inseridas pelo filtro indicator-cards.lua.
#let dicas-is-blank-page(page-number) = {
  let ends = query(metadata.where(value: "dicas-section-end"))
  let starts = query(heading.where(level: 1))
  ends.any(it => {
    let end-page = it.location().page()
    let next = starts.filter(h => h.location().page() > end-page)
    next != () and end-page < page-number and page-number < next.first().location().page()
  })
}

#set page(
  header: context {
    set text(font: "Source Sans 3", size: 8.5pt)
    let page-number = counter(page).at(here()).first()
    let chapter-headings = query(heading.where(level: 1))
    let chapter-opening = chapter-headings.any(
      it => it.location().page() == page-number
    )
    let part-opening = chapter-headings.any(
      it => it.location().page() == page-number and dicas-is-part-title(it.body)
    )
    let intentional-blank = dicas-is-blank-page(page-number)
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
              align(right, text(size: 8.5pt, running-title)),
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
    let intentional-blank = dicas-is-blank-page(page-number)
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

// Topo de 7,875 pt + distância de 6,125 pt entre caixas = entrelinha de 14 pt.
// Conferida entre as origens de linhas consecutivas no PDF renderizado.
#set text(font: "Libertinus Serif", size: 10.5pt, fill: black, top-edge: 0.75em, bottom-edge: 0.25em)
#set par(leading: 6.125pt, spacing: 0.65em)
#show figure.caption: set text(font: "Libertinus Serif", size: 9pt)
#show figure.caption: set par(justify: false, first-line-indent: 0pt, leading: 3pt)
#show figure.caption: it => block(width: 100%)[#align(left, it)]
#set figure(gap: 6pt)
#show table.cell.where(y: 0): set text(font: "Source Sans 3", weight: "semibold")
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
