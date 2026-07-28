# Guia de revisão da versão inicial

## Finalidade

Esta versão foi preparada para revisão editorial, metodológica e visual. Ela não é uma edição completa do livro: estabiliza a arquitetura de 14 capítulos, dois capítulos desenvolvidos, três fichas demonstrativas e o cadastro inicial de fontes.

Os artefatos a revisar são:

- site em `_output/web/index.html`;
- PDF em `_output/print/dados-indicadores-clima-ambiente-saude.pdf`;
- conteúdo-fonte em `index.qmd`, `chapters/`, `frontmatter/` e `backmatter/`;
- fichas em `indicators/data/`;
- fontes em `sources/data/sources.yml`.

## Fora do escopo

Não revisar como se estivessem fechados: capa final, ISBN, ficha catalográfica, editora, créditos institucionais definitivos, normas ainda não verificadas, séries estatísticas, limiares operacionais e capítulos marcados como `TODO`.

Os `TODO` dos capítulos provisórios são deliberados. Devem ser comentados quando estiverem mal formulados, incompletos ou fora de lugar, não apenas por ainda existirem.

## Ordem sugerida

1. Ler a página inicial e o capítulo 2 para avaliar público, propósito e vocabulário.
2. Ler o capítulo 5 para avaliar profundidade, tom e padrão de um capítulo temático.
3. Comparar as três fichas e verificar se o núcleo RIPSA e as extensões ambientais estão claros.
4. Percorrer o índice de fontes e avaliar a separação entre instituição, sistema, plataforma, base, produto, painel e API.
5. Examinar a estrutura dos demais capítulos, seus limites e indicadores previstos.
6. Revisar o site e o PDF como produtos editoriais distintos.

## Questões para decisão editorial

### Arquitetura

- As quatro partes formam um percurso claro entre fundamentos, temas, integração e aplicação?
- As fronteiras declaradas resolvem as sobreposições entre ilhas de calor, eventos hidrológicos, desastres, vulnerabilidade, efeitos e resposta?
- Algum tema essencial está ausente ou merece mudança de capítulo?

### Conteúdo-modelo

- O capítulo 2 distingue adequadamente dado, variável, índice e indicador?
- O capítulo 5 separa temperatura do ar, temperatura da superfície, extremos e exposição sem criar equivalências indevidas?
- O nível de detalhe serve às equipes de vigilância, epidemiologia, planejamento e gestão?

### Fichas

- Os 16 campos da FQI são reconhecíveis e suficientes como núcleo?
- Os campos ambientais adicionais são necessários e não duplicam o núcleo?
- “Granularidade” e “resolução espacial original” estão diferenciadas?
- A análise descritiva deve permanecer fora da ficha até existir uma série validada?

### Fontes

- O objeto cadastrado está corretamente tipificado?
- A instituição responsável está separada do sistema, plataforma, produto, painel ou API efetivamente usado?
- Os campos pendentes estão suficientemente explícitos para impedir uso inadvertido?

## Revisão do site

Verificar:

- navegação lateral, ordem das partes e destaque da página ativa;
- sumário local e profundidade dos títulos;
- busca e presença das páginas no índice;
- links entre capítulos, fichas, fontes e referências;
- tabelas e fichas em tela larga e estreita;
- contraste, foco, legibilidade e rolagem horizontal de tabelas em telas pequenas.

O arquivo `search.json` deve existir na raiz de `_output/web/`. Links locais e âncoras são verificados automaticamente por `scripts/validate_project.R`.

## Revisão do PDF

Verificar:

- formato de 155 × 230 mm e margens espelhadas;
- página de título, sumário, abertura das partes e início dos capítulos;
- cabeçalhos, fólios e páginas de verso;
- quebras das fichas, fórmulas, tabelas e referências;
- hifenização, linhas órfãs ou viúvas, cortes e páginas vazias;
- legibilidade em preto e branco.

As aberturas de partes e capítulos começam em página ímpar nesta versão. Os versos inseridos automaticamente mantêm o fólio e devem ser avaliados como decisão provisória de projeto gráfico, não como fechamento da paginação.

## Como registrar um comentário

Indicar o arquivo ou a página, a seção e uma destas categorias:

- **bloqueio:** impede compreender, validar ou compilar;
- **decisão:** exige escolha editorial ou metodológica;
- **ajuste:** correção localizada de redação, hierarquia ou desenho.

Quando possível, descrever o problema antes de sugerir uma solução. Para fichas e fontes, citar o código ou ID do registro.

## Reproduzir a versão

```sh
quarto render
quarto render --profile web
quarto render --profile print
make
Rscript scripts/validate_project.R
```

Os comandos regeneram páginas derivadas de fichas e fontes antes da compilação.
