"""
Orquestrador principal da pipeline.

Responsabilidades
-----------------
- Executar a ingestão da camada Bronze.
- Executar a padronização da camada Silver.
- Coordenar a execução completa da pipeline.
"""

from pipelines.config import (
    DATASETS,
    SQL_DIR,
    BRONZE_DIR,
    SILVER_DIR,
)

from pipelines.ingest.download_dataset import download_dataset
from pipelines.silver.transform_dataset import transform_dataset


def run_bronze() -> None:
    """
    Executa a ingestão dos datasets da camada Bronze.

    Para cada dataset configurado:
    - executa a consulta SQL;
    - realiza o download dos dados;
    - grava o arquivo Parquet na camada Bronze.
    """

    print("=" * 60)
    print("PIPELINE BRONZE")
    print("=" * 60)

    for dataset in DATASETS:

        if not dataset["enabled"]:
            continue

        sql_file = SQL_DIR / dataset["sql_file"]

        output_file = BRONZE_DIR / dataset["output_file"]

        download_dataset(
            sql_path=sql_file,
            output_path=output_file,
        )


def run_silver() -> None:
    """
    Executa as transformações da camada Silver.

    Para cada dataset configurado:
    - lê o Parquet da Bronze;
    - valida a chave candidata;
    - padroniza os dados;
    - grava o Parquet na camada Silver.
    """

    print()
    print("=" * 60)
    print("PIPELINE SILVER")
    print("=" * 60)

    for dataset in DATASETS:

        if not dataset["enabled"]:
            continue

        input_file = BRONZE_DIR / dataset["output_file"]

        output_file = SILVER_DIR / dataset["output_file"]

        transform_dataset(
            input_file=input_file,
            output_file=output_file,
            key=dataset["key"],
        )


def main() -> None:
    """
    Executa toda a pipeline do projeto.

    Fluxo atual:

    Bronze
        ↓
    Silver
    """

    run_bronze()

    run_silver()

    print()
    print("=" * 60)
    print("PIPELINE FINALIZADA")
    print("=" * 60)


if __name__ == "__main__":
    main()