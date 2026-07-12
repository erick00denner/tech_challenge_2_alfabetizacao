"""
Formatação do relatório da camada Quality.

Responsabilidades
-----------------
- Exibir os resultados das validações.
- Exibir o resumo da execução.
"""

from __future__ import annotations


# =============================================================================
# Cabeçalho
# =============================================================================

def imprimir_cabecalho() -> None:
    """
    Exibe o cabeçalho da execução.
    """

    print()
    print("=" * 70)
    print("QUALITY CHECK")
    print("=" * 70)


# =============================================================================
# Camada
# =============================================================================

def imprimir_camada(
    nome: str,
    resultados: list[dict],
) -> None:
    """
    Exibe o resultado de uma camada.

    Parameters
    ----------
    nome : str
        Nome da camada.

    resultados : list[dict]
        Resultado das validações.
    """

    print()
    print(nome.upper())
    print("-" * 70)

    for resultado in resultados:

        simbolo = "✓" if resultado["status"] else "✗"

        print(
            f"{simbolo} "
            f"{resultado['dataset']:<35}"
            f"Registros: {resultado['registros']:>8}   "
            f"{resultado['mensagem']}"
        )


# =============================================================================
# Resumo
# =============================================================================

def imprimir_resumo(
    resultados: list[list[dict]],
) -> None:
    """
    Exibe o resumo da execução.

    Parameters
    ----------
    resultados : list[list[dict]]
        Resultado consolidado das camadas.
    """

    datasets = sum(
        len(camada)
        for camada in resultados
    )

    aprovados = sum(
        resultado["status"]
        for camada in resultados
        for resultado in camada
    )

    falhas = datasets - aprovados

    print()
    print("=" * 70)
    print("RESUMO")
    print("=" * 70)

    print(f"Datasets avaliados...: {datasets}")
    print(f"Aprovados............: {aprovados}")
    print(f"Falhas...............: {falhas}")

    print("=" * 70)