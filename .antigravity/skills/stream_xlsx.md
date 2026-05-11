# Skill: stream_xlsx

## Descrição
Leitura de alta performance para arquivos `.xlsx` massivos (acima de 50MB ou 500k linhas).

## Funcionalidades
- **Calamine Engine**: Substitui o motor padrão (como `openpyxl`) por engines baseadas em Rust (ex: `calamine` com `polars` ou `pandas`) para leitura até 10x mais rápida.
- **Data-Only Mode**: Ignora completamente formatações condicionais, macros (VBA), gráficos e estilos de fonte, extraindo estritamente os valores brutos.
- **Chunking**: Permite ler planilhas gigantescas em lotes (chunks) para não estourar a memória RAM da máquina.