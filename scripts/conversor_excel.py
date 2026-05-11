import pandas as pd
import os

def ler_csv_universal(caminho_arquivo):
    """
    Tenta ler qualquer CSV lidando com separadores automáticos, 
    múltiplos encodings e pulando linhas corrompidas.
    """
    encodings_para_testar = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    
    for enc in encodings_para_testar:
        try:
            df = pd.read_csv(
                caminho_arquivo,
                sep=None,             
                engine='python',      
                encoding=enc,         
                on_bad_lines='skip'   
            )
            print(f"  [Info] Arquivo lido com sucesso (Encoding: '{enc}')")
            return df
            
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"  [Erro] Falha ao tentar ler com encoding {enc}: {e}")
            break
            
    print("  [Erro Crítico] Não foi possível ler o arquivo com nenhum padrão.")
    return None

# ==========================================
# INÍCIO DO SCRIPT PRINCIPAL
# ==========================================

# Pede os arquivos no terminal
entrada = input("Digite os nomes dos arquivos .csv separados por vírgula: ")
arquivos_csv = [arquivo.strip() for arquivo in entrada.split(',')]

pasta_origem = '../data'
pasta_destino = os.path.join('..', 'data_excel')

# Verifica se a pasta JÁ existe. Se não existir, ele cria.
if os.path.exists(pasta_destino):
    print(f"📁 A pasta '{pasta_destino}' já existe. Usando a pasta atual.")
else:
    os.makedirs(pasta_destino)
    print(f"📁 Pasta '{pasta_destino}' criada com sucesso.")

for arquivo in arquivos_csv:
    caminho = os.path.join(pasta_origem, arquivo)
    print(f"\n--- Convertendo: {caminho} ---")
    
    # Valida se o arquivo existe antes de tentar ler
    if not os.path.exists(caminho):
        print(f"❌ Erro: O arquivo {caminho} não foi encontrado.")
        continue
    
    # Usa a nova função para ler o dataframe
    df = ler_csv_universal(caminho)
    
    # Se a leitura foi um sucesso (df não é vazio), converte para Excel
    if df is not None:
        nome_arquivo = arquivo.replace('.csv', '.xlsx')
        caminho_excel = os.path.join(pasta_destino, nome_arquivo)
        
        try:
            df.to_excel(caminho_excel, index=False, engine='openpyxl')
            print(f"✅ Arquivo salvo com sucesso em: {caminho_excel}")
        except Exception as e:
            print(f"❌ Erro ao salvar o arquivo Excel: {e}")