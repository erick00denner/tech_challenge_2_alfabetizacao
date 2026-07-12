"""
Pipeline de Streaming.

Executa:

Simulador

↓

Producer
"""

from pathlib import Path

from streaming.producer import publicar_evento
from streaming.simulator import gerar_eventos


def main():

    print("=" * 60)
    print("STREAMING")
    print("=" * 60)

    eventos = gerar_eventos(
        Path("data/silver/municipio.parquet")
    )

    for evento in eventos:

        publicar_evento(evento)


if __name__ == "__main__":
    main()