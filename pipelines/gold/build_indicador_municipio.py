"""
Módulo responsável pela construção do dataset analítico
Indicador por Município.

Responsabilidades
-----------------
- Ler os datasets da camada Silver.
- Integrar indicadores e metas por município.
- Produzir um dataset pronto para consumo analítico.
"""

from pathlib import Path

import pandas as pd


def build_indicador_municipio(
    municipio_file: Path,
    meta_file: Path,
    output_file: Path,
) -> None:
    """
    Constrói o dataset analítico de indicadores por município.

    Parameters
    ----------
    municipio_file : Path
        Arquivo municipio.parquet da camada Silver.

    meta_file : Path
        Arquivo meta_alfabetizacao_municipio.parquet da camada Silver.

    output_file : Path
        Caminho do arquivo da camada Gold.

    Returns
    -------
    None
    """

    print()
    print("=" * 60)
    print("INDICADOR POR MUNICÍPIO")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # Leitura dos datasets
    # -------------------------------------------------------------------------

    municipio = pd.read_parquet(municipio_file)

    meta = pd.read_parquet(meta_file)

    print(f"Registros município.....: {len(municipio):,}")
    print(f"Registros metas.........: {len(meta):,}")

    # -------------------------------------------------------------------------
    # Integração dos datasets
    # -------------------------------------------------------------------------

    indicador = municipio.merge(
        meta,
        how="left",
        on=["ano", "id_municipio", "rede"],
        suffixes=("", "_meta"),
    )

    # -------------------------------------------------------------------------
    # Renomeia colunas para facilitar o consumo analítico
    # -------------------------------------------------------------------------

    indicador = indicador.rename(
        columns={
            "id_municipio_nome": "municipio"
        }
    )

    # -------------------------------------------------------------------------
    # Seleção e organização das colunas
    # -------------------------------------------------------------------------

    indicador = indicador[
        [
            "ano",
            "id_municipio",
            "municipio",
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

    # -------------------------------------------------------------------------
    # Ordenação
    # -------------------------------------------------------------------------

    indicador = indicador.sort_values(
        by=["ano", "id_municipio", "rede"],
        ignore_index=True,
    )

    # -------------------------------------------------------------------------
    # Validação da chave
    # -------------------------------------------------------------------------

    duplicados = indicador.duplicated(
        subset=["ano", "id_municipio", "rede"]
    ).sum()

    # -------------------------------------------------------------------------
    # Estatísticas de qualidade
    # -------------------------------------------------------------------------

    print(f"Registros resultado.....: {len(indicador):,}")
    print(f"Duplicados chave........: {duplicados}")

    print()

    print("Valores nulos")

    print(
        indicador[
            [
                "nivel_alfabetizacao",
                "percentual_participacao",
            ]
        ]
        .isnull()
        .sum()
    )

    # -------------------------------------------------------------------------
    # Escrita do arquivo
    # -------------------------------------------------------------------------
    indicador = indicador.astype(
        {
            "id_municipio": "string",
            "municipio": "string",
            "rede": "string",
            "nivel_alfabetizacao": "Int64",
        }
    )
    
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    indicador.to_parquet(
        output_file,
        index=False,
    )

    print()
    print(f"Colunas................: {len(indicador.columns)}")
    print(f"Arquivo salvo..........: {output_file}")

    print("=" * 60)