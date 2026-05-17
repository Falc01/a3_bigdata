import pandas as pd

base_consolidada_path = r'c:\Users\joaof\Downloads\Unifacs\analise_dados_big_data\a3\dataset\data\gold\base_consolidada.csv'
df = pd.read_csv(base_consolidada_path)

print("--- Filtering base_consolidada.csv for BA ---")
df_ba = df[df['sg_uf'] == 'BA']
print(df_ba[['co_anomes', 'sg_uf', 'vl_indicador_saude_infantil']])

print("\n--- Unique years/months in base_consolidada.csv ---")
print(df['co_anomes'].unique())

print("\n--- Checking if 2023 is in base_consolidada.csv ---")
df_2023 = df[df['co_anomes'].astype(str).str.startswith('2023')]
print(f"Count of records for 2023: {len(df_2023)}")
if len(df_2023) > 0:
    print(df_2023[['co_anomes', 'sg_uf', 'vl_indicador_saude_infantil']])
