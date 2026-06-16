import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuração global de estilo do Seaborn para ficar harmonioso com a interface
sns.set_theme(style="whitegrid")
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

def plot_mortalidade_histogram(df):
    """Gera o histograma de distribuição da taxa de mortalidade infantil."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.histplot(
        data=df, 
        x='taxa_mortalidade_infantil', 
        kde=True, 
        ax=ax, 
        color='#e74c3c', # Vermelho suave/coral para mortalidade
        bins=20
    )
    ax.set_title('Distribuição da Taxa de Mortalidade Infantil (Municípios da BA)', fontweight='bold', pad=12)
    ax.set_xlabel('Taxa de Mortalidade (óbitos por 1.000 nascidos vivos)')
    ax.set_ylabel('Frequência (Nº de Municípios)')
    plt.tight_layout()
    return fig

def plot_agua_boxplot(df):
    """Gera o boxplot de cobertura de atendimento de água."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(
        data=df, 
        y='tx_atendimento_agua', 
        ax=ax, 
        color='#3498db', # Azul água
        width=0.4
    )
    ax.set_title('Distribuição da Cobertura de Atendimento de Água', fontweight='bold', pad=12)
    ax.set_ylabel('Taxa de Atendimento de Água (%)')
    ax.set_xlabel('Municípios Baianos')
    plt.tight_layout()
    return fig

def plot_esgoto_scatter(df):
    """Gera o gráfico de dispersão de esgoto vs mortalidade infantil."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.scatterplot(
        data=df, 
        x='tx_coleta_esgoto', 
        y='taxa_mortalidade_infantil', 
        ax=ax, 
        alpha=0.7, 
        color='#9b59b6', # Roxo esgoto
        edgecolor='w',
        s=60
    )
    # Adicionar uma linha de tendência (regressão linear) discreta
    if len(df) > 1:
        try:
            sns.regplot(
                data=df,
                x='tx_coleta_esgoto',
                y='taxa_mortalidade_infantil',
                scatter=False,
                ax=ax,
                color='#2c3e50',
                line_kws={'linestyle': '--', 'linewidth': 1.5}
            )
        except Exception:
            pass
            
    ax.set_title('Dispersão: Coleta de Esgoto vs. Mortalidade Infantil', fontweight='bold', pad=12)
    ax.set_xlabel('Taxa de Coleta de Esgoto (%)')
    ax.set_ylabel('Taxa de Mortalidade (por 1.000 nv)')
    plt.tight_layout()
    return fig

def plot_correlation_heatmap(df):
    """Gera a matriz de correlação de Pearson focada."""
    colunas_analise = [
        'taxa_mortalidade_infantil',
        'tx_atendimento_agua', 
        'tx_coleta_esgoto',
        'tx_coleta_lixo_pop_total'
    ]
    
    # Renomear para exibição amigável no heatmap
    df_friendly = df[colunas_analise].rename(columns={
        'taxa_mortalidade_infantil': 'Mortalidade Infantil',
        'tx_atendimento_agua': 'Cobertura de Água',
        'tx_coleta_esgoto': 'Coleta de Esgoto',
        'tx_coleta_lixo_pop_total': 'Coleta de Lixo'
    })
    
    matriz_corr = df_friendly.corr()
    
    fig, ax = plt.subplots(figsize=(5, 4.5))
    sns.heatmap(
        matriz_corr[['Mortalidade Infantil']].drop('Mortalidade Infantil', errors='ignore'), 
        annot=True, 
        cmap='RdBu_r', 
        vmin=-1, 
        vmax=1, 
        fmt='.3f', 
        linewidths=0.5,
        cbar=True,
        ax=ax
    )
    ax.set_title('Correlação de Pearson com a\nMortalidade Infantil (Censo 2022)', 
              fontsize=11, fontweight='bold', pad=12)
    plt.tight_layout()
    return fig

def plot_historical_trend(df_hist):
    """Gera o gráfico de dois eixos para comparar evolução histórica (Bahia)."""
    anos_validos = [2018, 2019, 2022, 2023]
    df_plot = df_hist[df_hist['ano'].isin(anos_validos)].sort_values('ano')
    
    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    
    # Eixo 1: Coleta de Esgoto (Azul)
    color = '#2980b9'
    ax1.set_xlabel('Ano (Escopo Corrigido)', fontweight='bold')
    ax1.set_ylabel('Taxa de Coleta de Esgoto (%)', color=color, fontweight='bold')
    sns.lineplot(
        data=df_plot, 
        x='ano', 
        y='tx_cobertura_esgoto', 
        marker='o', 
        color=color, 
        ax=ax1, 
        linewidth=2.5,
        label='Coleta de Esgoto (%)'
    )
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(anos_validos)
    ax1.get_legend().remove() # remover a legenda padrão pois faremos a de dois eixos manual
    
    # Eixo 2: Mortalidade Infantil (Vermelho)
    ax2 = ax1.twinx()  
    color = '#c0392b'
    ax2.set_ylabel('Mortalidade Infantil (por 1.000 nv)', color=color, fontweight='bold')
    sns.lineplot(
        data=df_plot, 
        x='ano', 
        y='taxa_mortalidade_infantil', 
        marker='s', 
        color=color, 
        ax=ax2, 
        linewidth=2.5,
        label='Mortalidade Infantil'
    )
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Evolução Temporal: Coleta de Esgoto vs. Mortalidade Infantil na Bahia\n(Nota: Anos 2020-2021 omitidos devido ao apagão de dados do SNIS na pandemia)', 
              fontsize=11, fontweight='bold', pad=12)
    plt.tight_layout()
    return fig

def plot_esgoto_bins(analise_faixas):
    """Gera o gráfico de barras por faixas de esgoto para resolver Simpson's Paradox."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    
    # Plot das barras
    sns.barplot(
        data=analise_faixas, 
        x='faixa_esgoto', 
        y='taxa_mortalidade_infantil', 
        palette='Blues_r',
        ax=ax
    )
    
    # Adicionar os valores numéricos por cima das barras
    for index, row in analise_faixas.iterrows():
        ax.text(
            index, 
            row['taxa_mortalidade_infantil'] + 0.3, 
            f"{row['taxa_mortalidade_infantil']:.2f}", 
            color='black', 
            ha="center", 
            fontweight='bold',
            fontsize=10
        )
        
    ax.set_title('Taxa de Mortalidade Infantil Média por Nível de Coleta de Esgoto\n(Agrupamento de Municípios - Censo 2022)', 
              fontsize=11, fontweight='bold', pad=12)
    ax.set_xlabel('Nível de Cobertura de Esgoto do Município', fontweight='bold')
    ax.set_ylabel('Mortalidade Infantil Média (por 1.000 nv)', fontweight='bold')
    
    # Dar uma margem no topo do eixo y para o texto caber
    max_val = analise_faixas['taxa_mortalidade_infantil'].max()
    ax.set_ylim(0, max_val + 2)
    
    plt.tight_layout()
    return fig
