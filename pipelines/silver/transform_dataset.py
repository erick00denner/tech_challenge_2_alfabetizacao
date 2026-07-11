"""
Módulo responsável pela transformação da camada Bronze para a camada Silver.

Responsabilidades
-----------------
- Ler os datasets da camada Bronze.
- Validar a integridade dos dados.
- Padronizar campos textuais.
- Ordenar os registros utilizando a chave candidata.
- Salvar os dados tratados na camada Silver.

Nenhuma transformação altera o significado dos dados originais.
"""

from pathlib import Path

import pandas as pd


def transform_dataset(
    input_file: Path,
    output_file: Path,
    key: list[str],
) -> None:
    """
    Executa as transformações padronizadas da camada Silver.

    Parameters
    ----------
    input_file : Path
        Caminho do arquivo Parquet da camada Bronze.

    output_file : Path
        Caminho do arquivo Parquet da camada Silver.

    key : list[str]
        Colunas que compõem a chave candidata do dataset.

    Returns
    -------
    None
    """

    try:

        print(f"Processando {input_file.name}...")

        # ---------------------------------------------------------------------
        # Leitura do dataset Bronze
        # ---------------------------------------------------------------------

        df = pd.read_parquet(input_file)
        total_registros = len(df)
        total_colunas = len(df.columns)

        # ---------------------------------------------------------------------
        # Validação da chave candidata
        # ---------------------------------------------------------------------

        duplicados_chave = df.duplicated(subset=key).sum()

        if duplicados_chave > 0:
            raise RuntimeError(
                f"Chave candidata inválida. "
                f"Foram encontrados {duplicados_chave} registros duplicados."
            )
        
        print("=" * 60)
        print(f"Registros........: {total_registros:,}")
        print(f"Colunas..........: {total_colunas}")
        print(f"Duplicados chave.: {duplicados_chave}")

        # ---------------------------------------------------------------------
        # Padronização dos campos texto
        # ---------------------------------------------------------------------

        colunas_texto = df.select_dtypes(include="object").columns

        for coluna in colunas_texto:

            df[coluna] = df[coluna].str.strip()

        # ---------------------------------------------------------------------
        # Ordenação dos registros
        # ---------------------------------------------------------------------

        df = df.sort_values(
            by=key,
            ignore_index=True,
        )

        # ---------------------------------------------------------------------
        # Gravação da camada Silver
        # ---------------------------------------------------------------------

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_parquet(
            output_file,
            index=False,
        )

        print(f"Arquivo salvo....: {output_file}")
        print("=" * 60)

    except Exception as error:

        raise RuntimeError(
            f"Erro ao transformar '{input_file.name}'."
        ) from error