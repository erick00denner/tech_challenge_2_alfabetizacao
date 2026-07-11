# Ativar ambiente virtual
source .venv/bin/activate

# Executar pipeline
python -m pipelines.run_pipeline


# Estrutura do repositório
tech_challenge_2_alfabetizacao/
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│   ├── ANALISE_BRONZE.md
│   └── DECISIONS.md
│
├── notebooks/
│   └── 01_exploracao_bronze.ipynb
│
├── pipelines/
│   ├── ingest/
│   ├── silver/
│   ├── gold/
│   ├── config.py
│   └── run_pipeline.py
│
├── sql/
├── requirements.txt
└── README.md