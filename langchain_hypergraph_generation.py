import os
import random
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from helpers.visualization.plot_hypergraphs import visualize_knowledge_hypergraph
from helpers.xmlParser import extract_texts_from_xml

load_dotenv()

class Node(BaseModel):
    id: str = Field(description="Unique identifier for the entity, e.g. 'Albert Einstein', 'Paris', 'Apollo 11'")
    type: str = Field(description="Type of the entity, e.g. 'Person', 'Location', 'Mission'")

class HyperEdge(BaseModel):
    relation_name: str = Field(description="Name of the relationship, e.g. 'Crew members of', 'Co-authors'")
    connected_nodes: List[str] = Field(description="List of node IDs that participate in the relationship. Should be 3 or more.")

class HyperGraphData(BaseModel):
    nodes: List[Node]
    hyperedges: List[HyperEdge]

llm = ChatGroq(
    temperature=0,
    model_name="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

structured_llm = llm.with_structured_output(HyperGraphData)

xml_file_path = "./data/webnlg.xml"
dataset = extract_texts_from_xml(xml_file_path)

# FOR TESTS 5 SENTENCES ONLY
dataset = random.sample(dataset, min(5, len(dataset)))

print("Wyciąganie hipergrafu...")
for text in dataset:
    print(text)
    prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an algorithm for extracting knowledge. Your task is to read the following text and identify entities (nodes) and their relationships (hyperedges). Each hyperedge should connect 3 or more nodes. Please return the results in a structured JSON format."),
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
    visualize_knowledge_hypergraph(result)