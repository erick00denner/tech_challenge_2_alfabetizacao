"""
Atualização do dataset indicador_municipio.

Responsabilidades
-----------------
- Receber um evento do Kafka.
- Atualizar o indicador correspondente.
- Persistir novamente o dataset Gold.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def update_indicador(
    evento: dict,
    indicador_file: Path,
) -> None:
    """
    Atualiza um indicador do dataset Gold.
    """

    indicador = pd.read_parquet(indicador_file)

    filtro = (
        (indicador["ano"] == evento["ano"])
        & (indicador["id_municipio"] == evento["id_municipio"])
        & (indicador["rede"] == evento["rede"])
    )

    if filtro.sum() == 0:

        print(
            f"Registro não encontrado: "
            f"{evento['ano']} | "
            f"{evento['id_municipio']} | "
            f"{evento['rede']}"
        )

        return

    indicador.loc[
        filtro,
        "media_portugues",
    ] = evento["media_portugues_atual"]

    indicador.to_parquet(
        indicador_file,
        index=False,
    )

    print(
        "Indicador atualizado -> "
        f"{evento['id_municipio']} | "
        f"{evento['ano']}"
    )