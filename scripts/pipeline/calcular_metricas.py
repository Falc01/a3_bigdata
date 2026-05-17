import pandas as pd
import os

# Pede os arquivos no terminal
entrada = input("Digite os nomes dos arquivos .csv separados por vírgula: ")
arquivos_csv = [arquivo.strip() for arquivo in entrada.split(',')]

pasta_origem = '../data'

for arquivo in arquivos_csv:
    caminho_csv = os.path.join(pasta_origem, arquivo)
    print(f"\n--- Métricas de: {caminho_csv} ---")
    
    try:
        df = pd.read_csv(caminho_csv)
        df_num = df.select_dtypes(include=['number'])
        
        if not df_num.empty:
            print("Média:\n", df_num.mean().round(2), "\n")
            print("Mediana:\n", df_num.median().round(2), "\n")
            print("Moda:\n", df_num.mode().iloc[0].round(2), "\n")
            print("Variância:\n", df_num.var().round(2), "\n")
            print("Desvio Padrão:\n", df_num.std().round(2), "\n")
            print("Amplitude:\n", (df_num.max() - df_num.min()).round(2), "\n")
        else:
            print("Aviso: Nenhuma coluna numérica encontrada para cálculos.")
            
    except FileNotFoundError:
        print(f"❌ Erro: O arquivo {caminho_csv} não foi encontrado.")