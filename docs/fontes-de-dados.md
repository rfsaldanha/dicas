# Fontes de dados

## Princípio

O catálogo não presume que toda instituição ofereça um único conjunto homogêneo. Cada uso deve identificar sistema, produto, variável, versão, cobertura, resolução, período, acesso e licença.

## Cadastro

Os registros ficam em `sources/data/sources.yml`. O índice e os quadros são gerados por `scripts/build_catalogs.R`. O modelo de campos está em `sources/data/source-template.yml`.

Todos os campos publicados devem conter informação verificada. Quando a documentação oficial não declarar uma característica, o cadastro registra “não informado” e descreve a consequência em limitações. A data de verificação informa quando a página ou documentação foi consultada.

Cada cadastro identifica primeiro o objeto descrito em `tipo_registro`: instituição, unidade institucional, programa, sistema de informação, plataforma, base de dados, produto, serviço ou cadastro provisório. Recursos associados são classificados separadamente em `recursos_relacionados`; APIs têm campo próprio. Assim, o portal de uma instituição não é tratado como se fosse a base ou o produto usado no cálculo.

## Registros

O catálogo cobre fontes brasileiras e internacionais usadas pelas fichas, incluindo INMET, CEMADEN, produtos Copernicus, MapBiomas, Programa Queimadas, Vigiagua/Sisagua, SINISA, S2iD e Atlas Digital, IBGE, DATASUS, MonitorAr, OMS, JMP, Landsat, Ipea e UN-Habitat.

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
