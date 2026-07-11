"""
Módulo responsável pela construção do dataset analítico
Alunos para Modelagem.

Responsabilidades
-----------------
- Ler o dataset de alunos da camada Silver.
- Integrar indicadores municipais da camada Gold.
- Produzir um dataset enriquecido para análises estatísticas
  e treinamento de modelos de Machine Learning.
"""

from pathlib import Path

import pandas as pd


def build_alunos_modelagem(
    alunos_file: Path,
    indicador_file: Path,
    output_file: Path,
) -> None:
    """
    Constrói o dataset analítico de alunos para modelagem.

    Parameters
    ----------
    alunos_file : Path
        Arquivo alunos.parquet da camada Silver.

    indicador_file : Path
        Arquivo indicador_municipio.parquet da camada Gold.

    output_file : Path
        Caminho do arquivo da camada Gold.

    Returns
    -------
    None
    """

    print()
    print("=" * 60)
    print("ALUNOS MODELAGEM")
    print("=" * 60)

    # ------------------------------------------------------------
    # Leitura
    # ------------------------------------------------------------

    alunos = pd.read_parquet(alunos_file)

    indicador = pd.read_parquet(indicador_file)

    print(f"Alunos.....................: {len(alunos):,}")
    print(f"Indicadores...............: {len(indicador):,}")

    # ------------------------------------------------------------
    # Seleção das colunas necessárias
    # ------------------------------------------------------------

    indicador = indicador[
        [
            "ano",
            "id_municipio",
            "rede",
            "taxa_alfabetizacao",
            "media_portugues",
            "nivel_alfabetizacao",
            "percentual_participacao",
            "meta_alfabetizacao_2024",
            "meta_alfabetizacao_2025",
            "meta_alfabetizacao_2026",
            "meta_alfabetizacao_2027",
            "meta_alfabetizacao_2028",
            "meta_alfabetizacao_2029",
            "meta_alfabetizacao_2030",
        ]
    ]

    # ------------------------------------------------------------
    # Enriquecimento
    # ------------------------------------------------------------

    dataset = alunos.merge(
        indicador,
        how="left",
        on=[
            "ano",
            "id_municipio",
            "rede",
        ],
    )

    # ------------------------------------------------------------
    # Padronização dos tipos
    # ------------------------------------------------------------

    dataset = dataset.astype(
        {
            "id_aluno": "string",
            "id_escola": "string",
            "id_municipio": "string",
            "id_municipio_nome": "string",
            "serie": "string",
            "rede": "string",
            "presenca": "string",
            "preenchimento_caderno": "string",
            "alfabetizado": "string",
            "nivel_alfabetizacao": "Int64",
        }
    )

    # ------------------------------------------------------------
    # Estatísticas
    # ------------------------------------------------------------

    sem_indicador = dataset["taxa_alfabetizacao"].isna().sum()

    print()
    print(f"Registros finais..........: {len(dataset):,}")
    print(f"Colunas...................: {dataset.shape[1]}")

    print()

    print(
        f"Alunos sem indicador......: "
        f"{sem_indicador:,} "
        f"({sem_indicador / len(dataset):.2%})"
    )

    # ------------------------------------------------------------
    # Escrita
    # ------------------------------------------------------------

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataset.to_parquet(
        output_file,
        index=False,
    )

    print()
    print(f"Arquivo salvo.............: {output_file}")