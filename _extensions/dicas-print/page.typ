#set page(
  width: 160mm,
  height: 230mm,
  binding: left,
  margin: (
    inside: 25mm,
    outside: 18mm,
    top: 20mm,
    bottom: 22mm,
  ),
  numbering: $if(page-numbering)$"$page-numbering$"$else$"1"$endif$,
  footer: context {
    let page-number = counter(page).at(here()).first()
    let chapter-opening = query(heading.where(level: 1)).any(
      it => it.location().page() == page-number
    )
    let textual-headings = query(heading.where(level: 1)).filter(
      it => it.body == [Bem-vindo]
    )
    let textual-start = if textual-headings == () {
      1
    } else {
      textual-headings.first().location().page()
    }
    if page-number >= textual-start and chapter-opening {
      align(center, numbering(
        $if(page-numbering)$"$page-numbering$"$else$"1"$endif$,
        page-number,
      ))
    }
  },
  columns: $if(columns)$$columns$$else$1$endif$,
)
