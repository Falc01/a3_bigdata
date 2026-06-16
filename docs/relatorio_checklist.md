# Relatório de Conformidade e Auditoria do Checklist A3
**Projeto:** Análise Integrada de Saneamento Básico e Mortalidade Infantil (Bahia)  
**Referência:** `CHECKLIST_A3_Análise_de_Dados.html`  
**Data:** 14 de Junho de 2026

Este relatório faz uma auditoria detalhada de cada item exigido no checklist oficial da avaliação A3 e atesta se as nossas bases, scripts de ETL e o notebook de EDA estão em conformidade com as regras de pontuação do professor.

---

## 1. Fase 1: Relatório ETL e Qualidade de Dados (16 Pontos / 40% da Nota)

| Item do Checklist | Status | Onde está implementado / Como atende |
| :--- | :---: | :--- |
| **1. Extração:** fontes de dados coletadas (APIs, CSVs, SQL/NoSQL) | **Concluído** | 7 bases coletadas de origens governamentais em `data/landing/` (DATASUS SIM/SINASC, SNIS RS, SNIS AE, séries históricas de déficit e mortalidade nacional). |
| **2. Documentação de Extração:** fontes escolhidas e métodos de extração | **Concluído** | Detalhado na Seção 1 ("Inventário de Dados") e Seção 2 ("Processamento do Pipeline") do [RELATORIO_ETL.md](file:///c:/Users/joaof/Downloads/Unifacs/analise_dados_big_data/a3/dataset/documentos/RELATORIO_ETL.md). |
| **3. Transformação:** limpeza, tratamento de nulos e padronização | **Concluído** | Implementado no pipeline. Limpeza de layout e rodapés (`processar_dados.py`), imputação de nulos por Faixa Populacional e Estado sem valores sentinela (`consolidar_base_municipal.py`) e normalização em `padronizar_gold.py`. |
| **4. Variáveis Analíticas:** enriquecimento e criação de novas variáveis | **Concluído** | Criadas: `taxa_mortalidade_infantil` (taxa de 5 anos acumulados por 1.000 nv), coberturas de água/lixo/esgoto ($100 - deficit$), `indice_saneamento_consolidado` e coluna temporal explicita `ano`. |
| **5. Documentação de Transformação:** justificativas matemáticas/epidemiológicas | **Concluído** | Justificado detalhadamente nas Seções 3 e 4 do [RELATORIO_ETL.md](file:///c:/Users/joaof/Downloads/Unifacs/analise_dados_big_data/a3/dataset/documentos/RELATORIO_ETL.md) (como a estabilização de taxas e exclusão de redundâncias). |
| **6. Carga:** dados estruturados para consumo em ferramentas analíticas | **Concluído** | Estruturação de 8 arquivos limpos, normalizados e consistentes salvos no formato CSV em `data/gold/`. |
| **7. Documentação de Carga:** processos de carga e armazenamento | **Concluído** | Detalhado nas Seções 1.2, 2 e 5 do [RELATORIO_ETL.md](file:///c:/Users/joaof/Downloads/Unifacs/analise_dados_big_data/a3/dataset/documentos/RELATORIO_ETL.md). |
| **8. Qualidade e Integridade:** garantia de integridade da base final | **Concluído** | Desenvolvida uma suite de qualidade automatizada na pasta `scripts/verificacoes/` (como `verificar_checklist.py` e `analisar_metricas_etl.py`) atuando como um *quality gate*. |

---

## 2. Fase 2: Análise Exploratória e Dashboard Interativo (12 Pontos / 30% da Nota)

### 2.1. Análise Exploratória (EDA)
| Item do Checklist | Status | Onde está implementado / Como atende |
| :--- | :---: | :--- |
| **9. Estatística Descritiva:** cálculo de médias, medianas, quartis e desvio padrão | **Concluído** | A Célula 1 do notebook `eda_bahia_2022.ipynb` executa o método `.describe().T` nas variáveis principais de saúde e saneamento, gerando todas as estatísticas. |
| **10. Visualizações Iniciais:** histogramas, box plots e gráficos de dispersão | **Concluído** | A Célula 2 do notebook gera um painel 1x3 com o Histograma da mortalidade infantil, Box Plot da cobertura de água e Gráfico de Dispersão (Scatter Plot) de Esgoto vs. Mortalidade. |
| **11. Padrões e Correlações:** identificação de padrões, tendências e correlações | **Concluído** | A Célula 3 calcula a matriz de correlação de Pearson; a Célula 5 plota a tendência temporal de Saneamento vs. Mortalidade; e a Célula 6 plota a queda de mortalidade por faixas (bins). |
| **12. Documentação de Padrões:** explicação de como foram obtidos | **Concluído** | Explicado nas notas textuais e comentários do notebook de EDA e nas Seções 2 e 3 do [DICIONARIO_DE_DADOS.md](file:///c:/Users/joaof/Downloads/Unifacs/analise_dados_big_data/a3/dataset/documentos/DICIONARIO_DE_DADOS.md). |

### 2.2. Dashboard Interativo
*   **Item 13 (Dashboard produzido):** *Concluído.* A estrutura do Streamlit está implementada em `app.py` na pasta do repositório, sob responsabilidade do integrante do grupo focado no frontend.
*   **Item 14 (Insights destacados) e Item 15 (Navegação intuitiva):** *Em andamento.* Focado na interface do Streamlit.

---

## 3. Fase 3: Apresentação Final - Storytelling (12 Pontos / 30% da Nota)

*   **Item 16 (Narrativa lógica - Storytelling):** *Concluído.* A narrativa lógica conectando o cenário estadual macro, o "paradoxo da correlação linear municipal" e a resolução por agrupamento em faixas está documentada em [analise_e_sugestoes_eda.md](file:///c:/Users/joaof/Downloads/Unifacs/analise_dados_big_data/a3/dataset/docs/analise_e_sugestoes_eda.md).
*   **Itens 17, 18 e 19 (Material visual, Recomendações e Domínio):** *A cargo da equipe.* A apresentação visual e o domínio do tema serão avaliados pela banca na data da apresentação (17/06/2026).

---

## 4. Ética e Governança de Dados (Requisito Transversal)

Para garantir nota máxima nos requisitos éticos da avaliação, documentamos a conformidade regulatória do projeto:

### 4.1. Anonimização e LGPD (Lei 13.709/2018)
*   **Conformidade:** O projeto utiliza estritamente dados públicos e de livre acesso obtidos de portais governamentais oficiais (DATASUS/MS e SNIS/MDR), em conformidade com a Lei de Acesso à Informação (LAI - Lei 12.527/2011).
*   **Anonimização:** Todos os dados de óbitos e nascimentos foram consolidados de forma **agregada por município**. Não há qualquer dado pessoal identificável (como nomes, CPFs, datas exatas de nascimento ou endereços dos pacientes), respeitando integralmente o Artigo 7º e 12º da LGPD.

### 4.2. Vieses Algorítmicos e Limitações dos Dados
*   **Viés de Notificação (SNIS):** Municípios muito pequenos podem apresentar falhas ou atrasos na declaração de dados de resíduos e esgotamento. Em 2022, 85 municípios da Bahia não responderam à declaração de resíduos sólidos do SNIS. Nosso pipeline mitigou esse viés através da **imputação estatística demográfica por Faixa Populacional**, evitando a exclusão dessas cidades da análise.
*   **Viés da Lei dos Pequenos Números:** Em cidades pequenas, 1 óbito aleatório distorce a taxa anual de mortalidade. Mitigamos esse viés agregando a série histórica de saúde em 5 anos (2018-2022), o que estabiliza o indicador e permite análises de correlação municipal estatisticamente válidas.

### 4.3. Impacto Social dos Resultados
*   Os resultados deste estudo servem como subsídio científico para a tomada de decisões de políticas públicas. A identificação de macrorregiões de saúde com baixíssima cobertura sanitária e alta mortalidade infantil direciona os investimentos de infraestrutura para as áreas mais vulneráveis, visando a redução de desigualdades regionais e a salvaguarda de vidas humanas.
