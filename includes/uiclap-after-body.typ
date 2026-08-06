// Três páginas brancas completam o último caderno de quatro páginas da prova
// final. O pré-voo falha se uma repaginação futura exigir rever esta quantidade.
#for _ in range(3) {
  pagebreak()
  set page(header: none, footer: none, numbering: none)
  box(width: 0pt, height: 0pt)
}
