import pandas as pd
from pathlib import Path

def consolidar_municipal():
    gold_path = Path("data/gold")
    mortalidade_file = gold_path / "base_mortalidade_municipal_2022.csv"
    snis_file = gold_path / "base_snis_geografia.csv"
    ae_file = gold_path / "base_snis_agua_esgoto_2022.csv"
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
    
    if 'cod_municipio' in df_snis.columns and 'co_municipio' not in df_snis.columns:
        df_snis = df_snis.rename(columns={'cod_municipio': 'co_municipio'})
        
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
    
    # Integrar Água e Esgoto
    if ae_file.exists():
        print("[LOAD] Integrando SNIS Agua e Esgoto (AE) na base municipal...")
        df_ae = pd.read_csv(ae_file)
        df_ae['co_municipio'] = pd.to_numeric(df_ae['co_municipio'], errors='coerce')
        df_ae['co_uf'] = pd.to_numeric(df_ae['co_uf'], errors='coerce')
        df_ae['sg_uf'] = df_ae['sg_uf'].astype(str).str.strip()
        
        if 'no_municipio' in df_ae.columns:
            df_ae = df_ae.drop(columns=['no_municipio'])
            
        df_consolidada = pd.merge(df_consolidada, df_ae, on=['co_municipio', 'co_uf', 'sg_uf'], how='left')
        
    # Dropar colunas redundantes para otimização de memória
    cols_to_drop = [
        'co_regiao_pais', 'regiao_pais', 'nome_da_regiao', 'sigla_da_regiao',
        'uf_x', 'uf_y', 'codigo_do_ibge', 'codigo_do_municipio', 'municipio'
    ]
    df_consolidada = df_consolidada.drop(columns=[c for c in cols_to_drop if c in df_consolidada.columns], errors='ignore')
    
    # Tratamento de Nulos Avançado na base municipal
    colunas_numericas = df_consolidada.select_dtypes(include=['number']).columns.tolist()
    colunas_texto = df_consolidada.select_dtypes(exclude=['number']).columns.tolist()
    
    # Excluir chaves críticas do loop para segurança
    chaves_seguranca = ['co_municipio', 'co_uf', 'ano']
    for c in chaves_seguranca:
        if c in colunas_numericas:
            colunas_numericas.remove(c)
            
    colunas_para_dropar = []
    
    for col in colunas_numericas:
        nulos = df_consolidada[col].isnull().sum()
        if nulos == 0:
            continue
            
        pct_nulos = nulos / len(df_consolidada)
        
        if pct_nulos == 1.0:
            # Dropar colunas 100% nulas
            colunas_para_dropar.append(col)
        elif pct_nulos >= 0.75:
            # Sentinel value para colunas muito esparsas
            df_consolidada[col] = df_consolidada[col].fillna(-1)
        else:
            # Imputação hierárquica por Faixa Populacional -> Estado -> Sentinel
            # Calcular medianas por grupo
            if 'identificacao_da_faixa_populacional' in df_consolidada.columns:
                medianas_grupo = df_consolidada.groupby('identificacao_da_faixa_populacional')[col].transform('median')
            else:
                medianas_grupo = pd.Series([pd.NA] * len(df_consolidada))
                
            mediana_estado = df_consolidada[col].median()
            
            # Se a mediana do estado for nula, o fallback final é -1
            fallback_val = mediana_estado if not pd.isna(mediana_estado) else -1
            
            # Preencher com a mediana do grupo
            df_consolidada[col] = df_consolidada[col].fillna(medianas_grupo)
            # Preencher o restante (se houver) com a mediana do estado/sentinel
            df_consolidada[col] = df_consolidada[col].fillna(fallback_val)
            
    # Dropar as colunas de fato
    if colunas_para_dropar:
        print(f"  [CLEAN] Dropando {len(colunas_para_dropar)} colunas com 100% de nulos na base municipal.")
        df_consolidada = df_consolidada.drop(columns=colunas_para_dropar)
        
    # Tratar colunas de texto com sentinela
    for col in colunas_texto:
        if df_consolidada[col].isnull().sum() > 0:
            df_consolidada[col] = df_consolidada[col].fillna('Não Informado')
            
    # Salvar base consolidada municipal
    df_consolidada.to_csv(output_file, index=False)
    print(f"[OK] Base consolidada municipal gerada com sucesso: {output_file.name}")
    print(f"   Shape: {df_consolidada.shape} ({len(df_consolidada)} municipios unificados)")

if __name__ == "__main__":
    consolidar_municipal()
