# Roteiro de Apresentação e Falas (A3)

Este roteiro detalha as falas sugeridas para cada slide durante a apresentação final do projeto de **Análise de Dados e Big Data**.

---

### Slide 1: Abertura e Introdução
> "Hoje vamos apresentar para vocês o nosso projeto, que se chama 'O Peso da Infraestrutura: Uma análise da mortalidade infantil e saneamento básico na Bahia'. A ideia central aqui foi usar a engenharia de dados e o conceito de Big Data para responder a uma questão bem direta: o quanto a falta de saneamento básico e de água tratada impacta de verdade, na prática, a vida e a sobrevivência das crianças no nosso estado."

---

### Slide 2: O Panorama da Saúde Infantil Baiana
> "Para começar, a gente precisa olhar para a nossa realidade geográfica. A Bahia tem 417 municípios, mas se vocês olharem para a nossa base de dados Gold final, nós trabalhamos com 332 cidades. Isso nos deu uma taxa de pareamento, um match rate, de quase 80%. E por que os outros 19% ficaram de fora? Simplesmente porque em 2022 essas prefeituras não declararam seus dados de saneamento ao SNIS. Citar isso é fundamental para mostrar o nosso cuidado com a qualidade dos dados desde o início.
>
> Dentro dessa base consolidada, nós cruzamos uma série histórica que mapeou quase 1 milhão de nascimentos, mais precisamente 950.814 nascidos vivos. Só que, infelizmente, esse mesmo período registrou uma tragédia silenciosa de 14.206 crianças que morreram antes de completar o primeiro ano de vida. Estamos falando de uma taxa média ponderada de quase 15 mortes para cada mil nascidos. O grande nó que a gente tentou desatar é que essas informações de saúde e infraestrutura ficam presas em sistemas que não se conversam, como o DATASUS e o SNIS, deixando qualquer gestor público completamente no escuro."

---

### Slide 3: Série Histórica: O Impacto no Longo Prazo
> "Para resolver esse problema, nós criamos um pipeline de dados usando a arquitetura Medalhão. Nós limpamos tabelas horríveis do TabNet, corrigimos nomes de cidades com caracteres quebrados e, na camada Gold, aplicamos o princípio técnico do DRY. Basicamente, nós limpamos a estrutura eliminando colunas redundantes, como a coluna duplicada ano_de_referencia na base municipal, deixando as tabelas muito mais leves e focadas nas regras de negócio.
>
> Quando a gente roda a análise dessa série histórica a nível macro, olhando para o estado como um tempo e como um todo (2018-2023), o resultado é incontestável. A correlação é fortíssima e negativa: -0.603 para saneamento e -0.637 para cobertura de água. Vale fazer um destaque importante aqui: nós deixamos de fora os anos de 2020 e 2021 por causa do apagão de dados que o SNIS sofreu durante a pandemia da COVID-19. Fizemos isso para evitar qualquer distorção na série. Mas a conclusão dessa etapa é óbvia: se a infraestrutura sobe, a mortalidade cai."

---

### Slide 4: O "Paradoxo de Simpson" no Nível Municipal
> "Só que a beleza do Big Data está nos detalhes. Quando a gente parou de olhar o macro e desceu para analisar os municípios de forma isolada e estática em 2022, aconteceu uma coisa intrigante: a correlação linear de Pearson foi praticamente para zero, marcando apenas 0.074 para esgoto. Se um analista olhasse para esse gráfico de dispersão com pressa, ia acabar concluindo, de forma totalmente errada, que saneamento e mortalidade infantil não têm relação nenhuma no nível local. Esse fenômeno é conhecido na estatística como o Paradoxo de Simpson, que é quando uma tendência forte que você vê no macro simplesmente some ou se inverte quando você olha para os grupos divididos. E foi aí que a nossa engenharia de dados precisou investigar o porquê desse comportamento."

---

### Slide 5: Por que a correlação linear municipal parece fraca?
> "Investigando a fundo, nós descobrimos que o Paradoxo de Simpson acontecia por dois motivos muito práticos do mundo real. O primeiro é o viés de subnotificação. Em muitas cidades pequenas do interior, quando uma criança morre numa zona rural isolada, o óbito às vezes nem chega a ser registrado de forma correta no sistema de saúde. O segundo motivo é puramente técnico: o SNIS mede 'rede de esgoto encanada'. Muitas cidades pequenas utilizam fossas sépticas individuais que funcionam muito bem e são seguras, mas o sistema computava isso como 0% de esgoto, gerando um ruído gigante nos gráficos. Enquanto isso, nas grandes cidades, a densidade é tão alta que qualquer falha na rede provoca surtos rápidos de doenças nas crianças."

---

### Slide 6: Eliminando o Ruído: Análise por Faixas de Cobertura
> "A solução que nós encontramos na nossa camada Gold para corrigir esse paradoxo foi mudar a abordagem: em vez de jogar os municípios soltos no gráfico de forma linear, nós os agrupamos por faixas de cobertura de esgoto. Quando a gente organiza os dados desse jeito, limpando o viés e o ruído das cidades menores, a verdade aparece com total clareza. Fica nítido que os municípios que estão nas faixas de melhor infraestrutura de esgoto têm, sim, taxas de mortalidade muito menores. A tese do saneamento preventivo acabou sendo confirmada."

---

### Slide 7: O Gargalo da Infraestrutura Sanitária
> "O que o nosso trabalho escancarou é que o grande gargalo da infraestrutura sanitária na Bahia tem um recorte demográfico muito claro. São as cidades de pequeno porte, com menos de 20 mil habitantes, as que mais sofrem com a falta crônica de serviços básicos. Para deixar a nossa base final de 59 colunas totalmente consistente e robusta, nós tratamos os dados nulos usando uma imputação avançada baseada na mediana de cada Faixa Populacional do IBGE. Isso garantiu que a nossa análise respeitasse as diferenças reais entre o tamanho de cada município."

---

### Slide 8: Ética, Transparência e LGPD
> "Um ponto que o nosso grupo fez questão de blindar foi a parte de governança e ética. Nós trabalhamos única e exclusivamente com dados públicos de livre acesso, extraídos de portais oficiais com base na Lei de Acesso à Informação. Além disso, todas as informações de saúde foram agregadas por município. Não tem nome de ninguém, não tem prontuário e muito menos CPF circulando no nosso pipeline. O projeto foi desenhado do início ao fim em total e irrestrita conformidade com a LGPD."

---

### Slide 9: Conclusão: Saneamento é Saúde Preventiva
> "Para fechar, o nosso projeto deixa claro que investir em saneamento básico não é apenas uma obra de engenharia civil, é fazer medicina preventiva de alto impacto para salvar vidas. As nossas bases Gold estão tratadas, higienizadas e prontas para alimentar qualquer painel no Streamlit, no Power BI ou modelos preditivos avançados.
>
> As nossas recomendações práticas para a gestão pública são: concentrar os recursos do Marco do Saneamento nas macrorregiões de saúde mais vulneráveis, criar subsídios e projetos padrão para fossas sépticas seguras nas cidades com menos de 20 mil habitantes e treinar as equipes de saúde da família para zerar a subnotificação no interior. Os dados estão limpos e estruturados, agora eles precisam ser usados para transformar essa realidade. Muito obrigado."
