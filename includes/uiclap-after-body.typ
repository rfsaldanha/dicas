// Fecha o último caderno pela página física de uma âncora anterior ao complemento.
// A âncora evita que as quebras acrescentadas alterem a própria posição medida.
#box(width: 0pt, height: 0pt) <uiclap-content-end>
#context {
  let last-content-page = query(<uiclap-content-end>).first().location().page()
  let remaining = calc.rem(4 - calc.rem(last-content-page, 4), 4)
  for _ in range(remaining) {
    pagebreak()
    set page(header: none, footer: none, numbering: none)
    box(width: 0pt, height: 0pt)
  }
}
