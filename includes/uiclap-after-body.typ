// Completa o último caderno a partir da página onde o conteúdo termina.
// A âncora fica fora do contexto que cria páginas, para não se deslocar com ele.
#metadata("fim-do-conteudo") <dicas-end>
#context {
  let last-content-page = query(<dicas-end>).first().location().page()
  let blanks = calc.rem(4 - calc.rem(last-content-page, 4), 4)
  for _ in range(blanks) {
    page(header: none, footer: none, numbering: none)[
      #box(width: 0pt, height: 0pt)
    ]
  }
}
