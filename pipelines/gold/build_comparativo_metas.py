"""
Módulo responsável pela construção do dataset analítico
Comparativo de Metas.

Responsabilidades
-----------------
- Ler os datasets da camada Silver.
- Padronizar as tabelas de metas.
- Transformar as metas do formato wide para long.
- Consolidar Brasil, UF e Município em um único dataset.
"""

from pathlib import Path

import pandas as pd


# =============================================================================
# Constantes
# =============================================================================

COLUNAS_META = [
    "meta_alfabetizacao_2024",
    "meta_alfabetizacao_2025",
    "meta_alfabetizacao_2026",
    "meta_alfabetizacao_2027",
    "meta_alfabetizacao_2028",
    "meta_alfabetizacao_2029",
    "meta_alfabetizacao_2030",
]


# =============================================================================
# Função auxiliar
# =============================================================================

def _melt_metas(
    dataframe: pd.DataFrame,
    id_vars: list[str],
) -> pd.DataFrame:
    """
    Converte as colunas de metas para o formato long.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataset de entrada.

    id_vars : list[str]
        Colunas que permanecem fixas.

    Returns
    -------
    pd.DataFrame
    """

    resultado = dataframe.melt(
        id_vars=id_vars,
        value_vars=COLUNAS_META,
        var_name="ano_meta",
        value_name="meta_alfabetizacao",
    )

    resultado["ano_meta"] = (
        resultado["ano_meta"]
        .str.replace("meta_alfabetizacao_", "", regex=False)
        .astype(int)
    )

    return resultado


# =============================================================================
# Transformação Brasil
# =============================================================================

def transformar_brasil(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Padroniza o dataset de metas do Brasil.
    """

    brasil = _melt_metas(
        dataframe=dataframe,
        id_vars=[
            "ano",
            "rede",
            "taxa_alfabetizacao",
            "percentual_participacao",
        ],
    )

    brasil = brasil.rename(
        columns={
            "ano": "ano_origem",
        }
    )

    brasil["nivel_geografico"] = "Brasil"
    brasil["uf"] = pd.NA
    brasil["id_municipio"] = pd.NA
    brasil["municipio"] = pd.NA
    brasil["nivel_alfabetizacao"] = pd.NA

    brasil = brasil[
        [
            "nivel_geografico",
            "ano_origem",
            "ano_meta",
            "uf",
            "id_municipio",
            "municipio",
            "rede",
            "taxa_alfabetizacao",
            "nivel_alfabetizacao",
            "percentual_participacao",
            "meta_alfabetizacao",
        ]
    ]

    return brasil

# =============================================================================
# Transformação UF
# =============================================================================

def transformar_uf(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Padroniza o dataset de metas por UF.
    """

    uf = _melt_metas(
        dataframe=dataframe,
        id_vars=[
            "ano",
            "sigla_uf",
            "sigla_uf_nome",
            "rede",
            "taxa_alfabetizacao",
            "percentual_participacao",
        ],
    )

    uf = uf.rename(
        columns={
            "ano": "ano_origem",
            "sigla_uf": "uf",
        }
    )

    uf["nivel_geografico"] = "UF"
    uf["id_municipio"] = pd.NA
    uf["municipio"] = pd.NA
    uf["nivel_alfabetizacao"] = pd.NA

    uf = uf[
        [
            "nivel_geografico",
            "ano_origem",
            "ano_meta",
            "uf",
            "id_municipio",
            "municipio",
            "rede",
            "taxa_alfabetizacao",
            "nivel_alfabetizacao",
            "percentual_participacao",
            "meta_alfabetizacao",
        ]
    ]

    return uf

# =============================================================================
# Transformação Município
# =============================================================================

def transformar_municipio(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Padroniza o dataset de metas por município.
    """

    municipio = _melt_metas(
        dataframe=dataframe,
        id_vars=[
            "ano",
            "id_municipio",
            "id_municipio_nome",
            "rede",
            "taxa_alfabetizacao",
            "nivel_alfabetizacao",
            "percentual_participacao",
        ],
    )

    municipio = municipio.rename(
        columns={
            "ano": "ano_origem",
            "id_municipio_nome": "municipio",
        }
    )

    municipio["nivel_geografico"] = "Município"
    municipio["uf"] = pd.NA

    municipio = municipio[
        [
            "nivel_geografico",
            "ano_origem",
            "ano_meta",
            "uf",
            "id_municipio",
            "municipio",
            "rede",
            "taxa_alfabetizacao",
            "nivel_alfabetizacao",
            "percentual_participacao",
            "meta_alfabetizacao",
        ]
    ]

    return municipio

# =============================================================================
# Construção do dataset
# =============================================================================

def build_comparativo_metas(
    brasil_file: Path,
    uf_file: Path,
    municipio_file: Path,
    output_file: Path,
) -> None:
    """
    Constrói o dataset analítico de comparação de metas.

    Parameters
    ----------
    brasil_file : Path
        Arquivo meta_alfabetizacao_brasil.parquet.

    uf_file : Path
        Arquivo meta_alfabetizacao_uf.parquet.

    municipio_file : Path
        Arquivo meta_alfabetizacao_municipio.parquet.

    output_file : Path
        Arquivo de saída da camada Gold.

    Returns
    -------
    None
    """

    print()
    print("=" * 60)
    print("COMPARATIVO DE METAS")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # Leitura
    # -------------------------------------------------------------------------

    brasil = pd.read_parquet(brasil_file)

    uf = pd.read_parquet(uf_file)

    municipio = pd.read_parquet(municipio_file)

    print(f"Brasil.................: {len(brasil):,}")
    print(f"UF.....................: {len(uf):,}")
    print(f"Municípios.............: {len(municipio):,}")

    # -------------------------------------------------------------------------
    # Transformação
    # -------------------------------------------------------------------------

    brasil = transformar_brasil(brasil)

    uf = transformar_uf(uf)

    municipio = transformar_municipio(municipio)

    # -------------------------------------------------------------------------
    # Consolidação
    # -------------------------------------------------------------------------

    comparativo = pd.concat(
        [
            brasil,
            uf,
            municipio,
        ],
        ignore_index=True,
    )

    # -------------------------------------------------------------------------
    # Ordenação
    # -------------------------------------------------------------------------

    comparativo = comparativo.sort_values(
        by=[
            "nivel_geografico",
            "ano_origem",
            "ano_meta",
        ],
        ignore_index=True,
    )

    comparativo = comparativo.astype(
    {
        "nivel_geografico": "string",
        "uf": "string",
        "id_municipio": "string",
        "municipio": "string",
        "rede": "string",
    }
)

    # -------------------------------------------------------------------------
    # Estatísticas
    # -------------------------------------------------------------------------

    print()

    print(f"Registros finais.......: {len(comparativo):,}")
    print(f"Colunas................: {len(comparativo.columns)}")

    print()

    print("Registros por nível geográfico")

    print(
        comparativo["nivel_geografico"]
        .value_counts()
        .sort_index()
    )

    print()

    print("Metas por ano")

    print(
        comparativo["ano_meta"]
        .value_counts()
        .sort_index()
    )

    # -------------------------------------------------------------------------
    # Escrita
    # -------------------------------------------------------------------------

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    comparativo.to_parquet(
        output_file,
        index=False,
    )

    print()

    print(f"Arquivo salvo..........: {output_file}")

    print("=" * 60)