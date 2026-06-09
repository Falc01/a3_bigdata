import pandas as pd
from pathlib import Path

def ler_tabnet_limpo(caminho):
    # Encontrar dinamicamente a linha de cabeçalho onde aparece 'Munic' e ';'
    header_row = 3
    with open(caminho, 'r', encoding='latin1') as f:
        for idx, line in enumerate(f):
            if 'Munic' in line and ';' in line:
                header_row = idx
                break
                
    # Lendo arquivo
    df = pd.read_csv(caminho, sep=';', encoding='latin1', skiprows=header_row, engine='python')
    
    # Pegar o nome da primeira coluna (Município) e da segunda (Valor do indicador)
    col_municipio = df.columns[0]
    col_valor = df.columns[1]
    
    # Tratar traços e valores não numéricos
    df[col_valor] = df[col_valor].astype(str).str.replace('-', '0')
    df[col_valor] = pd.to_numeric(df[col_valor], errors='coerce')
    
    # Remover linhas de rodapé (onde o valor é nulo) e a linha de Total geral
    df = df.dropna(subset=[col_valor])
    df = df[~df[col_municipio].str.contains('Total', na=False, case=False)]
    
    # Remover "MUNICIPIO IGNORADO"
    df = df[~df[col_municipio].str.contains('IGNORADO', na=False, case=False)]
    
    # Separar código IBGE e Nome do município
    # O formato é "290010 ABAIRA"
    df['co_municipio'] = df[col_municipio].str.extract(r'^(\d+)').astype(str)
    df['no_municipio'] = df[col_municipio].str.replace(r'^\d+\s', '', regex=True).str.strip()
    
    # Filtrar apenas as colunas úteis
    return df[['co_municipio', 'no_municipio', col_valor]]

def processar_sim_sinasc():
    print("--- Processando SIM e SINASC (2022) ---")
    
    sim_path = Path("data/landing/sim_cnv_obt10ba135205187_107_8_217.csv")
    sinasc_path = Path("data/landing/sinasc_cnv_nvba135328187_107_8_217.csv")
    gold_path = Path("data/gold")
    gold_path.mkdir(parents=True, exist_ok=True)
    
    # Extração e Limpeza Básica
    df_sim = ler_tabnet_limpo(sim_path)
    df_sim = df_sim.rename(columns={df_sim.columns[2]: 'obitos_infantis'})
    
    df_sinasc = ler_tabnet_limpo(sinasc_path)
    df_sinasc = df_sinasc.rename(columns={df_sinasc.columns[2]: 'nascidos_vivos'})
    
    # Transformação: Merge
    df_merged = pd.merge(df_sinasc, df_sim, on=['co_municipio', 'no_municipio'], how='outer')
    
    # Preencher NaN com 0 para casos onde não houve óbito
    df_merged['obitos_infantis'] = df_merged['obitos_infantis'].fillna(0)
    df_merged['nascidos_vivos'] = df_merged['nascidos_vivos'].fillna(0)
    
    # Transformação: Cálculo da Taxa
    # Evitar divisão por zero
    df_merged['taxa_mortalidade_infantil'] = df_merged.apply(
        lambda row: (row['obitos_infantis'] / row['nascidos_vivos'] * 1000) if row['nascidos_vivos'] > 0 else 0, 
        axis=1
    )
    
    # Adicionar ano e uf
    df_merged['ano'] = 2022
    df_merged['co_uf'] = 29
    df_merged['sg_uf'] = 'BA'
    
    # Reordenar colunas
    colunas_finais = [
        'ano', 'co_uf', 'sg_uf', 'co_municipio', 'no_municipio', 
        'nascidos_vivos', 'obitos_infantis', 'taxa_mortalidade_infantil'
    ]
    df_merged = df_merged[colunas_finais]
    
    # Carga: Salvar na camada Gold
    dest = gold_path / "base_mortalidade_municipal_2022.csv"
    df_merged.to_csv(dest, index=False)
    
    print(f"[OK] Base consolidada salva em: {dest.name}")
    print(f"Total de registros: {len(df_merged)}")
    print(df_merged.head())

if __name__ == "__main__":
    processar_sim_sinasc()
