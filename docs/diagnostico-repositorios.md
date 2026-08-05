# Diagnóstico dos repositórios de referência

## Escopo da inspeção

Foram examinados, sem modificações, `../sis`, `../diisp` e `../sis_pdf`: estrutura, configurações, capítulos, estilos, bibliografia, fichas, extensões Typst, scripts de sincronização e validadores.

## `../sis`

O projeto digital usa Quarto Book, publica em `docs/`, mantém capítulos no nível raiz e configura busca, referências cruzadas, bibliografia e um tipo customizado de quadro. Scripts R geram lista de siglas, índice de assuntos e relações entre páginas. O CSS resolve necessidades editoriais específicas, inclusive quadros e responsividade.

Padrões aproveitáveis:

- Fonte única de capítulos;
- Navegação e busca nativas do Quarto;
- Pré-render para índices derivados;
- Convenção explícita para quadros;
- Bibliografia BibTeX compartilhada;
- Automação editorial em R.

Limites para o novo projeto:

- Muitos arquivos no nível raiz dificultariam um livro com catálogos estruturados;
- A configuração concentra recursos específicos de áudio e de um livro maduro;
- HTML e PDF simples no mesmo formato não atendem ao acabamento impresso requerido aqui.

## `../diisp`

O livro organiza uma sequência metodológica próxima ao tema deste projeto. O arquivo `template_indicador` define campos editoriais básicos — conceituação, interpretação, usos, limitações, fontes, cálculo e categorias —, mas não é estruturado para geração de índices ou validação.

Padrões aproveitáveis:

- Progressão entre fundamentos, qualidade, incerteza e capítulos temáticos;
- Linguagem orientada ao uso;
- Fichas como unidade editorial dentro do domínio;
- Exemplos de distinção entre dado, variável e indicador.

Limites para o novo projeto:

- Ficha sem metadados legíveis por máquina;
- Ausência de versão impressa ativa;
- Estrutura plana e sem catálogo de fontes;
- Campos insuficientes para suporte espacial, natureza do produto e disponibilidade.

## `../sis_pdf`

O projeto impresso usa Quarto e Typst com formato local especializado. O miolo mede 160 × 230 mm, tem margens espelhadas, Libertinus Serif, capítulos em páginas ímpares, pré-voo de fontes e imagens e auditoria detalhada de paginação. O conteúdo é sincronizado de `../sis`, mantendo dois repositórios e uma cópia derivada não versionada.

Padrões aproveitáveis:

- Typst para composição de impressão sob demanda;
- Dimensões e margens explícitas;
- Extensão local de formato;
- Nome previsível do PDF;
- Validação pós-render com Poppler;
- Auditoria de elementos iniciais, fontes incorporadas e tamanho de página.

Riscos que não foram repetidos:

- Separar web e impressão em repositórios distintos criaria sincronização precoce;
- Copiar a extensão completa traria regras específicas do SIS, QR codes, índice digital e filtros sem função neste livro;
- Validações altamente acopladas a títulos e páginas só são apropriadas após o conteúdo estabilizar.

## Estratégia recomendada e adotada

O DICAS mantém uma única árvore de conteúdo e usa perfis `web` e `print`. Uma extensão Typst local mínima controla apenas formato físico e paginação; diferenças editoriais ficam em condicionais e includes. Fichas individuais em YAML e um catálogo central de fontes alimentam páginas e índices por um script R.

Dependências: Quarto, R com `yaml` e Poppler para validação. Não há dependência de rede na compilação.

## Riscos e decisões pendentes

- O ISBN, a ficha catalográfica, a editora e a licença editorial precisam ser definidos.
- O alvo de 400–500 páginas só deve ser avaliado depois do desenvolvimento técnico.
- A lista de 55–65 fichas precisa de priorização e revisão temática.
- Normas e limiares vigentes exigem verificação por capítulo.
- A paginação final, listas automáticas e índice remissivo devem ser refinados no fechamento.
