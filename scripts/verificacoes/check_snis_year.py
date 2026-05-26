import pandas as pd
from pathlib import Path
import re
import sys

file_path = Path('data/gold/base_snis_geografia.csv')
if not file_path.exists():
    print(f"[ERRO] Arquivo nao encontrado: {file_path}")
    sys.exit(1)

# Read a sample to determine encoding if utf-8 fails
try:
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='latin1')

# Find columns related to year/date using precise matching
# e.g., 'ano', 'co_anomes', 'dt_competencia', etc. (not 'urbano', 'funcionarios')
pattern = re.compile(r'^(ano|co_anomes|dt_competencia|ano_referencia|ano_de_referencia)$', re.IGNORECASE)
year_cols = [c for c in df.columns if pattern.match(c)]
print(f"Potential year columns: {year_cols}")

if year_cols:
    for col in year_cols:
        print(f"\nUnique values in '{col}':")
        print(df[col].value_counts().head())
else:
    print("No obvious year column found. First few columns in file:")
    print(df.columns.tolist()[:10])
