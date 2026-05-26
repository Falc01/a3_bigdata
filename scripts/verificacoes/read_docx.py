import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

def read_docx_text(file_path):
    print(f"--- Reading DOCX: {file_path} ---")
    if not file_path.exists():
        print(f"[ERRO] Error: Word document not found at {file_path}")
        return
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            xml_content = zip_ref.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            # Namespaces are usually required for parsing Word XML
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            }
            
            paragraphs = tree.findall('.//w:t', namespaces)
            text = " ".join([p.text for p in paragraphs if p.text])
            
            # Avoid encoding issues on standard windows terminals by encoding/decoding with replacement
            sys.stdout.reconfigure(encoding='utf-8')
            print(text)
    except Exception as e:
        print(f"Error reading DOCX: {e}")

docx_path = Path('docs/DADOS RETIRADOS DE.docx')
read_docx_text(docx_path)
