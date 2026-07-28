# Fontes de dados

## Princípio

O catálogo não presume que toda instituição ofereça um único conjunto homogêneo. Cada uso deve identificar sistema, produto, variável, versão, cobertura, resolução, período, acesso e licença.

## Cadastro

Os registros ficam em `sources/data/sources.yml`. O índice e os quadros são gerados por `scripts/build_catalogs.R`. O modelo de campos está em `sources/data/source-template.yml`.

Campos sem confirmação usam `TODO: verificar`. A data de verificação não transforma um cadastro incompleto em fonte validada; ela informa quando a página ou documentação foi consultada.

## Registros iniciais

Foram criados registros para INMET, CPTEC/INPE, CEMADEN, Climate Data Store, ERA5-Land, CAMS, MapBiomas, Programa Queimadas, Vigiagua/Sisagua, SINISA, S2iD, IBGE, DATASUS e um registro provisório para redes de qualidade do ar.

## Critérios de seleção

1. aderência à pergunta;
2. autoridade e documentação;
3. natureza do dado;
4. cobertura espacial e temporal;
5. qualidade e incerteza;
6. atualização e estabilidade;
7. acesso, licença e custo;
8. possibilidade de reprodução;
9. compatibilidade com o território e a decisão.

## Verificação

Antes de publicar uma característica:

- consulte página institucional ou documentação primária;
- registre a URL específica, não apenas a página inicial;
- confira a versão vigente;
- confirme licença, cadastro e custo;
- teste o download ou API;
- abra um arquivo e confira metadados e unidade;
- registre data e responsável pela verificação.

O processo de compilação não consulta serviços externos. Isso mantém a construção reproduzível e permite que indisponibilidade temporária de um portal não interrompa o livro.

