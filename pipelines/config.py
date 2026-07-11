"""
Arquivo central de configuração da pipeline.

Responsabilidades
-----------------
- Definir o projeto do Google Cloud utilizado pela Base dos Dados.
- Centralizar os diretórios utilizados pela pipeline.
- Definir os datasets utilizados durante toda a pipeline.
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

SILVER_DIR = BASE_DIR / "data" / "silver"

# ============================================================================
# Configuração dos datasets da camada Bronze
# ============================================================================

DATASETS = [
    {
        "name": "uf",
        "enabled": True,
        "sql_file": "uf.sql",
        "output_file": "uf.parquet",
        "key": ["ano", "sigla_uf", "serie", "rede"],
    },
    {
        "name": "municipio",
        "enabled": True,
        "sql_file": "municipio.sql",
        "output_file": "municipio.parquet",
        "key": ["ano", "id_municipio", "serie", "rede"],
    },
    {
        "name": "meta_alfabetizacao_brasil",
        "enabled": True,
        "sql_file": "meta_alfabetizacao_brasil.sql",
        "output_file": "meta_alfabetizacao_brasil.parquet",
        "key": ["ano", "rede"],
    },
    {
        "name": "meta_alfabetizacao_uf",
        "enabled": True,
        "sql_file": "meta_alfabetizacao_uf.sql",
        "output_file": "meta_alfabetizacao_uf.parquet",
        "key": ["ano", "sigla_uf", "rede"],
    },
    {
        "name": "meta_alfabetizacao_municipio",
        "enabled": True,
        "sql_file": "meta_alfabetizacao_municipio.sql",
        "output_file": "meta_alfabetizacao_municipio.parquet",
        "key": ["ano", "id_municipio", "rede"],
    },
    {
        "name": "alunos",
        "enabled": True,
        "sql_file": "alunos.sql",
        "output_file": "alunos.parquet",
        "key": ["ano", "id_aluno"],
    },
]