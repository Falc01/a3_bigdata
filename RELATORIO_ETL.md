# Relatório Técnico de Engenharia de Dados: Pipeline ETL
**Projeto:** Análise Integrada de Saneamento Básico e Mortalidade Infantil (Bahia)  
**Disciplina:** Análise de Dados e Big Data (AV3)  

Este relatório detalha a arquitetura, as transformações e as decisões de engenharia adotadas na construção do pipeline de dados de saneamento e saúde para a avaliação AV3. O pipeline segue a arquitetura de camadas (Medalhão) e foi projetado para gerar bases estáveis e livres de ruídos estatísticos a nível municipal e estadual.

---

## 1. Inventário de Dados (Origem e Destino)

O pipeline lê **7 arquivos brutos** de origens governamentais na camada `data/landing/` e gera **8 arquivos limpos** na camada `data/gold/`.

### 1.1. Bases de Entrada (Landing/Bronze)
| Arquivo | Origem | Descrição | Justificativa de Uso |
| :--- | :--- | :--- | :--- |
| `sim_cnv_inf10ba131422187_107_8_217.csv` | DATASUS (TabNet) | Soma de óbitos infantis por residência na Bahia (2018-2022). | Indicador direto de mortalidade infantil acumulada para 5 anos. |
| `sinasc_cnv_nvba131418187_107_8_217.csv` | DATASUS (TabNet) | Soma de nascidos vivos por residência da mãe na Bahia (2018-2022). | Denominador epidemiológico para o cálculo estável da taxa de mortalidade. |
| `Planilha_RS_2022_atualizado_29112024.zip` | SNIS (2022) | Planilhas brutas de Resíduos Sólidos (coleta de lixo). | Dados de infraestrutura de limpeza urbana nos municípios. |
| `DIAGNOSTICO_TEMATICO_VISAO_GERAL_AE_SNIS_2023_ATUALIZADO.zip` | SNIS (2022) | Planilhas de prestadores de Água e Esgoto (Jacobina, Salvador, EMBASA). | Dados de infraestrutura e cobertura de abastecimento de água e coleta de esgoto. |
| `proporcao_agua.csv` / `proporcao_lixo.csv` / `proporcao_sanitaria.csv` | SNIS (Histórico) | Indicadores de déficit de saneamento a nível de estado. | Análise temporal histórica comparativa das UFs. |
| `mgdi_ms_k5p.csv` | Min. Saúde | Série histórica nacional de mortalidade infantil (UFs). | Histórico de saúde a nível de estados para cruzamento nacional. |

### 1.2. Bases de Saída (Gold - `data/gold/`)
| Arquivo | Descrição |
| :--- | :--- |
| `base_consolidada_municipal_2022.csv` | **Base final municipal da Bahia.** Une dados de mortalidade (2018-2022), coleta de lixo (SNIS RS), água e esgotamento sanitário (SNIS AE). |
| `base_snis_agua_esgoto_2022.csv` | Dados consolidados de água, esgoto e conformidade da água da Bahia por município. |
| `base_snis_geografia.csv` | Mapeamento geográfico regionalizado do SNIS Resíduos Sólidos. |
| `base_mortalidade_municipal_2022.csv` | Dados limpos e taxa de mortalidade infantil por município baiano (série agregada). |
| `base_consolidada.csv` | Painel de dados históricos de todas as UFs (estados) brasileiras (2016-2023). |
| `base_consolidada_2022.csv` | Recorte do painel de estados restrito ao ano de 2022 (Bahia). |
| `base_mortalidade_nacional.csv` | Série nacional de mortalidade por UF (2000-2023) limpa. |
| `base_mortalidade_nacional_2022.csv` | Recorte de 2022 da mortalidade nacional por UF. |

---

## 2. Processamento do Pipeline de ETL (Etapa por Etapa)

O fluxo de dados é orquestrado de forma modular, respeitando a separação física por camadas:

```
[Landing] -> extrair_dados.py -> [Bronze] -> processar_dados.py -> [Silver] -> consolidar/padronizar -> [Gold]
```

### Passo 1: Extração e Deduplicação (`extrair_dados.py`)
*   **Ação:** Cria a camada `data/bronze/` a partir dos arquivos brutos. Descompacta todos os arquivos `.zip` recursivamente de forma idempotente e copia arquivos XLSX/CSV.
*   **Regra de Deduplicação:** Se houver um arquivo XLSX e um CSV com o mesmo nome na origem, o script **prioriza o arquivo Excel (.xlsx)** e descarta o CSV bruto correspondente para economizar espaço e evitar duplicações no pipeline.

### Passo 2: Limpeza de Saneamento Silver (`processar_dados.py`)
*   **Ação:** Limpa os dados estaduais do SNIS salvando na camada `data/silver/`.
*   **Tratamentos:**
    *   Executa o algoritmo `fix_excel_layout` para remover rodapés textuais e marcas d'água de arquivos governamentais.
    *   Remove linhas onde a coluna de valor do indicador (`vl_indicador_calculado_uf`) seja nula.

### Passo 3: Processamento de Saúde Municipal (`processar_sim_sinasc.py`)
*   **Ação:** Une as tabelas brutas de nascidos e óbitos da Bahia em `base_mortalidade_municipal_2022.csv`.
*   **Cálculo da Taxa:** 
    $$\text{taxa\_mortalidade\_infantil} = \left(\frac{\text{obitos\_infantis}}{\text{nascidos\_vivos}}\right) \times 1000$$
*   **Tratamento de Anomalias:** Valores ausentes (*NaN*) de óbitos em municípios pequenos são preenchidos com `0`. Cidades que possuem zero nascimentos ativos recebem taxa `0` de mortalidade (evitando divisão por zero).

### Passo 4: Cruzamento Geográfico Municipal (`consolidar_snis_geografia.py`)
*   **Ação:** Carrega o mapeamento de saúde (`macroregiao_de_saude_clean.csv`) e realiza o join interno (*inner merge*) com o SNIS de Resíduos Sólidos 2022 por meio do código do município do IBGE. Filtra o resultado apenas para o estado da Bahia (`sg_uf == 'BA'`).

### Passo 5: Consolidação de Água e Esgoto (`consolidar_snis_agua_esgoto.py`)
*   **Ação:** Consolida as planilhas locais e regionais das prestadoras baianas ( Salvador, Jacobina, EMBASA) em `base_snis_agua_esgoto_2022.csv`.
*   **Agrupamento:** Como municípios podem possuir mais de um prestador cadastrado no SNIS, o script agrupa os dados por `co_municipio`, extraindo os valores máximos de cobertura e o primeiro nome do prestador do serviço de água.

### Passo 6: Consolidação Final Municipal (`consolidar_base_municipal.py`)
*   **Ação:** Une os dados de saúde do DATASUS com os dados de lixo (SNIS RS) e água/esgoto (SNIS AE), gerando a base consolidada final municipal.

### Passos 7 e 8: Integração Nacional e Estadual (`integrar_base_historica.py` e `consolidar_base.py`)
*   **Ação:** Constrói os painéis nacionais de estados agregando a série histórica do Ministério da Saúde (`mgdi_ms_k5p.csv`) com os indicadores de saneamento estaduais.

### Passo 9: Normalização de Nomes (`padronizar_gold.py`)
*   **Ação:** Padroniza a nomenclatura de todas as tabelas Gold para um formato limpo, sem caracteres especiais e em minúsculas (padrão *snake_case*).

---

## 3. Mapeamento de Colunas (Alterações, Exclusões e Justificativas)

Todas as alterações estruturais nas tabelas foram justificadas matematicamente ou epidemiologicamente.

### 3.1. Colunas Adicionadas (Calculadas)
| Tabela Gold | Coluna Criada | Fórmula / Regra | Justificativa Técnica/Epidemiológica |
| :--- | :--- | :--- | :--- |
| `base_mortalidade_municipal_2022.csv` | `taxa_mortalidade_infantil` | `(obitos_infantis / nascidos_vivos) * 1000` | Cria o indicador padrão de mortalidade infantil. O uso do acumulado de 5 anos (2018-2022) remove o ruído estatístico de municípios muito pequenos (evitando que 1 óbito aleatório crie uma taxa astronômica). |
| `base_consolidada.csv` | `tx_cobertura_agua` | `100 - deficit_agua` | Transforma o indicador original de **déficit** (falta de acesso) em cobertura de atendimento, facilitando a interpretação direta no gráfico. |
| `base_consolidada.csv` | `tx_cobertura_lixo` | `100 - deficit_lixo` | Transforma o indicador de déficit de resíduos sólidos em índice de cobertura de coleta de lixo. |
| `base_consolidada.csv` | `tx_cobertura_esgoto` | `100 - deficit_esgoto` | Transforma o déficit de esgotamento sanitário em cobertura de esgoto. |
| `base_consolidada.csv` | `indice_saneamento_consolidado` | `(agua + lixo + esgoto) / 3` | Cria uma métrica consolidada de saneamento geral por estado para análise global de regressão. |

### 3.2. Colunas Removidas (Deduplicação de Joins)
| Tabela Gold | Coluna Removida | Justificativa da Remoção |
| :--- | :--- | :--- |
| `base_snis_geografia.csv` | `uf_x`, `uf_y` | Removidas por redundância. A sigla de UF é mantida unicamente na coluna padronizada `sg_uf`. |
| `base_snis_geografia.csv` | `codigo_do_ibge`, `codigo_do_municipio` | Removidas por redundância. O código identificador numérico oficial de 6 ou 7 dígitos do IBGE é unificado em `co_municipio`. |
| `base_snis_geografia.csv` | `municipio` | Removida para evitar inconsistências gráficas de acentuação. Mantém-se o nome oficial limpo obtido do DATASUS na coluna `no_municipio`. |

---

## 4. Alterações de Layout, Limpeza e Codificação

Para garantir a robustez e impedir falhas de execução em diferentes sistemas operacionais (como Windows e Linux), adotou-se:

1.  **Deteção Dinâmica de Linha de Cabeçalho:**
    *   *O que foi feito:* Arquivos gerados pelo TabNet ou SNIS possuem de 3 a 8 linhas introdutórias de texto explicativo. O pipeline lê dinamicamente o início do arquivo e define como cabeçalho apenas a primeira linha que contenha a palavra chave `'Munic'` e o delimitador `;` (para CSV) ou `'Código do Município'` (para Excel).
    *   *Justificativa:* Evita que o código quebre caso os portais governamentais adicionem ou removam linhas explicativas no topo das planilhas.
2.  **Conversão de Delimitadores e Nulos Epidemiológicos:**
    *   *O que foi feito:* Substituição de caracteres de preenchimento de nulos textuais do TabNet (como o caractere `-`) por `0`. Substituição do separador decimal `,` por `.` antes de realizar o cast de tipo.
    *   *Justificativa:* Permite a correta tipagem numérica da coluna de floats para cálculos matemáticos do Pandas.
3.  **Encoding Robusto (Latin1 vs. UTF-8):**
    *   *O que foi feito:* Uso do encoding `latin1` como fallback na leitura dos arquivos brutos do DATASUS e salvamento de todas as tabelas Gold estritamente em `utf-8`.
    *   *Justificativa:* Previne a quebra do pipeline devido a caracteres acentuados típicos da língua portuguesa em nomes de cidades (ex: "América Dourada", "Abraão").
4.  **Correção do Layout SIM (Classes vs. Total):**
    *   *O que foi feito:* Caso o download do TabNet do SIM traga colunas separadas por outras classes, o script detecta e utiliza apenas a coluna `'Total'` para a taxa municipal de óbitos infantis.
    *   *Justificativa:* Impede a atribuição errônea dos óbitos de uma única cidade (como Alagoinhas) a todos os outros municípios da planilha.

---

## 5. Resultados e Homologação Final do Pipeline

Após a execução do pipeline de ETL, os dados gerados revelam as seguintes estatísticas estruturadas:

*   **Taxa de Pareamento Geográfico (Match Rate):** **79.62%** (332 de 417 municípios da Bahia). A diferença de 19% representa municípios pequenos que não preencheram o SNIS em 2022.
*   **Estatística Consolidada da Bahia (Série 2018-2022 Acumulada):**
    *   Total de Nascidos Vivos: **950.814**
    *   Total de Óbitos Infantils (<1 ano): **14.206**
    *   Taxa de Mortalidade Geral do Estado: **14.94** óbitos por 1.000 nascidos vivos.
*   **Auditoria de Qualidade (Quality Gate):** Todos os 8 arquivos gerados na pasta Gold foram aprovados pelo script `verificar_checklist.py`.

### Correlações de Impacto (Nível Estadual)
A relação estatística entre a cobertura de saneamento básico e a queda da mortalidade infantil é nítida e negativa (quanto maior a cobertura sanitária, menor a taxa de mortalidade):
*   Correlação Geral (Índice de Saneamento): **-0.414**
*   Correlação Esgotamento Sanitário: **-0.402**
*   Correlação Coleta de Lixo: **-0.365**
*   Correlação Abastecimento de Água: **-0.330**
