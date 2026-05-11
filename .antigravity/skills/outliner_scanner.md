# Skill: outlier_scanner

## Descrição
Detecta anomalias estatísticas multidimensionais, não apenas valores extremos isolados.

## Funcionalidades
- **Isolation Forest**: Algoritmo de ML leve para encontrar outliers em múltiplas dimensões simultaneamente.
- **Z-Score Robusto**: Usa MAD (Median Absolute Deviation) para não ser enviesado pelos próprios outliers.
- **Contextualização**: Tenta agrupar os outliers para ver se formam um novo cluster ou se são apenas ruído.