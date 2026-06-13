import pandas as pd
from pathlib import Path
import re
import unicodedata

def remove_accents_and_special(input_str):
    if not isinstance(input_str, str):
        return input_str
    # Substituir os caracteres de erro comuns e acentos
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    # Substituir caracteres nao alfanumericos por underscore
    clean = re.sub(r'[^\w\s]', '_', only_ascii)
    # Limpar espacos e underscores multiplos
    clean = re.sub(r'[\s_]+', '_', clean).strip('_')
    return clean.lower()

gold_dir = Path('data/gold')

# 1. Padronizar base_snis_geografia.csv
p_snis = gold_dir / 'base_snis_geografia.csv'
if p_snis.exists():
    df_snis = pd.read_csv(p_snis)

    # Drops
    cols_to_drop = [
        'uf_x', 'uf_y', 'codigo_do_ibge', 'codigo_do_municipio', 'municipio',
        'co_regiao_pais', 'regiao_pais', 'nome_da_regiao', 'sigla_da_regiao'
    ]
    df_snis = df_snis.drop(columns=[c for c in cols_to_drop if c in df_snis.columns])

    # Renames & Encoding fixes
    new_cols = []
    for c in df_snis.columns:
        name = remove_accents_and_special(c)
        if name == 'cod_municipio': name = 'co_municipio'
        if name == 'cod_macrorregiao_de_saude': name = 'co_macrorregiao_saude'
        if name == 'cod_regiao_de_saude': name = 'co_regiao_saude'
        new_cols.append(name)
        
    df_snis.columns = new_cols
    df_snis.to_csv(p_snis, index=False)
    print('Padronizado base_snis_geografia.csv')

# 2. Padronizar base_consolidada.csv e base_consolidada_2022.csv
renames = {
    'vl_indicador_calculado_uf_agua': 'tx_cobertura_agua',
    'vl_indicador_calculado_uf_lixo': 'tx_cobertura_lixo',
    'vl_indicador_calculado_uf_sani': 'tx_cobertura_esgoto',
    'vl_indicador_saude_infantil': 'taxa_mortalidade_infantil'
}

for file_name in ['base_consolidada.csv', 'base_consolidada_2022.csv']:
    p_cons = gold_dir / file_name
    if p_cons.exists():
        df_cons = pd.read_csv(p_cons)
        df_cons = df_cons.rename(columns={c: r for c, r in renames.items() if c in df_cons.columns})
        df_cons.to_csv(p_cons, index=False)
        print(f'Padronizado {file_name}')
