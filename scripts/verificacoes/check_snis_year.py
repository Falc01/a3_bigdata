import pandas as pd

file_path = 'data/gold/base_snis_geografia.csv'

# Read a sample to determine encoding if utf-8 fails
try:
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='latin1')

# Find columns related to year/date
year_cols = [c for c in df.columns if 'ano' in c.lower() or 'data' in c.lower() or 'ref' in c.lower()]
print(f"Potential year columns: {year_cols}")

if year_cols:
    for col in year_cols:
        print(f"\nUnique values in '{col}':")
        print(df[col].value_counts().head())
else:
    print("No obvious year column found. Checking first few rows:")
    print(df.head())
