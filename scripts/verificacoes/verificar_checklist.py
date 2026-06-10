import pandas as pd
from pathlib import Path
import os
import shutil
import re

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
                print("  Nenhuma coluna de UF encontrada. Verificando codigos de municipios...")
                # Se nao tem coluna UF, mas tem de municipio, verifica se os codigos começam com 29 (BA)
                mun_cols = [c for c in df.columns if 'municipio' in c.lower() or 'ibge' in c.lower()]
                if mun_cols:
                    mun_col = mun_cols[0]
                    unique_muns = df[mun_col].dropna().unique().tolist()
                    only_ba = all(str(m).strip().startswith('29') for m in unique_muns)
                    print(f"  Codigos de municipios começam com 29 (BA): {only_ba}")
                else:
                    print("  Nenhuma coluna de UF ou Municipio encontrada.")
            
            # 2. Check 2022
            pattern = re.compile(r'^(ano|co_anomes|dt_competencia|ano_referencia|ano_de_referencia)$', re.IGNORECASE)
            year_cols = [c for c in df.columns if pattern.match(c)]
            only_2022 = False
            if year_cols:
                year_col = year_cols[0]
                unique_years = df[year_col].dropna().unique().tolist()
                print(f"  Anos encontrados: {unique_years}")
                # Check if only 2022 or 202212
                only_2022 = all(str(y).startswith('2022') for y in unique_years)
            else:
                if '2022' in file.name or 'base_snis_geografia' in file.name:
                    print("  Nenhuma coluna de ano encontrada, mas o ano 2022 esta implicito no arquivo.")
                    only_2022 = True
                else:
                    print("  Nenhuma coluna de ano encontrada e sem 2022 no nome do arquivo.")

            # Theme check (Health/Sanitation)
            theme_related = True # Assuming files in gold are relevant
            
            print(f"  Resultado: Bahia={only_ba}, 2022={only_2022}")
            
            if not (only_ba and only_2022):
                # Ignorar verificacao restrita para bases declaradas como nacionais/historicas
                if 'nacional' in file.name.lower() or 'historica' in file.name.lower() or file.name == 'base_consolidada.csv':
                    print(f"  [KEEP] {file.name} e uma base nacional/historica. Mantendo.")
                    results.append({'file': file.name, 'status': 'Kept', 'reason': 'OK (National/Historical)'})
                else:
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
