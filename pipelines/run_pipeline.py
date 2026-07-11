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
    GOLD_DIR,

)

from pipelines.ingest.download_dataset import download_dataset

from pipelines.silver.transform_dataset import transform_dataset

from pipelines.gold.build_indicador_municipio import build_indicador_municipio
from pipelines.gold.build_comparativo_metas import build_comparativo_metas
from pipelines.gold.build_evolucao_temporal import build_evolucao_temporal
from pipelines.gold.build_alunos_modelagem import build_alunos_modelagem


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
    print()

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
    print()

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


def run_gold() -> None:
    """
    Executa a construção dos datasets analíticos da camada Gold.
    """

    print()
    print("=" * 60)
    print("PIPELINE GOLD")
    print("=" * 60)

    # ------------------------------------------------------------
    # Indicador por município
    # ------------------------------------------------------------

    print()
    print("Construindo indicador_municipio.parquet...")

    build_indicador_municipio(
        municipio_file=SILVER_DIR / "municipio.parquet",
        meta_file=SILVER_DIR / "meta_alfabetizacao_municipio.parquet",
        output_file=GOLD_DIR / "indicador_municipio.parquet",
    )

    # ------------------------------------------------------------
    # Comparativo de metas
    # ------------------------------------------------------------

    print()
    print("Construindo comparativo_metas.parquet...")

    build_comparativo_metas(
        brasil_file=SILVER_DIR / "meta_alfabetizacao_brasil.parquet",
        uf_file=SILVER_DIR / "meta_alfabetizacao_uf.parquet",
        municipio_file=SILVER_DIR / "meta_alfabetizacao_municipio.parquet",
        output_file=GOLD_DIR / "comparativo_metas.parquet",
    )

    # ------------------------------------------------------------
    # Evolução temporal
    # ------------------------------------------------------------

    print()
    print("Construindo evolucao_temporal.parquet...")

    build_evolucao_temporal(
        brasil_file=SILVER_DIR / "meta_alfabetizacao_brasil.parquet",
        uf_file=SILVER_DIR / "uf.parquet",
        municipio_file=SILVER_DIR / "municipio.parquet",
        output_file=GOLD_DIR / "evolucao_temporal.parquet",
    )

    # ------------------------------------------------------------
    # Alunos para modelagem
    # ------------------------------------------------------------

    print()
    print("Construindo alunos_modelagem.parquet...")

    build_alunos_modelagem(
        alunos_file=SILVER_DIR / "alunos.parquet",
        indicador_file=GOLD_DIR / "indicador_municipio.parquet",
        output_file=GOLD_DIR / "alunos_modelagem.parquet",
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

    run_gold()

    print()
    print("=" * 60)
    print("PIPELINE FINALIZADA")
    print("=" * 60)


if __name__ == "__main__":
    main()