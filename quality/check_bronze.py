"""
Validação da camada Bronze.
"""

from __future__ import annotations

from pathlib import Path

from quality.checks import validar_camada
from quality.config import QUALITY_CONFIG


def executar(base_path: Path) -> list[dict]:
    """
    Executa as validações da camada Bronze.

    Parameters
    ----------
    base_path : Path
        Diretório raiz do projeto.

    Returns
    -------
    list[dict]
        Resultado das validações.
    """

    return validar_camada(
        base_path,
        QUALITY_CONFIG["bronze"],
    )