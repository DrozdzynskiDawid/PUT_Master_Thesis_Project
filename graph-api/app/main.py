from fastapi import FastAPI, Response
from langchain.langchain_graph_generation import generate_graph_from_text
from langchain.langchain_hypergraph_generation import generate_hypergraph_from_text
from helpers.visualization.plot_hypergraphs import visualize_knowledge_hypergraph
from helpers.visualization.plot_graphs import visualize_knowledge_graph
from app.hypergraph_request_model import HypergraphRequest
from app.graph_request_model import NodeLinkGraphModel
from helpers.transformation import transform_to_graph_clique
from helpers.get_stats import get_graph_stats
import xgi

app = FastAPI()

@app.get("/api")
def hello():
    return {"name": "Graph API", "version": "1.0"}

@app.get("/api/graph")
def get_graph():
    return generate_graph_from_text()

@app.post("/api/graph/visualization")
def get_graph_png(G: NodeLinkGraphModel):
    png = visualize_knowledge_graph(G)
    if png is None:
        return Response(content="Brak danych", status_code=400)
    return Response(content=png, media_type="image/png")

@app.get("/api/graph/stats")
def get_stats(data: NodeLinkGraphModel):
    return get_graph_stats(data)

@app.get("/api/hypergraph")
def get_hypergraph():
    return generate_hypergraph_from_text()

@app.post("/api/hypergraph/visualization")
def get_hypergraph_png(data: HypergraphRequest):
    png = visualize_knowledge_hypergraph(data)
    if png is None:
        return Response(content="Brak danych", status_code=400)
    return Response(content=png, media_type="image/png")

@app.post("/api/hypergraph/transformation")
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