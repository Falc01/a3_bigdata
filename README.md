<p align="center">
  <img src="docs/unifacs.svg" width="150" alt="UNIFACS Logo">
</p>

# UNIVERSIDADE SALVADOR — UNIFACS
## CURSO DE TECNOLOGIA DA INFORMAÇÃO / COMPUTAÇÃO
## DISCIPLINA: ANÁLISE DE DADOS E BIG DATA

<br>

---

<br>

# RELATÓRIO FINAL CONSOLIDADO: IMPACTO DA INFRAESTRUTURA DE SANEAMENTO BÁSICO NA TAXA DE MORTALIDADE INFANTIL NO ESTADO DA BAHIA

<br>

**AUTORES (EQUIPE DE DESENVOLVIMENTO):**
*   Aurea dos Reis Santos Neta (RA: 12723131562)
*   Daniel Costa Santos (RA: 1272323654)
*   João Guilherme Perrone Hohlenwerger (RA: 1272328057)
*   João Spinola Falcão (RA: 12723116406)
*   Kawan Oliveira Carneiro (RA: 12723119606)
*   Pedro Adaime Ribeiro (RA: 12723119338)

<br>

---

<br>

**PREÂMBULO:**
> Trabalho acadêmico apresentado como relatório final consolidado da atividade prática para a disciplina de Análise de Dados e Big Data do Curso de Tecnologia da Informação / Computação, sob a orientação do professor da disciplina.

<br>

**SALVADOR — BA**
**2026**

---

<br>

## 🔗 LINKS DO PROJETO

*   **Aplicação em Produção (Streamlit Cloud):**
    👉 **[https://a3bigdata.streamlit.app/](https://a3bigdata.streamlit.app/)**
*   **Repositório de Código Fonte (GitHub):**
    👉 **[https://github.com/Falc01/a3_bigdata](https://github.com/Falc01/a3_bigdata)**

---

<br>

## 1. INTRODUÇÃO E RESUMO EXECUTIVO

Este documento apresenta o relatório final integrado das fases de Engenharia de Dados (ETL), Análise Exploratória (EDA), Storytelling e Ética de Dados aplicados ao estudo da correlação entre indicadores de saneamento básico (abastecimento de água, coleta de lixo e esgotamento sanitário) e a saúde básica infantil (mortalidade de crianças menores de 1 ano) no estado da Bahia. O estudo demonstra a forte ligação macro-histórica entre a infraestrutura e a preservação de vidas e analisa as distorções estatísticas decorrentes de vieses de notificação nos municípios.

---

<br>

## 2. ENGENHARIA DE DADOS E PIPELINE ETL

O pipeline foi construído de forma modular respeitando a arquitetura de medalhão (Landing $\rightarrow$ Bronze $\rightarrow$ Silver $\rightarrow$ Gold), com foco na consistência de tipos, integridade de junções de dados e tratamento estatístico avançado de nulos.

### A. Inventário de Dados e Fontes Utilizadas (Entradas e Saídas)
O pipeline consome **7 fontes governamentais brutas** na camada `landing/`:
1.  **DATASUS (SIM):** Total acumulado de óbitos infantis por residência na Bahia (Série Estabilizada 2018-2022).
2.  **DATASUS (SINASC):** Total acumulado de nascidos vivos por residência da mãe na Bahia (2018-2022).
3.  **SNIS (Resíduos Sólidos):** Planilhas municipais de coleta de lixo do ano de 2022.
4.  **SNIS (Água e Esgoto):** Dados locais e regionais de abastecimento, esgotamento e conformidade de água de 2022.
5.  **Históricos Estaduais (SNIS):** Indicadores históricos de déficit de saneamento estaduais.
6.  **Série Histórica Nacional (MS):** Mortalidade de crianças menores de 1 ano do Ministério da Saúde para todas as UFs.

Como resultado, o pipeline gera **8 tabelas estruturadas na camada Gold** (`data/gold/`), organizadas de forma modular em duas categorias fundamentais:

*   **Tabelas Temáticas (Específicas de cada Domínio):**
    *   `base_mortalidade_municipal_2022.csv`: Dados higienizados de saúde (óbitos e nascidos vivos) por município baiano.
    *   `base_snis_agua_esgoto_2022.csv`: Cobertura municipal de água e esgoto do SNIS AE.
    *   `base_snis_geografia.csv`: Cobertura municipal de coleta de resíduos sólidos do SNIS RS com metadados geográficos.
    *   `base_mortalidade_nacional.csv` / `base_mortalidade_nacional_2022.csv`: Séries históricas de mortalidade agregadas por UF.
*   **Tabelas Consolidadas (Cruzamento Multidomínio):**
    *   `base_consolidada_municipal_2022.csv`: Base integrada final municipal unindo Saúde e Saneamento. É a base principal utilizada na análise exploratória (EDA) municipal e no dashboard Streamlit.
    *   `base_consolidada.csv` / `base_consolidada_2022.csv`: Painéis consolidados estaduais unindo a evolução histórica temporal de saneamento e saúde na Bahia.

Essa arquitetura de banco de dados modular garante que outros analistas possam consumir dados específicos de saúde ou saneamento isoladamente, enquanto a nossa análise de impacto utiliza as tabelas consolidadas pré-computadas para otimizar o tempo de resposta e evitar joins em tempo de execução.

### B. Regras de Limpeza, Junção (Merge) e Tipagem
*   **Ajuste de Layout (Header Finder):** Implementação de detecção dinâmica de cabeçalhos nos relatórios do TabNet/SNIS para ignorar linhas introdutórias de texto e notas explicativas.
*   **Unificação de Chaves Municipais:** Utilização do código do município de 6 dígitos do IBGE (`co_municipio`) como chave primária de junção (*merge*), eliminando inconsistências gráficas de acentuação e prefixos textuais (como o prefixo "BA - " presente nas bases originais do SNIS).
*   **Deduplicação de Colunas:** Exclusão sistemática de variáveis geográficas redundantes (`co_regiao_pais`, `regiao_pais`, `nome_da_regiao`, `sigla_da_regiao` e `ano_de_referencia`) nas bases municipais de Gold.

### C. Enriquecimento de Dados
*   **Cálculo da Taxa de Mortalidade Infantil (TMI):** Calculada a partir do acumulado de 5 anos (2018-2022) para neutralizar a volatilidade estatística de cidades pequenas (evitando que um óbito congênito isolado gere uma taxa artificialmente astronômica):
    $$\text{TMI} = \left(\frac{\text{obitos\_infantis}}{\text{nascidos\_vivos}}\right) \times 1000$$
*   **Conversão de Déficits em Cobertura:** Os indicadores históricos de déficits estaduais de saneamento foram convertidos em taxas diretas de cobertura ($100 - \text{deficit}$), simplificando a plotagem de tendências.
*   **Índice de Saneamento Consolidado:** Criada a variável sintética que calcula a média simples das três coberturas (água, esgoto e lixo) para análise global.

### D. Tratamento Avançado de Nulos (Zero Sentinelas)
Para preservar a integridade matemática da base municipal final, desenvolvemos um fluxo de imputação estatística livre de valores artificiais (como `-1` ou `'Não Informado'`):
1.  **Exclusão (Drop):** Remoção de 15 colunas operacionais que vieram 100% nulas no estado da Bahia.
2.  **Imputação por Faixa Populacional:** Para dados numéricos nulos do SNIS, aplicou-se a mediana do grupo da mesma Faixa Populacional do município (com base nos grupos de porte demográfico do IBGE).
3.  **Fallback por Mediana Estadual:** Caso o grupo demográfico inteiro fosse nulo, aplicou-se a mediana geral do estado.
4.  **Vazio Real (NaN):** Registros residuais que persistam sem dados de imputação são mantidos como `NaN` para que o Pandas os ignore nativamente em cálculos estatísticos (como `.mean()` e `.corr()`).

---

<br>

## 3. ANÁLISE EXPLORATÓRIA DE DADOS (EDA)

A análise exploratória foi realizada por meio do notebook `eda_bahia_2022.ipynb` carregando diretamente as bases Gold.

### A. Estatística Descritiva das Variáveis Principais (Censo 2022)
Abaixo estão sumarizadas as métricas gerais calculadas a nível de município na Bahia (332 municípios unificados):
*   **Taxa de Mortalidade Infantil (TMI):** Média de **15,19** óbitos por 1.000 nascidos vivos, com desvio padrão de **5,64** e mediana de **14,58**.
*   **Abastecimento de Água (`tx_atendimento_agua`):** Média de **69,38%** de cobertura, com mediana de **70,12%**.
*   **Coleta de Esgoto (`tx_coleta_esgoto`):** Média de **17,54%** de cobertura, com mediana de **0,00%** (indicando um forte gargalo estrutural).
*   **Coleta de Lixo (`tx_coleta_lixo_pop_total`):** Média de **75,19%** de cobertura, com mediana de **76,14%**.

### B. Visualizações de Distribuição e Dispersão
*   **Histograma de Mortalidade:** Demonstra uma distribuição aproximadamente normal inclinada à direita (assimetria positiva), concentrada na faixa de 10 a 20 óbitos por 1.000 nascidos vivos, com outliers de alta mortalidade em municípios pequenos.
*   **Box Plot de Água:** Apresenta grande amplitude interquartil, com o primeiro quartil na casa de 50% e cauda inferior longa, demonstrando que há um grupo significativo de municípios baianos com baixíssimo abastecimento de água potável.
*   **Gráfico de Dispersão (Esgoto vs. Mortalidade):** Revela uma densa nuvem de pontos concentrada no eixo de 0% de coleta de esgoto com eixos verticais de dispersão de mortalidade flutuando de 0 a 30 por mil, provando a ausência de uma relação linear pura simples no nível de municípios individuais.

---

<br>

## 4. O PARADOXO DA CORRELAÇÃO MUNICIPAL (STORYTELLING)

Um dos achados mais significativos do projeto é a discrepância entre a análise temporal macro e a análise transversal municipal de correlação, conhecido como o **Paradoxo de Simpson** adaptado a dados de saúde pública:

### A. O Fenômeno Macro-Temporal (Bahia)
Ao analisarmos a série histórica agregada da Bahia (2018-2023), há uma correlação linear negativa **fortíssima** entre saneamento e mortalidade:
*   Correlação Geral (Índice de Saneamento Consolidado): **-0.603**
*   Correlação Cobertura de Água: **-0.637**
*   Correlação Coleta de Lixo: **-0.627**
*   Correlação Esgotamento Sanitário: **-0.545**

Isso comprova que, com o passar dos anos, o avanço sistêmico da infraestrutura e o desenvolvimento geral do estado estão fortemente vinculados à queda da mortalidade de bebês.

### B. O Paradoxo Municipal (Pearson Próximo a Zero)
Quando calculamos a matriz de correlação linear (Pearson) município a município em 2022, os coeficientes ficam próximos de zero (ex: esgoto com **0.074**). O estudo decifrou que esse paradoxo ocorre devido a três fatores do mundo real:
1.  **O Viés de Notificação do DATASUS:** Cidades pequenas e isoladas do interior (que têm 0% de coleta de esgoto) frequentemente sofrem com subnotificação de óbitos infantis em áreas rurais distantes. Já os grandes centros (com alta cobertura de esgoto) concentram nascimentos e óbitos em hospitais sob fiscalização estrita, gerando notificações próximas a 100%. Isso cria a ilusão estatística de que as cidades com saneamento têm mortalidade mais alta.
2.  **A Armadilha das Fossas Sépticas no SNIS:** O SNIS registra "coleta de esgoto por rede pública". Pequenas cidades rurais usam fossas sépticas individuais seguras (0% de rede no SNIS, mas com proteção sanitária real). 
3.  **Densidade Demográfica Urbana:** Grandes cidades possuem áreas periféricas populosas. Mesmo com alta cobertura geral de esgoto, pequenos gargalos de esgoto a céu aberto em áreas com altíssima densidade urbana espalham vírus e infecções de forma muito mais rápida do que em áreas rurais isoladas.

### C. A Resolução do Paradoxo: Agrupamento em Faixas (Bins)
Para neutralizar o ruído estatístico individual das pequenas cidades, os municípios foram agrupados em faixas de cobertura. O agrupamento demonstrou de forma límpida que a mortalidade média das faixas mais estruturadas de esgotamento sanitário é significativamente menor que as faixas sem infraestrutura, comprovando cientificamente a tese preventiva de saneamento.

---

<br>

## 5. RECOMENDAÇÕES GOVERNAMENTAIS BASEADAS EM EVIDÊNCIAS

Com base nos dados estruturados da camada Gold e análises exploratórias, recomendamos três intervenções práticas de política pública:
1.  **Priorização Macrorregional:** Concentrar recursos federais e estaduais do Marco Legal do Saneamento Básico nas macrorregiões de saúde baianas identificadas com as maiores taxas de TMI.
2.  **Subsídio a Fossas Rurais:** Desenvolver programas de financiamento público para construção e manutenção de fossas sépticas individuais seguras nos municípios de pequeno porte (Faixas 1 e 2 do IBGE - menos de 20 mil habitantes).
3.  **Combate à Subnotificação:** Treinar agentes comunitários de saúde no interior do estado para monitorar e registrar adequadamente nascimentos e óbitos rurais, aprimorando a base de governança do DATASUS.

---

<br>

## 6. ÉTICA E GOVERNANÇA DE DADOS (LGPD)

O projeto seguiu rígidos padrões éticos regulatórios:
*   **Anonimização Estrita:** Todos os dados individuais foram anonimizados. O pipeline atua exclusivamente sobre somas agrupadas de nascimentos e óbitos a nível de município e estado, respeitando integralmente os artigos 7º e 12º da Lei Geral de Proteção de Dados (LGPD - Lei 13.709/2018).
*   **Acesso à Informação:** As fontes consultadas são dados governamentais abertos tutelados pela Lei de Acesso à Informação (LAI - Lei 12.527/2011), garantindo a transparência e legalidade do estudo.
*   **Mitigação de Vieses:** O pipeline tratou os vieses demográficos de omissão do SNIS por meio da imputação por Faixa Populacional, garantindo representatividade estatística sem exclusão de populações vulneráveis de cidades pequenas da Bahia.

---

<br>

## REFERÊNCIAS BIBLIOGRÁFICAS

*   BRASIL. **Lei Geral de Proteção de Dados Pessoais (LGPD)**. Lei nº 13.709, de 14 de agosto de 2018. Dispõe sobre o tratamento de dados pessoais.
*   BRASIL. **Lei de Acesso à Informação (LAI)**. Lei nº 12.527, de 18 de novembro de 2011. Regula o direito constitucional de acesso às informações públicas.
*   BRASIL. Ministério da Saúde. Departamento de Informática do SUS (DATASUS). **Sistema de Informações sobre Mortalidade (SIM)**. Disponível em: <http://datasus.saude.gov.br/>. Acesso em: jun. 2026.
*   BRASIL. Ministério da Saúde. Departamento de Informática do SUS (DATASUS). **Sistema de Informações sobre Nascidos Vivos (SINASC)**. Disponível em: <http://datasus.saude.gov.br/>. Acesso em: jun. 2026.
*   BRASIL. Ministério do Desenvolvimento Regional. **Sistema Nacional de Informações sobre Saneamento (SNIS)**. Disponível em: <http://www.snis.gov.br/>. Acesso em: jun. 2026.
*   INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Censo Demográfico 2022**. Disponível em: <https://www.ibge.gov.br/>. Acesso em: jun. 2026.
