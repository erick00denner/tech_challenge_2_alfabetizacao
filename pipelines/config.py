"""
Arquivo central de configuração da pipeline.

Responsabilidades
-----------------
- Definir o projeto do Google Cloud utilizado pela Base dos Dados.
- Centralizar os diretórios utilizados pela pipeline.
- Definir os datasets que serão ingeridos para a camada Bronze.

Qualquer alteração de tabelas, diretórios ou arquivos SQL deve ser
realizada exclusivamente neste módulo.
"""

from pathlib import Path

# ============================================================================
# Projeto Google Cloud
# ============================================================================

PROJECT_ID = "techchallengefiap-502114"

# ============================================================================
# Diretórios do projeto
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SQL_DIR = BASE_DIR / "pipelines" / "sql"

BRONZE_DIR = BASE_DIR / "data" / "bronze"

# ============================================================================
# Configuração dos datasets da camada Bronze
# ============================================================================

DATASETS = [
    {
        "name": "uf",
        "enabled": True,
        "sql_file": "uf.sql",
        "output_file": "uf.parquet",
    },
    {
        "name": "municipio",
        "enabled": True,
        "sql_file": "municipio.sql",
        "output_file": "municipio.parquet",
    },
    {
        "name": "meta_alfabetizacao_brasil",
        "enabled": True,
        "sql_file": "meta_alfabetizacao_brasil.sql",
        "output_file": "meta_alfabetizacao_brasil.parquet",
    },
    {
        "name": "meta_alfabetizacao_uf",
        "enabled": True,
        "sql_file": "meta_alfabetizacao_uf.sql",
        "output_file": "meta_alfabetizacao_uf.parquet",
    },
    {
        "name": "meta_alfabetizacao_municipio",
        "enabled": True,
        "sql_file": "meta_alfabetizacao_municipio.sql",
        "output_file": "meta_alfabetizacao_municipio.parquet",
    },
    {
        "name": "alunos",
        "enabled": True,
        "sql_file": "alunos.sql",
        "output_file": "alunos.parquet",
    },
]