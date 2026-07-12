"""
Schema dos eventos publicados no Kafka.
"""

EVENT_COLUMNS = [
    "event_id",
    "event_source",
    "timestamp",
    "ano",
    "id_municipio",
    "rede",
    "media_portugues_anterior",
    "media_portugues_atual",
]


def validar_evento(evento: dict) -> None:
    """
    Valida se o evento possui todos os campos obrigatórios.

    Parameters
    ----------
    evento : dict
        Evento recebido.

    Raises
    ------
    ValueError
        Caso algum campo obrigatório esteja ausente.
    """

    faltantes = [
        coluna
        for coluna in EVENT_COLUMNS
        if coluna not in evento
    ]

    if faltantes:
        raise ValueError(
            f"Campos obrigatórios ausentes: {faltantes}"
        )