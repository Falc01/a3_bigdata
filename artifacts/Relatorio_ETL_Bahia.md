# Relatório de ETL: Fase 1 - Saúde e Saneamento (Bahia)

Este documento resume o trabalho realizado na Fase 1 do projeto, focado na estruturação de dados reais e não redundantes para o Estado da Bahia.

## 1. Estratégia de Dados
Realizamos uma auditoria de qualidade que identificou que os arquivos RIPSA originais eram duplicatas dos dados de saneamento. Por isso, adotamos o **SNIS 2022** como fonte primária e integramos com o mapeamento oficial de saúde.

### Tabelas Ativas:
1.  **`macroregiao_de_saude.csv`**: Base de referência geográfica para Saúde.
2.  **`Planilha_Indicadores_RS_2022.xlsx`**: Dados oficiais do SNIS sobre Resíduos Sólidos.
3.  **`base_snis_geografia.csv`**: Base final consolidada (Camada Gold).

---

## 2. Metodologia (Pipeline Medalhão)

### Camada Bronze (Bruta)
Extração e organização de arquivos originais. Nada é deletado; os originais estão preservados para auditoria.

### Camada Silver (Limpeza)
Tratamento automático de cabeçalhos complexos e normalização de textos (remoção de acentos e caracteres especiais). Tipagem otimizada para performance.

### Camada Gold (Consolidação)
Cruzamento (Join) via código IBGE entre o SNIS e o Mapa de Saúde, com **recorte exclusivo para o estado da Bahia (332 municípios)**.

---

## 3. Dicionário de Dados Principal

| Coluna | Descrição | Fonte |
| :--- | :--- | :--- |
| `cod_municipio` | Código IBGE (Chave de Ligação) | Geografia |
| `no_municipio` | Nome da Cidade | Geografia |
| `macrorregiao_de_saude` | Região de Saúde (Agregador) | Geografia |
| `populacao_ibge_2022` | População Oficial 2022 | Geografia |
| `in052` | Índice de cobertura de coleta de lixo | SNIS |
| `in022` | Resíduos coletados per capita | SNIS |

---

## 4. Próximos Passos
A base está pronta para a **Fase 2 (Análise Exploratória)**. Qualquer nova fonte de saúde trazida pelo grupo poderá ser integrada facilmente usando a coluna `cod_municipio`.
