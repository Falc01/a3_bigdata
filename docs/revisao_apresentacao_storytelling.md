# Revisão Técnica da Apresentação e Storytelling (A3)

Este documento centraliza as revisões técnicas necessárias para os slides e para o roteiro de apresentação do projeto, corrigindo erros estatísticos e alinhando os textos com os dados reais consolidados na camada Gold.

---

## 1. Resumo das Correções Críticas

### 1.1. Substituição do Termo: "Paradoxo de Simpson" (Slide 4)
*   **Erro:** O roteiro e os slides citavam o *"Paradoxo de Pearson"*.
*   **Correção:** Modificado para **"Paradoxo de Simpson"**. Pearson é o autor do coeficiente de correlação linear usado, enquanto o paradoxo estatístico do desaparecimento da correlação ao mudar de escala (macro para micro) chama-se cientificamente Paradoxo de Simpson.

### 1.2. Correção do Número de Municípios Analisados (Slide 2 e 7)
*   **Erro:** O slide citava *"cada um dos 417 municípios baianos"*.
*   **Correção:** Alterado para **"332 dos 417 municípios"** (com 79,62% de pareamento no Censo 2022). O pipeline de ETL filtrou os municípios que não responderam ao censo do SNIS em 2022. Declarar 417 cidades geraria contradição direta com o banco de dados entregue.

### 1.3. Justificativa do Apagão de Dados / Pandemia (Slide 3)
*   **Melhoria:** Adicionada explicação no roteiro justificando por que os anos de 2020 e 2021 foram omitidos da série temporal histórica (blackout de dados do SNIS gerado pela pandemia de COVID-19).

---

## 2. Roteiro Corrigido para os Slides (Pronto para Uso)

### Slide 1: Abertura
> "Hoje vamos apresentar o projeto 'O Peso da Infraestrutura: Uma análise da mortalidade infantil e saneamento básico na Bahia'. Este trabalho propõe uma jornada através da engenharia de Big Data para responder a uma pergunta fundamental: o quanto a nossa infraestrutura sanitária pesa na sobrevivência das nossas crianças?"

### Slide 2: O Panorama da Saúde Infantil Baiana
> "Para entendermos o cenário, precisamos olhar para o mundo como ele é. Imagine o maior estado do Nordeste. A Bahia registrou uma série histórica acumulada recente de quase 1 milhão de nascimentos — exatamente 950.814 nascidos vivos. Junto a isso, enfrentamos uma tragédia silenciosa: 14.206 crianças que não sobreviveram ao primeiro ano de vida. Isso nos dá uma taxa média ponderada de 14,94 óbitos por mil nascidos. Mas o que está por trás desses números? O grande conflito é que esses dados de saúde pública e infraestrutura vivem isolados em silos como o DATASUS e o SNIS. Cada um fala uma língua diferente, criando uma invisibilidade das conexões. Em nosso projeto, a engenharia de dados conseguiu parear e consolidar as informações de **332 municípios baianos (79,62% de cobertura)** que declararam seus dados no Censo 2022, lançando luz sobre essas conexões."

### Slide 3: Série Histórica: O Impacto no Longo Prazo
> "Para resolver essa dor, construímos um pipeline de dados baseado na arquitetura Medalhão. Ingerimos 7 fontes governamentais brutas, limpamos cabeçalhos confusos e corrigimos codificações de cidades do interior. Uma das nossas principais decisões técnicas foi aplicar o princípio DRY: eliminamos todas as colunas redundantes de anos na camada Gold para despoluir as tabelas, como a duplicada 'ano_de_referencia'. E quando analisamos essa série histórica a nível macro ao longo do tempo (2018-2023), os dados falaram por si. **Omitindo os anos de 2020 e 2021 devido ao apagão de dados do SNIS gerado pela pandemia**, a correlação histórica é fortíssima e negativa: -0.603 para o índice de saneamento e -0.637 para cobertura de água. Fica matematicamente claro: à medida que a infraestrutura avança, a mortalidade infantil despenca no estado."

### Slide 4: O "Paradoxo de Simpson" no Nível Municipal
> "No entanto, o verdadeiro desafio de Big Data apareceu quando descemos a análise para a escala dos municípios de forma estática em 2022. Nós nos deparamos com o **'Paradoxo de Simpson'**: a correlação linear clássica de Pearson cidade a cidade deu muito próxima de zero, marcando apenas 0.074 para esgoto. Olhando para este gráfico de dispersão, um analista desatento cometeria o erro grave de concluir que saneamento e mortalidade não possuem relação no nível local. Mas nossa engenharia de dados nos permitiu ir além para investigar o que esse ruído estava escondendo."

### Slide 5: Por que a correlação linear municipal parece fraca?
> "Descobrimos que esse paradoxo ocorre por dois motivos práticos. O primeiro é o viés de notificação: pequenas cidades do interior sofrem com registros incompletos de óbitos porque as crianças nascem e morrem em zonas rurais distantes dos hospitais. O segundo é que o SNIS mede apenas 'redes de esgoto' coletivas públicas. Pequenas cidades usam fossas sépticas, que são soluções individuais perfeitamente seguras, mas que entravam no sistema computadas como 0% de esgoto. Já nas grandes metrópoles, a altíssima densidade urbana faz com que qualquer falha de saneamento gere surtos rápidos de infecções entre as crianças."

### Slide 6: Eliminando o Ruído: Análise por Faixas de Cobertura
> "Para neutralizar esse ruído estatístico das pequenas cidades, nossa camada Gold aplicou uma abordagem corrigida: agrupamos os municípios em faixas de cobertura de esgoto. Quando estruturamos os dados dessa forma, a verdadeira relação finalmente se revela com clareza: cidades integradas nas faixas de maior infraestrutura de coleta apresentam taxas significativamente menores de óbitos. A tese estatística municipal de saneamento preventivo foi finalmente confirmada."

### Slide 7: O Gargalo da Infraestrutura Sanitária
> "Essa consolidação expôs o verdadeiro gargalo demográfico da infraestrutura sanitária na Bahia. São justamente as cidades menores, de faixa populacional 1 e 2, com menos de 20 mil habitantes, as que mais sofrem com a falta crônica de rede de esgoto e água tratada. Para garantir a consistência técnica da nossa base final, realizamos imputações avançadas de nulos baseando-nos na mediana de cada Faixa Populacional do IBGE, respeitando essas discrepâncias estruturais."

### Slide 8: Ética, Transparência e LGPD
> "Como estamos lidando com dados sensíveis de saúde pública, a governança foi prioridade. Garantimos total integridade e ética trabalhando exclusivamente com dados públicos anonimizados obtidos via Lei de Acesso à Informação. O pipeline opera apenas com dados consolidados e agregados por município e estado. Não existem nomes, prontuários ou CPFs nas tabelas, mantendo o projeto em irrestrita conformidade com a LGPD."

### Slide 9: Conclusão: Saneamento é Saúde Preventiva
> "Para concluir, este projeto de Big Data prova definitivamente que obras de saneamento são ferramentas de medicina preventiva de alto impacto. Nossas bases Gold estão perfeitamente higienizadas e prontas para alimentar dashboards e modelos preditivos. Mas o pipeline não é o fim: ele é o meio para guiar decisões reais. Recomendamos investimentos focados nas macrorregiões mais críticas, subsídios para fossas rurais seguras em cidades pequenas e o fortalecimento das equipes de saúde da família para erradicar a subnotificação. Os dados estão prontos, limpos e estruturados. Agora, eles devem ser usados para salvar vidas na Bahia. Muito obrigado."
