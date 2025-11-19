import json
import hypernetx as hnx
import matplotlib.pyplot as plt

# Przykładowe dane hipergrafu w formacie JSON
json_data = """
{
  "Spotkanie1": ["Anna", "Piotr", "Maria"],
  "ProjektA": ["Anna", "Tomek", "Zofia"],
  "Spotkanie2": ["Piotr", "Tomek", "Adam"],
  "Briefing": ["Maria", "Zofia"]
}
"""

data_dict = json.loads(json_data)
H = hnx.Hypergraph(data_dict)

plt.figure(figsize=(10, 7))

hnx.draw(H)

plt.title("Wizualizacja Hipergrafu")
plt.show()