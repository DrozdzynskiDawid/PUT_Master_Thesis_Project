import xgi
import networkx as nx

def transform_to_graph_clique(H):
    G_clique = xgi.to_graph(H)
    G = nx.DiGraph(G_clique)
    for node_id, attrs in H.nodes.attrs.items():
        if node_id in G.nodes:
            G.nodes[node_id].update(attrs)
            
    for edge_id in H.edges:
        members = list(H.edges.members(edge_id))
        edge_attrs = H.edges.attrs[edge_id]
        for i in range(len(members)):
            for j in range(len(members)):
                if i != j:
                    u, v = members[i], members[j]
                    if G.has_edge(u, v):
                        G.edges[u, v].update(edge_attrs)
                        if 'relation_name' in edge_attrs and 'label' not in G.edges[u, v]:
                            G.edges[u, v]['label'] = edge_attrs['relation_name']

    return nx.node_link_data(G)

# def transform_to_graph_bipartite(H):
    # G_bipartite = xgi.to_bipartite_graph(H)
