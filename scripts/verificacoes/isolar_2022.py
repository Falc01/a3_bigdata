import pandas as pd
from pathlib import Path

# Paths
input_file = Path('data/gold/base_consolidada.csv')
output_file = Path('data/gold/base_consolidada_2022.csv')

print(f"Lendo o arquivo: {input_file}")
df = pd.read_csv(input_file)

# The column is co_anomes, let's filter for anything starting with 2022
# Usually it's an integer like 202212
df_2022 = df[df['co_anomes'].astype(str).str.startswith('2022')]

print(f"Total de registros originais: {len(df)}")
print(f"Total de registros para 2022 isolados: {len(df_2022)}")

# Save the filtered data
df_2022.to_csv(output_file, index=False)
print(f"Base salva com sucesso em: {output_file}")
