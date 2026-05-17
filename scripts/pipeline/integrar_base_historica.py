import pandas as pd
from pathlib import Path

def integrar_base_historica():
    print("--- Integrando Base Histórica Nacional (Filtro 2022) ---")
    
    origem_path = Path("data/AV3--ANALISE-DE-DADOS-E-BIG-DATA-main/data-sets/mgdi_ms_k5p.csv")
    gold_path = Path("data/gold")
    gold_path.mkdir(parents=True, exist_ok=True)
    
    if not origem_path.exists():
        print(f"[ERRO] Arquivo não encontrado: {origem_path}")
        return
        
    # Extração
    df = pd.read_csv(origem_path)
    
    # Transformaçao: Nomes de Colunas (Semelhante ao app.py deles)
    df.columns = ['Indicador', 'Ano', 'co_uf', 'obitos_infantis', 'nascidos_vivos', 'Fator']
    
    # Transformação: Filtrar 2022
    df_2022 = df[df['Ano'] == 2022].copy()
    
    # Transformação: Cálculo da Taxa
    df_2022['taxa_mortalidade_infantil'] = (df_2022['obitos_infantis'] / df_2022['nascidos_vivos']) * df_2022['Fator']
    
    # Remover colunas desnecessárias para a Gold
    df_2022 = df_2022[['Ano', 'co_uf', 'nascidos_vivos', 'obitos_infantis', 'taxa_mortalidade_infantil']]
    df_2022 = df_2022.rename(columns={'Ano': 'ano'})
    
    # Carga: Salvar na camada Gold
    dest = gold_path / "base_mortalidade_nacional_2022.csv"
    df_2022.to_csv(dest, index=False)
    
    print(f"[OK] Base nacional 2022 salva em: {dest.name}")
    print(f"Total de registros (UFs): {len(df_2022)}")
    print(df_2022.head())

if __name__ == "__main__":
    integrar_base_historica()
