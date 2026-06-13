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
        'uf_x', 'uf_y', 'codigo_do_ibge', 'codigo_do_municipio', 'municipio',
        'ano_de_referencia'  # Dropar ano_de_referencia para evitar duplicação com a coluna 'ano'
    ]
    df_consolidada = df_consolidada.drop(columns=[c for c in cols_to_drop if c in df_consolidada.columns], errors='ignore')
    
    # Dicionário de renomeação para simplificar nomes de colunas extensas do SNIS
    renomeacoes = {
        'nome_do_orgao_responsavel_pela_gestao': 'orgao_gestor',
        'sigla_do_orgao_responsavel_pela_gestao': 'sigla_orgao_gestor',
        'natureza_juridica_do_orgao_municipal_responsavel': 'natureza_juridica_orgao',
        'tx_cobertura_da_coleta_rdo_em_relacao_a_pop_total': 'tx_coleta_lixo_pop_total',
        'taxa_de_terceirizacao_da_coleta': 'tx_terceirizacao_coleta',
        'produtividades_media_de_coletadores_e_motorista': 'produtividade_media_coleta',
        'massa_rdo_coletada_per_capita_em_relacao_a_pop_total_atendida': 'massa_lixo_per_capita',
        'custo_unitario_da_coleta': 'custo_unitario_coleta',
        'incidencia_do_custo_da_coleta_no_custo_total_do_manejo': 'incid_custo_coleta_total',
        'incidencia_de_emprega_da_coleta_no_total_de_empregados_no_manejo': 'incid_empregados_coleta',
        'relacao_quantidade_rcd_coletada_pela_pref_p_quant_total_rdo_rpu': 'rel_rcd_rdo_rpu',
        'relacao_quantidades_coletadas_de_rpu_por_rdo': 'rel_rpu_rdo',
        'massa_rdo_rpu_coletada_per_capita_em_relacao_a_populacao_total_atendida': 'massa_rdo_rpu_per_capita',
        'taxa_de_recuperacao_de_reciclaveis_em_relacao_a_quantidade_de_rdo_e_rpu': 'tx_recuperacao_reciclaveis',
        'relacao_entre_quantidades_da_coleta_seletiva_e_rdo': 'rel_coleta_seletiva_rdo',
        'incid_de_papel_papelao_sobre_total_mat_recuperado': 'incid_papel_recuperado',
        'incid_de_plasticos_sobre_total_material_recuperado': 'incid_plastico_recuperado',
        'incid_de_metais_sobre_total_material_recuperado': 'incid_metal_recuperado',
        'incid_de_vidros_sobre_total_de_material_recuperado': 'incid_vidro_recuperado',
        'incidencia_de_outros_sobre_total_material_recuperado': 'incid_outros_recuperado',
        'taxa_de_rss_sobre_rdo_rpu': 'tx_rss_rdo_rpu',
        'taxa_de_terceirizacao_de_varredores': 'tx_terceirizacao_varredores',
        'taxa_de_terceirizacao_de_varricao': 'tx_terceirizacao_varricao',
        'custo_unitario_da_varricao': 'custo_unitario_varricao',
        'produtividade_media_do_varredores': 'produtividade_media_varredores',
        'incidencia_do_custo_da_varricao_no_custo_total_do_manejo': 'incid_custo_varricao_total',
        'incidencia_de_varredores_no_total_de_empregados_no_manejo': 'incid_varredores_total',
        'relacao_de_capinadores_no_total_de_empregados_no_manejo': 'incid_capinadores_total',
        'incidencia_de_despesas_com_rsu_na_prefeitura': 'incid_despesa_rsu_prefeitura',
        'incidencia_de_despesas_com_empresas_contratadas': 'incid_despesa_contratadas',
        'incidencia_de_empregados_proprios': 'incid_empregados_proprios',
        'incidencia_de_empreg_de_empr_contrat_no_total_de_empreg_no_manejo': 'incid_empregados_contratados',
        'incidencia_de_empreg_admin_no_total_de_empreg_no_manejo': 'incid_empregados_admin',
        'tx_atendimento_total_agua': 'tx_atendimento_agua',
        'tx_atendimento_urbano_agua': 'tx_atendimento_urbano_agua',
        'tx_atendimento_urbano_esgoto': 'tx_atendimento_urbano_esgoto',
        'tx_coleta_esgoto': 'tx_coleta_esgoto',
        'tx_tratamento_esgoto': 'tx_tratamento_esgoto',
        'no_prestador_servico_ae': 'prestador_servico_ae'
    }
    df_consolidada = df_consolidada.rename(columns=renomeacoes)
    
    # Tratamento de Nulos Avançado na base municipal (sem valores sentinelas)
    colunas_numericas = df_consolidada.select_dtypes(include=['number']).columns.tolist()
    
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
        else:
            # Imputação hierárquica por Faixa Populacional -> Estado -> NaN (Vazio real do Pandas)
            if 'identificacao_da_faixa_populacional' in df_consolidada.columns:
                medianas_grupo = df_consolidada.groupby('identificacao_da_faixa_populacional')[col].transform('median')
            else:
                medianas_grupo = pd.Series([pd.NA] * len(df_consolidada))
                
            mediana_estado = df_consolidada[col].median()
            
            # Preencher com a mediana do grupo
            df_consolidada[col] = df_consolidada[col].fillna(medianas_grupo)
            # Preencher o restante (se houver) com a mediana do estado
            if not pd.isna(mediana_estado):
                df_consolidada[col] = df_consolidada[col].fillna(mediana_estado)
            # Os nulos que ainda restarem permanecerão como NaN (vazio real)
            
    # Dropar as colunas de fato
    if colunas_para_dropar:
        print(f"  [CLEAN] Dropando {len(colunas_para_dropar)} colunas com 100% de nulos na base municipal.")
        df_consolidada = df_consolidada.drop(columns=colunas_para_dropar)
        
    # Salvar base consolidada municipal
    df_consolidada.to_csv(output_file, index=False)
    print(f"[OK] Base consolidada municipal gerada com sucesso: {output_file.name}")
    print(f"   Shape: {df_consolidada.shape} ({len(df_consolidada)} municipios unificados)")

if __name__ == "__main__":
    consolidar_municipal()
