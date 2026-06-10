import pandas as pd
from pathlib import Path
import sys

def analisar_metricas():
    # Garantir codificacao UTF-8 para evitar problemas de console no Windows
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

    print("==================================================")
    print("      RELATORIO DE METRICAS E QUALIDADE ETL       ")
    print("==================================================")
    
    # Paths
    landing_path = Path("data/landing")
    gold_path = Path("data/gold")
    
    sim_file = landing_path / "sim_cnv_inf10ba131422187_107_8_217.csv"
    sinasc_file = landing_path / "sinasc_cnv_nvba131418187_107_8_217.csv"
    
    gold_mort_file = gold_path / "base_mortalidade_municipal_2022.csv"
    gold_snis_file = gold_path / "base_snis_geografia.csv"
    gold_cons_file = gold_path / "base_consolidada_municipal_2022.csv"
    
    # 1. AUDITORIA DE RETENCAO E DEDUPLICACAO
    print("\n--- 1. Retencao e Deduplicacao de Dados ---")
    
    if sim_file.exists() and sinasc_file.exists() and gold_mort_file.exists():
        try:
            # Encontrar dinamicamente a linha de cabeçalho
            def find_header_and_load(path):
                h_row = 3
                with open(path, 'r', encoding='latin1') as f_in:
                    for idx, line in enumerate(f_in):
                        if 'Munic' in line and ';' in line:
                            h_row = idx
                            break
                return pd.read_csv(path, sep=';', encoding='latin1', skiprows=h_row)

            # Ler brutos (Landing)
            df_sim_raw = find_header_and_load(sim_file)
            df_sim_raw = df_sim_raw.dropna(subset=[df_sim_raw.columns[0]])
            df_sim_raw = df_sim_raw[~df_sim_raw[df_sim_raw.columns[0]].str.contains('Total|IGNORADO', na=False, case=False)]
            sim_raw_count = len(df_sim_raw)
            
            df_sinasc_raw = find_header_and_load(sinasc_file)
            df_sinasc_raw = df_sinasc_raw.dropna(subset=[df_sinasc_raw.columns[0]])
            df_sinasc_raw = df_sinasc_raw[~df_sinasc_raw[df_sinasc_raw.columns[0]].str.contains('Total|IGNORADO', na=False, case=False)]
            sinasc_raw_count = len(df_sinasc_raw)
            
            # Ler processado (Gold)
            df_mort_gold = pd.read_csv(gold_mort_file)
            gold_mort_count = len(df_mort_gold)
            
            print(f"Municipios mapeados na Landing SIM (Obitos): {sim_raw_count}")
            print(f"Municipios mapeados na Landing SINASC (Nascidos): {sinasc_raw_count}")
            print(f"Municipios gravados na Gold Mortalidade: {gold_mort_count} (Esperado: 417)")
            print(f"Taxa de Retencao de Municipios: {gold_mort_count / 417 * 100:.2f}%")
        except Exception as e:
            print(f"[ERRO] Falha ao analisar retencao de mortalidade: {e}")
    else:
        print("[AVISO] Arquivos do SIM/SINASC ou Gold Mortalidade nao encontrados.")
        
    # 2. GRAU DE COBERTURA GEOGRAFICA (MATCH RATE)
    print("\n--- 2. Cobertura Geografica (Match Saneamento/Geografia) ---")
    if gold_snis_file.exists():
        try:
            df_snis = pd.read_csv(gold_snis_file)
            snis_count = len(df_snis)
            total_ba_mun = 417
            print(f"Municipios da Bahia pareados com SNIS: {snis_count} de {total_ba_mun}")
            print(f"Taxa de Pareamento (Match Rate): {snis_count / total_ba_mun * 100:.2f}%")
            print("Nota: A diferenca representa os municipios que nao preencheram o SNIS de Residuos Solidos em 2022.")
        except Exception as e:
            print(f"[ERRO] Falha ao analisar match geografico: {e}")
            
    # 3. METRICAS DO NOVO CONSOLIDADO MUNICIPAL
    print("\n--- 3. Nova Base Consolidada Municipal ---")
    if gold_cons_file.exists():
        try:
            df_cons = pd.read_csv(gold_cons_file)
            print(f"Quantidade de linhas (Municipios unificados): {len(df_cons)}")
            print(f"Quantidade de colunas (Variaveis integradas): {df_cons.shape[1]}")
            
            # Calcular correlacao entre saneamento (lixo) e saude
            col_lixo = 'tx_cobertura_da_coleta_rdo_em_relacao_a_pop_total'
            col_saude = 'taxa_mortalidade_infantil'
            
            if col_lixo in df_cons.columns and col_saude in df_cons.columns:
                # Tratar nulos temporariamente para correlacao
                sub_df = df_cons[[col_lixo, col_saude]].dropna()
                if len(sub_df) > 1:
                    correlacao = sub_df[col_lixo].corr(sub_df[col_saude])
                    print(f"Correlacao de Pearson (Cobertura Lixo vs Taxa Mortalidade): {correlacao:.4f}")
                else:
                    print("Dados insuficientes para correlacao.")
        except Exception as e:
            print(f"[ERRO] Falha ao analisar base consolidada: {e}")
            
    # 4. AUDITORIA DE NULOS (DATA QUALITY)
    print("\n--- 4. Qualidade dos Dados (Valores Nulos na Gold) ---")
    gold_files = {
        'Mortalidade Municipal': gold_mort_file,
        'SNIS Geografia': gold_snis_file,
        'Consolidado Municipal': gold_cons_file
    }
    
    for name, path in gold_files.items():
        if path.exists():
            try:
                df = pd.read_csv(path)
                nulls = df.isnull().sum().sum()
                total_cells = df.size
                null_pct = (nulls / total_cells * 100) if total_cells > 0 else 0
                print(f"Tabela '{name}': {nulls} nulos de {total_cells} celulas ({null_pct:.2f}%)")
            except Exception as e:
                print(f"[ERRO] Falha ao auditar nulos para {name}: {e}")
                
    # 5. SANIDADE MATEMATICA
    print("\n--- 5. Sanidade Matematica (Regras de Negocio) ---")
    if gold_mort_file.exists():
        try:
            df_mort = pd.read_csv(gold_mort_file)
            
            # Regra 1: nascidos_vivos >= obitos_infantis
            anomalias_regra1 = df_mort[df_mort['obitos_infantis'] > df_mort['nascidos_vivos']]
            print(f"Regra (Obitos <= Nascidos): {len(anomalias_regra1)} anomalias detectadas.")
            
            # Regra 2: taxa de mortalidade = (obitos/nascidos)*1000 (onde nascidos > 0)
            valid_rows = df_mort[df_mort['nascidos_vivos'] > 0].copy()
            valid_rows['taxa_calculada'] = (valid_rows['obitos_infantis'] / valid_rows['nascidos_vivos'] * 1000)
            diff = (valid_rows['taxa_calculada'] - valid_rows['taxa_mortalidade_infantil']).abs()
            anomalias_regra2 = valid_rows[diff > 0.01]
            print(f"Regra (Taxa calculada correta): {len(anomalias_regra2)} anomalias detectadas.")
            
            # Imprimir estatistica basica de mortalidade infantil na Bahia
            ba_births = df_mort['nascidos_vivos'].sum()
            ba_deaths = df_mort['obitos_infantis'].sum()
            ba_overall_rate = (ba_deaths / ba_births * 1000) if ba_births > 0 else 0
            print(f"\nEstatistica Consolidada da Bahia (Série 2018-2022 Acumulada):")
            print(f"  Total de Nascidos Vivos: {int(ba_births)}")
            print(f"  Total de Obitos Infantils (<1 ano): {int(ba_deaths)}")
            print(f"  Taxa de Mortalidade Geral do Estado: {ba_overall_rate:.2f} por 1.000 nascidos vivos")
        except Exception as e:
            print(f"[ERRO] Falha ao testar sanidade matematica: {e}")

if __name__ == "__main__":
    analisar_metricas()
