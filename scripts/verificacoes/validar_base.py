import pandas as pd
from pathlib import Path

def auto_eda(df):
    """
    Skill: auto_eda
    - Sumario Estatistico
    - Tipagem
    - Missing Values
    - Correlacao
    """
    print("\n--- AUTO EDA REPORT ---")
    
    print("\n[INFO] Tipos de Dados e Nulos:")
    info_df = pd.DataFrame({
        'Tipo': df.dtypes,
        'Nulos (%)': (df.isnull().sum() / len(df) * 100).round(2)
    })
    print(info_df.head(20)) # Print first 20 columns for brevity
    if len(info_df) > 20:
        print(f"... and {len(info_df) - 20} more columns.")
    
    print("\n[DESCRIBE] Estatisticas Descritivas:")
    print(df.describe().round(2))
    
    print("\n[CORRELATION] Matriz de Correlacao (Saude vs Saneamento Municipal):")
    cols_interesse = [
        'nascidos_vivos',
        'obitos_infantis',
        'taxa_mortalidade_infantil',
        'populacao_ibge_2022',
        'tx_cobertura_da_coleta_rdo_em_relacao_a_pop_total'
    ]
    # Filtra colunas que realmente existem no DataFrame para evitar erros
    cols_existentes = [c for c in cols_interesse if c in df.columns]
    if len(cols_existentes) > 1:
        corr = df[cols_existentes].corr().round(4)
        print(corr)
    else:
        print("Aviso: Menos de duas colunas de interesse encontradas para correlação.")
    
    return None

def validar_base():
    gold_path = Path("data/gold/base_consolidada_municipal_2022.csv")
    if not gold_path.exists():
        print(f"[ERRO] Base Gold nao encontrada em: {gold_path}!")
        return
        
    df = pd.read_csv(gold_path)
    auto_eda(df)

if __name__ == "__main__":
    validar_base()
