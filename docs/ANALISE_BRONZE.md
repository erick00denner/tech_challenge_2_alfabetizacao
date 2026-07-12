# Análise Exploratória da Camada Bronze

## Objetivo

Este documento resume os principais resultados da análise exploratória realizada
sobre os datasets da camada Bronze.

O objetivo da exploração foi avaliar a qualidade dos dados e identificar
transformações necessárias para a construção da camada Silver.

---

## Papel da Camada Bronze

A camada Bronze representa o ponto de entrada dos dados públicos utilizados pela plataforma.

Seu objetivo é preservar os datasets em formato estruturado, mantendo a maior fidelidade possível às fontes originais e servindo como base para as etapas posteriores de tratamento (Silver) e consolidação analítica (Gold).

As análises apresentadas neste documento têm caráter exploratório e apoiaram a compreensão inicial das características dos dados, subsidiando as decisões de modelagem implementadas ao longo do projeto.

---

# Datasets analisados

- UF
- Município
- Meta Alfabetização Brasil
- Meta Alfabetização UF
- Meta Alfabetização Município
- Alunos

---

# Principais evidências

## Qualidade dos dados

A análise demonstrou que os datasets apresentam boa qualidade e consistência.

Durante a exploração foram verificadas:

- quantidade de registros;
- tipos de dados;
- valores nulos;
- registros duplicados;
- possíveis chaves candidatas.

Não foram identificados problemas de integridade que justificassem alterações
nos dados originais.

---

## Duplicidades

Nenhuma das tabelas apresentou registros duplicados.

As seguintes chaves candidatas foram identificadas:

| Tabela | Chave candidata |
|----------|----------------|
| UF | (ano, sigla_uf, serie, rede) |
| Município | (ano, id_municipio, serie, rede) |
| Meta Alfabetização Brasil | (ano, rede) |
| Meta Alfabetização UF | (ano, sigla_uf, rede) |
| Meta Alfabetização Município | (ano, id_municipio, rede) |
| Alunos | (ano, id_aluno) |

---

## Tipos de dados

Os identificadores geográficos foram disponibilizados como texto e permanecerão
nesse formato durante todo o projeto.

Destacam-se:

- sigla_uf
- id_municipio
- id_escola
- id_aluno

Não foi identificada necessidade de conversão desses campos para tipos numéricos.

---

## Valores nulos

Foram identificados valores nulos em algumas tabelas.

Após investigação, concluiu-se que esses nulos representam ausência legítima
de informação e não erros de ingestão.

Exemplos:

- distribuição por níveis de alfabetização;
- metas indisponíveis para determinadas combinações de ano e município;
- alunos ausentes, sem proficiência e peso amostral.

Dessa forma, optou-se por preservar integralmente os valores nulos.

---

# Decisões para a camada Silver

A camada Silver terá como objetivo principal padronizar e validar os datasets,
preservando integralmente o significado dos dados da camada Bronze.

Serão realizadas apenas transformações não destrutivas, como:

- validação das chaves candidatas;
- validação de duplicidades;
- padronização de campos textuais;
- ordenação dos registros;
- padronização dos tipos de dados;
- gravação em formato Parquet.

Não serão realizadas:

- remoção de registros;
- substituição de valores nulos;
- alterações semânticas dos dados.

---

# Conclusão

A exploração confirmou que os datasets apresentam elevada qualidade e estão
aptos para a construção da camada Silver.

A exploração inicial dos datasets permitiu compreender a estrutura, granularidade e relacionamento entre as diferentes fontes disponibilizadas pelo INEP.

Essas análises serviram como base para definição das transformações implementadas na camada Silver, para construção dos datasets analíticos da camada Gold e para definição das regras de qualidade incorporadas posteriormente à plataforma.