"""
Schema dos eventos de streaming.

Responsabilidades
-----------------
- Validar eventos.
- Serializar eventos para Kafka.
- Desserializar mensagens do Kafka.
"""

from __future__ import annotations

import json
from typing import Any

from jsonschema import validate


EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "event_id": {"type": "string"},
        "event_source": {"type": "string"},
        "timestamp": {"type": "string"},
        "ano": {"type": "integer"},
        "id_municipio": {"type": "string"},
        "rede": {"type": "string"},
        "media_portugues_anterior": {"type": "number"},
        "media_portugues_atual": {"type": "number"},
    },
    "required": [
        "event_id",
        "event_source",
        "timestamp",
        "ano",
        "id_municipio",
        "rede",
        "media_portugues_anterior",
        "media_portugues_atual",
    ],
}


def validate_event(evento: dict[str, Any]) -> None:
    """
    Valida um evento conforme o schema.
    """

    validate(
        instance=evento,
        schema=EVENT_SCHEMA,
    )


def serialize_event(evento: dict) -> bytes:
    """
    Valida e serializa um evento para envio ao Kafka.
    """

    validate_event(evento)

    return json.dumps(
        evento,
        ensure_ascii=False,
    ).encode("utf-8")


def deserialize_event(payload: bytes) -> dict:
    """
    Converte uma mensagem Kafka em dicionário.
    """

    return json.loads(
        payload.decode("utf-8")
    )