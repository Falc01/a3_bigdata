# Guia de Análise Exploratória e Dicionário de Dados (EDA)
**Arquivo de Referência:** `data/gold/base_consolidada_municipal_2022.csv`  
**Escopo:** Municípios da Bahia (Série Acumulada de Saúde 2018-2022 + SNIS 2022)  

Este guia foi elaborado para orientar o grupo na Análise Exploratória de Dados (EDA) e no desenvolvimento do *storytelling*, mapeando os principais campos do arquivo municipal consolidado da Bahia, as hipóteses de correlação e as observações mais relevantes para a investigação.

---

## 1. Dicionário de Variáveis Chave

Para guiar a análise entre as 79 colunas unificadas das bases de saúde e saneamento, utilize as variáveis abaixo como foco principal:

### 1.1. Identificadores e Regionalização
*   `no_municipio` *(Texto)*: Nome oficial do município baiano (ex: "Salvador", "Feira de Santana").
*   `co_municipio` *(Numérico)*: Código identificador oficial do município de 6 dígitos do IBGE.
*   `populacao_ibge_2022` *(Numérico)*: População total obtida no Censo Demográfico do IBGE de 2022.
*   `regiao_saude` *(Texto)*: Região de Saúde à qual o município pertence administrativamente.
*   `macrorregiao_saude` *(Texto)*: Macrorregião de Saúde do município.

### 1.2. Indicadores de Saúde Infantil (DATASUS - 2018 a 2022 Acumulado)
*   `nascidos_vivos` *(Numérico)*: Total acumulado de bebês nascidos vivos no período de 5 anos.
*   `obitos_infantis` *(Numérico)*: Total acumulado de óbitos de crianças com menos de 1 ano de idade no período.
*   `taxa_mortalidade_infantil` *(Numérico)*: Taxa média de mortalidade infantil calculada sobre o acumulado de 5 anos:
    $$\text{taxa\_mortalidade} = \left(\frac{\text{obitos\_infantis}}{\text{nascidos\_vivos}}\right) \times 1000$$

### 1.3. Saneamento: Coleta de Lixo (SNIS Resíduos Sólidos - 2022)
*   `tx_coleta_lixo_pop_total` *(Numérico)*: Cobertura de coleta de lixo doméstico em relação à população total do município (%).
*   `auto_suficiencia_financeira` *(Numérico)*: Índice de autossuficiência financeira dos serviços públicos de manejo de resíduos (%).
*   `tx_terceirizacao_coleta` *(Numérico)*: Grau de terceirização do serviço de coleta de resíduos (%).
*   `massa_lixo_per_capita` *(Numérico)*: Quantidade de lixo doméstico gerada por habitante atendido (kg/hab/ano).

### 1.4. Saneamento: Água e Esgoto (SNIS AE - 2022)
*   `tx_atendimento_agua` *(Numérico)*: Porcentagem da população total do município abastecida com água tratada encanada.
*   `tx_coleta_esgoto` *(Numérico)*: Porcentagem da população total do município atendida por rede de coleta de esgoto doméstico.
*   `tx_tratamento_esgoto` *(Numérico)*: Índice de tratamento de esgoto doméstico coletado (%).
*   `consumo_per_capita_agua` *(Numérico)*: Consumo médio de água tratada por habitante (Litros/habitante/dia).
*   `idx_conformidade_coliformes` *(Numérico)*: Índice de conformidade da qualidade da água quanto à presença de coliformes totais (indicador biológico de contaminação bacteriana).
*   `prestador_servico_ae` *(Texto)*: Prestador principal de abastecimento e esgotamento sanitário (ex: EMBASA, SAAE).

---

## 2. Possíveis Correlações e Hipóteses de Estudo

A equipe de EDA deve testar as seguintes correlações fundamentadas na saúde pública:

*   **Abastecimento de Água vs. Mortalidade Infantil:** Espera-se uma correlação negativa. Municípios com menor atendimento de água encanada tratada (`tx_atendimento_agua`) tendem a apresentar maior mortalidade infantil por conta da ingestão de água contaminada e da proliferação de doenças diarreicas agudas.
*   **Esgotamento Sanitário vs. Mortalidade Infantil:** A ausência de redes de coleta (`tx_coleta_esgoto`) expõe a população infantil ao esgoto a céu aberto, aumentando os casos de infecções parasitárias e gastroenterites. O grupo deve investigar se o esgotamento é um gargalo de saúde pública mais acentuado na Bahia do que o abastecimento de água.
*   **Coleta de Lixo vs. Mortalidade Infantil:** O acúmulo inadequado de resíduos sólidos propicia a proliferação de vetores de doenças (roedores e insetos). Espera-se que municípios com baixas taxas de coleta de lixo (`tx_coleta_lixo_pop_total`) tenham piores índices de saúde básica infantil.
*   **Índice de Qualidade da Água vs. Mortalidade:** Verificar se desvios na conformidade biológica da água tratada (`idx_conformidade_coliformes`) têm impacto direto na taxa de óbitos de crianças por infecções intestinais.

---

## 3. Observações Relevantes e Cruzamentos Recomendados

*   **Estabilidade Estatística (Recorte de 5 Anos):** A taxa de mortalidade municipal foi calculada agregando os nascimentos e óbitos de **2018 a 2022**. Cidades pequenas possuem poucas ocorrências por ano, o que faria um óbito pontual distorcer a taxa anual. A agregação de 5 anos estabiliza o indicador e reflete melhor a realidade de longo prazo de cada município no momento do censo de 2022.
*   **Desigualdade Regional (Macrorregiões de Saúde):** A Bahia apresenta realidades socioeconômicas muito distintas entre o Recôncavo, o Sertão e o Extremo Sul. Recomendamos cruzar e agrupar as taxas por `macrorregiao_saude` para identificar gargalos geográficos onde os investimentos em infraestrutura sanitária são mais urgentes.
*   **Tipos de Prestadores de Serviço:** O grupo pode analisar o impacto do modelo de gestão de água e esgoto agrupando os dados por `prestador_servico_ae`. É possível comparar o desempenho de municípios atendidos pela estatal estadual **EMBASA** com aqueles geridos por SAAEs municipais autônomos ou prestadores privados em termos de taxas de atendimento e reflexo na mortalidade.
*   **Tratamento de Dados Ausentes (Nulos e Imputação):** O dataset final municipal foi tratado no ETL para ter **zero valores nulos (NaN)**. O grupo deve estar ciente de que:
    *   **Colunas Deletadas:** 15 colunas operacionais que estavam 100% nulas na Bahia foram removidas (otimizando a base de 79 para 59 colunas).
    *   **Imputação por Faixa Populacional:** Colunas operacionais com nulos tiveram seus valores ausentes preenchidos com a **mediana da respectiva Faixa Populacional** do município.
    *   **Fallback por Mediana Estadual:** Caso o grupo populacional inteiro não possua dados, utilizou-se a mediana estadual para garantir o preenchimento, e qualquer caso residual seria mantido como `NaN` (vazio real) para evitar distorções matemáticas de valores sentinela (como `-1`).

