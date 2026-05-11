# Skill: parse_workbook

## Descrição
Faz um raio-X completo do arquivo Excel antes de carregar os dados na memória.

## Funcionalidades
- **Mapeamento de Abas**: Lista todas as planilhas (sheets) disponíveis no arquivo.
- **Detecção de Volume**: Retorna a dimensão estimada (linhas x colunas) de cada aba.
- **Auditoria Oculta**: Identifica abas que estão ocultas (hidden) ou vazias, evitando processamento desnecessário.

## Exemplo de Uso
```python
# Retorna um dicionário com o metadado estrutural do Excel
parse_workbook("relatorio_financeiro.xlsx")