# Relatório de Análise e Sugestões do Notebook de EDA
**Arquivo Analisado:** `eda_bahia_2022.ipynb`  
**Objetivo:** Orientar a equipe de Análise Exploratória de Dados (EDA) e Storytelling sobre correções técnicas obrigatórias e melhorias visuais nas correlações.

---

## 1. Correções Técnicas Efetuadas (Compatibilidade com o ETL Gold)

O notebook original apresentava erros críticos que impediriam sua execução em um ambiente limpo (gerando falhas de *NameError* e *KeyError*). O arquivo foi atualizado com as seguintes correções:

*   **Carregamento dos Dados:** Adicionamos as linhas de carregamento utilizando `pd.read_csv("data/gold/base_consolidada.csv")` na Célula 1 e `pd.read_csv("data/gold/base_consolidada_municipal_2022.csv")` na Célula 3. O notebook original tentava ler variáveis que nunca haviam sido definidas.
*   **Ajuste de Variáveis (Rename):** As chaves de colunas antigas foram atualizadas para os novos nomes curtos da base municipal:
    *   De `tx_atendimento_total_agua` para `tx_atendimento_agua`.
    *   De `tx_cobertura_da_coleta_rdo_em_relacao_a_pop_urbana` para `tx_coleta_lixo_pop_total`.
*   **Remoção de Filtros Sentinelas (`-1`):** No pipeline de ETL atualizado, substituímos os valores `-1` por imputações estatísticas ou `NaN` (vazio real). Portanto, simplificamos o filtro da Célula 3 para usar o método nativo `.notna()` do Pandas, permitindo cálculos limpos e rápidos.

---

## 2. A Estrutura de Storytelling (Narrativa de Dados)

Sugerimos que o grupo adote a seguinte linha de raciocínio na apresentação do trabalho acadêmico. Ela demonstra maturidade analítica e destaca como o grupo resolveu problemas estatísticos clássicos:

1.  **O Cenário Geral (Série Histórica):**
    Mostre o gráfico de linhas temporal. Ele prova que, historicamente (2018-2023), o avanço do saneamento na Bahia é acompanhado por uma redução consistente na taxa de mortalidade infantil (Correlação geral de **-0.603**).
2.  **O Desafio / Paradoxo (Pearson Municipal):**
    Apresente a matriz de correlação município a município em 2022. Ela mostrará um valor próximo de zero. Lance a provocação ao público: *"Se historicamente a relação é tão forte, por que a correlação cidade a cidade parece nula?"*
3.  **A Explicação Teórica:**
    Explique a **Lei dos Pequenos Números** (pequenos municípios têm poucos óbitos e nascimentos, gerando um ruído estatístico enorme que "achata" a correlação de Pearson linear) e a **Multifatoriedade** (outras variáveis de saúde agem no curtíssimo prazo, enquanto saneamento é estrutural).
4.  **A Resolução (Agrupamento por Faixas):**
    Apresente o gráfico de barras agrupadas por faixas de cobertura. Mostre que, ao agrupar os municípios para anular o ruído individual, a tese se confirma: cidades com baixa cobertura têm mais óbitos infantis por mil nascidos do que aquelas com alta cobertura.

---

## 3. Sugestões de Novos Gráficos (Código Pronto)

Para enriquecer visualmente o dashboard ou os slides, sugerimos que a equipe de EDA inclua os seguintes gráficos no notebook:

### Sugestão A: O Gráfico de Dispersão com Regressão Linear (`sns.regplot`)
Este gráfico ilustra de forma perfeita a "nuvem de dados" (ruído) a nível municipal, provando visualmente o porquê de a correlação de Pearson linear ser fraca.

```python
# Adicionar após a Célula 3 (Matriz de Correlação)
plt.figure(figsize=(9, 5))
sns.regplot(
    data=df_municipal_filtrado, 
    x='tx_coleta_esgoto', 
    y='taxa_mortalidade_infantil', 
    scatter_kws={'alpha': 0.4, 'color': '#2b7bba'}, 
    line_kws={'color': '#e74c3c', 'linewidth': 2.5}
)
plt.title('Dispersão Municipal: Cobertura de Esgoto vs. Mortalidade Infantil\n(Note a dispersão vertical causada por ruídos em municípios pequenos)', fontsize=12, fontweight='bold')
plt.xlabel('Taxa de Coleta de Esgoto (%)', fontweight='bold')
plt.ylabel('Taxa de Mortalidade Infantil (por 1.000 nv)', fontweight='bold')
plt.tight_layout()
plt.show()
```

### Sugestão B: Visão Lado a Lado (Água, Esgoto e Lixo)
Atualmente, o notebook só analisa as faixas de esgoto. Saneamento é composto por três pilares. O código abaixo plota um gráfico 1x3 mostrando que a mesma lógica em degraus se repete para todas as coberturas.

```python
# Gerar as faixas de Água e Lixo no DataFrame
df_municipal_filtrado['faixa_agua'] = pd.qcut(
    df_municipal_filtrado['tx_atendimento_agua'], q=3, 
    labels=['Baixa Água', 'Média Água', 'Alta Água'], duplicates='drop'
)
df_municipal_filtrado['faixa_lixo'] = pd.qcut(
    df_municipal_filtrado['tx_coleta_lixo_pop_total'], q=3, 
    labels=['Baixa Lixo', 'Média Lixo', 'Alta Lixo'], duplicates='drop'
)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: Água
sns.barplot(
    data=df_municipal_filtrado.groupby('faixa_agua', observed=False)['taxa_mortalidade_infantil'].mean().reset_index(),
    x='faixa_agua', y='taxa_mortalidade_infantil', palette='Blues_r', ax=axes[0]
)
axes[0].set_title('Mortalidade por Cobertura de Água', fontweight='bold')
axes[0].set_ylabel('Mortalidade Média (por 1.000 nv)')

# Plot 2: Esgoto
sns.barplot(
    data=df_municipal_filtrado.groupby('faixa_esgoto', observed=False)['taxa_mortalidade_infantil'].mean().reset_index(),
    x='faixa_esgoto', y='taxa_mortalidade_infantil', palette='Oranges_r', ax=axes[1]
)
axes[1].set_title('Mortalidade por Cobertura de Esgoto', fontweight='bold')
axes[1].set_ylabel('')

# Plot 3: Lixo
sns.barplot(
    data=df_municipal_filtrado.groupby('faixa_lixo', observed=False)['taxa_mortalidade_infantil'].mean().reset_index(),
    x='faixa_lixo', y='taxa_mortalidade_infantil', palette='Greens_r', ax=axes[2]
)
axes[2].set_title('Mortalidade por Coleta de Lixo', fontweight='bold')
axes[2].set_ylabel('')

plt.suptitle('Taxa de Mortalidade Infantil por Faixas de Cobertura de Infraestrutura Sanitária (Bahia - 2022)', fontsize=14, fontweight='bold', y=1.05)
plt.tight_layout()
plt.show()
```

### Sugestão C: Boxplot Demográfico (Desigualdade de Cobertura por Porte da Cidade)
Provando que a cobertura de saneamento está diretamente ligada ao porte demográfico do município, justificando o porquê de termos feito a imputação de nulos baseada nas Faixas Populacionais do IBGE.

```python
plt.figure(figsize=(9, 5))
sns.boxplot(
    data=df_municipal_filtrado, 
    x='identificacao_da_faixa_populacional', 
    y='tx_coleta_esgoto', 
    palette='Blues'
)
plt.title('Desigualdade Sanitária: Cobertura de Esgoto por Porte Populacional\n(Faixas IBGE: 1 = Cidades Pequenas, 4 = Cidades Grandes)', fontsize=12, fontweight='bold')
plt.xlabel('Faixa Populacional (Município)', fontweight='bold')
plt.ylabel('Taxa de Coleta de Esgoto (%)', fontweight='bold')
plt.tight_layout()
plt.show()
```
