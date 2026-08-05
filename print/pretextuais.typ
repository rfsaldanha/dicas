#let pretext-title(title) = {
  set par(first-line-indent: 0pt)
  text(size: 24pt, weight: "bold", title)
  v(3mm)
  line(length: 30mm, stroke: 1.2pt + black)
  v(11mm)
}

#let pretextuais = [
#pagebreak(to: "odd")
#[
  #set page(header: none, footer: none, numbering: none)
  #set par(first-line-indent: 1.2em, leading: 0.5em, spacing: 0.75em, justify: true)

  #show heading.where(level: 1): it => none
  #heading(level: 1, outlined: true, numbering: none)[Agradecimentos]
  #pretext-title([Agradecimentos])

  Este livro se apoia no trabalho continuado de profissionais que produzem,
  qualificam, documentam e divulgam dados meteorológicos, ambientais,
  territoriais, demográficos e de saúde. Agradeço especialmente às equipes do
  Sistema Único de Saúde e das instituições públicas responsáveis pelas fontes
  cadastradas nesta obra.

  Também reconheço a contribuição das comunidades científicas que desenvolveram
  os indicadores, métodos e padrões aqui sistematizados, bem como das pessoas e
  comunidades que transformam informação em proteção cotidiana. Erros e escolhas
  editoriais permanecem sob responsabilidade do autor.
]

#pagebreak(to: "odd")
#[
  #set page(header: none, footer: none, numbering: none)
  #set par(first-line-indent: 1.2em, leading: 0.5em, spacing: 0.75em, justify: true)

  #show heading.where(level: 1): it => none
  #heading(level: 1, outlined: true, numbering: none)[Apresentação]
  #pretext-title([Apresentação])

  Clima e ambiente não são apenas o cenário em que a saúde acontece.
  Temperaturas extremas, chuvas intensas, secas, fumaça, contaminação da água,
  transformações do território e desastres alteram exposições, agravam
  desigualdades e pressionam serviços. Esses efeitos se distribuem de forma
  desigual: dependem das condições de vida, da infraestrutura, da organização
  do território e da capacidade pública de antecipar, proteger e responder.

  Transformar fenômenos tão distintos em informação útil exige mais que reunir
  bases ou calcular taxas. É necessário formular a pergunta de gestão, distinguir
  perigo, exposição, vulnerabilidade, efeito e resposta, escolher escalas
  espaciais e temporais compatíveis, conhecer a origem dos registros e tornar
  explícitas suas limitações. Um indicador só ganha sentido quando sua definição,
  sua fonte e sua incerteza são consideradas junto da decisão que deverá apoiar.

  Este livro foi concebido para oferecer essa base comum. Reúne conceitos,
  métodos, fontes e critérios de interpretação para profissionais e estudantes
  que atuam na vigilância, na epidemiologia, no planejamento, na gestão e na
  pesquisa em saúde pública. Os capítulos são organizados pelos fenômenos; dentro
  deles, as fichas permitem comparar diferentes formas de medição sem separar o
  indicador do contexto que lhe dá significado.

  A obra pode ser lida em sequência, como percurso de formação, ou consultada
  conforme uma necessidade concreta: estruturar um painel, revisar uma medida,
  integrar bases, planejar uma rotina de monitoramento ou qualificar a comunicação
  de riscos. Em todos esses usos, a proposta é a mesma: substituir escolhas
  automáticas por decisões documentadas, transparentes e passíveis de revisão.

  O livro não substitui normas, protocolos, documentação oficial, conhecimento do
  território nem pactuação institucional. Seu papel é ajudar a fazer perguntas
  melhores, reconhecer o que os dados podem — e não podem — sustentar e aproximar
  evidência, responsabilidade e ação pública.
]

#pagebreak(to: "odd")
#[
  #set page(header: none, footer: none, numbering: none)
  #set par(first-line-indent: 1.2em, leading: 0.5em, spacing: 0.75em, justify: true)

  #show heading.where(level: 1): it => none
  #heading(level: 1, outlined: true, numbering: none)[Prefácio do autor]
  #pretext-title([Prefácio do autor])

  Dados ambientais e dados de saúde costumam chegar às equipes por caminhos
  separados. Uma estação mede temperatura; um satélite estima propriedades da
  superfície; um sistema registra internações; outro reúne ocorrências de
  desastres. A decisão pública, porém, acontece no mesmo território e no mesmo
  tempo. Este livro foi escrito para aproximar esses caminhos sem apagar suas
  diferenças.

  Essa aproximação exige entendimento comum entre profissões que observam objetos
  diferentes, trabalham com escalas distintas e respondem por etapas
  complementares. O ponto de partida deste livro é que ninguém precisa dominar
  sozinho toda a interface entre clima, ambiente e saúde: o vocabulário, os
  limites e as rotinas precisam ser construídos de forma compartilhada.

  Não há um indicador universal de “risco climático para a saúde”. Perigo,
  exposição, vulnerabilidade, efeito e capacidade de resposta são dimensões
  relacionadas, mas não intercambiáveis. Somá-las em um escore pode ser atraente
  e, ainda assim, esconder as pessoas, os mecanismos e as responsabilidades que
  deveriam orientar a ação.

  Por isso, a obra parte de indicadores consolidados em normas, programas de
  monitoramento e literatura científica, com preferência por aplicações em saúde
  pública. As fichas estão integradas ao capítulo de cada fenômeno. Elas registram
  conceito, objetivo, fórmula, fontes, resolução, limitações, relação com a saúde
  e uso gerencial. O leitor pode conhecer o fenômeno, comparar as medidas
  disponíveis e chegar ao detalhe operacional sem sair do contexto.

  O livro também assume que o dado tem história. Uma série pode mudar porque a
  rede cresceu, o instrumento foi substituído, a classificação mudou ou o serviço
  se tornou inacessível durante um desastre. Toda interpretação deve conservar
  fonte, versão, cobertura, tempo, território e incerteza.

  O resultado pretendido é prático: ajudar profissionais, estudantes,
  pesquisadores e gestores a formular perguntas melhores, escolher medidas
  defendíveis e ligar resultados a ações. Indicadores não decidem. Eles tornam
  mais clara a evidência sobre a qual pessoas e instituições decidem — e tornam
  essa decisão mais passível de exame, correção e aprendizado.
]

]
