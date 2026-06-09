import pandas as pd
from pathlib import Path

def consolidar_municipal():
    gold_path = Path("data/gold")
    mortalidade_file = gold_path / "base_mortalidade_municipal_2022.csv"
    snis_file = gold_path / "base_snis_geografia.csv"
    output_file = gold_path / "base_consolidada_municipal_2022.csv"
    
    print("--- Consolidando Bases Municipais (Saude + Saneamento) ---")
    
    if not mortalidade_file.exists():
        print(f"[ERRO] Arquivo de mortalidade municipal nao encontrado em {mortalidade_file}")
        return
    if not snis_file.exists():
        print(f"[ERRO] Arquivo do SNIS geografia nao encontrado em {snis_file}")
        return
        
    df_mort = pd.read_csv(mortalidade_file)
    df_snis = pd.read_csv(snis_file)
    
    # Garantir tipagem numerica para a chave
    df_mort['co_municipio'] = pd.to_numeric(df_mort['co_municipio'], errors='coerce')
    df_snis['co_municipio'] = pd.to_numeric(df_snis['co_municipio'], errors='coerce')
    
    # Garantir tipagem numerica e consistencia para co_uf e sg_uf
    df_mort['co_uf'] = pd.to_numeric(df_mort['co_uf'], errors='coerce')
    df_snis['co_uf'] = pd.to_numeric(df_snis['co_uf'], errors='coerce')
    df_mort['sg_uf'] = df_mort['sg_uf'].astype(str).str.strip()
    df_snis['sg_uf'] = df_snis['sg_uf'].astype(str).str.strip()
    
    # Remover no_municipio do SNIS para nao duplicar e manter o limpo da mortalidade
    if 'no_municipio' in df_snis.columns:
        df_snis = df_snis.drop(columns=['no_municipio'])
        
    # Merge inner usando chaves comuns para evitar colunas duplicadas (_x, _y)
    df_consolidada = pd.merge(df_mort, df_snis, on=['co_municipio', 'co_uf', 'sg_uf'], how='inner')
    
    # Salvar base consolidada municipal
    df_consolidada.to_csv(output_file, index=False)
    print(f"[OK] Base consolidada municipal gerada com sucesso: {output_file.name}")
    print(f"   Shape: {df_consolidada.shape} ({len(df_consolidada)} municipios unificados)")

if __name__ == "__main__":
    consolidar_municipal()
