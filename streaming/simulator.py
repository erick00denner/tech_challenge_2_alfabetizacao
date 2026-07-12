"""
Simulador de eventos de atualização dos indicadores
de alfabetização.
"""

from datetime import datetime
from pathlib import Path
import uuid

import numpy as np
import pandas as pd

from streaming.kafka_config import (
    EVENTS_PER_EXECUTION,
    RANDOM_SEED,
)

np.random.seed(RANDOM_SEED)


def gerar_eventos(
    municipio_file: Path,
) -> list[dict]:
    """
    Gera eventos simulados de atualização da média de
    proficiência em Português.
    """

    municipio = pd.read_parquet(municipio_file)

    amostra = municipio.sample(
        EVENTS_PER_EXECUTION,
        random_state=RANDOM_SEED,
    )

    eventos = []

    for _, linha in amostra.iterrows():

        media_anterior = float(linha["media_portugues"])

        variacao = np.random.normal(
            loc=0,
            scale=0.7,
        )

        media_atual = round(
            media_anterior + variacao,
            2,
        )

        media_atual = max(
            0,
            min(800, media_atual),
        )

        eventos.append(
            {
                "event_id": str(uuid.uuid4()),
                "event_source": "simulator",
                "timestamp": datetime.now().isoformat(),
                "ano": int(linha["ano"]),
                "id_municipio": str(linha["id_municipio"]),
                "rede": linha["rede"],
                "media_portugues_anterior": media_anterior,
                "media_portugues_atual": media_atual,
            }
        )

    return eventos


def imprimir_resumo(
    eventos: list[dict],
) -> None:
    """
    Exibe um resumo da simulação.
    """

    anos = sorted(
        {
            evento["ano"]
            for evento in eventos
        }
    )

    media = np.mean(
        [
            evento["media_portugues_atual"]
            for evento in eventos
        ]
    )

    print("=" * 70)
    print("SIMULAÇÃO DE EVENTOS")
    print("=" * 70)
    print(f"Eventos gerados.....: {len(eventos):,}")
    municipios = len(
        {
            evento["id_municipio"]
            for evento in eventos
        }
    )

    print(f"Municípios únicos...: {municipios:,}")
    print(
        f"Anos................: {', '.join(map(str, anos))}"
    )
    print(f"Média simulada......: {media:.2f}")
    print("=" * 70)


def imprimir_eventos(
    eventos: list[dict],
) -> None:
    """
    Exibe os eventos em formato tabular.
    """

    print()

    print("=" * 130)
    print(
        f"{'EVENT_ID':<10}"
        f"{'ANO':>8}"
        f"{'MUNICÍPIO':>15}"
        f"{'REDE':>35}"
        f"{'ANTERIOR':>15}"
        f"{'ATUAL':>15}"
    )

    print("=" * 130)

    for evento in eventos:

        print(
            f"{evento['event_id'][:8]:<10}"
            f"{evento['ano']:>8}"
            f"{evento['id_municipio']:>15}"
            f"{evento['rede'][:30]:>35}"
            f"{evento['media_portugues_anterior']:>15.2f}"
            f"{evento['media_portugues_atual']:>15.2f}"
        )

    print("=" * 130)