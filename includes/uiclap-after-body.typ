// Complemento do último caderno; rever a quantidade depois de repaginar.
// O pré-voo exige que o total de páginas seja múltiplo de quatro.
#for _ in range(3) {
  pagebreak()
  set page(header: none, footer: none, numbering: none)
  box(width: 0pt, height: 0pt)
}
