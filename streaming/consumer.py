"""
Consumidor de eventos Kafka.

Responsável por consumir eventos publicados pelo Producer
e preparar a atualização dos indicadores analíticos.
"""

from __future__ import annotations

import json

from streaming.kafka_config import create_consumer

from pathlib import Path

from streaming.update_gold import update_indicador


def consumir_eventos() -> None:
    """
    Consome continuamente os eventos do Kafka.
    """

    consumer = create_consumer()

    print()
    print("=" * 70)
    print("CONSUMIDOR INICIADO")
    print("=" * 70)

    try:

        while True:

            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(f"Erro: {msg.error()}")
                continue

            evento = json.loads(msg.value().decode("utf-8"))

            update_indicador(
                evento,
                Path("data/gold/indicador_municipio.parquet"),
            )

            print(
                f"""
Evento recebido
------------------------------------------------------------
ID.............: {evento["event_id"][:8]}
Ano............: {evento["ano"]}
Município......: {evento["id_municipio"]}
Rede...........: {evento["rede"]}
Média anterior.: {evento["media_portugues_anterior"]:.2f}
Média atual....: {evento["media_portugues_atual"]:.2f}
------------------------------------------------------------
"""
            )

    except KeyboardInterrupt:

        print("\nEncerrando consumer...")

    finally:

        consumer.close()


if __name__ == "__main__":
    consumir_eventos()