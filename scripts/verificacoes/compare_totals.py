import pandas as pd

excel_path = r'c:\Users\joaof\Downloads\Unifacs\analise_dados_big_data\a3\dataset\data\gold\Book1.xlsx'
df_excel = pd.read_excel(excel_path)

# Cleanup excel data
# Row 0 is "TOTAL"
total_births = df_excel.iloc[0, 1]
total_deaths = df_excel.iloc[0, 3]
total_rate = (total_deaths / total_births) * 1000

print(f"Excel Total Births: {total_births}")
print(f"Excel Total Deaths: {total_deaths}")
print(f"Excel Calculated Rate (Total): {total_rate:.2f}")

base_consolidada_path = r'c:\Users\joaof\Downloads\Unifacs\analise_dados_big_data\a3\dataset\data\gold\base_consolidada.csv'
df_base = pd.read_csv(base_consolidada_path)
ba_2023 = df_base[(df_base['sg_uf'] == 'BA') & (df_base['co_anomes'] == 202312)]

if not ba_2023.empty:
    print(f"Base Consolidada BA 2023 Indicator: {ba_2023['vl_indicador_saude_infantil'].values[0]}")
else:
    print("BA 2023 not found in base_consolidada.csv")

# Let's check other UFs for 2023 to see if they follow the same pattern
print("\n--- 2023 Indicators for all UFs ---")
print(df_base[df_base['co_anomes'] == 202312][['sg_uf', 'vl_indicador_saude_infantil']])
