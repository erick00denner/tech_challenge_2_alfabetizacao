from pathlib import Path

from streaming.producer import publicar_evento
from streaming.simulator import (
    gerar_eventos,
    imprimir_resumo,
)


def main():

    eventos = gerar_eventos(
        Path("data/silver/municipio.parquet")
    )

    imprimir_resumo(eventos)

    print()

    print("=" * 70)
    print("PUBLICANDO EVENTOS")
    print("=" * 70)

    for evento in eventos:

        publicar_evento(evento)


if __name__ == "__main__":
    main()