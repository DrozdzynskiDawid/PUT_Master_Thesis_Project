from fastapi import FastAPI, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from langchain.langchain_graph_generation import generate_graph_from_text
from langchain.langchain_hypergraph_generation import generate_hypergraph_from_text
from helpers.visualization.plot_hypergraphs import visualize_knowledge_hypergraph
from helpers.visualization.plot_graphs import visualize_knowledge_graph
from app.hypergraph_request_model import HypergraphRequest
from app.graph_request_model import NodeLinkGraphModel
from helpers.transformation import transform_to_graph_clique
from langchain.langchain_transformation import transform_to_graph_selected_clique
from helpers.get_stats import get_graph_stats
from helpers.dataset_parser import get_random_sentence
from helpers.get_embedding_similarity import get_graph_similarity
import xgi

app = FastAPI(
    title="Graph API",
    description="API projektu dla pracy magisterskiej do generowania i analizy grafów wiedzy z tekstu",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def hello():
    return {"name": "Graph API", "version": "1.0"}

@app.get("/api/random-text")
def get_random_text(file_path: str):
    return {"text": get_random_sentence(file_path)}

@app.post("/api/graph")
def get_graph(text: str = Body(..., embed=True)):
    return generate_graph_from_text(text)

@app.post("/api/graph/visualization")
def get_graph_png(G: NodeLinkGraphModel):
    png = visualize_knowledge_graph(G)
    if png is None:
        return Response(content="Brak danych", status_code=400)
    return Response(content=png, media_type="image/png")

@app.post("/api/graph/stats")
def get_stats(data: NodeLinkGraphModel):
    return get_graph_stats(data)

@app.post("/api/hypergraph")
def get_hypergraph(text: str = Body(..., embed=True)):
    return generate_hypergraph_from_text(text)

@app.post("/api/hypergraph/visualization")
def get_hypergraph_png(data: HypergraphRequest):
    png = visualize_knowledge_hypergraph(data)
    if png is None:
        return Response(content="Brak danych", status_code=400)
    return Response(content=png, media_type="image/png")

@app.post("/api/hypergraph/transformation/clique")
def transform_hypergraph_to_graph(data: HypergraphRequest):
    H = xgi.Hypergraph()
    for node in data.nodes:
        H.add_node(node.id, type=node.type)
    for edge in data.hyperedges:
        valid_nodes = [n for n in edge.connected_nodes if n in H.nodes]
        if valid_nodes:
            H.add_edge(valid_nodes, relation=edge.relation_name)
    graph = transform_to_graph_clique(H)
    if graph is None:
        return Response(content="Brak danych", status_code=400)
    return graph

@app.post("/api/hypergraph/transformation/selected_clique")
def transform_hypergraph_to_graph_llm(data: HypergraphRequest):
    return transform_to_graph_selected_clique(data)

@app.post("/api/graph/comparison")
def compare_graphs(graph1: NodeLinkGraphModel, graph2: NodeLinkGraphModel):
    return get_graph_similarity(graph1.model_dump(), graph2.model_dump())