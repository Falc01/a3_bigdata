# Relatório de ETL: Integração de Saúde, Saneamento e Mortalidade (Bahia 2022)

Este documento resume o trabalho realizado para estruturação e engenharia de dados do projeto de Consistência de Dados (Big Data), com foco estrito no estado da Bahia para o ano de **2022**. 

## 1. Estratégia de Dados e Escopo
Após auditorias de qualidade na Fase 1, o escopo foi expandido na Fase 2 para contemplar os dados reais de **Mortalidade Infantil**. O foco do projeto foi mantido em 2022, necessitando filtragens e cruzamentos nas novas fontes.

> [!NOTE]
> **Decisão de Arquitetura (Omissão do Ano):**
> Como o objetivo principal do projeto é a apresentação focada exclusivamente no ano de 2022, todas as colunas redundantes que marcavam o ano estaticamente (`ano` nas tabelas de mortalidade e `ano_de_referência` no SNIS) foram **excluídas** da camada Gold.
> Isso foi feito para despoluir a visualização e simplificar as tabelas (DRY - *Don't Repeat Yourself*). A única exceção é a `base_consolidada_2022.csv`, que manteve as marcações de mês/competência (`co_anomes`, `dt_competencia`), pois o fator mensal pode ser relevante para eventuais análises ou construções de histogramas temporais.

### Arquitetura de Tabelas Ativas (Camada Gold):
1.  **`base_consolidada_municipal_2022.csv`**: Cruzamento final municipal de Saúde + Geografia + Saneamento de Resíduos Sólidos (332 municípios).
2.  **`base_mortalidade_municipal_2022.csv`**: Taxa de Mortalidade Infantil real calculada por residência para todos os 417 municípios da Bahia.
3.  **`base_snis_agua_esgoto_2022.csv`**: Indicadores completos de cobertura de água, esgoto, tratamento e qualidade de água para 405 municípios da Bahia.
4.  **`base_snis_geografia.csv`**: Indicadores de resíduos sólidos (lixo) acoplados à geografia da saúde (332 municípios).
5.  **`base_consolidada_2022.csv`**: Indicadores consolidados estaduais de saneamento e saúde para a Bahia (1 linha).
6.  **`base_mortalidade_nacional_2022.csv`**: Taxa de mortalidade infantil estadual consolidada para a Bahia (1 linha).

---

## 2. Metodologia (Pipeline Medalhão)

O fluxo segue a arquitetura Medallion (Bronze/Silver/Gold) e foi enriquecido com a documentação do projeto integrado **MGDI**.

### Camada Bronze / Landing (Dados Brutos)
- Extração de relatórios de Residência do TabNet (Datasus): `SIM` (Óbitos por residência) e `SINASC` (Nascidos vivos por residência da mãe).
- Ingestão da base histórica nacional `mgdi_ms_k5p.csv` (Série temporal 2000-2023).
- Ingestão das planilhas municipais e de provedores (como EMBASA) de Água e Esgoto do SNIS 2022.

### Camada Silver (Limpeza e Transformação)
- Limpeza dos cabeçalhos textuais dos relatórios do TabNet com busca dinâmica.
- Separação dos códigos IBGE (ex: `"290010 ABAIRA"` → `290010` e `ABAIRA`).
- Tipagem garantida com conversão de marcadores como `-` para `0` ou `NaN`.

### Camada Gold (Consolidação e Regras de Negócio)
- **Cálculo da Taxa de Mortalidade**: Em ambos os cruzamentos (municipal e nacional), a taxa foi gerada programaticamente no pipeline usando a fórmula:
  $$Taxa = \left( \frac{\text{Óbitos Infantis}}{\text{Nascidos Vivos}} \right) \times 1000$$
- **Isolamento Temporal:** Filtro estrito de `Ano == 2022` aplicado a todas as bases originais antes da omissão da coluna para garantir consistência estrutural.

---

## 3. Especificações Técnicas (Integração MGDI)

Conforme a documentação oficial da equipe (`documentacao_etl_mgdi.pdf`), o dataset Nacional segue as seguintes especificações incorporadas ao nosso projeto:

*   **Foco de Negócio:** Indicadores de Saúde Pública (Mortalidade Infantil por UF).
*   **Dicionário de Entrada:**
    *   `Numerador`: Óbitos infantis estimados (menores de 1 ano).
    *   `Denominador`: Nascidos vivos estimados.
    *   `Fator`: Constante estática de 1000.
    *   `Indicador`: Estático (MRT.1.01).

---

## 4. Dicionário de Dados Principal (Gold)

| Coluna | Descrição | Fonte |
| :--- | :--- | :--- |
| `co_municipio` / `co_uf` | Código IBGE Numérico (Chaves Primárias de Relacionamento) | Geografia/SIM/SINASC/SNIS |
| `sg_uf` | Sigla da Unidade Federativa (ex: BA) | Geografia/Consolidada/SNIS |
| `populacao_ibge_2022` | População Oficial 2022 | Geografia (SNIS Lixo) |
| `nascidos_vivos` | Total de nascidos vivos registrados no município/UF | SINASC (Residência) / MGDI |
| `obitos_infantis` | Total de óbitos em menores de 1 ano registrados | SIM (Residência) / MGDI |
| `taxa_mortalidade_infantil` | Cálculo: (Óbitos / Nascidos) * 1000 | ETL Programático |
| `tx_cobertura_agua` | Taxa de cobertura de água encanada no município (consolidado) | SNIS |
| `tx_cobertura_lixo` | Taxa de cobertura de coleta de lixo no município (consolidado) | SNIS |
| `tx_cobertura_esgoto` | Taxa de cobertura de rede de esgoto no município (consolidado) | SNIS |
| `tx_causas_mal_definidas` | Antiga métrica de saúde genérica (Proporção Causas Mal Definidas) | RIPSA |
| `indice_saneamento_consolidado`| Média aritmética da cobertura de Água, Lixo e Esgoto | Consolidado |
| `no_prestador_servico_ae` | Nome do prestador local/regional de Água e Esgoto (ex: EMBASA) | SNIS Água/Esgoto |
| `tx_atendimento_total_agua` | Índice de atendimento total de água do prestador (%) | SNIS Água/Esgoto |
| `tx_atendimento_urbano_agua` | Índice de atendimento urbano de água do prestador (%) | SNIS Água/Esgoto |
| `tx_atendimento_total_esgoto`| Índice de atendimento total de esgoto referido aos at. com água (%) | SNIS Água/Esgoto |
| `tx_atendimento_urbano_esgoto`| Índice de atendimento urbano de esgoto referido aos at. com água (%) | SNIS Água/Esgoto |
| `tx_coleta_esgoto` | Índice de coleta de esgoto (%) | SNIS Água/Esgoto |
| `tx_tratamento_esgoto` | Índice de tratamento de esgoto (%) | SNIS Água/Esgoto |
| `consumo_per_capita_agua` | Consumo médio per Capita de água (L/hab/dia) | SNIS Água/Esgoto |
| `idx_conformidade_coliformes` | Índice de conformidade da qualidade da água - Coliformes Totais (%) | SNIS Água/Esgoto |

---

## 5. Próximos Passos
1.  **Dashboard e EDA:** As tabelas estão em seu estado final (Gold), higienizadas, despoluídas temporalmente, e prontas para uso em painéis (Streamlit, PowerBI) e rotinas de Análise Exploratória (Machine Learning / Correlações).
