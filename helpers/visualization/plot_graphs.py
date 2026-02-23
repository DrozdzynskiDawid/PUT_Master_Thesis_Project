import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def visualize_knowledge_graph(graph_doc, sentence_index):
    if not graph_doc.nodes and not graph_doc.relationships:
        print("Brak danych do narysowania grafu.")
        return

    G = nx.DiGraph()
    node_types = {}
    for node in graph_doc.nodes:
        G.add_node(node.id)
        node_types[node.id] = node.type
    for rel in graph_doc.relationships:
        G.add_edge(rel.source.id, rel.target.id, label=rel.type)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42, k=2.0) 
    unique_types = list(set(node_types.values()))
    cmap = plt.get_cmap('tab10')
    type_to_color = {t: cmap(i % 10) for i, t in enumerate(unique_types)}
    node_colors = [type_to_color[node_types[node_id]] for node_id in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=3000, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", font_family="sans-serif")
    nx.draw_networkx_edges(
        G, pos, 
        edge_color='gray', 
        width=1.5, 
        arrows=True, 
        arrowsize=25, 
        node_size=3000,
        connectionstyle='arc3, rad=0.1'
    )
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, font_color='red')

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label=t, 
               markerfacecolor=type_to_color[t], markersize=12, markeredgecolor='black') 
        for t in unique_types
    ]
    plt.legend(handles=legend_elements, title="Typy węzłów", loc="best", fontsize=10, title_fontsize=11)

    plt.title(f"Graf wiedzy z tekstu #{sentence_index + 1}", fontsize=14, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()