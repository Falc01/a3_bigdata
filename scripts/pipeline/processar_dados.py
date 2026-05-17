import pandas as pd
import os
from pathlib import Path

def fix_excel_layout(df):
    """
    Skill: fix_excel_layout
    - Header Finder: Encontra a linha de cabecalho real
    - Drop Totals: Remove linhas de resumo
    """
    # 1. Encontrar a linha onde comecam os dados reais (ex: onde tem 'Código do Município' ou similar)
    # Vamos procurar por palavras-chave comuns
    keywords = ['codigo', 'municipio', 'estado', 'uf', 'indicador']
    header_idx = 0
    for i in range(min(20, len(df))):
        row_str = " ".join([str(x).lower() for x in df.iloc[i].values])
        if any(key in row_str for key in keywords):
            header_idx = i
            break
            
    # Ajustar colunas
    new_header = df.iloc[header_idx]
    df = df[header_idx + 1:].copy()
    df.columns = new_header
    
    # 2. Drop Totals (Linhas que comecam com 'Total' ou 'Fonte')
    if not df.empty:
        first_col = df.columns[0]
        df = df[~df[first_col].astype(str).str.contains('Total|Fonte|Legenda', case=False, na=False)]
        
    return df

def clean_dataframe(df, threshold_null=0.5):
    # 0. Garantir colunas unicas
    df.columns = [str(c).strip().lower().replace(" ", "_").replace(".", "_") for c in df.columns]
    
    # Se houver duplicatas, renomear com sufixo
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols == dup] = [f"{dup}_{i}" if i != 0 else dup for i in range(sum(cols == dup))]
    df.columns = cols

    # 1. Deduplicação
    df = df.drop_duplicates()
    
    # 2. Tratamento de Nulos
    limit = len(df) * threshold_null
    df = df.dropna(axis=1, thresh=limit)
    
    # 3. Cast de Tipos
    for col in df.columns:
        series = df[col]
        if series.dtype == 'object':
            try:
                df[col] = pd.to_numeric(series)
            except:
                if series.nunique() / len(df) < 0.1:
                    df[col] = series.astype('category')
        elif 'int' in str(series.dtype):
            df[col] = pd.to_numeric(series, downcast='integer')
        elif 'float' in str(series.dtype):
            df[col] = pd.to_numeric(series, downcast='float')
            
    return df

def processar_silver():
    bronze_path = Path("data/bronze")
    silver_path = Path("data/silver")
    silver_path.mkdir(parents=True, exist_ok=True)
    
    print("--- Iniciando Processamento Camada Silver (Refinado) ---")
    
    # Configuração de processamento por arquivo
    config = {
        "Planilha_Indicadores_RS_2022.xlsx": {"type": "xlsx", "fix_layout": True},
        "macroregiao_de_saude.csv": {"type": "csv", "sep": None}
    }
    
    for nome, cfg in config.items():
        caminho = bronze_path / nome
        if not caminho.exists():
            print(f"[AVISO] Arquivo nao encontrado: {nome}")
            continue
            
        print(f"[PROCESSANDO] {nome}...")
        try:
            if cfg["type"] == "xlsx":
                df = pd.read_excel(caminho)
            else:
                df = pd.read_csv(caminho, sep=cfg.get("sep", ","))
                
            # Aplicar Fix Layout se necessário
            if cfg.get("fix_layout"):
                df = fix_excel_layout(df)
            
            # Aplicar limpeza base
            df = clean_dataframe(df)
            
            # Aplicar filtro TC (Todas as Categorias) para bases RIPSA/Proporcao
            if cfg.get("tc_filter") and "sg_categoria" in df.columns:
                df = df[df["sg_categoria"].astype(str).str.upper() == "TC"]
                print(f"  [FILTER] Mantidos {len(df)} registros (TC)")
            
            # Salvar em Silver
            dest = silver_path / f"{caminho.stem}_clean.csv"
            df.to_csv(dest, index=False)
            print(f"[OK] Salvo em Silver: {dest.name}")
            
        except Exception as e:
            print(f"[ERRO] Erro ao processar {nome}: {e}")

if __name__ == "__main__":
    processar_silver()
