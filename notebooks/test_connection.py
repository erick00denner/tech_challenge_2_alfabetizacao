import basedosdados as bd

PROJECT_ID = "techchallengefiap-502114"

bd.config.billing_project_id = PROJECT_ID

print("Projeto configurado:", PROJECT_ID)

df = bd.read_table(
    dataset_id="br_bd_diretorios_brasil",
    table_id="municipio",
    limit=5
)

print(df.head())