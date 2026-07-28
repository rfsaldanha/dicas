# Guia de compilação

## Ambiente validado

- Quarto 1.10.18;
- R 4.6.1;
- pacote R `yaml`;
- Typst 0.15.1, distribuído com o Quarto usado;
- Poppler com `pdfinfo`, `pdftotext` e `pdffonts`.

## Comandos

Versão web padrão:

```sh
quarto render
```

Perfis explícitos:

```sh
quarto render --profile web
quarto render --profile print
```

Fluxo completo:

```sh
make
```

Somente catálogos ou validação:

```sh
make catalogs
make validate
```

## Saídas

- `_output/web/index.html`;
- `_output/web/search.json`;
- `_output/print/dados-indicadores-clima-ambiente-saude.pdf`.

## Ordem da compilação

O pré-render executa `scripts/build_catalogs.R`. Esse script lê YAML, valida campos e códigos e gera páginas e índices. Em seguida, o Quarto compõe o livro. A validação completa deve ser executada após as duas saídas existirem.

## Solução de problemas

**Pacote `yaml` ausente:** execute `install.packages("yaml")`.

**PDF ausente:** confira se o perfil `print` foi usado e se a extensão `_extensions/dicas-print/` está presente.

**Fonte indisponível:** instale Libertinus Serif ou selecione uma família livre equivalente após teste de paginação.

**Link interno quebrado:** use caminhos relativos ao arquivo `.qmd`; execute `make validate`.

**Página de ficha desatualizada:** edite o YAML, nunca o `.qmd` gerado, e execute `make catalogs`.

## Limpeza

```sh
make clean
```

O alvo remove somente `_output` e `.quarto`, que são artefatos regeneráveis. Não remove dados, capítulos ou metadados.

