from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from app.graph_request_model import GraphLink, GraphNode, NodeLinkGraphModel
from helpers.get_llm import get_llm

class LLMLinkOutput(BaseModel):
    links: List[GraphLink] = Field(description="List of the most essential, meaningful binary connections.")

def transform_to_graph_selected_clique(hypergraph_data):
    print("\nFiltrowanie krawędzi i budowa grafu...")
    llm = get_llm()
    structured_llm_links = llm.with_structured_output(LLMLinkOutput)
    
    hyperedges_str = "\n".join([
        f"- Relation: '{e.relation_name}', Connected Entities: [{', '.join(e.connected_nodes)}]" 
        for e in hypergraph_data.hyperedges
    ])
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an expert knowledge graph engineer. You are provided with a hypergraph consisting of hyperedges (a single relation connecting multiple entities).
        Your task is to decompose these hyperedges into the most essential and logically sound binary (1-to-1) directed edges.
        
        RULES:
        1. DO NOT create a full clique. Do not connect every entity to every other entity just because they share a hyperedge.
        2. Deduce the logical subject-object relationships based on the entities' names and the name of the relation.
        3. Exclude trivial or redundant connections.
        4. Put the relation name in the 'relation' field of the link.
        """),
        ("user", """
        Here are the hyperedges to analyze:
        
        {hyperedges}
        
        Extract the most important binary edges.
        """)
    ])

    chain = prompt | structured_llm_links
    llm_result = chain.invoke({"hyperedges": hyperedges_str})
    final_nodes = []
    for node in hypergraph_data.nodes:
        final_nodes.append(GraphNode(
            id=node.id, 
            label=node.id,
            type=node.type
        ))
    final_links = llm_result.links
    final_graph = NodeLinkGraphModel(
        directed=True,
        multigraph=False,
        nodes=final_nodes,
        links=final_links
    )

    print("\n--- ODFILTROWANE KRAWĘDZIE ---")
    for link in final_graph.links:
        print(f"{link.source} --[{link.label}]--> {link.target}")

    return final_graph