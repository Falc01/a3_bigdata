# Skill: table_spotter

## Descrição
Extrai múltiplas tabelas independentes que foram desenhadas dentro de uma mesma aba do Excel.

## Funcionalidades
- **Clusterização por NaNs**: Mapeia linhas e colunas inteiramente em branco para identificar onde uma tabela termina e outra começa.
- **Multi-Frame Output**: Separa visualmente uma aba caótica em uma lista de `[df1, df2, df3]`, cada um com seu próprio escopo de dados isolado.
- **Tratamento de Margem**: Remove bordas em branco inúteis nas extremidades da área com dados úteis.