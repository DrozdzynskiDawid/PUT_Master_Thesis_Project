import os
from dotenv import load_dotenv
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_groq import ChatGroq  
from langchain_core.documents import Document
from helpers.xmlParser import extract_texts_from_xml
from helpers.visualization.graphs import visualize_knowledge_graph
import random

load_dotenv()

llm = ChatGroq(
    temperature=0,
    model_name="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

llm_transformer = LLMGraphTransformer(
    llm=llm
)

xml_file_path = "./data/webnlg.xml"
dataset = extract_texts_from_xml(xml_file_path)

documents = [Document(page_content=text) for text in dataset]
# FOR TESTS 5 SENTENCES ONLY
documents = random.sample(documents, min(5, len(documents)))

try:
    print("Wysyłanie zapytania do Groq...")
    graph_documents = llm_transformer.convert_to_graph_documents(documents)

    print("--- WYNIKI ---")
    for i, graph_doc in enumerate(graph_documents):
        print(f"\n[Zdanie {i+1}]: {documents[i].page_content}")
        
        if graph_doc.nodes or graph_doc.relationships:
            print(f"Nodes ({len(graph_doc.nodes)}):")
            for node in graph_doc.nodes:
                print(f"  - {node.id} ({node.type})")
                
            print(f"Relationships ({len(graph_doc.relationships)}):")
            for rel in graph_doc.relationships:
                print(f"  {rel.source.id} --[{rel.type}]--> {rel.target.id}")
            
            # VISUALIZATION
            visualize_knowledge_graph(graph_doc, i)
        else:
            print("Nie znaleziono relacji lub węzłów w tym zdaniu.")
        print("-" * 50)
        
except Exception as e:
    print(f"Wystąpił błąd podczas przetwarzania: {e}")