import pandas as pd
from pathlib import Path

def consolidar_gold():
    silver_path = Path("data/silver")
    gold_path = Path("data/gold")
    gold_path.mkdir(parents=True, exist_ok=True)
    
    print("--- Iniciando Consolidacao Camada Gold ---")
    
    try:
        # 1. Carregar bases Silver
        print("[LOAD] Carregando bases Silver...")
        df_agua = pd.read_csv(silver_path / "proporcao_agua_clean.csv")
        df_lixo = pd.read_csv(silver_path / "proporcao_lixo_clean.csv")
        df_sani = pd.read_csv(silver_path / "proporcao_sanitaria_clean.csv")
        df_saude = pd.read_csv(silver_path / "ripsa014sc_clean.csv")
        
        # 2. Filtrar por Categoria Principal (Para evitar explosao no merge)
        print("[FILTER] Filtrando por 'Todas as categorias'...")
        df_agua = df_agua[df_agua['sg_categoria'] == 'TC']
        df_lixo = df_lixo[df_lixo['sg_categoria'] == 'TC']
        df_sani = df_sani[df_sani['sg_categoria'] == 'TC']
        df_saude = df_saude[df_saude['sg_categoria'] == 'TC']
        
        # 3. Merge de Saneamento
        print("[MERGE] Unificando dados de saneamento...")
        df_saneamento = df_agua.merge(df_lixo[['co_anomes', 'co_uf', 'vl_indicador_calculado_uf']], 
                                     on=['co_anomes', 'co_uf'], 
                                     suffixes=('_agua', '_lixo'))
        
        df_saneamento = df_saneamento.merge(df_sani[['co_anomes', 'co_uf', 'vl_indicador_calculado_uf']], 
                                           on=['co_anomes', 'co_uf'])
        df_saneamento = df_saneamento.rename(columns={'vl_indicador_calculado_uf': 'vl_indicador_calculado_uf_sani'})
        
        # 4. Merge com Saude
        print("[MERGE] Unificando com dados de saude infantil...")
        df_final = df_saneamento.merge(df_saude[['co_anomes', 'co_uf', 'vl_indicador_calculado_uf']], 
                                      on=['co_anomes', 'co_uf'])
        df_final = df_final.rename(columns={'vl_indicador_calculado_uf': 'vl_indicador_saude_infantil'})
        
        # 5. Criacao de Metricas Agregadas
        print("[CALC] Criando indice consolidado...")
        df_final['indice_saneamento_consolidado'] = (
            df_final['vl_indicador_calculado_uf_agua'] + 
            df_final['vl_indicador_calculado_uf_lixo'] + 
            df_final['vl_indicador_calculado_uf_sani']
        ) / 3
        
        # 5. Salvar Gold
        dest = gold_path / "base_consolidada.csv"
        df_final.to_csv(dest, index=False)
        print(f"[OK] Base consolidada salva em: {dest.name}")
        print(f"Total de registros: {len(df_final)}")
        
    except Exception as e:
        print(f"[ERRO] Falha na consolidacao Gold: {e}")

if __name__ == "__main__":
    consolidar_gold()
