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
    print(info_df)
    
    print("\n[DESCRIBE] Estatisticas Descritivas:")
    print(df.describe().round(2))
    
    print("\n[CORRELATION] Matriz de Correlacao (Saneamento vs Saude):")
    cols_interesse = [
        'vl_indicador_calculado_uf_agua',
        'vl_indicador_calculado_uf_lixo',
        'vl_indicador_calculado_uf_sani',
        'vl_indicador_saude_infantil',
        'indice_saneamento_consolidado'
    ]
    corr = df[cols_interesse].corr().round(4)
    print(corr)
    
    return corr

def validar_base():
    gold_path = Path("data/gold/base_consolidada.csv")
    if not gold_path.exists():
        print("[ERRO] Base Gold nao encontrada!")
        return
        
    df = pd.read_csv(gold_path)
    auto_eda(df)

if __name__ == "__main__":
    validar_base()
