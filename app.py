import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Configuração da página Streamlit (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="UNIFACS - Dashboard A3 Saneamento e Saúde",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importações dos módulos internos do dashboard
from dashboard.data_loader import load_municipal_data, load_historical_data, get_binned_data
from dashboard.plots import (
    plot_mortalidade_histogram,
    plot_agua_boxplot,
    plot_esgoto_scatter,
    plot_correlation_heatmap,
    plot_historical_trend,
    plot_esgoto_bins
)
from dashboard.styles import inject_custom_css

# Injetar o CSS customizado
inject_custom_css()

# Carregar os dados
df_municipal = load_municipal_data()
df_historico = load_historical_data()

# ==============================================================================
# BARRA LATERAL (SIDEBAR) - FILTROS E NAVEGAÇÃO
# ==============================================================================
st.sidebar.image("docs/unifacs.svg" if Path("docs/unifacs.svg").exists() else "https://via.placeholder.com/150", width=150)
st.sidebar.title("Navegação")

menu = st.sidebar.radio(
    "Ir para:",
    [
        "🏠 Início & Resumo Executivo",
        "⚙️ Pipeline ETL & Qualidade",
        "📊 Análise Exploratória (EDA)",
        "💡 Storytelling & Paradoxo",
        "⚖️ LGPD & Recomendações"
    ]
)

# Filtros apenas visíveis na aba de EDA
df_filtered = df_municipal.copy()
if menu == "📊 Análise Exploratória (EDA)":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtros de Análise")
    
    # Filtro de Porte Populacional
    portes_disponiveis = sorted(df_municipal["faixa_populacional_nome"].dropna().unique().tolist())
    portes_selecionados = st.sidebar.multiselect(
        "Filtrar por Porte Populacional:",
        options=portes_disponiveis,
        default=portes_disponiveis
    )
    
    # Filtro de Coleta de Esgoto Mínima
    esgoto_min = st.sidebar.slider(
        "Cobertura de Esgoto Mínima (%):",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=5.0
    )
    
    # Aplicar os filtros ao df_filtered
    if portes_selecionados:
        df_filtered = df_filtered[df_filtered["faixa_populacional_nome"].isin(portes_selecionados)]
    df_filtered = df_filtered[df_filtered["tx_coleta_esgoto"] >= esgoto_min]
    
    # Exibir resumo do filtro na sidebar
    st.sidebar.info(f"Mostrando {len(df_filtered)} de {len(df_municipal)} municípios.")

# Rodapé da sidebar com os autores
st.sidebar.markdown("---")
st.sidebar.markdown("**Desenvolvedores:**")
st.sidebar.caption("* Aurea dos Reis Santos Neta")
st.sidebar.caption("* Daniel Costa Santos")
st.sidebar.caption("* João G. P. Hohlenwerger")
st.sidebar.caption("* João Spinola Falcão")
st.sidebar.caption("* Kawan Oliveira Carneiro")
st.sidebar.caption("* Pedro Adaime Ribeiro")

# ==============================================================================
# MENU 1: INÍCIO & RESUMO EXECUTIVO
# ==============================================================================
if menu == "🏠 Início & Resumo Executivo":
    st.markdown('<h1 class="main-title">Impacto do Saneamento na Mortalidade Infantil</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Série Histórica Estadual (2018-2023) e Análise Transversal Municipal (2022)</p>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="preamble-box">
        <strong>PREÂMBULO:</strong><br>
        Trabalho acadêmico apresentado como relatório final consolidado da atividade prática para a disciplina 
        de <strong>Análise de Dados e Big Data</strong> do Curso de Tecnologia da Informação / Computação da 
        <strong>Universidade Salvador — UNIFACS</strong>, sob a orientação do professor da disciplina.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Seção de Métricas Principais (KPIs) com Estilo Customizado
    st.subheader("Indicadores Gerais de Saneamento e Saúde (Bahia - Censo 2022)")
    
    # Calcular médias
    avg_agua = df_municipal["tx_atendimento_agua"].mean()
    avg_esgoto = df_municipal["tx_coleta_esgoto"].mean()
    avg_lixo = df_municipal["tx_coleta_lixo_pop_total"].mean()
    avg_mort = df_municipal["taxa_mortalidade_infantil"].mean()
    
    # Injetar HTML para os cartões de KPI
    st.markdown(
        f"""
        <div class="kpi-container">
            <div class="kpi-card kpi-blue">
                <div class="kpi-label">Abastecimento de Água</div>
                <div class="kpi-value">{avg_agua:.2f}%</div>
                <div class="kpi-sub">Média dos municípios da BA</div>
            </div>
            <div class="kpi-card kpi-purple">
                <div class="kpi-label">Coleta de Esgoto</div>
                <div class="kpi-value">{avg_esgoto:.2f}%</div>
                <div class="kpi-sub">Forte gargalo de rede pública</div>
            </div>
            <div class="kpi-card kpi-green">
                <div class="kpi-label">Coleta de Lixo</div>
                <div class="kpi-value">{avg_lixo:.2f}%</div>
                <div class="kpi-sub">Atendimento de resíduos sólidos</div>
            </div>
            <div class="kpi-card kpi-red">
                <div class="kpi-label">Mortalidade Infantil</div>
                <div class="kpi-value">{avg_mort:.2f}</div>
                <div class="kpi-sub">Óbitos por 1.000 nascidos vivos</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### Resumo Executivo")
    st.write(
        """
        Este projeto prático investiga a correlação entre as taxas de cobertura de infraestrutura sanitária básica 
        (abastecimento de água, esgotamento e coleta de resíduos sólidos) e os indicadores de saúde infantil (taxa de mortalidade 
        em crianças menores de 1 ano) no estado da Bahia. 
        
        A análise compreende duas abordagens estatísticas complementares:
        1. **Abordagem Macro-Temporal (Bahia):** Estudo da evolução das taxas estaduais agregadas ao longo da série histórica 2018-2023, 
        revelando fortes tendências de redução de mortalidade decorrentes do avanço sistêmico da infraestrutura.
        2. **Abordagem Transversal Municipal (2022):** Análise detalhada dos 332 municípios consolidados da Bahia no ano do Censo 2022, 
        identificando distorções de subnotificação e revelando a real eficácia das redes de saneamento básico após o agrupamento correto em faixas.
        """
    )
    
    st.markdown('<div class="footer-text">Universidade Salvador (UNIFACS) · Salvador — BA · 2026</div>', unsafe_allow_html=True)

# ==============================================================================
# MENU 2: PIPELINE ETL & QUALIDADE
# ==============================================================================
elif menu == "⚙️ Pipeline ETL & Qualidade":
    st.markdown('<h1 class="main-title">Engenharia de Dados & Pipeline ETL</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Arquitetura de Medalhão e Tratamento de Qualidade de Dados</p>', unsafe_allow_html=True)
    
    st.subheader("1. Fluxo e Orquestração do Pipeline")
    st.write(
        """
        O pipeline foi construído seguindo a arquitetura clássica de camadas (Landing → Bronze → Silver → Gold), 
        garantindo a modularidade, o tratamento correto de nulos e o pareamento geográfico íntegro.
        """
    )
    
    # Exibir a estrutura em colunas
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**1. Landing Layer**")
        st.caption("Armazena 7 arquivos governamentais brutos (.csv e .zip) baixados do DATASUS (SIM/SINASC), SNIS e Ministério da Saúde.")
    with c2:
        st.markdown("**2. Bronze Layer**")
        st.caption("Extração e descompactação idempotente de zips. Prioriza formatos ricos (.xlsx sobre .csv) e remove duplicidades de leitura.")
    with c3:
        st.markdown("**3. Silver Layer**")
        st.caption("Limpeza inicial, tratamento de layouts corrompidos do Excel (rodapés explicativos do TabNet) e conversão de encondings para UTF-8.")
    with c4:
        st.markdown("**4. Gold Layer**")
        st.caption("Cruzamentos municipais pelo código IBGE, cálculo da TMI de 5 anos, imputações hierárquicas populacionais e remoção definitiva de sentinelas (-1).")
        
    st.markdown("---")
    st.subheader("2. 🗃️ Inventário de Fontes de Dados (Landing)")
    st.write(
        """
        Os arquivos brutos (camada **Landing**) são provenientes de plataformas públicas oficiais de saúde e saneamento. 
        Estes dados são extraídos em formatos brutos e compactados antes de serem submetidos ao pipeline de processamento:
        """
    )
    
    # Criar DataFrame com as fontes de dados da camada landing
    landing_data = {
        "Arquivo / Diretório": [
            "sim_cnv_inf10ba131422187_107_8_217.csv",
            "sinasc_cnv_nvba131418187_107_8_217.csv",
            "Planilha_RS_2022_atualizado_29112024.zip",
            "DIAGNOSTICO_TEMATICO_VISAO_GERAL_AE_SNIS_2023_ATUALIZADO.zip",
            "proporcao_agua.csv",
            "proporcao_lixo.csv",
            "proporcao_sanitaria.csv",
            "mgdi_ms_k5p.csv *"
        ],
        "Origem": [
            "DATASUS / SIM",
            "DATASUS / SINASC",
            "SNIS (Manejo de Resíduos Sólidos)",
            "SNIS (Água e Esgoto)",
            "SNIS (Série Histórica)",
            "SNIS (Série Histórica)",
            "SNIS (Série Histórica)",
            "Ministério da Saúde"
        ],
        "Período": [
            "2018 - 2022",
            "2018 - 2022",
            "2022",
            "2022",
            "2018 - 2023",
            "2018 - 2023",
            "2018 - 2023",
            "2000 - 2023"
        ],
        "Descrição Básica": [
            "Óbitos infantis acumulados (< 1 ano) por município de residência (BA).",
            "Nascidos vivos acumulados por município de residência da mãe (BA).",
            "Dados de saneamento de resíduos sólidos (coleta e manejo de lixo).",
            "Informações de prestadores sobre abastecimento de água e coleta de esgoto.",
            "Histórico estadual de déficit de abastecimento de água tratada.",
            "Histórico estadual de déficit de coleta de resíduos sólidos (lixo).",
            "Histórico estadual de déficit de esgotamento sanitário por rede pública.",
            "Série de mortalidade infantil estadual geral para todas as UFs."
        ]
    }
    df_landing = pd.DataFrame(landing_data)
    st.dataframe(df_landing, use_container_width=True)
    st.caption("* Nota: O arquivo `mgdi_ms_k5p.csv` é um conjunto de dados suplementar de apoio para a série histórica estadual.")

    st.markdown("##### 🔍 Detalhamento das Fontes e Métodos de Extração")
    st.write(
        """
        Para entender a confiabilidade e o contexto de obtenção de cada registro, clique para expandir as seções abaixo:
        """
    )
    
    with st.expander("🩺 Sistema de Informações de Saúde (SIM & SINASC / DATASUS)"):
        st.write(
            """
            * **Origem Governamental:** Ministério da Saúde / Departamento de Informática do SUS (DATASUS).
            * **SIM (Sistema de Informações sobre Mortalidade):** Criado para registrar os dados de óbitos no país, baseia-se nas Declarações de Óbito (DO) preenchidas por médicos. Ele fornece estatísticas cruciais para a análise de causas de morte evitáveis na infância.
            * **SINASC (Sistema de Informações sobre Nascidos Vivos):** Reúne dados de nascimentos com base nas Declarações de Nascido Vivo (DNV) preenchidas em maternidades de todo o Brasil.
            * **Como foi extraído:** As bases de saúde da Bahia foram baixadas via portal **TabNet (DATASUS)**, selecionando os dados consolidados agregados por município de residência de 2018 a 2022. O agrupamento de 5 anos é uma decisão epidemiológica para reduzir anomalias estatísticas de cidades muito pequenas.
            """
        )

    with st.expander("🚰 Sistema Nacional de Informações sobre Saneamento (SNIS / MDR)"):
        st.write(
            """
            * **Origem Governamental:** Ministério do Desenvolvimento Regional (MDR) / Ministério das Cidades.
            * **SNIS Água e Esgoto (AE):** Coleta anualmente dados operacionais, financeiros, de qualidade e gerenciais de prestadores públicos e privados de serviços de água e esgoto no Brasil. Fornece indicadores como taxas de atendimento de água, taxas de coleta de esgoto e índices de perdas de distribuição.
            * **SNIS Resíduos Sólidos (RS):** Focado na coleta e destinação final de resíduos sólidos domésticos e na limpeza urbana, fornecendo informações sobre a cobertura da população atendida com coleta regular de lixo.
            * **Como foi extraído:** Os arquivos compactados (.zip) contendo as bases de dados brutas do SNIS para o ano-base de 2022 (publicados no final de 2023) foram obtidos diretamente do site oficial do SNIS na seção de dados abertos e diagnósticos anuais.
            """
        )
        
    with st.expander("📈 Séries Históricas Estaduais Consolidadas (SNIS & MS)"):
        st.write(
            """
            * **Déficits de Saneamento (`proporcao_agua`, `proporcao_lixo`, `proporcao_sanitaria`):** São planilhas históricas contendo a evolução temporal anual do déficit (população não atendida) por estado de 2018 a 2023. O pipeline inverte esses indicadores para obter a taxa de cobertura real ($100 - \\text{déficit}$).
            * **Série Geral de Mortalidade (`mgdi_ms_k5p.csv`):** Base histórica contendo a taxa de mortalidade infantil estadual oficial do Ministério da Saúde de 2000 a 2023. Permite correlacionar a evolução histórica de saneamento da Bahia com o panorama geral de saúde ao longo de mais de duas décadas.
            """
        )
        
    st.markdown("---")
    st.subheader("3. Dicionário de Variáveis Principais (Gold)")
    st.write("Filtre e busque abaixo o significado e a tipagem das principais colunas consumidas pelas análises:")
    
    # Criar DataFrame do Dicionário de Dados
    dict_data = {
        "Variável": [
            "no_municipio", "co_municipio", "populacao_ibge_2022", "taxa_mortalidade_infantil", 
            "nascidos_vivos", "obitos_infantis", "tx_atendimento_agua", "tx_coleta_esgoto", 
            "tx_coleta_lixo_pop_total", "idx_conformidade_coliformes", "prestador_servico_ae"
        ],
        "Tipo": [
            "Texto", "Numérico", "Numérico", "Numérico", "Numérico", "Numérico", "Numérico", "Numérico", "Numérico", "Numérico", "Texto"
        ],
        "Origem": [
            "IBGE / DATASUS", "IBGE", "IBGE (Censo)", "DATASUS (SIM/SINASC)", "DATASUS (SINASC)", 
            "DATASUS (SIM)", "SNIS AE", "SNIS AE", "SNIS RS", "SNIS AE", "SNIS AE"
        ],
        "Descrição": [
            "Nome oficial do município baiano.",
            "Código oficial do IBGE de 6 dígitos.",
            "População total contada no Censo 2022.",
            "Taxa acumulada de mortalidade infantil de 5 anos (por 1.000 nv).",
            "Soma acumulada de bebês nascidos vivos no período de 5 anos (2018-2022).",
            "Soma acumulada de óbitos infantis (< 1 ano) no período (2018-2022).",
            "Cobertura de atendimento de água potável no município (%).",
            "Cobertura de rede pública de coleta de esgoto doméstico (%).",
            "Cobertura de coleta de lixo doméstico da população total (%).",
            "Conformidade bacteriológica da água (presença de coliformes).",
            "Nome do prestador de serviço de água e esgoto (ex: EMBASA)."
        ]
    }
    df_dict = pd.DataFrame(dict_data)
    
    # Caixa de busca interativa
    search_query = st.text_input("🔍 Digite o nome ou descrição de uma variável para buscar:", "")
    if search_query:
        df_filtered_dict = df_dict[
            df_dict["Variável"].str.contains(search_query, case=False) | 
            df_dict["Descrição"].str.contains(search_query, case=False)
        ]
        st.dataframe(df_filtered_dict, use_container_width=True)
    else:
        st.dataframe(df_dict, use_container_width=True)
        
    st.markdown("---")
    st.subheader("4. 🛠️ Higienização e Engenharia de Recursos")
    st.write(
        """
        Para garantir a integridade da análise estatística, o pipeline de ETL aplicou transformações 
        avançadas nas planilhas governamentais originais. Expanda as caixas abaixo para ver os detalhes técnicos:
        """
    )
    
    with st.expander("📁 Ajuste Dinâmico de Layouts (TabNet/SNIS)"):
        st.write(
            """
            * **Filtro de Cabeçalho Explícito:** Os arquivos brutos continham de 3 a 8 linhas de texto explicativo antes da tabela real. O pipeline localiza dinamicamente a linha que inicia com 'Munic' ou 'Código do Município' para iniciar a carga.
            * **Deduplicação de Arquivos:** O pipeline prioriza arquivos de planilha Excel (.xlsx) sobre arquivos de valores separados por vírgula (.csv) em caso de mesma origem, evitando duplicidade de dados brutos na camada Bronze.
            * **Conversão de Separadores:** Caracteres vazios do TabNet (como o traço `-`) e vírgulas decimais foram limpos e padronizados para garantir a tipagem numérica correta dos campos.
            """
        )
        
    with st.expander("🔢 Tratamento de Nulos & Erradicação de Sentinelas (-1)"):
        st.write(
            """
            * **Substituição de Sentinelas:** Valores como `-1` ou `'Não Informado'` foram erradicados e substituídos por nulos reais (`NaN`). Isso garante que funções matemáticas do Pandas (como `.mean()` ou `.corr()`) ignorem esses registros e não gerem correlações artificiais.
            * **Imputação Hierárquica:** Municípios com dados parciais em branco receberam a **mediana da sua respectiva Faixa Populacional do IBGE** (Pequeno Porte, Médio Porte, etc.). 
            * **Mediana do Estado:** Caso o grupo demográfico inteiro fosse nulo, aplicou-se a mediana estadual como fallback secundário.
            """
        )
        
    with st.expander("🔤 Padronização e Codificação (UTF-8)"):
        st.write(
            """
            * **Codificação de Caracteres:** Arquivos originais do DATASUS foram convertidos do encoding `Latin-1` (típico do Windows) para `UTF-8` de forma robusta, prevenindo falhas de compilação em diferentes sistemas operacionais decorrentes de acentuações geográficas (ex: 'América Dourada').
            * **Nomes em Snake_Case:** Colunas longas do SNIS (ex: `tx_cobertura_da_coleta_rdo_em_relacao_a_pop_total`) foram mapeadas e renomeadas em lote para nomes concisos e inteligíveis (ex: `tx_coleta_lixo_pop_total`), reduzindo a complexidade de desenvolvimento de código.
            """
        )
        
    st.markdown("---")
    st.subheader("5. Suite de Validação de Qualidade (Quality Gate)")
    st.success("✅ **Suite `verificar_checklist.py` executada com sucesso!**")
    st.info(
        """
        **Métricas de Homologação:**
        * **Taxa de Pareamento Geográfico (Match Rate):** **79.62%** (332 de 417 municípios integrados). A ausência residual representa pequenas vilas que não enviaram declarações ao SNIS em 2022.
        * **Nulos Sentinela (-1):** Totalmente erradicados e convertidos para vazio real (NaN) para garantir a integridade das funções estatísticas do Pandas.
        """
    )

# ==============================================================================
# MENU 3: ANÁLISE EXPLORATÓRIA (EDA)
# ==============================================================================
elif menu == "📊 Análise Exploratória (EDA)":
    st.markdown('<h1 class="main-title">Análise Exploratória de Dados (EDA)</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Investigação Transversal da Infraestrutura Municipal na Bahia (Censo 2022)</p>', unsafe_allow_html=True)
    
    st.write(
        """
        Nesta seção você pode explorar a distribuição e a relação entre as variáveis principais de saneamento 
        e saúde do ano de 2022. Utilize a barra lateral para filtrar os municípios por porte populacional e 
        ver os gráficos recalcularem dinamicamente.
        """
    )
    
    # Grid 1: Histograma e Boxplot
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Distribuição da Mortalidade Infantil")
        if not df_filtered.empty:
            fig1 = plot_mortalidade_histogram(df_filtered)
            st.pyplot(fig1)
            plt.close(fig1)
            st.caption("O histograma exibe uma distribuição com assimetria positiva, concentrada na faixa de 10 a 20 óbitos por 1.000 nascidos vivos.")
            
            # Estatísticas dinâmicas para a Mortalidade Infantil
            tmi_mean = df_filtered['taxa_mortalidade_infantil'].mean()
            tmi_median = df_filtered['taxa_mortalidade_infantil'].median()
            tmi_mode_series = df_filtered['taxa_mortalidade_infantil'].mode()
            tmi_mode = tmi_mode_series.iloc[0] if not tmi_mode_series.empty else 0.0
            tmi_var = df_filtered['taxa_mortalidade_infantil'].var()
            tmi_std = df_filtered['taxa_mortalidade_infantil'].std()
            tmi_amp = df_filtered['taxa_mortalidade_infantil'].max() - df_filtered['taxa_mortalidade_infantil'].min()
            
            st.markdown(
                f"""
                <div class="stats-box">
                    <div class="stats-header">📊 Estatísticas Descritivas (Mortalidade Infantil)</div>
                    • <strong>Média:</strong> {tmi_mean:.2f} &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Mediana:</strong> {tmi_median:.2f} &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Moda:</strong> {tmi_mode:.2f}<br>
                    • <strong>Desvio Padrão:</strong> {tmi_std:.2f} &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Variância:</strong> {tmi_var:.2f} &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Amplitude:</strong> {tmi_amp:.2f}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Sem dados disponíveis com os filtros selecionados.")
            
    with col2:
        st.markdown("#### Cobertura de Atendimento de Água")
        if not df_filtered.empty:
            fig2 = plot_agua_boxplot(df_filtered)
            st.pyplot(fig2)
            plt.close(fig2)
            st.caption("O box plot revela grande amplitude de atendimento, evidenciando municípios com níveis críticos de água potável (abaixo de 50%).")
            
            # Estatísticas dinâmicas para a Cobertura de Água
            agua_mean = df_filtered['tx_atendimento_agua'].mean()
            agua_median = df_filtered['tx_atendimento_agua'].median()
            agua_mode_series = df_filtered['tx_atendimento_agua'].mode()
            agua_mode = agua_mode_series.iloc[0] if not agua_mode_series.empty else 0.0
            agua_var = df_filtered['tx_atendimento_agua'].var()
            agua_std = df_filtered['tx_atendimento_agua'].std()
            agua_amp = df_filtered['tx_atendimento_agua'].max() - df_filtered['tx_atendimento_agua'].min()
            
            # Cálculo dos quartis (25% e 75%)
            agua_q1 = df_filtered['tx_atendimento_agua'].quantile(0.25)
            agua_q3 = df_filtered['tx_atendimento_agua'].quantile(0.75)
            
            st.markdown(
                f"""
                <div class="stats-box">
                    <div class="stats-header">💧 Estatísticas & Quartis (Cobertura de Água)</div>
                    • <strong>Média (Losango Vermelho ♦):</strong> {agua_mean:.2f}% &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Mediana (Q2 - 50%):</strong> {agua_median:.2f}%<br>
                    • <strong>Quartil 1 (Q1 - 25%):</strong> {agua_q1:.2f}% &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Quartil 3 (Q3 - 75%):</strong> {agua_q3:.2f}%<br>
                    • <strong>Desvio Padrão:</strong> {agua_std:.2f}% &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Amplitude:</strong> {agua_amp:.2f}%
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Sem dados disponíveis com os filtros selecionados.")
            
    st.markdown("---")
    
    # Grid 2: Dispersão e Heatmap
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### Relação Transversal Esgoto vs. Mortalidade")
        if not df_filtered.empty:
            fig3 = plot_esgoto_scatter(df_filtered)
            st.pyplot(fig3)
            plt.close(fig3)
            st.caption("Gráfico de dispersão mostrando a densa nuvem de municípios com 0% de coleta de esgoto pública formal e a linha de regressão correspondente.")
            
            # Estatísticas dinâmicas para a Coleta de Esgoto
            esgoto_mean = df_filtered['tx_coleta_esgoto'].mean()
            esgoto_median = df_filtered['tx_coleta_esgoto'].median()
            esgoto_mode_series = df_filtered['tx_coleta_esgoto'].mode()
            esgoto_mode = esgoto_mode_series.iloc[0] if not esgoto_mode_series.empty else 0.0
            esgoto_var = df_filtered['tx_coleta_esgoto'].var()
            esgoto_std = df_filtered['tx_coleta_esgoto'].std()
            esgoto_amp = df_filtered['tx_coleta_esgoto'].max() - df_filtered['tx_coleta_esgoto'].min()
            
            st.markdown(
                f"""
                <div class="stats-box">
                    <div class="stats-header">🚽 Estatísticas Descritivas (Coleta de Esgoto)</div>
                    • <strong>Média:</strong> {esgoto_mean:.2f}% &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Mediana:</strong> {esgoto_median:.2f}% &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Moda:</strong> {esgoto_mode:.2f}%<br>
                    • <strong>Desvio Padrão:</strong> {esgoto_std:.2f}% &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Variância:</strong> {esgoto_var:.2f} &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Amplitude:</strong> {esgoto_amp:.2f}%
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Sem dados disponíveis com os filtros selecionados.")
            
    with col4:
        st.markdown("#### Matriz de Correlação de Pearson")
        if not df_filtered.empty:
            fig4 = plot_correlation_heatmap(df_filtered)
            st.pyplot(fig4)
            plt.close(fig4)
            st.caption("A correlação de Pearson de 2022 município a município demonstra coeficientes lineares puros muito baixos (próximos a zero).")
            
            # Estatísticas dinâmicas para a Coleta de Lixo
            lixo_mean = df_filtered['tx_coleta_lixo_pop_total'].mean()
            lixo_median = df_filtered['tx_coleta_lixo_pop_total'].median()
            lixo_mode_series = df_filtered['tx_coleta_lixo_pop_total'].mode()
            lixo_mode = lixo_mode_series.iloc[0] if not lixo_mode_series.empty else 0.0
            lixo_var = df_filtered['tx_coleta_lixo_pop_total'].var()
            lixo_std = df_filtered['tx_coleta_lixo_pop_total'].std()
            lixo_amp = df_filtered['tx_coleta_lixo_pop_total'].max() - df_filtered['tx_coleta_lixo_pop_total'].min()
            
            # Correlações dinâmicas com Mortalidade Infantil
            corr_agua = df_filtered['taxa_mortalidade_infantil'].corr(df_filtered['tx_atendimento_agua'])
            corr_esgoto = df_filtered['taxa_mortalidade_infantil'].corr(df_filtered['tx_coleta_esgoto'])
            corr_lixo = df_filtered['taxa_mortalidade_infantil'].corr(df_filtered['tx_coleta_lixo_pop_total'])
            
            st.markdown(
                f"""
                <div class="stats-box">
                    <div class="stats-header">🗑️ Coleta de Lixo & Correlações com a TMI</div>
                    • <strong>Média Coleta de Lixo:</strong> {lixo_mean:.2f}% &nbsp;&nbsp;&nbsp;&nbsp;
                    • <strong>Mediana:</strong> {lixo_median:.2f}%<br>
                    • <strong>R de Pearson com a Mortalidade Infantil:</strong><br>
                    &nbsp;&nbsp;- Cobertura de Água: <strong>{corr_agua:+.4f}</strong><br>
                    &nbsp;&nbsp;- Coleta de Esgoto: <strong>{corr_esgoto:+.4f}</strong><br>
                    &nbsp;&nbsp;- Coleta de Lixo: <strong>{corr_lixo:+.4f}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Sem dados disponíveis com os filtros selecionados.")

# ==============================================================================
# MENU 4: STORYTELLING & PARADOXO
# ==============================================================================
elif menu == "💡 Storytelling & Paradoxo":
    st.markdown('<h1 class="main-title">O Paradoxo de Simpson em Saúde Pública</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">A Discrepância entre Análise Macro-Temporal e Transversal Municipal</p>', unsafe_allow_html=True)
    
    st.write(
        """
        Nesta seção apresentamos a narrativa analítica principal do projeto, evidenciando o **Paradoxo de Simpson** 
        na relação entre saneamento básico e saúde infantil.
        """
    )
    
    st.markdown("### 1. O Cenário Macro-Temporal da Bahia (2018-2023)")
    st.write(
        """
        Ao longo do tempo, o avanço da infraestrutura do estado da Bahia está associado a uma queda constante 
        e significativa da mortalidade infantil geral. A correlação de Pearson histórica é de **-0.545** para Esgoto 
        e **-0.637** para Água potável, comprovando a eficácia preventiva sistêmica.
        """
    )
    
    # Renderizar gráfico temporal
    fig_temp = plot_historical_trend(df_historico)
    st.pyplot(fig_temp)
    plt.close(fig_temp)
    
    st.markdown("---")
    st.markdown("### 2. O Paradoxo Municipal: Por que a correlação pura em 2022 é próxima a zero?")
    st.write(
        """
        Na matriz de correlação calculada para os 332 municípios em 2022, o coeficiente de Pearson para Coleta de Esgoto 
        ficou em apenas **0.074**. Essa ausência de relação linear pura ocorre por três vieses do mundo real:
        """
    )
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("##### 🚨 A. Viés de Notificação (DATASUS)")
        st.write(
            """
            Municípios muito pequenos e rurais têm baixo saneamento formal (0%), mas também sofrem com a 
            subnotificação de óbitos domiciliares de recém-nascidos. Cidades grandes, com mais hospitais e redes de saneamento, 
            registram 100% dos óbitos. Isso faz parecer estatisticamente que cidades estruturadas têm mais mortalidade.
            """
        )
    with c2:
        st.markdown("##### 🏠 B. Armadilha das Fossas Sépticas (SNIS)")
        st.write(
            """
            O SNIS mede esgotamento ligado à rede pública formal. Pequenos municípios utilizam fossas sépticas individuais 
            e sumidouros autônomos construídos pelos moradores, que oferecem proteção biológica real mas constam como 
            **0.00% de coleta de esgoto** nos relatórios do SNIS.
            """
        )
    with c3:
        st.markdown("##### 🏙️ C. Densidade Demográfica Urbana")
        st.write(
            """
            Nas metrópoles populosas, mesmo coberturas de 70% de esgoto expõem milhares de crianças a vírus em áreas 
            periféricas adensadas. A proximidade física acelera contágios muito mais rápido do que em áreas rurais isoladas 
            que possuem 0% de rede de esgoto pública.
            """
        )
        
    st.markdown("---")
    st.markdown("### 3. A Resolução do Paradoxo: Análise por Faixas de Cobertura (Bins)")
    st.write(
        """
        Para anular o ruído individual de pequenas cidades e vieses locais, os municípios foram classificados em faixas 
        de cobertura (Bins). Quando olhamos a média por grupo, o impacto real do saneamento aparece de forma incontestável: 
        cidades com maior cobertura têm menor taxa média de óbitos de crianças.
        """
    )
    
    # Gerar dados agrupados e plotar
    df_faixas = get_binned_data(df_municipal)
    fig_faixas = plot_esgoto_bins(df_faixas)
    st.pyplot(fig_faixas)
    plt.close(fig_faixas)

# ==============================================================================
# MENU 5: LGPD & RECOMENDAÇÕES
# ==============================================================================
elif menu == "⚖️ LGPD & Recomendações":
    st.markdown('<h1 class="main-title">Ética de Dados & Recomendações</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Conformidade Regulatória (LGPD) e Políticas Públicas Baseadas em Evidências</p>', unsafe_allow_html=True)
    
    st.subheader("1. Conformidade com a Lei Geral de Proteção de Dados (LGPD)")
    st.write(
        """
        O pipeline de ETL e o dashboard foram desenvolvidos respeitando de forma rigorosa as legislações vigentes 
        sobre sigilo e acesso à informação:
        
        * **Lei 13.709/2018 (LGPD - Artigos 7º e 12º):** Todos os dados do DATASUS foram consolidados de forma agrupada 
        e agregada a nível municipal e estadual. Não há exposição de nenhuma variável sensível, identificadores diretos (nomes, 
        CPFs, prontuários) ou informações que permitam a reidentificação de pacientes ou recém-nascidos.
        * **Lei 12.527/2011 (Lei de Acesso à Informação - LAI):** As fontes de dados primárias utilizadas são bases públicas, 
        abertas e auditadas pelos órgãos oficiais da administração pública direta (DATASUS/SIM/SINASC e MDR/SNIS).
        * **Mitigação de Vieses Algorítmicos:** Aplicou-se a imputação hierárquica estatística por faixas populacionais para assegurar 
        que cidades pequenas do interior baiano não fossem simplesmente excluídas da análise devido à omissão de dados do SNIS, 
        evitando viés de invisibilidade demográfica.
        """
    )
    
    st.markdown("---")
    st.subheader("2. Recomendações Governamentais Baseadas em Evidências")
    st.write(
        """
        Com base no cruzamento analítico dos dados Gold, propomos três linhas de ação prioritárias para o 
        governo do estado da Bahia e prefeituras:
        """
    )
    
    # Mostrar recomendações em cartões simples
    st.info(
        """
        **1. Concentração no Marco Legal do Saneamento:**
        Direcionar repasses orçamentários do Marco Legal prioritariamente para as macrorregiões de saúde baianas 
        que combinam as maiores taxas históricas de óbitos infantis e os menores índices de esgotamento.
        """
    )
    st.success(
        """
        **2. Linha de Financiamento de Fossas Sépticas Familiares:**
        Como a rede pública centralizada é inviável em áreas rurais dispersas de municípios pequenos (Pequeno Porte I e II), 
        o estado deve subsidiar e fiscalizar a instalação de fossas sépticas individuais seguras, conferindo imunidade 
        patológica real à população local.
        """
    )
    st.warning(
        """
        **3. Combate Ativo à Subnotificação de Saúde:**
        Capacitar equipes locais de saúde de pequenas cidades para o registro ágil e correto de nascidos vivos 
        e óbitos domiciliares rurais. Dados precisos são a chave para a formulação de qualquer política pública eficaz.
        """
    )
