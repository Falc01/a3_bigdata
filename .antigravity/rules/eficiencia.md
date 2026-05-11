# Rule: eficiencia

## Definição
Diretriz mandatória para garantir a performance do processamento de dados e economia de recursos.[cite: 2]

## Mandamentos
1. **Vetorização**: Nunca utilize loops `for` ou `iterrows` para manipular DataFrames. Use operações nativas do Pandas/NumPy.[cite: 2]
2. **Memory Management**: Utilize tipos de dados adequados (ex: `int32` em vez de `int64`, `category` para strings repetitivas).[cite: 2]
3. **Lazy Loading**: Prefira `Polars` ou `Dask` para datasets que excedam 60% da RAM disponível.[cite: 2]
4. **Queries Otimizadas**: Sempre use `LIMIT` em testes e evite `SELECT *` em bancos de produção.[cite: 2]