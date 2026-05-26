import pandas as pd
from pathlib import Path
import sys

base_consolidada_path = Path('data/gold/base_consolidada_2022.csv')
if not base_consolidada_path.exists():
    print(f"❌ Erro: O arquivo '{base_consolidada_path}' não existe.")
    sys.exit(1)

df = pd.read_csv(base_consolidada_path)

# Descobrir a coluna de saúde disponível
saude_col = 'tx_causas_mal_definidas' if 'tx_causas_mal_definidas' in df.columns else (
    'vl_indicador_saude_infantil' if 'vl_indicador_saude_infantil' in df.columns else df.columns[-2]
)

print(f"--- Filtering {base_consolidada_path.name} for BA ---")
df_ba = df[df['sg_uf'] == 'BA']
print(df_ba[['co_anomes', 'sg_uf', saude_col]])

print(f"\n--- Unique years/months in {base_consolidada_path.name} ---")
print(df['co_anomes'].unique())

print(f"\n--- Checking if 2023 is in {base_consolidada_path.name} ---")
df_2023 = df[df['co_anomes'].astype(str).str.startswith('2023')]
print(f"Count of records for 2023: {len(df_2023)}")
if len(df_2023) > 0:
    print(df_2023[['co_anomes', 'sg_uf', saude_col]])
