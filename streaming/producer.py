"""
Producer Kafka.
"""

from __future__ import annotations

from confluent_kafka import KafkaException

from streaming.kafka_config import (
    TOPIC,
    create_producer,
)
from streaming.schemas import (
    deserialize_event,
    serialize_event,
)


def delivery_report(err, msg) -> None:
    """
    Callback executado após o envio da mensagem.
    """

    if err is not None:
        print(f"❌ Erro: {err}")

    else:

        evento = deserialize_event(msg.value())

        print(
            f"✔ Evento enviado | "
            f"{evento['event_id'][:8]} | "
            f"{evento['id_municipio']}"
        )


def publish_events(eventos: list[dict]) -> None:
    """
    Publica uma lista de eventos no Kafka.
    """

    producer = create_producer()

    print()
    print("=" * 70)
    print("PUBLICANDO EVENTOS")
    print("=" * 70)

    try:

        for evento in eventos:

            producer.produce(
                topic=TOPIC,
                key=evento["id_municipio"],
                value=serialize_event(evento),
                callback=delivery_report,
            )

            producer.poll(0)

        producer.flush()

        print("=" * 70)
        print("Publicação concluída.")
        print("=" * 70)

    except KafkaException as exc:

        print(exc)