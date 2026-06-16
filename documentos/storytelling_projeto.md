# Storytelling do Projeto - Saneamento e Mortalidade Infantil na Bahia

Este documento apresenta a análise de storytelling detalhada desenvolvida para o projeto **"O Peso da Infraestrutura: Uma análise da mortalidade infantil e saneamento básico na Bahia"** da disciplina de **Análise de Dados e Big Data**.

---

## 1. O Cenário e a Problemática Institucional

O projeto investiga a interconexão entre as condições sanitárias estruturais e os indicadores de saúde pública no maior estado da Região Nordeste. A relevância da pesquisa ganha contornos críticos ao observar-se que, no recorte temporal analisado, a Bahia registrou um volume expressivo de **950.814 nascidos vivos** acumulados. Paralelamente a esse contingente, o estado computou a perda de **14.206 crianças** que não sobreviveram ao primeiro ano de vida, estabelecendo uma taxa média ponderada de mortalidade infantil de **14,94 óbitos** a cada mil nascidos vivos.

Historicamente, o principal obstáculo para a formulação de diagnósticos precisos nessa área reside na fragmentação e no ruído das bases de dados governamentais. Enquanto o DATASUS custodia os registros vitais de natalidade e mortalidade por meio dos sistemas SIM e SINASC, os indicadores de infraestrutura sanitária são geridos de forma independente pelo Sistema Nacional de Informações sobre Saneamento (SNIS), além de autarquias locais como a EMBASA. Essa desconexão estrutural entre os ecossistemas de informação impunha uma barreira técnica que invisibilizava as correlações locais, relegando gestores públicos e pesquisadores a tomarem decisões estratégicas sob cenários de assimetria de informação.

---

## 2. Arquitetura de Dados e Estratégia de Ingestão (Pipeline Medalhão)

Com o objetivo de mitigar a dispersão dos dados e unificar as fontes em um repositório íntegro e acionável, este projeto desenvolveu um pipeline de dados baseado na arquitetura computacional Medalhão, subdividido nas camadas Bronze, Silver e Gold. O processo iniciou-se com a ingestão automatizada de sete fontes governamentais brutas, superando inconsistências complexas de engenharia, tais como cabeçalhos textuais poluídos nos relatórios do TabNet, codificações de caracteres corrompidas de municípios específicos e arquivos estruturados em layouts heterogêneos.

A modelagem final implementada na camada Gold guiou-se pelo rigor metodológico e pelas melhores práticas de engenharia de software, com destaque para a aplicação do princípio DRY (*Don't Repeat Yourself*). Visando otimizar o desempenho de futuras consultas e despoluir o esquema relacional, eliminou-se a coluna duplicada `ano_de_referencia` na base municipal ativa de 2022.

Ademais, o pipeline registrou uma taxa de pareamento geográfico (*match rate*) de **79,62%**, consolidando com sucesso **332 dos 417 municípios** baianos. A exclusão dos 85 municípios remanescentes na base cruzada final não decorreu de falha algorítmica, mas sim de uma limitação da fonte de origem: a omissão e a falta de declaração ativa de dados de saneamento por parte dessas administrações locais ao SNIS no ano de 2022.

---

## 3. A Divergência Escalar e o Paradoxo de Simpson

A etapa de análise exploratória de dados revelou um comportamento estatístico de alta complexidade analítica. Sob uma perspectiva macro e de longo prazo, a avaliação da série histórica estadual (2018-2023) demonstrou uma correlação linear de Pearson fortíssima e inversamente proporcional entre o avanço da infraestrutura e os óbitos. Os coeficientes atingiram marcas expressivas de **-0,603** para o índice consolidado de saneamento e **-0,637** para a cobertura de água, evidenciando que a expansão dos serviços básicos está associada a reduções drásticas na mortalidade. Para garantir a fidelidade desses coeficientes, a engenharia de recursos identificou e expurgou do histórico os anos de 2020 e 2021, período que sofreu um severo apagão de dados regulatórios em virtude dos impactos operacionais da pandemia da COVID-19.

Contudo, ao transicionar a escala de análise do nível macro (estadual) para o micro (municipal estático em 2022), o coeficiente de correlação linear aproximou-se de zero, configurando formalmente o fenômeno estatístico conhecido como **Paradoxo de Simpson**. Uma interpretação superficial e desprovida de técnicas de Big Data induziria ao falso diagnóstico de que a infraestrutura sanitária perde efeito preventivo no âmbito local.

A engenharia de dados do projeto solucionou esse paradoxo ao isolar duas variáveis de confusão de natureza prática:
1.  O viés de subnotificação cartográfica em distritos rurais isolados, que mascara o real volume de óbitos infantis em pequenas localidades;
2.  A limitação taxonômica do SNIS, que contabilizava municípios dependentes de fossas sépticas individuais seguras como detentores de "0% de rede de esgoto".

---

## 4. Conclusão e Próximos Passos Baseados em Evidências

Para neutralizar os vieses de escala provocados pelas assimetrias demográficas, a camada Gold do pipeline agrupou os municípios por faixas equivalentes de cobertura. Essa reestruturação analítica dissipou o ruído estatístico local e ratificou a tese inicial: o saneamento básico atua de forma direta na redução da mortalidade infantil local, com impactos severamente acentuados nas cidades de pequeno porte (faixas populacionais 1 e 2, com menos de 20 mil habitantes), que concentram os maiores deficits de infraestrutura do estado. Para assegurar a consistência matemática da base final de 59 colunas, os valores omissos foram tratados por meio de imputação estatística fundamentada na mediana de cada faixa populacional correspondente do IBGE.

Finalmente, cumpre destacar que todo o tratamento de dados observou estritamente os preceitos de governança, ética e conformidade legal com a Lei Geral de Proteção de Dados (LGPD). O fluxo de ETL operou exclusivamente sobre dados públicos anonimizados, agregados em nível municipal e estadual, eliminando riscos associados à reidentificação de indivíduos.

As bases sanitizadas da camada Gold encontram-se homologadas e prontas para o provisionamento de dashboards em tempo real (Streamlit/PowerBI) ou para o treinamento de modelos preditivos avançados. Os resultados científicos deste projeto transcendem a engenharia de dados ao fornecerem aos tomadores de decisão um arcabouço empírico para a priorização de investimentos regionais nas macrorregiões de saúde mais vulneráveis, o fomento a subsídios de saneamento descentralizado no interior e o combate sistemático às subnotificações de saúde pública na Bahia.
