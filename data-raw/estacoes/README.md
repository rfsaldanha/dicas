# Exemplos observados do apêndice B

Os arquivos preservam dois exemplos independentes. Não constituem uma análise conjunta de meteorologia e poluição, pois diferem em estação e ano.

## INMET

- Original: `inmet-a701-2024-original.csv`, extraído sem alterações do ZIP anual oficial de 2024.
- Recorte: `inmet-a701-2024-01-01.csv`, com as 24 linhas de 1º de janeiro de 2024 em UTC.
- Estação: São Paulo–Mirante, A701; códigos e coordenadas são mantidos conforme o cabeçalho da fonte.
- Ausências: células vazias continuam vazias; não houve imputação. A rotina também reconhece o sentinela `-9999`, sem aplicar essa convenção a outras fontes.
- Proveniência, hash do ZIP e do membro original: `inmet-proveniencia.json`.

A coluna de temperatura horária e a de máxima na hora anterior têm significados diferentes. A janela UTC não é o dia civil de São Paulo. As dez células vazias de radiação são preservadas mesmo quando situadas no período noturno.

## CETESB

- Originais: `cetesb-2021-relatorio-original.pdf` e `cetesb-2021-apendice4-original.pdf`, obtidos do repositório oficial.
- Edição: *Qualidade do ar no estado de São Paulo 2021*, publicada em 2022.
- Recorte: `cetesb-mp25-2021.csv`, seis estações da Tabela D, página impressa 183, página física 9 do PDF do Apêndice 4.
- Método da rede: atenuação beta para MP₂,₅, conforme a Tabela 3.3 do relatório, página 60.
- `N` na coluna original de contagem é o número de dias válidos. Na coluna de representatividade, `N` significa que o critério anual não foi atendido. Os significados estão separados nos campos derivados.
- A classificação anual foi preservada da fonte; não foi estimada pelo total de dias. São José do Rio Preto é mantida na tabela, mas não recebe ponto de média anual no gráfico.
- Proveniência e hashes: `cetesb-proveniencia.json`.

O relatório de 2021 foi escolhido por permitir conferência direta dos dados e critérios em arquivos públicos. A tentativa inicial de obter as edições 2023/2024 pelo antigo site encontrou bloqueio de navegador. Não se apresenta 2021 como a edição mais recente.

## Reprodução e condições de uso

Executar `python3 scripts/build_estacoes_data.py` na raiz do projeto para recriar os CSV. Executar `python3 scripts/build_estacoes_data.py --check` para comparar os derivados com os arquivos originais sem reescrevê-los. A extração usa apenas a biblioteca padrão Python e `pdftotext`; não acessa a rede. As figuras são compostas por `scripts/build_estacoes_art.py`.

Os dados e documentos conservam as condições de uso de INMET e CETESB. Citar instituição, produto, estação, período e data de acesso. A licença GPL-3.0 dos códigos e desenhos autorais não é atribuída aos documentos das instituições. O relatório CETESB permite reprodução com citação da fonte.
