# Documentação do Processo de ETL e Métricas (Bahia 2022)

Este documento descreve detalhadamente a engenharia de dados aplicada na integração dos dados de saúde e saneamento para o estado da Bahia no ano de **2022**, abrangendo a origem dos dados brutos, as regras de transformação aplicadas e a qualidade/métricas dos datasets resultantes.

---

## 1. Origem dos Dados (Extract / Ingestão)

Os dados de entrada provêm de duas fontes principais da saúde pública e saneamento do governo brasileiro, localizados na camada `data/landing/`:

1.  **SIM (Sistema de Informações sobre Mortalidade - Datasus):**
    *   **Arquivo:** `sim_cnv_inf10ba180535179_105_131_169.csv`
    *   **Extração:** Extraído via TabNet. Contém contagens de óbitos infantis (menores de 1 ano) segregados por município de residência na Bahia.
    *   **Filtros de Origem:** Estado: Bahia; Ano de Referência: 2022; Categoria: Óbitos por residência.
2.  **SINASC (Sistema de Informações sobre Nascidos Vivos - Datasus):**
    *   **Arquivo:** `sinasc_cnv_nvba180642179_105_131_169.csv`
    *   **Extração:** Extraído via TabNet. Contém o total de nascimentos por município de residência na Bahia.
    *   **Filtros de Origem:** Estado: Bahia; Ano de Referência: 2022.
3.  **SNIS (Sistema Nacional de Informações sobre Saneamento):**
    *   **Arquivo:** `Planilha_RS_2022_atualizado_29112024.zip`
    *   **Extração:** Fornecido pela Secretaria Nacional de Saneamento. Contém planilhas Excel detalhando os indicadores de Resíduos Sólidos Urbanos (RS) preenchidos por prestadores de serviços de manejo.
    *   **Filtros de Origem:** Recorte para o estado da Bahia executado em pipeline.

---

## 2. Regras de Negócio e Transformações (Transform)

O fluxo de processamento foi desenhado para limpar, padronizar e cruzar os temas utilizando chaves geo-espaciais consistentes:

```
[Landing SIM/SINASC] ──> [Limpeza & Separação IBGE] ──> [Merge & Cálculo de Taxa] ──> Mortalidade Gold
[Landing SNIS RS]    ──> [Limpeza & Filtro Bahia]    ──> [Merge Geografia Saúde] ──> SNIS Geografia Gold
                                                                                         │
                                         [Merge Municipal por co_municipio] <────────────┘
                                                         │
                                                         ▼
                                          Consolidado Municipal Gold
```

### 2.1. Higienização de Cabeçalhos e Rodapés
*   As linhas de notas de rodapé descritivas geradas automaticamente pelo TabNet são excluídas.
*   Registros contendo `"Total"` ou `"MUNICIPIO IGNORADO"` são removidos para evitar duplicidade ou poluição estatística.

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
*   A chave comum de acoplamento é o código IBGE de 6 dígitos (`co_municipio`). O nome redundante do SNIS (que continha o prefixo `"BA - "`) é descartado para manter a padronização simplificada.

---

## 3. Estrutura de Arquivos da Camada Gold

Os dados processados e homologados pelo checklist estão salvos no diretório `data/gold/`:

*   **`base_mortalidade_municipal_2022.csv`:** Taxas brutas de mortalidade infantil para os 417 municípios baianos.
*   **`base_snis_geografia.csv`:** Indicadores de saneamento (manejo de resíduos sólidos) e informações da geografia da saúde (regiões e macrorregiões) para 332 municípios.
*   **`base_consolidada_municipal_2022.csv`:** Cruzamento completo de Saneamento + Saúde para 332 municípios baianos.

---

## 4. Métricas e Auditoria de Qualidade dos Dados (Load)

De acordo com o analisador de métricas analíticas de ETL (`analisar_metricas_etl.py`), os indicadores de qualidade do processo são:

### 4.1. Taxas de Retenção e Pareamento
*   **Retenção de Saúde:** **100%**. Todos os 417 municípios oficiais do estado da Bahia foram preservados no cálculo de mortalidade infantil.
*   **Pareamento SNIS (Match Rate):** **79,62%** (332 de 417 municípios). Os 85 municípios restantes não preencheram a declaração anual do SNIS RS em 2022, sendo desconsiderados no consolidado final por falta de registros de saneamento.

### 4.2. Qualidade dos Dados (Valores Nulos)
*   **Mortalidade Municipal:** **0,00% de nulos**.
*   **SNIS Geografia:** **45,41% de nulos**. Esse valor elevado é comum no SNIS devido ao não preenchimento de campos facultativos específicos (como custos de capina e varrição) pelas prefeituras.
*   **Consolidado Municipal:** **42,22% de nulos** (herdados da base SNIS).

### 4.3. Sanidade Epidemiológica (Óbitos vs Nascimentos)
A auditoria identificou **5 municípios** em que o número de óbitos é maior que o de nascidos vivos (Nascidos = 0, Óbitos > 0):
*   *Municípios:* **Almadina, Buerarema, Glória, Santa Brígida, Sítio do Quinto**.
*   *Explicação:* Casos comuns em municípios pequenos onde as gestantes realizam o parto em hospitais regionais de outras cidades (gerando registro de nascimento fora do município), mas a criança falece no município de residência declarado (gerando registro de óbito local).

### 4.4. Resultados Estatísticos e Correlações (Bahia 2022)
*   **Total de Nascidos Vivos no Estado:** 171.246
*   **Total de Óbitos Infantis no Estado:** 2.531
*   **Taxa Geral de Mortalidade do Estado:** **14,78 óbitos** por 1.000 nascidos vivos.
*   **Correlação de Pearson (Cobertura Coleta de Lixo vs Taxa Mortalidade):** **0.1257**. Indica uma correlação linear fraca e positiva no nível municipal, sinalizando que a mortalidade é influenciada de forma multifatorial (não apenas por resíduos sólidos de forma direta).

---

## 5. Scripts de Verificação e Validação

O repositório conta com uma suite de testes na pasta `scripts/verificacoes/` para garantir a manutenção da integridade dos dados:

*   `validar_base.py`: Gera sumário estatístico e matriz de correlação das variáveis.
*   `check_consistency.py`: Verifica se existem registros órfãos ou inconsistências temporais (anos fora de 2022).
*   `check_snis_year.py`: Audita colunas de ano de forma isolada usando expressões regulares para evitar falsos positivos.
*   `compare_totals.py`: Compara as somas de nascidos/óbitos das tabelas consolidadas contra dados globais do Excel de controle.
*   `read_docx.py`: Valida a leitura de metadados textuais da pasta de documentação técnica.
*   `verificar_checklist.py`: Validador oficial de deploy que impede a gravação de arquivos com estados ou anos incorretos, permitindo que tabelas sem coluna temporal (design DRY) passem na validação baseadas no escopo.
*   `analisar_metricas_etl.py`: Executa a auditoria de nulos, sanidade matemática e taxas de retenção descritas na seção 4.
