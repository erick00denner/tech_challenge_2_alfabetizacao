from pathlib import Path

import pandas as pd

from streaming.simulator import (
    gerar_eventos,
    imprimir_resumo,
)

BASE_PATH = Path(__file__).resolve().parents[1]

indicador = pd.read_parquet(
    BASE_PATH
    / "data"
    / "gold"
    / "indicador_municipio.parquet"
)

eventos = gerar_eventos(
    indicador,
    quantidade=10,
)

imprimir_resumo(eventos)