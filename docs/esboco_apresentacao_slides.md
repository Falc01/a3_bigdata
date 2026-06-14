# Esboço da Apresentação de Slides — Saneamento e Saúde Infantil na Bahia
**Projeto:** Análise Integrada de Saneamento Básico e Mortalidade Infantil (Bahia)  
**Disciplina:** Análise de Dados e Big Data (AV3)  
**Roteiro:** Storytelling (Macroevolução -> O Paradoxo -> A Resolução)

---

## 💻 Slide 1: Capa e Introdução
*   **Título Principal:** O Peso da Infraestrutura: Uma Análise da Mortalidade Infantil e Saneamento Básico na Bahia
*   **Subtítulo:** Integração de dados do DATASUS (SIM/SINASC) e SNIS para tomadas de decisão baseadas em evidências
*   **Design Visual Recomendado:** Fundo limpo em degradê suave (tons de azul e verde escuros), tipografia moderna (ex: Outfit ou Inter) e a identificação de todos os componentes do grupo.
*   **Objetivo do Slide:** Capturar a atenção do professor e posicionar o saneamento básico sob a ótica de saúde pública e prevenção médica de longo prazo.
*   **Roteiro de Fala (Script sugerido):**
    > *"Boa noite a todos. Vamos apresentar o projeto da nossa equipe sobre a relação entre infraestrutura de saneamento básico (abastecimento de água, coleta de lixo e esgotamento sanitário) e as taxas de mortalidade de bebês de até um ano no estado da Bahia. Nosso trabalho uniu a engenharia de dados (via pipeline ETL robusto) e a análise exploratória (EDA) para investigar cientificamente se, e como, a infraestrutura sanitária é capaz de salvar vidas."*

---

## 💻 Slide 2: O Contexto e a Escala do Estudo (Bahia)
*   **Título:** O Panorama da Saúde Infantil Baiana
*   **Design Visual Recomendado:** Três cards ou caixas destacadas em tamanho grande com os seguintes números:
    *   **950.814** Nascidos Vivos (Série Histórica 2018-2022 acumulada)
    *   **14.206** Óbitos de crianças menores de 1 ano
    *   **14,94** Taxa de mortalidade infantil média ponderada do período (por 1.000 nascidos)
*   **Objetivo do Slide:** Apresentar a escala da massa de dados analisada e justificar o uso do acumulado de 5 anos de saúde para estabilização estatística.
*   **Roteiro de Fala (Script sugerido):**
    > *"Para garantir que nossa análise fosse consistente, nós cobrimos quase 1 milhão de nascimentos na Bahia entre 2018 e 2022. Acumular e somar esse período de 5 anos foi a nossa primeira grande decisão estatística no ETL: municípios muito pequenos têm pouquíssimos nascimentos por ano e qualquer óbito isolado distorceria a taxa anual de forma injusta. Ao acumular a série de saúde em 5 anos e compará-la com o censo do SNIS 2022, conseguimos um indicador robusto e representativo para cada um dos 417 municípios baianos."*

---

## 💻 Slide 3: A Tendência Histórica (A Visão Macro)
*   **Título:** Série Histórica: O Impacto no Longo Prazo
*   **Design Visual Recomendado:** O gráfico de dois eixos (`lineplot` com `twinx` gerado na Célula 5 do notebook) demonstrando a linha azul de esgoto subindo historicamente de 2018 a 2023, enquanto a linha vermelha de mortalidade descende de forma espelhada.
*   **Objetivo do Slide:** Demonstrar a forte correlação histórica negativa a nível macro do estado da Bahia.
*   **Roteiro de Fala (Script sugerido):**
    > *"Se analisarmos o estado da Bahia de forma macro ao longo do tempo, a relação é inquestionável. À medida que a cobertura de saneamento avança, a taxa de mortalidade infantil despenca de forma sistemática. Estatisticamente, a correlação temporal histórica no estado é fortíssima e negativa: -0.603 para o índice consolidado de saneamento, -0.637 para cobertura de água e -0.545 para coleta de esgoto. Isso mostra que o avanço estrutural geral do estado traz um ganho real em vidas salvas."*

---

## 💻 Slide 4: O Paradoxo dos Dados (A Visão Micro)
*   **Título:** O "Paradoxo de Pearson" no Nível Municipal
*   **Design Visual Recomendado:** O heatmap de correlação (Célula 3) e o gráfico de dispersão (`regplot` na Célula 2) exibindo a nuvem de dados municipais de 2022 extremamente dispersa e a linha de regressão linear quase horizontal.
*   **Objetivo do Slide:** Apresentar o problema estatístico encontrado nas correlações municipais diretas (Pearson próximo de zero, ex: **0.074** para esgoto).
*   **Roteiro de Fala (Script sugerido):**
    > *"Entretanto, quando descemos para a escala dos municípios de forma estática no ano de 2022, nos deparamos com um paradoxo: a correlação linear clássica de Pearson cidade a cidade deu muito próxima de zero. O gráfico de dispersão mostra que as taxas parecem flutuar sem padrão aparente no nível local. Um analista desatento poderia concluir incorretamente que saneamento e saúde não têm relação no nível municipal. Mas nós fomos além e investigamos os motivos desse paradoxo."*

---

## 💻 Slide 5: Decifrando o Paradoxo (Viés e Densidade)
*   **Título:** Por que a correlação linear municipal parece fraca?
*   **Design Visual Recomendado:** Divisão em dois blocos comparativos:
    *   **Bloco Esquerdo — O Viés de Notificação (DATASUS):** Municípios rurais muito pequenos sofrem com subnotificação de mortes no sistema central de saúde (parecendo ter mortalidade baixa mesmo sem esgoto). Grandes centros urbanos têm registro rígido e próximo a 100% (parecendo ter mortalidade mais alta).
    *   **Bloco Direito — Fossas vs. Densidade Urbana:** Municípios pequenos usam fossas sépticas individuais (saneamento seguro e limpo, mas computado como 0% de coleta no SNIS). Áreas urbanas densas (como Salvador) têm redes de esgoto, mas a densidade das periferias propaga doenças rapidamente onde a cobertura falha.
*   **Objetivo do Slide:** Explicar cientificamente as anomalias e vieses típicos de bases de dados de saúde do governo.
*   **Roteiro de Fala (Script sugerido):**
    > *"Esse paradoxo ocorre por dois motivos práticos. O primeiro é o viés de notificação: pequenas cidades do interior muitas vezes sofrem com subnotificação de óbitos de crianças nascidas em zonas rurais distantes de hospitais, fazendo sua mortalidade parecer artificialmente baixa. O segundo é a infraestrutura: o SNIS mede 'redes de esgoto'. Pequenas cidades usam fossas sépticas, que são soluções individuais seguras mas contam como 0% de esgoto. Já nas grandes metrópoles, a altíssima densidade urbana faz com que qualquer falha de saneamento gere surtos rápidos de infecções entre as crianças."*

---

## 💻 Slide 6: A Revelação dos Dados (Agrupamento por Faixas)
*   **Título:** Eliminando o Ruído: Análise por Faixas de Cobertura
*   **Design Visual Recomendado:** O gráfico de barras por faixas (bins) de coleta de esgoto (Célula 6 do notebook), demonstrando a queda na taxa média de mortalidade infantil à medida que os grupos de municípios progridem na escala de cobertura sanitária.
*   **Objetivo do Slide:** Provar a hipótese agrupando as cidades em categorias para mitigar os ruídos estatísticos individuais.
*   **Roteiro de Fala (Script sugerido):**
    > *"Para neutralizar o ruído estatístico local das pequenas cidades, nós agrupamos as cidades em faixas de cobertura. Quando agrupamos os municípios em categorias de infraestrutura, a verdadeira relação se revela com clareza: cidades integradas em faixas de maior infraestrutura de coleta de esgoto apresentam, em média, taxas menores de óbitos de crianças de até um ano de idade. A tese estatística municipal de saneamento preventivo foi finalmente confirmada."*

---

## 💻 Slide 7: Desigualdade Sanitária e Porte das Cidades
*   **Título:** O Gargalo da Infraestrutura Sanitária
*   **Design Visual Recomendado:** O Box Plot da Célula 2 (ou um boxplot de esgoto por Faixa Populacional) demonstrando que cidades de pequeno porte (Faixas 1 e 2 do IBGE) têm a pior cobertura sanitária do estado.
*   **Objetivo do Slide:** Demonstrar que o problema de saneamento básico na Bahia é demográfico e atinge desproporcionalmente as cidades menores.
*   **Roteiro de Fala (Script sugerido):**
    > *"Notamos também que a desigualdade sanitária tem um forte componente demográfico na Bahia. Cidades menores, de faixa populacional 1 e 2 (com menos de 20 mil habitantes), sofrem sistematicamente com coberturas de esgoto e água encanada tratada muito próximas a zero. Isso guiou inclusive o nosso ETL: na nossa base consolidada municipal final de 59 colunas, realizamos imputações avançadas de nulos baseando-nos na mediana de cada Faixa Populacional do IBGE, respeitando as discrepâncias estruturais decorrentes do tamanho dos municípios."*

---

## 💻 Slide 8: Governança, Ética e LGPD
*   **Título:** Ética, Transparência e LGPD
*   **Design Visual Recomendado:** Ícones ilustrativos representando dados agregados, transparência governamental e conformidade com a LGPD.
*   **Objetivo do Slide:** Demonstrar conformidade ética e regulatória (requisito transversal de nota).
*   **Roteiro de Fala (Script sugerido):**
    > *"Garantimos total integridade e ética neste projeto. Trabalhamos exclusivamente com dados públicos de livre acesso disponibilizados por portais oficiais sob a Lei de Acesso à Informação (LAI). Mais importante: todos os dados de saúde foram consolidados e agregados por município e estado. Não há nomes, prontuários, CPFs ou quaisquer informações pessoais sensíveis no pipeline, o que mantém o projeto em total e irrestrita conformidade com a Lei Geral de Proteção de Dados (LGPD)."*

---

## 💻 Slide 9: Conclusões e Recomendações Baseadas em Dados
*   **Título:** Saneamento é Saúde Preventiva
*   **Design Visual Recomendado:** Um sumário limpo com três ícones e recomendações práticas:
    1.  **Investimento Regional Focado:** Priorizar a aplicação de recursos do marco do saneamento nas macrorregiões de saúde baianas mais críticas de mortalidade infantil.
    2.  **Subsídio para Fossas Rurais:** Criar incentivos e padronizações para fossas sépticas individuais seguras em cidades com menos de 20 mil habitantes.
    3.  **Monitoramento no Interior:** Fortalecer e treinar equipes de saúde da família para erradicar a subnotificação de óbitos e nascimentos nas áreas rurais do interior.
*   **Objetivo do Slide:** Finalizar a apresentação demonstrando como a ciência de dados apoia decisões governamentais práticas.
*   **Roteiro de Fala (Script sugerido):**
    > *"Concluímos provando que obras de saneamento são, na verdade, ferramentas de medicina preventiva. Para reduzir as mortes infantis de forma sustentável, recomendamos investimentos regionais focados, fomento de fossas rurais seguras em pequenas cidades e a erradicação de subnotificações de saúde pública. Nosso pipeline ETL e análise EDA estão prontos para guiar essas decisões baseadas em evidências reais. Muito obrigado."*
