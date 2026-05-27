import matplotlib.pyplot as plt
import io
import xgi
import numpy as np

def visualize_knowledge_hypergraph(json_data):
    if not json_data.nodes and not json_data.hyperedges:
        print("Brak danych do narysowania hipergrafu.")
        return

    H = xgi.Hypergraph()

    for node in json_data.nodes:
        H.add_node(node.id, type=node.type)

    for edge in json_data.hyperedges:
        valid_nodes = [n for n in edge.connected_nodes if n in H.nodes]
        if valid_nodes:
            H.add_edge(valid_nodes, relation=edge.relation_name)
            
    fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
    pos = xgi.barycenter_spring_layout(H)

    node_types = {node_id: H.nodes[node_id]['type'] for node_id in H.nodes}
    unique_classes = sorted(list(set(node_types.values())))
    color_palette = plt.colormaps.get_cmap('Set3')
    
    div = max(1, len(unique_classes) - 1)
    class_to_color = {
        cls: color_palette(i / div if len(unique_classes) > 1 else 0.5) 
        for i, cls in enumerate(unique_classes)
    }

    node_colors = [class_to_color[node_types[node]] for node in H.nodes]

    xgi.draw(
        H, 
        pos=pos, 
        node_labels=True,
        node_size=70,
        node_lw=1.5,
        node_fc=node_colors,
        edge_fc="gray",
        edge_lw=1.5
    )

    for edge_id in H.edges:
        edge_members = H.edges.members(edge_id)
        relation_label = H.edges[edge_id].get('relation', '')
        
        if relation_label and edge_members:
            coords = np.array([pos[node] for node in edge_members if node in pos])
            if len(coords) > 0:
                centroid = coords.mean(axis=0)
                plt.text(
                    centroid[0], centroid[1], 
                    relation_label, 
                    fontsize=9, 
                    color='darkred', 
                    fontweight='bold',
                    ha='center', va='center',
                    bbox=dict(facecolor='white', alpha=0.85, edgecolor='lightgray', boxstyle='round,pad=0.3')
                )
    for cls in unique_classes:
        ax.scatter([], [], c=[class_to_color[cls]], label=cls, edgecolors='black')

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

    plt.title("Wizualizacja Hipergrafu Wiedzy", fontsize=16, fontweight='bold', pad=15)
    plt.axis('off')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    
    return buf.getvalue()