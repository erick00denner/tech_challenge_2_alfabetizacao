"""
Módulo responsável pela construção do dataset analítico
de evolução temporal da alfabetização.

Responsabilidades
-----------------
- Ler os datasets da camada Silver.
- Padronizar Brasil, UF e Município.
- Consolidar os três níveis geográficos.
- Gerar dataset otimizado para dashboards e análises temporais.
"""

from pathlib import Path

import pandas as pd


# =============================================================================
# Transformação Brasil
# =============================================================================


def transformar_brasil(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Padroniza o dataset nacional.
    """

    brasil = dataframe.rename(
        columns={
            "ano": "ano",
        }
    )

    brasil["nivel_geografico"] = "Brasil"

    brasil["uf"] = pd.NA
    brasil["id_municipio"] = pd.NA
    brasil["municipio"] = pd.NA
    brasil["nivel_alfabetizacao"] = pd.NA
    brasil["media_portugues"] = pd.NA

    brasil = brasil[
        [
            "nivel_geografico",
            "ano",
            "uf",
            "id_municipio",
            "municipio",
            "rede",
            "taxa_alfabetizacao",
            "media_portugues",
            "nivel_alfabetizacao",
            "percentual_participacao",
        ]
    ]

    return brasil


# =============================================================================
# Transformação UF
# =============================================================================


def transformar_uf(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    uf = dataframe.rename(
        columns={
            "sigla_uf": "uf",
        }
    )

    uf["nivel_geografico"] = "UF"

    uf["id_municipio"] = pd.NA
    uf["municipio"] = pd.NA
    uf["nivel_alfabetizacao"] = pd.NA
    uf["percentual_participacao"] = pd.NA

    uf = uf[
        [
            "nivel_geografico",
            "ano",
            "uf",
            "id_municipio",
            "municipio",
            "rede",
            "taxa_alfabetizacao",
            "media_portugues",
            "nivel_alfabetizacao",
            "percentual_participacao",
        ]
    ]

    return uf


# =============================================================================
# Transformação Município
# =============================================================================

def transformar_municipio(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    municipio = dataframe.rename(
        columns={
            "id_municipio_nome": "municipio",
        }
    )

    municipio["nivel_geografico"] = "Município"

    municipio["uf"] = pd.NA

    municipio["percentual_participacao"] = pd.NA
    municipio["nivel_alfabetizacao"] = pd.NA

    municipio = municipio[
        [
            "nivel_geografico",
            "ano",
            "uf",
            "id_municipio",
            "municipio",
            "rede",
            "taxa_alfabetizacao",
            "media_portugues",
            "nivel_alfabetizacao",
            "percentual_participacao",
        ]
    ]

    return municipio

# =============================================================================
# Construção do dataset
# =============================================================================


def build_evolucao_temporal(
    brasil_file: Path,
    uf_file: Path,
    municipio_file: Path,
    output_file: Path,
) -> None:
    """
    Constrói o dataset analítico de evolução temporal.
    """

    print()
    print("=" * 60)
    print("EVOLUÇÃO TEMPORAL")
    print("=" * 60)

    brasil = pd.read_parquet(brasil_file)

    uf = pd.read_parquet(uf_file)

    municipio = pd.read_parquet(municipio_file)

    print(f"Brasil.................: {len(brasil):,}")
    print(f"UF.....................: {len(uf):,}")
    print(f"Municípios.............: {len(municipio):,}")

    brasil = transformar_brasil(brasil)

    uf = transformar_uf(uf)

    municipio = transformar_municipio(municipio)

    evolucao = pd.concat(
        [
            brasil,
            uf,
            municipio,
        ],
        ignore_index=True,
    )

    evolucao = evolucao.sort_values(
        by=[
            "nivel_geografico",
            "ano",
        ],
        ignore_index=True,
    )

    evolucao = evolucao.astype(
        {
            "nivel_geografico": "string",
            "uf": "string",
            "id_municipio": "string",
            "municipio": "string",
            "rede": "string",
            "nivel_alfabetizacao": "Int64",
        }
    )

    print()

    print(f"Registros finais.......: {len(evolucao):,}")

    print(f"Colunas................: {len(evolucao.columns)}")

    print()

    print("Registros por nível geográfico")

    print(
        evolucao["nivel_geografico"]
        .value_counts()
        .sort_index()
    )

    print()

    print("Registros por ano")

    print(
        evolucao["ano"]
        .value_counts()
        .sort_index()
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    evolucao.to_parquet(
        output_file,
        index=False,
    )

    print()

    print(f"Arquivo salvo..........: {output_file}")

    print("=" * 60)