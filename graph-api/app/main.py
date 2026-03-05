from fastapi import FastAPI
from langchain.langchain_graph_generation import generate_graph_from_text
from langchain.langchain_hypergraph_generation import generate_hypergraph_from_text

app = FastAPI()

@app.get("/api")
def hello():
    return {"name": "Graph API", "version": "1.0"}

@app.get("/api/graph")
def get_graph():
    return generate_graph_from_text()

@app.get("/api/hypergraph")
def get_hypergraph():
    return generate_hypergraph_from_text()