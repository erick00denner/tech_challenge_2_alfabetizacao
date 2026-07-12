"""
Orquestrador da camada Quality.

Responsabilidades
-----------------
- Executar as validações das camadas Bronze, Silver e Gold.
- Consolidar os resultados.
- Exibir o relatório final.
"""

from __future__ import annotations

from pathlib import Path

from quality.check_bronze import executar as validar_bronze
from quality.check_gold import executar as validar_gold
from quality.check_silver import executar as validar_silver
from quality.report import (
    imprimir_cabecalho,
    imprimir_camada,
    imprimir_resumo,
)


# =============================================================================
# Execução
# =============================================================================

def executar_quality() -> None:
    """
    Executa todas as validações da pipeline.
    """

    base_path = Path(__file__).resolve().parent.parent

    imprimir_cabecalho()

    # -------------------------------------------------------------------------
    # Bronze
    # -------------------------------------------------------------------------

    bronze = validar_bronze(base_path)

    imprimir_camada(
        "Bronze",
        bronze,
    )

    # -------------------------------------------------------------------------
    # Silver
    # -------------------------------------------------------------------------

    silver = validar_silver(base_path)

    imprimir_camada(
        "Silver",
        silver,
    )

    # -------------------------------------------------------------------------
    # Gold
    # -------------------------------------------------------------------------

    gold = validar_gold(base_path)

    imprimir_camada(
        "Gold",
        gold,
    )

    # -------------------------------------------------------------------------
    # Resumo
    # -------------------------------------------------------------------------

    imprimir_resumo(
        [
            bronze,
            silver,
            gold,
        ]
    )


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    executar_quality()