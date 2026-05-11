# Skill: fix_excel_layout

## Descrição
Limpa automaticamente os piores "vícios" de formatação humana em planilhas.

## Funcionalidades
- **Unmerge & Fill**: Detecta células mescladas, desfaz a mesclagem e preenche os valores para baixo/direita (`ffill`/`bfill`), mantendo a integridade tabular.
- **Header Finder**: Escaneia as primeiras 20 linhas para encontrar a verdadeira linha de cabeçalho, ignorando títulos cosméticos ou logos em texto.
- **Drop Totals**: Identifica e remove linhas de "Subtotal" ou "Total Geral" que quebram agregações em ferramentas de BI ou pandas.