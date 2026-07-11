DEC-001 – Preservação dos dados na camada Bronze

A camada Bronze armazenará os dados exatamente como retornados pelas consultas SQL oficiais da Base dos Dados, sem remoção de colunas ou aplicação de regras de negócio. Transformações, filtros e seleção de atributos serão realizados apenas nas camadas Silver e Gold.

DEC-002 — Estrutura das metas de alfabetização

Durante a construção da camada Gold foi identificado que as tabelas de metas
(`meta_alfabetizacao_brasil`, `meta_alfabetizacao_uf` e
`meta_alfabetizacao_municipio`) armazenam metas futuras em formato wide
(uma coluna para cada ano).

Exemplo:

ano = 2023

taxa_alfabetizacao = 64,60

meta_alfabetizacao_2024 = 67,08

meta_alfabetizacao_2025 = 69,51

Portanto, não é possível comparar diretamente a taxa de alfabetização do
registro com uma única coluna de meta sem uma regra de negócio adicional.

Decisão:

A camada Gold preservará as metas conforme disponibilizadas pela Base dos
Dados e não calculará indicadores como:

- diferença para meta;
- percentual da meta atingida;
- atingiu meta.

Esses cálculos dependeriam de regras não documentadas na fonte oficial.