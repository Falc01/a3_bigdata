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
        
        # Carregar base de saude do MGDI (Nacional Historico)
        df_mgdi = pd.read_csv("data/AV3--ANALISE-DE-DADOS-E-BIG-DATA-main/data-sets/mgdi_ms_k5p.csv")
        df_mgdi.columns = ['Indicador', 'Ano', 'co_uf', 'obitos', 'nascidos', 'Fator']
        df_mgdi['taxa_mortalidade_infantil'] = (df_mgdi['obitos'] / df_mgdi['nascidos']) * df_mgdi['Fator']

        # 2. Filtrar por Categoria Principal (Para evitar explosao no merge)
        print("[FILTER] Filtrando por 'Todas as categorias'...")
        df_agua = df_agua[df_agua['sg_categoria'] == 'TC']
        df_lixo = df_lixo[df_lixo['sg_categoria'] == 'TC']
        df_sani = df_sani[df_sani['sg_categoria'] == 'TC']
        
        # Adicionar coluna Ano para o merge
        df_agua['Ano'] = df_agua['co_anomes'] // 100
        df_lixo['Ano'] = df_lixo['co_anomes'] // 100
        df_sani['Ano'] = df_sani['co_anomes'] // 100

        # Converter deficits para cobertura
        df_agua['tx_cobertura_agua'] = 100 - df_agua['vl_indicador_calculado_uf']
        df_lixo['tx_cobertura_lixo'] = 100 - df_lixo['vl_indicador_calculado_uf']
        df_sani['tx_cobertura_esgoto'] = 100 - df_sani['vl_indicador_calculado_uf']

        # 3. Merge de Saneamento
        print("[MERGE] Unificando dados de saneamento...")
        df_saneamento = df_agua.merge(df_lixo[['Ano', 'co_uf', 'tx_cobertura_lixo']], 
                                     on=['Ano', 'co_uf'])
        df_saneamento = df_saneamento.merge(df_sani[['Ano', 'co_uf', 'tx_cobertura_esgoto']], 
                                           on=['Ano', 'co_uf'])
        
        # 4. Merge com Saude
        print("[MERGE] Unificando com dados de saude infantil...")
        df_final = df_saneamento.merge(df_mgdi[['Ano', 'co_uf', 'taxa_mortalidade_infantil']], 
                                      on=['Ano', 'co_uf'])
        
        # 5. Criacao de Metricas Agregadas
        print("[CALC] Criando indice consolidado...")
        df_final['indice_saneamento_consolidado'] = (
            df_final['tx_cobertura_agua'] + 
            df_final['tx_cobertura_lixo'] + 
            df_final['tx_cobertura_esgoto']
        ) / 3
        
        # Adicionar coluna ano explicita
        df_final['ano'] = df_final['co_anomes'] // 100
        
        # Corrigir granularidade para UF (refletindo que os dados estaduais representam o estado inteiro)
        df_final['sg_granularidade'] = 'UF'
        df_final['ds_granularidade'] = 'Unidade da Federação'
        
        # Limpar colunas temporarias ou redundantes
        df_final = df_final.drop(columns=['Ano', 'vl_indicador_calculado_uf'])
        
        # Renomear para manter compatibilidade com padronizar_gold.py se necessario
        df_final = df_final.rename(columns={'taxa_mortalidade_infantil': 'vl_indicador_saude_infantil'})
        
        # Filtrar estritamente para o estado da Bahia (co_uf = 29)
        df_final = df_final[df_final['co_uf'].astype(float) == 29.0]
        
        # 6. Salvar Gold
        dest = gold_path / "base_consolidada.csv"
        df_final.to_csv(dest, index=False)
        print(f"[OK] Base consolidada completa salva em: {dest.name}")
        print(f"Total de registros: {len(df_final)}")
        
        # Gerar base_consolidada_2022.csv (Bahia 2022 apenas)
        df_2022 = df_final[(df_final['co_anomes'] == 202212) & (df_final['co_uf'] == 29.0)].copy()
        dest_2022 = gold_path / "base_consolidada_2022.csv"
        df_2022.to_csv(dest_2022, index=False)
        print(f"[OK] Base consolidada Bahia 2022 salva em: {dest_2022.name}")
        
    except Exception as e:
        print(f"[ERRO] Falha na consolidacao Gold: {e}")


if __name__ == "__main__":
    consolidar_gold()
