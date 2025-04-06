import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Example residual matrix (you can replace this with your actual matrix)
tags = ['AA', 'BB', 'CC', 'DD']
residual_matrix = np.array([
    [5, 2.5, -1.2, 0.0],
    [-0.3, 5, 3.0, 1.5],
    [0.8, -2.1, 5, 2.8],
    [1.2, 0.0, 0.0, 5]
])

# Threshold: only show significant connections
threshold = 1.96  # Typical cutoff for significance in residuals

# Create directed graph
G = nx.DiGraph()

# Add nodes
for tag in tags:
    G.add_node(tag)

# Add edges with weights if residual is significant
for i, source in enumerate(tags):
    for j, target in enumerate(tags):
        value = residual_matrix[i, j]
        if abs(value) >= threshold:
            G.add_edge(source, target, weight=value)

# Draw the graph
# pos = nx.spring_layout(G, seed=42)  # Layout algorithm
# pos = nx.spectral_layout(G)
pos = nx.spring_layout(G, iterations=100)

plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=10)

# Draw edges with labels
edge_labels = nx.get_edge_attributes(G, 'weight')
weights = [G[u][v]['weight'] for u, v in G.edges()]

# Optional: Normalize weights for better visual scaling
max_weight = max(weights)
normalized_weights = [w / max_weight * 5 for w in weights]  # scale to range 0–5 pt width

nx.draw_networkx_edges(
    G, pos,
    edge_color="gray",
    arrows=True,
    width=normalized_weights  # edge thickness based on weight
)


# nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')
nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.2f}" for k, v in edge_labels.items()}, font_color='black')

plt.title('Behavioral Sequential Analysis Graph')
plt.axis('off')
plt.show()
