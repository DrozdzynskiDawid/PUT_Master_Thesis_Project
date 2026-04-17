import io
import networkx as nx
import matplotlib.pyplot as plt
from app.graph_request_model import NodeLinkGraphModel

def visualize_knowledge_graph(data: NodeLinkGraphModel):
    if not data or not data.nodes:
        print("Brak danych do narysowania grafu.")
        return None

    G = nx.node_link_graph(data.model_dump(), edges="links")
    node_types = nx.get_node_attributes(G, 'type')
    fig, ax = plt.subplots(figsize=(12, 9))
    pos = nx.spring_layout(G, seed=42, k=2.0) 
    unique_classes = sorted(list(set(node_types.values())))
    color_palette = plt.cm.get_cmap('Set3', len(unique_classes))
    
    class_to_color = {cls: color_palette(i) for i, cls in enumerate(unique_classes)}

    for cls in unique_classes:
        node_list = [n for n in G.nodes() if node_types[n] == cls]
        nx.draw_networkx_nodes(
            G, pos, 
            nodelist=node_list,
            node_color=[class_to_color[cls]], 
            node_size=3000, 
            edgecolors='black',
            label=cls
        )

    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    nx.draw_networkx_edges(
        G, pos, 
        edge_color='gray', 
        width=1.5, 
        arrows=True, 
        arrowsize=25, 
        node_size=3000,
        connectionstyle='arc3, rad=0.1'
    )
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='black')
    leg = plt.legend(
        scatterpoints=1, 
        labelspacing=1.2, 
        title="Klasy węzłów", 
        loc='upper left', 
        bbox_to_anchor=(1, 1),
        fontsize=9
    )

    for handle in leg.legend_handles:
        handle.set_sizes([100.0])

    plt.title("Graf wiedzy", fontsize=14, pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    
    return buf.getvalue()