# Guia de Contribuição e Alocação da Equipe - Saneamento e Saúde BA

Este documento registra a divisão de tarefas e responsabilidades da equipe de desenvolvimento para o projeto de **Análise de Dados e Big Data** (Impacto do Saneamento na Mortalidade Infantil na Bahia).

Como este é um projeto acadêmico focado em engenharia de dados e dashboard interativo, todo o desenvolvimento de código do pipeline e da aplicação foi comitado na branch principal (`main`), mantendo a integração contínua do projeto.

---

## 📋 Alocação de Tarefas (6 Integrantes)

Abaixo está a divisão de tarefas baseada nas fases de entrega do projeto:

### 1. ⚙️ Engenharia de Dados & Pipeline ETL (Pair Programming)
*   **Foco e Responsabilidades:**
    *   Extração de 7 fontes governamentais brutas na camada `landing/` (DATASUS SIM/SINASC, SNIS RS, SNIS AE, Ministério da Saúde).
    *   Limpeza, ajuste de layouts de planilhas complexas e tratamento de encodings para UTF-8.
    *   Implementação de regras de imputação de nulos (mediana por Faixa Populacional e Estado) para eliminar valores sentinela (`-1`).
    *   Processamento e cruzamento de bases municipais via código IBGE, gerando as tabelas finais na camada Gold.
*   **Bibliotecas Utilizadas:** `pandas`, `numpy`, `pathlib`.
*   **Responsáveis:**
    *   👤 ***João Spinola Falcão***

---

### 2. 📊 Análise Exploratória (EDA) (Pair Programming)
*   **Foco e Responsabilidades:**
    *   Desenvolvimento do notebook Jupyter (`eda_bahia_2022.ipynb`).
    *   Cálculo de estatística descritiva completa (médias, medianas, desvio padrão, quartis) das variáveis principais de saúde e saneamento.
    *   Geração de histogramas, boxplots de atendimento e gráficos de dispersão transversal.
    *   Identificação de padrões, tendências históricas e matriz de correlação de Pearson.
*   **Bibliotecas Utilizadas:** `matplotlib`, `seaborn`, `pandas`, `numpy`.
*   **Responsáveis:**
    *   👤 ***Daniel***
    *   👤 ***Perrone***
    *   👤 ***Pedro Adaime Ribeiro***

---

### 3. 🖥️ Frontend & Dashboard Interativo (Individual)
*   **Foco e Responsabilidades:**
    *   Desenvolvimento do dashboard interativo de dados com Streamlit (`app.py`).
    *   Criação do menu lateral de navegação e filtros de porte municipal e saneamento em tempo real.
    *   Integração dos plots do Seaborn na aplicação e exibição dinâmica de métricas (KPIs).
    *   Estilização visual da página (Google Fonts - Inter, cartões estilizados de métrica com sombras e transições).
    *   Criação da ferramenta interativa de busca no dicionário de dados.
*   **Bibliotecas Utilizadas:** `streamlit`, `matplotlib`, `seaborn`
*   **Responsáveis:**
    *   👤 ***Aurea***

---

### 4. 💡 Storytelling, LGPD e Recomendações (Individual)
*   **Foco e Responsabilidades:**
    *   Desenho analítico e conceituação do **Paradoxo de Simpson** (macro-temporal vs. transversal municipal).
    *   Lógica de agrupamento por faixas de cobertura de esgotamento para neutralizar ruído estatístico.
    *   Redação das diretrizes éticas de conformidade com a LGPD (anonimização) e LAI.
    *   Formulação de recomendações de políticas públicas e roteiros de apresentação.
*   **Responsáveis:**
    *   👤 ***Kawan***
