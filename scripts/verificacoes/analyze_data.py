import pandas as pd
import os

def analyze_excel(file_path):
    print(f"--- Analyzing Excel: {file_path} ---")
    try:
        xls = pd.ExcelFile(file_path)
        print(f"Sheet names: {xls.sheet_names}")
        for sheet in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet)
            print(f"\nSheet: {sheet}")
            print(f"Columns: {df.columns.tolist()}")
            print(f"Shape: {df.shape}")
            print(df.head())
    except Exception as e:
        print(f"Error reading Excel: {e}")

def analyze_csv(file_path):
    print(f"\n--- Analyzing CSV: {file_path} ---")
    try:
        df = pd.read_csv(file_path)
        print(f"Columns: {df.columns.tolist()}")
        print(f"Shape: {df.shape}")
        print(df.head())
    except Exception as e:
        print(f"Error reading CSV: {e}")

excel_path = r'c:\Users\joaof\Downloads\Unifacs\analise_dados_big_data\a3\dataset\data\gold\Book1.xlsx'
base_consolidada_path = r'c:\Users\joaof\Downloads\Unifacs\analise_dados_big_data\a3\dataset\data\gold\base_consolidada.csv'
base_snis_geografia_path = r'c:\Users\joaof\Downloads\Unifacs\analise_dados_big_data\a3\dataset\data\gold\base_snis_geografia.csv'

analyze_excel(excel_path)
analyze_csv(base_consolidada_path)
analyze_csv(base_snis_geografia_path)
