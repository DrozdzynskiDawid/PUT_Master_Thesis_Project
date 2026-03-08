import os
from dotenv import load_dotenv
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_groq import ChatGroq  
from langchain_core.documents import Document
from helpers.xml_parser import get_random_sentence
import random
import networkx as nx

def generate_graph_from_text():
    load_dotenv()

    llm = ChatGroq(
        temperature=0,
        model_name=os.getenv("MODEL_NAME"),
        api_key=os.getenv("GROQ_API_KEY")
    )

    llm_transformer = LLMGraphTransformer(
        llm=llm
    )

    xml_file_path = "./data/testdata_with_lex.xml"
    text = get_random_sentence(xml_file_path)
    print(text)

    document = Document(page_content=text)
    try:
        print("Wysyłanie zapytania do Groq...")
        graph_doc = llm_transformer.convert_to_graph_documents([document])[0]          
        if graph_doc.nodes or graph_doc.relationships:
            print(f"Nodes ({len(graph_doc.nodes)}):")
            for node in graph_doc.nodes:
                print(f"  - {node.id} ({node.type})")
                
            print(f"Relationships ({len(graph_doc.relationships)}):")
            for rel in graph_doc.relationships:
                print(f"  {rel.source.id} --[{rel.type}]--> {rel.target.id}")
            
            G = nx.DiGraph()
            for node in graph_doc.nodes:
                G.add_node(node.id, type=node.type)
            for rel in graph_doc.relationships:
                G.add_edge(rel.source.id, rel.target.id, relation=rel.type)

            return nx.node_link_data(G)
        else:
            print("Nie znaleziono relacji lub węzłów w tym zdaniu.")
            
    except Exception as e:
        print(f"Wystąpił błąd podczas przetwarzania: {e}")