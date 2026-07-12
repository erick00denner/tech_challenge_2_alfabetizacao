from pathlib import Path

from streaming.simulator import (
    gerar_eventos,
    imprimir_eventos,
    imprimir_resumo,
)


def main():

    eventos = gerar_eventos(
        Path("data/silver/municipio.parquet")
    )

    imprimir_resumo(eventos)

    imprimir_eventos(eventos)


if __name__ == "__main__":
    main()