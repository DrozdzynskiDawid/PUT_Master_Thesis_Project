from fastapi import FastAPI, Response, Body
from langchain.langchain_graph_generation import generate_graph_from_text
from langchain.langchain_hypergraph_generation import generate_hypergraph_from_text
from helpers.visualization.plot_hypergraphs import visualize_knowledge_hypergraph
from helpers.visualization.plot_graphs import visualize_knowledge_graph
from app.hypergraph_request_model import HypergraphRequest
from app.graph_request_model import GraphRequest

app = FastAPI()

@app.get("/api")
def hello():
    return {"name": "Graph API", "version": "1.0"}

@app.get("/api/graph")
def get_graph():
    return generate_graph_from_text()

@app.post("/api/graph/visualization")
def get_graph_png(data: GraphRequest):
    png = visualize_knowledge_graph(data)
    if png is None:
        return Response(content="Brak danych", status_code=400)
    return Response(content=png, media_type="image/png")

@app.get("/api/hypergraph")
def get_hypergraph():
    return generate_hypergraph_from_text()

@app.post("/api/hypergraph/visualization")
def get_hypergraph_png(data: HypergraphRequest):
    png = visualize_knowledge_hypergraph(data)
    if png is None:
        return Response(content="Brak danych", status_code=400)
    return Response(content=png, media_type="image/png")