"""
Configuração dos clientes Kafka.

Responsabilidades
-----------------
- Carregar as configurações do ambiente (.env).
- Disponibilizar clientes Producer e Consumer.
- Centralizar toda a configuração do Kafka.
"""

from __future__ import annotations

import os

from confluent_kafka import Consumer, Producer
from dotenv import load_dotenv

load_dotenv()


# ============================================================================
# Configurações
# ============================================================================

BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)

TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "alfabetizacao-indicadores",
)

GROUP_ID = os.getenv(
    "KAFKA_GROUP_ID",
    "gold-consumer",
)


# ============================================================================
# Producer
# ============================================================================

def create_producer() -> Producer:
    """
    Cria um cliente Kafka Producer.

    Returns
    -------
    Producer
        Cliente configurado para publicação de eventos.
    """

    config = {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "client.id": "alfabetizacao-producer",
    }

    return Producer(config)


# ============================================================================
# Consumer
# ============================================================================

def create_consumer() -> Consumer:
    """
    Cria um cliente Kafka Consumer.

    Returns
    -------
    Consumer
        Cliente configurado para consumo de eventos.
    """

    config = {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True,
    }

    consumer = Consumer(config)

    consumer.subscribe([TOPIC])

    return consumer