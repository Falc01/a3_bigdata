import pandas as pd
from pathlib import Path

def analyze_excel(file_path):
    print(f"\n--- Analyzing Excel: {file_path} ---")
    if not file_path.exists():
        print(f"⚠️ Warning: Excel file not found: {file_path}")
        return
    try:
        xls = pd.ExcelFile(file_path)
        print(f"Sheet names: {xls.sheet_names}")
        for sheet in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet)
            print(f"\nSheet: {sheet}")
            print(f"Columns: {df.columns.tolist()[:10]}...")
            print(f"Shape: {df.shape}")
            print(df.head(2))
    except Exception as e:
        print(f"Error reading Excel: {e}")

def analyze_csv(file_path):
    print(f"\n--- Analyzing CSV: {file_path} ---")
    if not file_path.exists():
        print(f"⚠️ Warning: CSV file not found: {file_path}")
        return
    try:
        df = pd.read_csv(file_path)
        print(f"Columns: {df.columns.tolist()[:10]}...")
        print(f"Shape: {df.shape}")
        print(df.head(2))
    except Exception as e:
        print(f"Error reading CSV: {e}")

excel_path = Path('data_dump/Book1.xlsx')
base_consolidada_path = Path('data/gold/base_consolidada_2022.csv')
base_snis_geografia_path = Path('data/gold/base_snis_geografia.csv')

analyze_excel(excel_path)
analyze_csv(base_consolidada_path)
analyze_csv(base_snis_geografia_path)
