import pandas as pd
from pathlib import Path
import os
import shutil

gold_path = Path('data/gold')
dump_path = Path('data_dump')
dump_path.mkdir(parents=True, exist_ok=True)

results = []

for file in gold_path.iterdir():
    if file.suffix in ['.csv', '.xlsx']:
        print(f"--- Verificando {file.name} ---")
        try:
            if file.suffix == '.xlsx':
                df = pd.read_excel(file)
            else:
                try:
                    df = pd.read_csv(file, encoding='utf-8')
                except:
                    df = pd.read_csv(file, encoding='latin1')
            
            # 1. Check Bahia
            uf_cols = [c for c in df.columns if 'uf' in c.lower() or 'estado' in c.lower() or 'sg_uf' in c.lower()]
            only_ba = False
            if uf_cols:
                uf_col = uf_cols[0]
                unique_ufs = df[uf_col].dropna().unique().tolist()
                print(f"  UFs encontradas: {unique_ufs}")
                # Check if only BA or 29 (BA code)
                only_ba = all(str(u).strip().upper() in ['BA', '29', '29.0', 'BAHIA'] for u in unique_ufs)
            else:
                print("  Nenhuma coluna de UF encontrada.")
            
            # 2. Check 2022
            year_cols = [c for c in df.columns if 'ano' in c.lower() or 'ref' in c.lower() or 'competencia' in c.lower()]
            only_2022 = False
            if year_cols:
                year_col = year_cols[0]
                unique_years = df[year_col].dropna().unique().tolist()
                print(f"  Anos encontrados: {unique_years}")
                # Check if only 2022 or 202212
                only_2022 = all(str(y).startswith('2022') for y in unique_years)
            else:
                print("  Nenhuma coluna de ano encontrada.")

            # Theme check (Health/Sanitation)
            theme_related = True # Assuming files in gold are relevant
            
            print(f"  Resultado: Bahia={only_ba}, 2022={only_2022}")
            
            if not (only_ba and only_2022):
                print(f"  [MOVENDO] {file.name} para data_dump...")
                shutil.move(str(file), str(dump_path / file.name))
                results.append({'file': file.name, 'status': 'Moved', 'reason': f"BA={only_ba}, 2022={only_2022}"})
            else:
                results.append({'file': file.name, 'status': 'Kept', 'reason': 'OK'})
                
        except Exception as e:
            print(f"  [ERRO] Falha ao processar {file.name}: {e}")

print("\n--- Resumo Final ---")
for res in results:
    print(f"{res['file']}: {res['status']} ({res['reason']})")
