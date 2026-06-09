# Documentação do Processo de ETL e Métricas (Bahia 2022)

Este documento descreve detalhadamente a engenharia de dados aplicada na integração dos dados de saúde e saneamento para o estado da Bahia no ano de **2022**, abrangendo a origem dos dados brutos, as regras de transformação aplicadas e a qualidade/métricas dos datasets resultantes## 1. Origem dos Dados (Extract / Ingestão)

Os dados de entrada provêm de três fontes da saúde pública e saneamento do governo brasileiro, localizados na camada `data/landing/`:

1.  **SIM (Sistema de Informações sobre Mortalidade - Datasus):**
    *   **Arquivo:** `sim_cnv_obt10ba135205187_107_8_217.csv`
    *   **Extração:** Extraído via TabNet. Contém contagens de óbitos infantis (menores de 1 ano) segregados por município de **residência** da mãe na Bahia.
    *   **Filtros de Origem:** Estado: Bahia; Ano de Referência: 2022; Categoria: Óbitos por residência.
2.  **SINASC (Sistema de Informações sobre Nascidos Vivos - Datasus):**
    *   **Arquivo:** `sinasc_cnv_nvba135328187_107_8_217.csv`
    *   **Extração:** Extraído via TabNet. Contém o total de nascimentos por município de **residência** da mãe na Bahia.
    *   **Filtros de Origem:** Estado: Bahia; Ano de Referência: 2022.
3.  **SNIS (Sistema Nacional de Informações sobre Saneamento):**
    *   **Arquivo RS:** `Planilha_RS_2022_atualizado_29112024.zip` (Resíduos Sólidos/Lixo).
    *   **Arquivo AE:** `DIAGNOSTICO_TEMATICO_VISAO_GERAL_AE_SNIS_2023_ATUALIZADO.zip` (Contém as planilhas locais e regionais como `Planilha_AE_Indicadores_EMBASA-29274000.xls` de Água e Esgoto).

---

## 2. Regras de Negócio e Transformações (Transform)

O fluxo de processamento foi desenhado para limpar, padronizar e cruzar os temas utilizando chaves geo-espaciais consistentes:

```
[Landing SIM/SINASC] ──> [Limpeza & Separação IBGE] ──> [Merge & Cálculo de Taxa] ──> Mortalidade Gold ──┐
[Landing SNIS RS]    ──> [Limpeza & Filtro Bahia]    ──> [Merge Geografia Saúde] ──> SNIS Geografia Gold ├─> Consolidado Municipal Gold
[Landing SNIS AE]    ──> [Unificação LPU/LPR Bahia]  ──> [Deduplicação & Cast]   ──> SNIS Água & Esgoto ─┘
```

### 2.1. Higienização de Cabeçalhos e Rodapés
*   As linhas de notas de rodapé descritivas geradas automaticamente pelo TabNet são excluídas.
*   Registros contendo `"Total"` ou `"MUNICIPIO IGNORADO"` são removidos para evitar duplicidade ou poluição estatística.
*   Identificação de cabeçalhos de forma dinâmica verificando a presença de `'Munic'` e do caractere `;`.

### 2.2. Separação de Códigos e Nomes de Municípios
*   O TabNet unifica o código e o nome do município em uma única string (ex: `"290010 ABAIRA"`).
*   Utilizando expressões regulares em Python, a string é fracionada em:
    *   `co_municipio`: Código IBGE de 6 dígitos (chave primária de merge).
    *   `no_municipio`: Nome limpo do município (ex: `ABAIRA`).

### 2.3. Cálculo da Taxa de Mortalidade Infantil
*   A taxa municipal de mortalidade infantil é calculada pela fórmula clássica:
    $$Taxa = \left( \frac{\text{Óbitos Infantis}}{\text{Nascidos Vivos}} \right) \times 1000$$
*   Caso o município apresente 0 nascidos vivos no ano (maternidades indisponíveis localmente), a taxa é forçada para `0.0` para evitar divisões por zero.

### 2.4. Unificação Temática (Saúde + Saneamento)
*   O script `consolidar_base_municipal.py` realiza um `inner join` entre os indicadores de mortalidade e saneamento a nível municipal.
*   A chave comum de acoplamento foi corrigida no join para `['co_municipio', 'co_uf', 'sg_uf']`, eliminando colunas redundantes do Pandas com sufixos `_x` e `_y`. O nome redundante do SNIS (que continha o prefixo `"BA - "`) é descartado para manter a padronização simplificada.

---

## 3. Estrutura de Arquivos da Camada Gold

Os dados processados e homologados pelo checklist estão salvos no diretório `data/gold/`:

*   **`base_mortalidade_municipal_2022.csv`:** Taxas brutas de mortalidade infantil por residência para os 417 municípios baianos.
*   **`base_snis_geografia.csv`:** Indicadores de saneamento (resíduos sólidos) e informações da geografia da saúde para 332 municípios.
*   **`base_snis_agua_esgoto_2022.csv`:** Indicadores de atendimento total e urbano de água/esgoto, volume de esgoto tratado e índices de conformidade de coliformes na água para 405 municípios da Bahia.
*   **`base_consolidada_municipal_2022.csv`:** Cruzamento completo de Saneamento (Lixo) + Saúde para 332 municípios baianos.

---

## 4. Métricas e Auditoria de Qualidade dos Dados (Load)

De acordo com o analisador de qualidade de ETL (`analisar_metricas_etl.py`), os indicadores finais de qualidade do processo são:

### 4.1. Taxas de Retenção e Pareamento
*   **Retenção de Saúde:** **100%**. Todos os 417 municípios oficiais do estado da Bahia foram preservados no cálculo de mortalidade infantil.
*   **Pareamento SNIS Lixo (Match Rate):** **79,62%** (332 de 417 municípios). Os 85 municípios restantes não preencheram a declaração de Resíduos Sólidos do SNIS em 2022.
*   **Pareamento SNIS Água/Esgoto (Match Rate):** **97,12%** (405 de 417 municípios). Excelente representatividade estadual obtida combinando prestadores locais e regionais (EMBASA).

### 4.2. Qualidade dos Dados (Valores Nulos)
*   **Mortalidade Municipal:** **0,00% de nulos**.
*   **SNIS Geografia:** **45,41% de nulos**. Esse valor elevado é comum no SNIS devido ao não preenchimento de campos de custos facultativos pelas prefeituras.
*   **Consolidado Municipal:** **42,82% de nulos** (herdados da base SNIS).

### 4.3. Sanidade Epidemiológica (Óbitos vs Nascimentos)
*   **Anomalias de Saúde:** **0 anomalias detectadas**. 
*   **Explicação:** A migração de dados de ocorrência para dados de residência eliminou por completo as anomalias conceituais anteriores (onde nascidos eram 0, mas óbitos eram > 0 devido a partos em hospitais regionais de fora).

### 4.4. Resultados Estatísticos e Correlações (Bahia 2022)
*   **Total de Nascidos Vivos no Estado:** 173.821
*   **Total de Óbitos Infantis no Estado:** 2.661
*   **Taxa Geral de Mortalidade do Estado:** **15,31 óbitos** por 1.000 nascidos vivos.
*   **Correlação de Pearson (Cobertura Coleta de Lixo vs Taxa Mortalidade):** **0.0551**. Indica uma correlação linear fraca no nível municipal, o que motiva o uso da nova tabela de Água e Esgoto (onde a correlação com esgoto tratado/água potável é estatisticamente mais relevante).

---

## 5. Scripts de Verificação e Validação

O repositório conta com uma suite de testes na pasta `scripts/verificacoes/` para garantir a manutenção da integridade dos dados:

*   `validar_base.py`: Gera sumário estatístico e matriz de correlação das variáveis.
*   `check_consistency.py`: Verifica se existem registros órfãos ou inconsistências temporais.
*   `check_snis_year.py`: Audita colunas de ano de forma isolada usando expressões regulares para evitar falsos positivos.
*   `compare_totals.py`: Compara as somas de nascidos/óbitos das tabelas consolidadas contra dados globais.
*   `verificar_checklist.py`: Validador oficial de deploy que impede a gravação de arquivos com estados ou anos incorretos, reordenando colunas para que `co_uf` seja lido de forma segura.
*   `analisar_metricas_etl.py`: Executa a auditoria de nulos, sanidade matemática e taxas de retenção descritas na seção 4.

