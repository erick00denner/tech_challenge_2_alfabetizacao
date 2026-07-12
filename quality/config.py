"""
Configuração da camada Quality.

Responsabilidades
-----------------
- Centralizar as regras de validação dos datasets.
- Definir os caminhos das camadas.
- Definir chaves candidatas.
- Definir colunas obrigatórias.

Toda alteração de regras de validação deve ser realizada
neste arquivo, mantendo os validadores desacoplados da
estrutura dos datasets.
"""

from __future__ import annotations


# =============================================================================
# Configuração
# =============================================================================

QUALITY_CONFIG = {

    # =========================================================================
    # Bronze
    # =========================================================================

    "bronze": {

        "path": "data/bronze",

        "datasets": {

            "uf": {},

            "municipio": {},

            "meta_alfabetizacao_brasil": {},

            "meta_alfabetizacao_uf": {},

            "meta_alfabetizacao_municipio": {},

            "alunos": {},

        },

    },

    # =========================================================================
    # Silver
    # =========================================================================

    "silver": {

        "path": "data/silver",

        "datasets": {

            "uf": {

                "key": [
                    "sigla_uf",
                    "ano",
                    "serie",
                    "rede",
                ],

            },

            "municipio": {

                "key": [
                    "id_municipio",
                    "ano",
                    "rede",
                ],

            },

            "meta_alfabetizacao_brasil": {

                "key": [
                    "ano",
                    "rede",
                ],

            },

            "meta_alfabetizacao_uf": {

                "key": [
                    "sigla_uf",
                    "ano",
                    "rede",
                ],

            },

            "meta_alfabetizacao_municipio": {

                "key": [
                    "id_municipio",
                    "ano",
                    "rede",
                ],

            },

            "alunos": {

                "key": [
                    "id_aluno",
                    "ano",
                ],

            },

        },

    },

    # =========================================================================
    # Gold
    # =========================================================================

    "gold": {

        "path": "data/gold",

        "datasets": {

            "indicador_municipio": {

                "key": [
                    "id_municipio",
                    "ano",
                    "rede",
                ],

                "required": [
                    "id_municipio",
                    "ano",
                    "rede",
                ],

            },

            "comparativo_metas": {

                "required": [
                    "nivel_geografico",
                    "ano_meta",
                ],

            },

            "evolucao_temporal": {

                "required": [
                    "ano",
                ],

            },

            "alunos_modelagem": {

                "required": [
                    "id_aluno",
                    "id_municipio",
                ],

            },

        },

    },

}