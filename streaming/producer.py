"""
Publicador de eventos.

Nesta Sprint apenas valida o schema
e exibe o evento.
"""

from streaming.schemas import validar_evento


def publicar_evento(
    evento: dict,
) -> None:
    """
    Publica um evento.

    Nesta Sprint apenas realiza
    validação do schema.
    """

    validar_evento(evento)

    print(
        f"Evento publicado: "
        f"{evento['event_id'][:8]}"
    )