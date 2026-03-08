import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from helpers.xml_parser import get_random_sentence
from langchain.hypergraph_model import HyperGraphData

def generate_hypergraph_from_text():
    load_dotenv()

    llm = ChatGroq(
        temperature=0,
        model_name="openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY")
    )

    structured_llm = llm.with_structured_output(HyperGraphData)

    xml_file_path = "./data/webnlg.xml"
    text = get_random_sentence(xml_file_path)
    print(text)
    print("Wyciąganie hipergrafu...")
    prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an algorithm for extracting knowledge hypergraphs. Your task is to read the following text and identify entities (nodes) and their relationships (hyperedges). Each hyperedge should connect 3 or more nodes. Please return the results in a structured JSON format."),
            ("user", "{text}")
        ])
    
    chain = prompt | structured_llm
    result = chain.invoke({"text": text})
    print("\n--- WĘZŁY ---")
    for node in result.nodes:
        print(f"- {node.id} ({node.type})")

    print("\n--- HIPERKRAWĘDZIE ---")
    for edge in result.hyperedges:
        print(f"Relacja: {edge.relation_name}")
        print(f"Połączone byty: {', '.join(edge.connected_nodes)}")
    return result