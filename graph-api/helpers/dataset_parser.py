import xml.etree.ElementTree as ET
import random
import json
import pandas as pd

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

def extract_texts_from_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sentences = []
    for token_list in data['train']['text']:
        sentence = " ".join(token_list)
        sentences.append(sentence)
    return sentences

def extract_texts_from_parquet(parquet_file_path):
    df = pd.read_parquet(parquet_file_path)
    sentences = df['text'].tolist()
    return sentences


def get_random_sentence(file_path):
    if file_path.endswith('.xml'):
        sentences = extract_texts_from_xml(file_path)
    elif file_path.endswith('.json'):
        sentences = extract_texts_from_json(file_path)
    elif file_path.endswith('.parquet'):
        sentences = extract_texts_from_parquet(file_path)
    return random.choice(sentences) if sentences else None