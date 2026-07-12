"""
Funções reutilizáveis para validação dos datasets.

Responsabilidades
-----------------
- Carregar datasets.
- Validar arquivos.
- Validar estrutura.
- Validar chaves.
- Validar colunas obrigatórias.
- Consolidar os resultados das validações.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


# =============================================================================
# Dataset
# =============================================================================

def carregar_dataset(file_path: Path) -> pd.DataFrame:
    """
    Carrega um dataset Parquet.

    Parameters
    ----------
    file_path : Path
        Caminho do arquivo.

    Returns
    -------
    pd.DataFrame
    """

    return pd.read_parquet(file_path)


# =============================================================================
# Arquivo
# =============================================================================

def validar_arquivo(file_path: Path) -> bool:
    """
    Verifica se o arquivo existe.
    """

    return file_path.exists()


# =============================================================================
# Dataset vazio
# =============================================================================

def validar_dataset_vazio(df: pd.DataFrame) -> bool:
    """
    Verifica se o dataset possui registros.
    """

    return not df.empty


# =============================================================================
# Colunas obrigatórias
# =============================================================================

def validar_colunas(
    df: pd.DataFrame,
    required: list[str],
) -> bool:
    """
    Verifica se todas as colunas obrigatórias existem.
    """

    if not required:
        return True

    return set(required).issubset(df.columns)


# =============================================================================
# Duplicidade
# =============================================================================

def contar_duplicados(
    df: pd.DataFrame,
    key: list[str],
) -> int:
    """
    Conta registros duplicados considerando uma chave.
    """

    if not key:
        return 0

    return int(df.duplicated(key).sum())


# =============================================================================
# Validação da camada
# =============================================================================

def validar_camada(
    base_path: Path,
    rules: dict,
) -> list[dict]:
    """
    Executa todas as validações configuradas para uma camada.

    Parameters
    ----------
    base_path : Path
        Diretório raiz do projeto.

    rules : dict
        Regras da camada.

    Returns
    -------
    list[dict]
        Resultado consolidado das validações.
    """

    resultados = []

    data_path = base_path / rules["path"]

    for dataset, config in rules["datasets"].items():

        arquivo = data_path / f"{dataset}.parquet"

        resultado = {
            "dataset": dataset,
            "arquivo": False,
            "registros": 0,
            "vazio": False,
            "colunas": True,
            "duplicados": 0,
            "status": False,
            "mensagem": "",
        }

        # ==============================================================
        # Arquivo
        # ==============================================================

        resultado["arquivo"] = validar_arquivo(arquivo)

        if not resultado["arquivo"]:

            resultado["mensagem"] = "Arquivo não encontrado"

            resultados.append(resultado)

            continue

        # ==============================================================
        # Leitura
        # ==============================================================

        df = carregar_dataset(arquivo)

        # -----------------------------------------------------------------
        # DEBUG
        # -----------------------------------------------------------------

        #print()
        #print("=" * 70)
        #print(f"DATASET: {dataset}")
        #print("=" * 70)

        #for coluna in df.columns:
        #    print(coluna)

        #print("=" * 70)

        # -----------------------------------------------------------------

        resultado["registros"] = len(df)

        # ==============================================================
        # Dataset vazio
        # ==============================================================

        resultado["vazio"] = validar_dataset_vazio(df)

        # ==============================================================
        # Colunas obrigatórias
        # ==============================================================

        resultado["colunas"] = validar_colunas(
            df,
            config.get("required", []),
        )

        # ==============================================================
        # Duplicidade
        # ==============================================================

        resultado["duplicados"] = contar_duplicados(
            df,
            config.get("key", []),
        )

        # ==============================================================
        # Status final
        # ==============================================================

        resultado["status"] = all(
            [
                resultado["arquivo"],
                resultado["vazio"],
                resultado["colunas"],
                resultado["duplicados"] == 0,
            ]
        )

        # ==============================================================
        # Mensagem
        # ==============================================================

        if resultado["status"]:

            resultado["mensagem"] = "OK"

        elif not resultado["vazio"]:

            resultado["mensagem"] = "Dataset vazio"

        elif not resultado["colunas"]:

            resultado["mensagem"] = "Colunas obrigatórias ausentes"

        elif resultado["duplicados"] > 0:

            resultado["mensagem"] = (
                f"{resultado['duplicados']} duplicados"
            )

        resultados.append(resultado)

    return resultados