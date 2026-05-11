# Guia de Planejamento: Fase 2 - EDA (Bahia)

Este documento define a estratégia de visualização e análise exploratória para a base consolidada de Saneamento e Geografia da Bahia, conforme as diretrizes do agente **EDA_Specialist**.

## 1. Objetivos da Análise
- Identificar as macrorregiões de saúde com maiores déficits de saneamento.
- Validar a correlação entre o tamanho populacional e a eficiência na coleta de resíduos.
- Detectar outliers (municípios com indicadores muito acima ou abaixo da média estadual).

---

## 2. Proposta de Visualizações (Sem Código)

### A. Visão Geral e Distribuição
1.  **Histograma do Índice de Saneamento Consolidado**:
    *   **Objetivo**: Entender a frequência dos níveis de saneamento no estado (se a maioria dos municípios é precária, média ou avançada).
    *   **Variável**: `indice_saneamento_consolidado`.

2.  **Box Plot por Macrorregião de Saúde**:
    *   **Objetivo**: Comparar a variabilidade do saneamento entre as diferentes regiões da Bahia (ex: Extremo Sul vs Norte).
    *   **Variáveis**: `macrorregiao_de_saude` (Eixo X) e `indice_saneamento_consolidado` (Eixo Y).

### B. Rankings e Comparações
3.  **Gráfico de Barras Horizontais (Top 10 Melhores/Piores)**:
    *   **Objetivo**: Destacar os municípios que são referência positiva e os que necessitam de intervenção urgente.
    *   **Variáveis**: `no_municipio` e `indice_saneamento_consolidado`.

4.  **Gráfico de Barras Agrupadas por Macrorregião**:
    *   **Objetivo**: Comparar indicadores específicos (Coleta de Lixo vs Resíduos per Capita) entre as regiões.
    *   **Variáveis**: `macrorregiao_de_saude`, `in052` (cobertura) e `in022` (massa coletada).

### C. Relações e Correlações
5.  **Gráfico de Dispersão (Scatter Plot) com Linha de Tendência**:
    *   **Objetivo**: Verificar se municípios mais populosos possuem, proporcionalmente, uma coleta de lixo mais eficiente.
    *   **Variáveis**: `populacao_ibge_2022` (Eixo X) e `in052` (Eixo Y).

6.  **Matriz de Correlação (Heatmap)**:
    *   **Objetivo**: Visualizar a força da relação entre todos os indicadores numéricos da base Gold.
    *   **Variáveis**: Todas as colunas numéricas (IN, GE e Índices).

---

## 3. Hipóteses a Validar
- **H1**: Macrorregiões com maior densidade populacional possuem índices de saneamento superiores devido à economia de escala.
- **H2**: Existe uma disparidade significativa entre o litoral e o interior da Bahia quanto à gestão de resíduos sólidos.

---

## 4. Próximos Passos
Após a aprovação deste guia, iniciaremos a **Parte 2 da Fase 2**, que consiste na implementação técnica desses gráficos utilizando Python (`Pandas`, `Matplotlib` e `Seaborn`).
