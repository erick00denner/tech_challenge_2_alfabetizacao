"""
Executa o consumidor Kafka.

Responsável por iniciar o processamento contínuo
dos eventos publicados no tópico.
"""

from __future__ import annotations

from streaming.consumer import consumir_eventos


def main() -> None:
    """
    Inicializa o consumidor.
    """

    consumir_eventos()


if __name__ == "__main__":
    main()