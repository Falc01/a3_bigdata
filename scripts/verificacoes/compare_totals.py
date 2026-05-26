import pandas as pd
from pathlib import Path
import sys

excel_path = Path('data_dump/Book1.xlsx')
base_consolidada_path = Path('data/gold/base_consolidada_2022.csv')

if not excel_path.exists():
    print(f"❌ Erro: O arquivo de Excel '{excel_path}' não foi encontrado.")
    sys.exit(1)

if not base_consolidada_path.exists():
    print(f"❌ Erro: O arquivo de dados consolidado '{base_consolidada_path}' não foi encontrado.")
    sys.exit(1)

df_excel = pd.read_excel(excel_path)

# Cleanup excel data
# Row 0 is "TOTAL"
total_births = df_excel.iloc[0, 1]
total_deaths = df_excel.iloc[0, 3]
total_rate = (total_deaths / total_births) * 1000

print(f"Excel Total Births: {total_births}")
print(f"Excel Total Deaths: {total_deaths}")
print(f"Excel Calculated Rate (Total): {total_rate:.2f}")

df_base = pd.read_csv(base_consolidada_path)

# Descobrir a coluna de saúde disponível
saude_col = 'tx_causas_mal_definidas' if 'tx_causas_mal_definidas' in df_base.columns else (
    'vl_indicador_saude_infantil' if 'vl_indicador_saude_infantil' in df_base.columns else df_base.columns[-2]
)

ba_2022 = df_base[(df_base['sg_uf'] == 'BA') & (df_base['co_anomes'] == 202212)]

if not ba_2022.empty:
    print(f"Base Consolidada BA 2022 Indicator ({saude_col}): {ba_2022[saude_col].values[0]}")
else:
    print("BA 2022 not found in base_consolidada_2022.csv")

# Let's check other UFs for 2022 if they exist in this file
print("\n--- 2022 Indicators for all UFs in base ---")
if 'sg_uf' in df_base.columns and saude_col in df_base.columns:
    print(df_base[df_base['co_anomes'] == 202212][['sg_uf', saude_col]])
else:
    print("Columns sg_uf or saude_col not found.")
