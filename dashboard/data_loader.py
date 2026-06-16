import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_municipal_data():
    """Carrega a base consolidada municipal da Bahia de 2022."""
    path = Path("data/gold/base_consolidada_municipal_2022.csv")
    if not path.exists():
        return pd.DataFrame()
    
    df = pd.read_csv(path)
    
    # Adicionar classificação amigável por Faixa Populacional (para os filtros)
    faixa_map = {
        1: "Até 20.000 hab. (Pequeno Porte I)",
        2: "De 20.001 a 50.000 hab. (Pequeno Porte II)",
        3: "De 50.001 a 100.000 hab. (Médio Porte)",
        4: "De 100.001 a 500.000 hab. (Grande Porte)",
        5: "Mais de 500.000 hab. (Metrópole)"
    }
    
    # Criar uma coluna legível baseada na coluna identificacao_da_faixa_populacional
    if "identificacao_da_faixa_populacional" in df.columns:
        df["faixa_populacional_nome"] = df["identificacao_da_faixa_populacional"].map(faixa_map)
    else:
        df["faixa_populacional_nome"] = "Não Informada"
        
    return df

@st.cache_data
def load_historical_data():
    """Carrega a série histórica estadual da Bahia."""
    path = Path("data/gold/base_consolidada.csv")
    if not path.exists():
        return pd.DataFrame()
    
    df = pd.read_csv(path)
    
    # Certificar que a coluna ano existe
    if 'ano' not in df.columns and 'co_anomes' in df.columns:
        df['ano'] = df['co_anomes'].astype(str).str[:4].astype(int)
        
    return df

def get_binned_data(df):
    """Agrupa os municípios em faixas de esgoto para mitigar Simpson's Paradox."""
    df_clean = df[df['tx_coleta_esgoto'].notna() & df['taxa_mortalidade_infantil'].notna()].copy()
    
    # Determinar se podemos dividir em 3 ou 2 faixas com base na distribuição
    # Se a mediana ou 1º/2º quartis forem zero (caso da Bahia), dividimos em sem/baixa vs. alta cobertura
    if df_clean['tx_coleta_esgoto'].quantile(1/3) == 0:
        # Menos de 5% de rede é considerado baixa/sem cobertura
        df_clean['faixa_esgoto'] = df_clean['tx_coleta_esgoto'].apply(
            lambda x: 'Baixa Cobertura (Até 5%)' if x <= 5 else 'Alta Cobertura (Mais de 5%)'
        )
    else:
        df_clean['faixa_esgoto'] = pd.qcut(
            df_clean['tx_coleta_esgoto'],
            q=3,
            labels=['Baixa Cobertura', 'Média Cobertura', 'Alta Cobertura'],
            duplicates='drop'
        )
        
    analise_faixas = df_clean.groupby('faixa_esgoto', observed=False)['taxa_mortalidade_infantil'].mean().reset_index()
    return analise_faixas
