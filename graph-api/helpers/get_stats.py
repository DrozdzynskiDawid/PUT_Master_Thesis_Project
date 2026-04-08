import networkx as nx
from app.graph_request_model import NodeLinkGraphModel

def get_graph_stats(data: NodeLinkGraphModel):
    G = nx.node_link_graph(data.model_dump(), edges="links")

    return {
        "nodes_count": G.number_of_nodes(),
        "edges_count": G.number_of_edges(),
        "density": nx.density(G),
        "average_degree": sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0,
        "degree_histogram": nx.degree_histogram(G),
        "is_connected": nx.is_weakly_connected(G),
        # "average_shortest_path_length": nx.average_shortest_path_length(G) if not nx.is_weakly_connected(G) else None,
    }