import pandas as pd
from pathlib import Path

def ler_tabnet_limpo(caminho):
    # Lendo arquivo, pulando o cabeçalho descritivo do TabNet
    df = pd.read_csv(caminho, sep=';', encoding='latin1', skiprows=3, engine='python')
    
    # Pegar o nome da primeira coluna (Município)
    col_municipio = df.columns[0]
    
    # Tratar traços e valores não numéricos
    df['Total'] = df['Total'].replace('-', '0')
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    
    # Remover linhas de rodapé (onde Total é nulo) e a linha de Total geral
    df = df.dropna(subset=['Total'])
    df = df[~df[col_municipio].str.contains('Total', na=False, case=False)]
    
    # Remover "MUNICIPIO IGNORADO"
    df = df[~df[col_municipio].str.contains('IGNORADO', na=False, case=False)]
    
    # Separar código IBGE e Nome do município
    # O formato é "290010 ABAIRA"
    df['co_municipio'] = df[col_municipio].str.extract(r'^(\d+)').astype(str)
    df['no_municipio'] = df[col_municipio].str.replace(r'^\d+\s', '', regex=True).str.strip()
    
    # Filtrar apenas as colunas úteis
    return df[['co_municipio', 'no_municipio', 'Total']]

def processar_sim_sinasc():
    print("--- Processando SIM e SINASC (2022) ---")
    
    sim_path = Path("data/landing/sim_cnv_inf10ba180535179_105_131_169.csv")
    sinasc_path = Path("data/landing/sinasc_cnv_nvba180642179_105_131_169.csv")
    gold_path = Path("data/gold")
    gold_path.mkdir(parents=True, exist_ok=True)
    
    # Extração e Limpeza Básica
    df_sim = ler_tabnet_limpo(sim_path)
    df_sim = df_sim.rename(columns={'Total': 'obitos_infantis'})
    
    df_sinasc = ler_tabnet_limpo(sinasc_path)
    df_sinasc = df_sinasc.rename(columns={'Total': 'nascidos_vivos'})
    
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
