"""
Pipeline principal da camada Bronze.

Responsabilidades
-----------------
- Percorrer todos os datasets configurados em config.py.
- Executar a ingestão dos dados para a camada Bronze.
- Orquestrar a execução da pipeline Batch.

Nenhuma transformação ou regra de negócio é aplicada nesta etapa.
"""

from pipelines.config import (
    BRONZE_DIR,
    DATASETS,
    SQL_DIR,
)

from pipelines.ingest.download_dataset import download_dataset


def main() -> None:
    """
    Executa a pipeline completa da camada Bronze.
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
            sql_file,
            output_file,
        )

    print("=" * 60)
    print("PIPELINE FINALIZADA")
    print("=" * 60)


if __name__ == "__main__":
    main()