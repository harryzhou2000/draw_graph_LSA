import plotly.graph_objects as go
import networkx as nx
import numpy as np
from gseq_read import gseq_read_res_mat

# Example residual matrix (you can replace this with your actual matrix)
tags = ["AA", "BB", "CC", "DD"]
residual_matrix = np.array(
    [[5, 2.5, -1.2, 0.0], [-0.3, 5, 3.0, 1.5], [0.8, -2.1, 5, 2.8], [1.2, 0.0, 0.0, 5]]
)

tags, residual_matrix = gseq_read_res_mat("gseq_out_0.txt")

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

# Convert NetworkX graph to Plotly graph
edge_x = []
edge_y = []
edge_weight = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]["pos"]
    x1, y1 = G.nodes[edge[1]]["pos"]
    edge_x.append(x0)
    edge_y.append(y0)
    edge_x.append(x1)
    edge_y.append(y1)
    edge_weight.append(G[edge[0]][edge[1]]["weight"])

# Create edges plot
edges_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=1, color="gray", shape="spline"),
    hoverinfo="none",
    mode="lines+text",
)

# Plot nodes (customize as needed)
node_x = [G.nodes[node]["pos"][0] for node in G.nodes()]
node_y = [G.nodes[node]["pos"][1] for node in G.nodes()]
node_text = list(G.nodes())
node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    text=node_text,
    marker=dict(color="blue", size=15),
    textposition="bottom center",
)

# Create the layout for the Plotly figure
fig = go.Figure(
    data=[edges_trace, node_trace],
    layout=go.Layout(
        title="Directed Graph",
        showlegend=False,
        hovermode="closest",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    ),
)

# Display the figure
fig.show()
