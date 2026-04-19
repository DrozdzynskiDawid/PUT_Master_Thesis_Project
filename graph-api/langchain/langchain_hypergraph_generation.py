from langchain_core.prompts import ChatPromptTemplate
from langchain.hypergraph_model import HyperGraphData
from helpers.get_llm import get_llm

def generate_hypergraph_from_text(text):
    llm = get_llm()
    structured_llm = llm.with_structured_output(HyperGraphData)
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