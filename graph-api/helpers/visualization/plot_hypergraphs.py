import matplotlib.pyplot as plt
import xgi
import numpy as np

from helpers.transformation import visualize_transformations

def visualize_knowledge_hypergraph(result):
    if not result.nodes and not result.hyperedges:
        print("Brak danych do narysowania hipergrafu.")
        return

    H = xgi.Hypergraph()

    for node in result.nodes:
        H.add_node(node.id, type=node.type)

    for edge in result.hyperedges:
        valid_nodes = [n for n in edge.connected_nodes if n in H.nodes]
        if valid_nodes:
            H.add_edge(valid_nodes, relation=edge.relation_name)
            
    plt.figure(figsize=(10, 8), dpi=100)
    pos = xgi.barycenter_spring_layout(H)

    xgi.draw(
        H, 
        pos=pos, 
        node_labels=True,
        node_size=70,
        node_lw=1.5,
        node_fc="lightblue",
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

    plt.title("Wizualizacja Hipergrafu Wiedzy", fontsize=16, fontweight='bold', pad=15)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    visualize_transformations(H)