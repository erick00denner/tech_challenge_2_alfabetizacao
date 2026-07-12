# Architecture Decisions

## Objetivo

Este documento registra as principais decisões arquiteturais tomadas ao longo do desenvolvimento da solução.

Diferentemente dos requisitos definidos pelo Tech Challenge, as decisões apresentadas neste documento representam escolhas realizadas para organizar a arquitetura, reduzir complexidade, aumentar a modularidade e facilitar a evolução da plataforma.

Cada decisão descreve o contexto encontrado durante o desenvolvimento, as alternativas consideradas e a justificativa para a solução adotada.

---

# AD-001 — Arquitetura híbrida para integração entre Batch e Streaming

## Contexto

O projeto previa a implementação de pipelines Batch e Streaming como requisitos independentes. Entretanto, durante o desenvolvimento surgiu a necessidade de definir como esses dois fluxos coexistiriam dentro da arquitetura da solução.

## Alternativas avaliadas

- Manter pipelines completamente independentes.
- Atualizar toda a camada Gold sempre que um novo evento fosse recebido.
- Construir uma arquitetura híbrida, utilizando o Batch para criação inicial da camada Gold e o Streaming para atualização incremental.

## Decisão

Foi adotada uma arquitetura híbrida, na qual o processamento Batch realiza a construção inicial do Data Lake e o processamento Streaming mantém a camada Gold continuamente atualizada.

## Justificativa

Essa abordagem evita reprocessamentos completos, reduz o consumo computacional e aproxima a solução de arquiteturas modernas orientadas a eventos, preservando uma única camada analítica para consumo por aplicações de BI e IA.

---

# AD-002 — Organização modular do projeto

## Contexto

As primeiras versões concentravam boa parte da lógica em poucos arquivos, dificultando manutenção, reutilização e evolução da solução.

## Alternativas avaliadas

- Centralizar toda a implementação em um único pipeline.
- Organizar o projeto por responsabilidade funcional.

## Decisão

A solução foi reorganizada em módulos independentes, separados por domínio de responsabilidade.

## Justificativa

A estrutura final passou a separar claramente os componentes responsáveis pelos pipelines Batch, Streaming, validação da qualidade dos dados, notebooks e documentação.

Essa organização reduz acoplamento, melhora a legibilidade do código e facilita futuras evoluções.

---

# AD-003 — Centralização das configurações

## Contexto

Durante o desenvolvimento, parâmetros como caminhos de diretórios, nomes de datasets e configurações do Kafka estavam distribuídos entre diferentes módulos.

## Alternativas avaliadas

- Manter configurações locais em cada componente.
- Centralizar as configurações em módulos específicos.

## Decisão

Foi adotada uma estratégia de configuração centralizada, mantendo cada domínio responsável por suas próprias configurações.

## Justificativa

A centralização simplificou a manutenção do projeto e reduziu duplicação de código, permitindo que alterações fossem realizadas em um único ponto sem impacto na lógica de processamento.

---

# AD-004 — Camada Quality desacoplada da pipeline

## Contexto

Durante a implementação surgiu a necessidade de validar a qualidade dos datasets produzidos.

Inicialmente as validações poderiam ser executadas diretamente durante o processamento das pipelines.

## Alternativas avaliadas

- Incorporar as validações dentro dos pipelines Batch.
- Criar um módulo independente para validação da qualidade dos dados.

## Decisão

Foi criada uma camada específica de Quality, executada de forma independente após a construção dos datasets.

## Justificativa

A separação entre processamento e validação tornou as regras reutilizáveis, facilitou a manutenção e permitiu que novas verificações fossem incorporadas sem alterar a lógica das pipelines.

---

# AD-005 — Arquitetura Cloud simplificada

## Contexto

O projeto deveria apresentar uma proposta de implantação em Cloud.

Durante a definição da arquitetura surgiram diferentes possibilidades de utilização de serviços gerenciados da AWS.

## Alternativas avaliadas

- Arquitetura composta por diversos serviços especializados.
- Arquitetura simplificada utilizando apenas os serviços diretamente relacionados à solução implementada.

## Decisão

Foi adotada uma arquitetura enxuta baseada em Amazon S3, Amazon EC2, Amazon MSK e Amazon SageMaker.

## Justificativa

Essa abordagem reduz complexidade, facilita compreensão da arquitetura e mantém total aderência aos componentes efetivamente implementados durante o desenvolvimento.

---

# AD-006 — FinOps orientado por decisões arquiteturais

## Contexto

O projeto deveria considerar práticas relacionadas à otimização de custos em ambientes Cloud.

## Alternativas avaliadas

- Tratar FinOps apenas como uma seção conceitual da documentação.
- Incorporar princípios de otimização diretamente nas decisões arquiteturais.

## Decisão

Os princípios de FinOps passaram a orientar decisões técnicas durante a construção da solução.

## Justificativa

Em vez de criar componentes específicos para controle de custos, a arquitetura foi concebida para reduzir naturalmente consumo de armazenamento, processamento e retrabalho por meio de decisões como atualização incremental da camada Gold, modularização da solução, validação antecipada da qualidade dos dados e utilização do formato Parquet.

---

# Lições Aprendidas

O desenvolvimento evidenciou que as principais melhorias da solução não surgiram da adoção de novas tecnologias, mas da evolução contínua da arquitetura ao longo do projeto.

Decisões como a adoção de uma arquitetura híbrida, a separação das responsabilidades entre módulos, a centralização das configurações e o desacoplamento da camada de qualidade aumentaram significativamente a organização, a escalabilidade e a facilidade de manutenção da plataforma.

Como resultado, a solução evoluiu de um conjunto de pipelines independentes para uma plataforma de Engenharia de Dados modular, preparada para crescimento incremental e alinhada às práticas adotadas em ambientes corporativos.