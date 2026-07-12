"""
Executa uma simulação completa de streaming.

Fluxo
-----
1. Carrega o dataset indicador_municipio.
2. Gera eventos simulados.
3. Exibe um resumo da simulação.
4. Publica os eventos no Kafka.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from streaming.producer import publish_events
from streaming.simulator import (
    gerar_eventos,
    imprimir_resumo,
)


def main() -> None:
    """
    Executa uma simulação completa.
    """

    base_path = Path(__file__).resolve().parents[1]

    indicador = pd.read_parquet(
        base_path
        / "data"
        / "gold"
        / "indicador_municipio.parquet"
    )

    eventos = gerar_eventos(
        indicador,
        quantidade=10,
    )

    imprimir_resumo(eventos)

    publish_events(eventos)


if __name__ == "__main__":
    main()