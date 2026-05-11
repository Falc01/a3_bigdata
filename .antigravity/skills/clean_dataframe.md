# Skill: clean_dataframe

## Descrição
Pipeline automatizado para higienização e padronização de dados.[cite: 4]

## Etapas de Processamento
1. **Deduplicação**: Remoção de registros 100% idênticos.[cite: 4]
2. **Tratamento de Nulos**: Imputação (média/mediana) ou remoção baseada em threshold.[cite: 4]
3. **Normalização de Texto**: Strip de espaços, lowercase e remoção de caracteres especiais em headers.[cite: 4]
4. **Cast de Tipos**: Conversão inteligente de strings para datetime ou categorias para economia de memória.[cite: 4]
5. **Outliers**: Identificação via IQR (Interquartile Range).[cite: 4]

## Parâmetros Sugeridos
- `threshold_null`: 0.5 (descarta colunas com >50% nulos).[cite: 4]
- `inplace`: False.[cite: 4]