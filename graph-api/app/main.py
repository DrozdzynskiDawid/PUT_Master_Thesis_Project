import os

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
from app.experiment_result_model import ExperimentDetail
import xgi
import numpy as np
import networkx as nx
import time

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

@app.get("/api/experiment")
def run_full_experiment(file_path: str, count: int = 100, measure_time: bool = False):
    results = []
    similarities = []
    if measure_time:
        times_graph = []
        times_hypergraph = []
        for i in range(count):
            try:
                sentence = get_random_sentence(file_path)
                start_graph_time = time.perf_counter()
                graph_direct_raw = generate_graph_from_text(sentence)
                end_graph_time = time.perf_counter()
                times_graph.append(end_graph_time - start_graph_time)

                start_hypergraph_time = time.perf_counter()
                hypergraph_raw = generate_hypergraph_from_text(sentence)
                end_hypergraph_time = time.perf_counter()
                times_hypergraph.append(end_hypergraph_time - start_hypergraph_time)
            except Exception as e:
                print(f"Błąd w iteracji {i}: {e}")
                import traceback
                traceback.print_exc()
                continue
        return {
            "dataset": file_path,
            "total_samples": len(times_graph),
            "times_graph": times_graph,
            "times_hypergraph": times_hypergraph,
            "average_graph_time": float(np.mean(times_graph)) if times_graph else 0,
            "average_hypergraph_time": float(np.mean(times_hypergraph)) if times_hypergraph else 0,
            "model_name": os.getenv("MODEL_NAME"),
        }
    else:
        for i in range(count):
            try:
                sentence = get_random_sentence(file_path)
                def ensure_model(data):
                    if isinstance(data, NodeLinkGraphModel):
                        return data
                    return NodeLinkGraphModel(**data)
                graph_direct_raw = generate_graph_from_text(sentence)
                model_direct = ensure_model(graph_direct_raw)

                hypergraph_raw = generate_hypergraph_from_text(sentence)
                
                if not graph_direct_raw or not hypergraph_raw:
                    continue

                graph_transformed_raw = transform_to_graph_selected_clique(hypergraph_raw)
                H = xgi.Hypergraph()
                for node in hypergraph_raw.nodes:
                    H.add_node(node.id, type=node.type)
                for edge in hypergraph_raw.hyperedges:
                    valid_nodes = [n for n in edge.connected_nodes if n in H.nodes]
                    if valid_nodes:
                        H.add_edge(valid_nodes, relation=edge.relation_name)
                graph_clique_transformed_raw = transform_to_graph_clique(H)



                model_transformed = ensure_model(graph_transformed_raw)
                model_clique_transformed = ensure_model(graph_clique_transformed_raw)

                stats_direct = get_graph_stats(model_direct)
                stats_transformed = get_graph_stats(model_transformed)
                stats_clique_transformed = get_graph_stats(model_clique_transformed)
                
                similarity_result = get_graph_similarity(
                    model_direct.model_dump(), 
                    model_clique_transformed.model_dump()
                )
                
                if isinstance(similarity_result, dict):
                    sim_value = similarity_result.get("cosine_similarity", 0)
                else:
                    sim_value = getattr(similarity_result, "cosine_similarity", 0)
                
                similarities.append(sim_value)
                
                results.append(ExperimentDetail(
                    id=i,
                    text=sentence,
                    stats_direct=dict(stats_direct),
                    stats_transformed=dict(stats_transformed),
                    stats_clique_transformed=dict(stats_clique_transformed),
                    similarity=sim_value,
                    graph_edit_distance=float(nx.graph_edit_distance(
                        nx.node_link_graph(model_direct.model_dump(), edges="links"), 
                        nx.node_link_graph(model_clique_transformed.model_dump(), edges="links")
                    ))
                ))
                
            except Exception as e:
                print(f"Błąd w iteracji {i}: {e}")
                import traceback
                traceback.print_exc()
                continue

        report = {
            "dataset": file_path,
            "total_samples": len(results),
            "average_similarity": float(np.mean(similarities)) if similarities else 0,
            "standard_deviation": float(np.std(similarities)) if similarities else 0,
            "details": [res.model_dump() for res in results]
        }

        with open("experiment_results.json", "w", encoding='utf-8') as f:
            import json
            json.dump(report, f, ensure_ascii=False, indent=4)

        return report