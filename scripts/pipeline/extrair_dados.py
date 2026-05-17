import os
import zipfile
import shutil
from pathlib import Path

def extrair_bronze():
    """
    Implementação da Camada Bronze:
    - Extração de ZIPs
    - Deduplicação de arquivos (Prioriza XLSX sobre CSV)
    - Organização em data/bronze
    """
    base_path = Path(".")
    data_path = base_path / "data"
    excel_path = base_path / "data_excel"
    dump_path = base_path / "data_dump"
    bronze_path = data_path / "bronze"
    temp_extract_path = data_path / "temp_extract"

    # Garantir diretórios
    bronze_path.mkdir(parents=True, exist_ok=True)
    if temp_extract_path.exists():
        shutil.rmtree(temp_extract_path)
    temp_extract_path.mkdir()

    print(f"--- Iniciando extracao para Camada Bronze ---")

    # 1. Descompactar arquivos ZIP de 'data' e 'data_dump' (incluindo aninhados)
    processed_zips = set()
    zips_to_process = list(data_path.glob("*.zip")) + list(dump_path.glob("*.zip"))
    
    while zips_to_process:
        zip_file = zips_to_process.pop(0)
        if zip_file in processed_zips:
            continue
            
        print(f"[ZIP] Descompactando {zip_file.name}...")
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_path)
            processed_zips.add(zip_file)
            
            # Procurar novos zips extraídos
            for root, dirs, files in os.walk(temp_extract_path):
                for file in files:
                    if file.endswith(".zip"):
                        full_path = Path(root) / file
                        if full_path not in processed_zips:
                            zips_to_process.append(full_path)
        except Exception as e:
            print(f"[ERRO] Erro ao descompactar {zip_file.name}: {e}")
            processed_zips.add(zip_file) # Marcar como processado mesmo com erro para não repetir

    # 2. Mapear arquivos Excel da data_excel (Alta Prioridade)
    excel_files = {f.stem: f for f in excel_path.glob("*.xlsx")}
    for stem, path in excel_files.items():
        shutil.copy(path, bronze_path / path.name)
        print(f"[EXCEL] Copiado: {path.name}")

    # 3. Mapear arquivos CSV, JSON e XLSX (Deduplicação)
    for source in [data_path, dump_path, temp_extract_path]:
        for ext in ["**/*.csv", "**/*.json", "**/*.xlsx"]:
            for file in source.rglob(ext):
                if bronze_path in file.parents or excel_path in file.parents:
                    continue
                if file.suffix.lower() == ".csv" and file.stem in excel_files:
                    print(f"[SKIP] Ignorado (Duplicata CSV): {file.name}")
                    continue
                
                dest = bronze_path / file.name
                if not dest.exists():
                    try:
                        shutil.copy(file, dest)
                        print(f"[FILE] Copiado: {file.name}")
                    except Exception as e:
                        print(f"[ERRO] Falha ao copiar {file.name}: {e}")

    # Limpeza robusta
    print("\n--- Limpando arquivos temporarios ---")
    try:
        shutil.rmtree(temp_extract_path, ignore_errors=True)
    except:
        pass
    print(f"--- Camada Bronze concluida em: {bronze_path} ---")

if __name__ == "__main__":
    extrair_bronze()
