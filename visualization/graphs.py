import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_node("Anna", label="Osoba")
G.add_node("TechCorp", label="Firma")
G.add_node("Warszawa", label="Miasto")
G.add_node("Python", label="Technologia")

G.add_edge("Anna", "TechCorp", relation="PRACUJE_W")
G.add_edge("TechCorp", "Warszawa", relation="MA_SIEDZIBĘ_W")
G.add_edge("Anna", "Python", relation="ZNA")


pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)


node_labels = nx.get_node_attributes(G, 'label')
color_map = {
    "Osoba": "#a0eaff",
    "Firma": "#90ee90",
    "Miasto": "#ffb347",
    "Technologia": "#d8b4f8"
}

node_colors = [color_map[node_labels[node]] for node in G.nodes()]

edge_labels = nx.get_edge_attributes(G, 'relation')

plt.figure(figsize=(12, 8))

nx.draw_networkx_nodes(G, pos,
                       node_color=node_colors,
                       node_size=3000,
                       edgecolors='black'
                      )

nx.draw_networkx_edges(G, pos,
                       arrowstyle="->",
                       arrowsize=20,
                       edge_color="gray",
                       node_size=3000
                      )

nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

nx.draw_networkx_edge_labels(G, pos,
                             edge_labels=edge_labels,
                             font_color='red',
                             font_size=10
                            )

plt.title("Wizualizacja Grafu Wiedzy w NetworkX", size=15)
plt.axis('off')
plt.show()