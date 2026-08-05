# Dados da figura de mudança de suporte

A figura `assets/figures/mudanca-suporte.svg` usa somente dados reais e é reconstruída por `scripts/build_real_figures.R`.

Fontes e proveniência:

- Temperatura do ar a 2 m: previsão global do Copernicus Atmosphere Monitoring Service (CAMS), distribuída pelo ECMWF Atmosphere Data Store. O arquivo local é produzido pelo repositório `rfsaldanha/camsdata`, revisão `91d270cbe2674779fc24860c58c16773de40a0b0`.
- População residente: Grade Estatística 2022 do Instituto Brasileiro de Geografia e Estatística (IBGE), obtida pela função `geobr::read_statistical_grid()`.
- Limite territorial: Malha Estadual 2022 do IBGE, obtida pelo pacote `geobr`. A escolha dessa fonte segue o fluxo de dados oficiais empregado no repositório `rfsaldanha/aula_r_geo`, sem reutilizar suas geometrias municipais na figura.

O CSV derivado registra, para cada célula CAMS que intersecta o estado do Rio de Janeiro, temperatura, área de interseção e população agregada. O YAML registra data da rodada, validade, prazo, resolução e resultados apresentados. Esses arquivos permitem auditar os números sem confundi-los com dados simulados.

Links oficiais:

- <https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts>
- <https://github.com/ipeaGIT/geobr>
- <https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais.html>
