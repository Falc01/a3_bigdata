import pandas as pd
from pathlib import Path

def consolidar_snis_geografia():
    """
    Objetivo: Unificar o mapeamento geografico de saude com o SNIS 2022.
    Trabalha com COPIAS (Camada Silver) para seguranca.
    """
    silver_path = Path("data/silver")
    gold_path = Path("data/gold")
    gold_path.mkdir(parents=True, exist_ok=True)
    
    print("--- Iniciando Consolidacao SNIS + Geografia ---")
    
    try:
        # 1. Carregar Geografia (Mapeamento de Saude)
        print("[LOAD] Carregando Mapa de Saude...")
        df_geo = pd.read_csv(silver_path / "macroregiao_de_saude_clean.csv")
        
        # 2. Carregar SNIS 2022 (Bronze Copy)
        print("[LOAD] Carregando SNIS 2022 (Bronze Copy)...")
        snis_bronze = Path("data/bronze/Planilha_Indicadores_RS_2022.xlsx")
        # Ler sem cabecalho primeiro para encontrar a linha correta
        df_raw = pd.read_excel(snis_bronze, header=None, nrows=20)
        
        header_row = 0
        for i, row in df_raw.iterrows():
            if any('ódigo do município' in str(val).lower() for val in row.values):
                header_row = i
                break
        
        print(f"  [INFO] Cabecalho encontrado na linha: {header_row}")
        df_snis = pd.read_excel(snis_bronze, header=header_row)
        
        # 3. Limpeza Rapida do SNIS
        # Remover a primeira linha que contem unidades (%)
        df_snis = df_snis.iloc[1:].copy()
        # Normalizar colunas (remover acentos para evitar erros de encoding)
        df_snis.columns = [
            str(c).strip().lower()
            .replace(" ", "_")
            .replace("\n", "_")
            .replace("õ", "o")
            .replace("ó", "o")
            .replace("í", "i")
            .replace("ã", "a")
            .replace("ç", "c")
            for c in df_snis.columns
        ]
        
        # 4. Join (Merge)
        print("[MERGE] Unificando bases por Codigo de Municipio...")
        # Encontrar a coluna de codigo de municipio no SNIS (que agora deve ser 'codigo_do_municipio')
        col_municipio_snis = [c for c in df_snis.columns if 'codigo_do_municipio' in c][0]
        
        df_geo['cod_municipio'] = pd.to_numeric(df_geo['cod_municipio'], errors='coerce')
        df_snis[col_municipio_snis] = pd.to_numeric(df_snis[col_municipio_snis], errors='coerce')
        
        df_gold = df_geo.merge(df_snis, left_on='cod_municipio', right_on=col_municipio_snis, how='inner')
        
        # 5. Recorte Geográfico: Bahia (BA)
        print("[FILTER] Aplicando recorte para o estado da Bahia (BA)...")
        df_gold = df_gold[df_gold['sg_uf'] == 'BA'].copy()
        
        # 6. Salvar Gold
        dest = gold_path / "base_snis_geografia.csv"
        df_gold.to_csv(dest, index=False)
        print(f"[OK] Base consolidada (Bahia) salva em: {dest.name}")
        print(f"Registros da Bahia: {len(df_gold)}")
        
    except Exception as e:
        print(f"[ERRO] Falha na consolidacao: {e}")

if __name__ == "__main__":
    consolidar_snis_geografia()
