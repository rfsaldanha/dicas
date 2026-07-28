// Configuração do miolo: 155 × 230 mm, margens espelhadas e composição sóbria.
#set page(
  width: 155mm,
  height: 230mm,
  binding: left,
  margin: (
    inside: 20mm,
    outside: 15mm,
    top: 18mm,
    bottom: 20mm,
  ),
  header: context {
    let current = counter(page).get().first()
    if current > 2 {
      set text(size: 8.5pt, fill: luma(70))
      align(
        if calc.odd(current) { right } else { left },
        counter(page).display("1"),
      )
    }
  },
  footer: none,
)

#set text(lang: "pt", region: "BR")
#set par(justify: true, leading: 0.72em, first-line-indent: 1.2em)

#show heading.where(level: 1): it => {
  pagebreak(to: "odd", weak: true)
  set text(size: 22pt, weight: "bold")
  set par(justify: false, first-line-indent: 0pt)
  block(above: 18mm, below: 10mm, it)
}

#show heading.where(level: 2): it => {
  set text(size: 15pt, weight: "bold")
  set par(justify: false, first-line-indent: 0pt)
  block(above: 1.1em, below: .55em, it)
}

