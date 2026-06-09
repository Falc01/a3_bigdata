import pandas as pd
from pathlib import Path
import glob

def consolidar_agua_esgoto():
    bronze_path = Path("data/bronze")
    gold_path = Path("data/gold")
    gold_path.mkdir(parents=True, exist_ok=True)
    
    output_file = gold_path / "base_snis_agua_esgoto_2022.csv"
    
    print("--- Consolidando SNIS Agua e Esgoto (AE) 2022 ---")
    
    # Mapear todos os arquivos de indicadores locais e regionais da Bahia
    files = [bronze_path / "Planilha_LPU_Indicadores.xls"] + list(bronze_path.glob("Planilha_AE_Indicadores_*-29*.xls"))
    
    dfs = []
    for f in files:
        if f.exists():
            print(f"[LOAD] Lendo {f.name}...")
            dfs.append(pd.read_excel(f, header=7))
        else:
            print(f"[AVISO] Arquivo nao encontrado: {f.name}")
            
    if not dfs:
        print("[ERRO] Nenhuma base de Agua e Esgoto encontrada.")
        return
        
    try:
        df_all = pd.concat(dfs, ignore_index=True)
        
        # Filtrar apenas o estado da Bahia
        df_ba = df_all[df_all['UF'] == 'BA'].copy()
        
        # Selecionar colunas de interesse
        colunas_interesse = {
            'Cdigo do municpio': 'co_municipio',
            'Cód. Município': 'co_municipio', # Fallback
            'Nome do prestador de servios': 'no_prestador_servico_ae',
            'ndice de atendimento total de gua': 'tx_atendimento_total_agua',
            'ndice de atendimento urbano de gua': 'tx_atendimento_urbano_agua',
            'ndice de atendimento total de esgoto referido aos municpios atendidos com gua': 'tx_atendimento_total_esgoto',
            'ndice de atendimento urbano de esgoto referido aos municpios atendidos com gua': 'tx_atendimento_urbano_esgoto',
            'ndice de coleta de esgoto': 'tx_coleta_esgoto',
            'ndice de tratamento de esgoto': 'tx_tratamento_esgoto',
            'Consumo mdio per Capita de gua': 'consumo_per_capita_agua',
            'ndice de conformidade da quantidade de amostra - Coliformes Totais': 'idx_conformidade_coliformes'
        }
        
        # Renomear as colunas tratando caracteres de encoding
        cols_atuais = df_ba.columns.tolist()
        col_map = {}
        for original, amigavel in colunas_interesse.items():
            original_normalizado = original.encode('latin1', errors='ignore').decode('utf-8', errors='ignore').lower().replace(' ', '')
            for col in cols_atuais:
                col_normalizada = str(col).encode('latin1', errors='ignore').decode('utf-8', errors='ignore').lower().replace(' ', '')
                if original_normalizado in col_normalizada or col_normalizada in original_normalizado:
                    col_map[col] = amigavel
                    break
        
        if 'Cdigo do municpio' in df_ba.columns:
            col_map['Cdigo do municpio'] = 'co_municipio'
        elif 'Cód. Município' in df_ba.columns:
            col_map['Cód. Município'] = 'co_municipio'
            
        df_filtered = df_ba[list(col_map.keys())].copy()
        df_filtered = df_filtered.rename(columns=col_map)
        
        # Tratar tipos e normalizar
        df_filtered['co_municipio'] = pd.to_numeric(df_filtered['co_municipio'], errors='coerce')
        df_filtered = df_filtered.dropna(subset=['co_municipio'])
        df_filtered['co_municipio'] = df_filtered['co_municipio'].astype(int)
        
        # Converter colunas numericas de string para float
        cols_numericas = [
            'tx_atendimento_total_agua', 'tx_atendimento_urbano_agua',
            'tx_atendimento_total_esgoto', 'tx_atendimento_urbano_esgoto',
            'tx_coleta_esgoto', 'tx_tratamento_esgoto',
            'consumo_per_capita_agua', 'idx_conformidade_coliformes'
        ]
        
        for col in cols_numericas:
            if col in df_filtered.columns:
                df_filtered[col] = df_filtered[col].astype(str).str.replace('-', '0').str.replace(',', '.')
                df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').fillna(0)
                
        # Agrupar por municipio (pegar o valor maximo dos indices e o primeiro nome do prestador)
        agg_rules = {c: 'max' for c in cols_numericas if c in df_filtered.columns}
        if 'no_prestador_servico_ae' in df_filtered.columns:
            agg_rules['no_prestador_servico_ae'] = 'first'
            
        df_grouped = df_filtered.groupby('co_municipio').agg(agg_rules).reset_index()
        
        # Adicionar colunas de identificacao de estado
        df_grouped['co_uf'] = 29
        df_grouped['sg_uf'] = 'BA'
        
        # Reordenar colunas para colocar co_uf e sg_uf primeiro (evita que o validador confunda a palavra 'prestador' com a coluna de estado)
        cols_ordenadas = ['co_uf', 'sg_uf', 'co_municipio'] + [c for c in df_grouped.columns if c not in ['co_uf', 'sg_uf', 'co_municipio']]
        df_grouped = df_grouped[cols_ordenadas]
        
        # Salvar na camada Gold
        df_grouped.to_csv(output_file, index=False)
        print(f"[OK] Tabela de Agua e Esgoto consolidada gerada: {output_file.name}")
        print(f"   Shape: {df_grouped.shape} ({len(df_grouped)} municipios na Bahia)")
        
    except Exception as e:
        print(f"[ERRO] Falha na consolidacao de Agua e Esgoto: {e}")

if __name__ == "__main__":
    consolidar_agua_esgoto()
