from pathlib import Path

import pandas as pd

from streaming.producer import publish_events
from streaming.simulator import gerar_eventos

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

publish_events(eventos)