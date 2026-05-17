import zipfile
import xml.etree.ElementTree as ET

def read_docx_text(file_path):
    print(f"--- Reading DOCX: {file_path} ---")
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            xml_content = zip_ref.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            # Namespaces are usually required for parsing Word XML
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            }
            
            paragraphs = tree.findall('.//w:t', namespaces)
            text = "".join([p.text for p in paragraphs if p.text])
            print(text)
    except Exception as e:
        print(f"Error reading DOCX: {e}")

docx_path = r'c:\Users\joaof\Downloads\Unifacs\analise_dados_big_data\a3\dataset\artifacts\DADOS RETIRADOS DE.docx'
read_docx_text(docx_path)
