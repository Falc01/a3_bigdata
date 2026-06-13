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
    
    # Transformação: Cálculo da Taxa
    df['taxa_mortalidade_infantil'] = (df['obitos_infantis'] / df['nascidos_vivos']) * df['Fator']
    df_full = df[['Ano', 'co_uf', 'nascidos_vivos', 'obitos_infantis', 'taxa_mortalidade_infantil']].rename(columns={'Ano': 'ano'})
    
    # Filtrar estritamente para o estado da Bahia (co_uf = 29)
    df_full = df_full[df_full['co_uf'].astype(float) == 29.0]
    
    # Carga: Salvar na camada Gold a base histórica completa
    dest_full = gold_path / "base_mortalidade_nacional.csv"
    df_full.to_csv(dest_full, index=False)
    print(f"[OK] Base nacional completa salva em: {dest_full.name}")
    
    # Carga: Salvar na camada Gold a base 2022 para compatibilidade
    df_2022 = df_full[df_full['ano'] == 2022].copy()
    dest_2022 = gold_path / "base_mortalidade_nacional_2022.csv"
    df_2022.to_csv(dest_2022, index=False)
    print(f"[OK] Base nacional 2022 salva em: {dest_2022.name}")
    print(df_2022.head())

if __name__ == "__main__":
    integrar_base_historica()
