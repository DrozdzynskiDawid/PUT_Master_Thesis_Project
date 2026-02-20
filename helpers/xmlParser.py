import xml.etree.ElementTree as ET

def extract_texts_from_xml(xml_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        extracted_texts = [lex.text for lex in root.findall(".//lex") if lex.text]
        print(f"Znaleziono {len(extracted_texts)} zdań w pliku XML.\n")
        return extracted_texts
        
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku '{xml_file_path}'. Upewnij się, że plik jest w tym samym folderze.")
    except ET.ParseError:
        print("Błąd: Nie udało się sparsować pliku XML. Sprawdź, czy struktura pliku jest poprawna.")