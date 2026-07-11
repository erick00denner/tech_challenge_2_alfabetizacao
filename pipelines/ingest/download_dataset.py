"""
Módulo responsável pela ingestão dos dados da Base dos Dados.

Responsabilidades
-----------------
- Executar o SQL oficial disponibilizado pela Base dos Dados.
- Salvar os resultados em formato Parquet na camada Bronze.
- Não aplicar qualquer transformação nos dados.

A camada Bronze representa a cópia fiel da origem dos dados.
"""

from pathlib import Path

import basedosdados as bd

from pipelines.config import PROJECT_ID


def download_dataset(sql_path: Path, output_path: Path) -> None:
    """
    Executa uma consulta SQL da Base dos Dados e salva o resultado
    em formato Parquet na camada Bronze.

    Parameters
    ----------
    sql_path : Path
        Caminho do arquivo SQL.

    output_path : Path
        Caminho do arquivo Parquet que será gerado.
    """

    try:

        print(f"Baixando {sql_path.name}...")

        query = sql_path.read_text(encoding="utf-8")

        df = bd.read_sql(
            query=query,
            billing_project_id=PROJECT_ID,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_parquet(output_path, index=False)

        print(f"Arquivo salvo em {output_path}")

    except Exception as error:

        raise RuntimeError(
            f"Erro ao processar o dataset '{sql_path.name}'."
        ) from error