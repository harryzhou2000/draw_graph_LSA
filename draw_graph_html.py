import dash
from dash import html
import dash_cytoscape as cyto
import numpy as np
import math

# Example tag names and residual matrix
tag_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
nTag = len(tag_names)
# Example residual matrix (numpy array)
residual_matrix = np.array([[5, 2, -1, 0], [0, 5, 3, 1], [-2, 0, 5, 4], [1, 0, 0, 5]])

np.random.seed(13)
residual_matrix = (
    np.random.random(
        (nTag, nTag),
    )
    - 0.8
)
fname = "gseq_out_18_01.txt"
# fname = "gseq_out_19_03.txt"
# fname = "gseq_out_20_02.txt"

from gseq_read import gseq_read_res_mat

tag_names, residual_matrix = gseq_read_res_mat(fname)
residual_matrix[residual_matrix < 1.96] = -1
print(tag_names)

node_positions = None
# node_positions = {
#     k: {"x": 100 * i + 50, "y": 100 * i + 50} for i, k in enumerate(tag_names)
# }
layout = "cose"
# layout = "grid"
layout = "circle"


# Normalize residuals for edge thickness (optional)
def normalize(value, min_val, max_val, min_size=1, max_size=4):
    # Avoid division by zero
    if max_val - min_val == 0:
        return (min_size + max_size) / 2
    portion = (value - min_val) / (max_val - min_val)
    portion = min(portion, 1)
    portion = max(portion, 0)
    return min_size + (max_size - min_size) * portion


# Find min and max residuals (only positive)
positive_values = residual_matrix[residual_matrix > 0]
# min_residual = positive_values.min() if positive_values.size > 0 else 1
# max_residual = positive_values.max() if positive_values.size > 0 else 1
min_residual = 1.96
max_residual = 4


name2class = {
    "CG": "TC",
    "PT": "TC",
    "CN": "TC",
    "QM": "TC",
    "CE": "AR",
    "AQ": "AR",
    "AA": "AR",
    "RR": "AR",
    "OE": "ER",
    "PR": "ER",
    "TL": "OT",
    "OC": "OT",
}

# Create nodes


def get_node_dict(tag):
    return {"data": {"id": tag, "label": tag}, "classes": name2class[tag]}


if node_positions is not None:
    nodes = [
        get_node_dict(tag) + {"position": node_positions[tag]} for tag in tag_names
    ]
else:
    nodes = [get_node_dict(tag) for tag in tag_names]

# Create edges for positive residuals
edges = []
for i, source in enumerate(tag_names):
    for j, target in enumerate(tag_names):
        value = residual_matrix[i, j]
        if value > 0:
            thickness = normalize(value, min_residual, max_residual)
            edges.append(
                {
                    "data": {
                        "source": source,
                        "target": target,
                        "label": f"{value:.2f}",
                        "width": thickness,
                    }
                }
            )

# App layout
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape-graph",
            # layout={'name': 'circle'},
            # layout={'name': 'grid'},
            layout={
                "name": "preset" if node_positions is not None else layout,
                "radius": 150,  # Adjust the radius of the circle (larger = more spread out)
                "nodeSpacing": 35,  # Adjust spacing between nodes
            },
            style={"width": "100%", "height": "800px"},
            elements=nodes + edges,
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "label": "data(label)",
                        "width": "50px",
                        "height": "50px",
                        "background-color": "#1f77b4",
                        "color": "#000",
                        "text-valign": "center",
                        "text-halign": "center",
                        "font-size": "16px",
                        "border-color": "#606060",  # Border (edge) color of the node
                        "border-width": "3px",  # Border width of the node
                    },
                },
                {
                    "selector": ".AR",
                    "style": {"background-color": "#C6E0B4"},
                },
                {
                    "selector": ".TC",
                    "style": {"background-color": "#FFE699"},
                },
                {
                    "selector": ".ER",
                    "style": {"background-color": "#EAAFE9"},
                },
                {
                    "selector": ".OT",
                    "style": {"background-color": "#DBDBDB"},
                },
                {
                    "selector": "edge",
                    "style": {
                        "curve-style": "unbundled-bezier",
                        # "curve-style": "taxi",
                        "control-point-step-size": 20,
                        "target-arrow-shape": "triangle",
                        "arrow-scale": 1,
                        "line-color": "#ff7f0e",
                        "target-arrow-color": "#ff7f0e",
                        "label": "data(label)",
                        "width": "data(width)",  # <--- Thickness from data
                        "font-size": "12px",
                        "color": "#ff1f2e",
                        "text-background-color": "#ffffff",
                        "text-background-opacity": 0,
                        "text-background-shape": "roundrectangle",
                        "text-margin-y": -5,
                    },
                },
                {
                    "selector": "edge:loop",  #!
                    "style": {
                        "curve-style": "unbundled-bezier",
                        "loop-direction": "0deg",
                        "loop-sweep": "45deg",
                        "control-point-step-size": 40,
                        "line-color": "#000000",
                        "target-arrow-shape": "triangle",
                        "target-arrow-color": "#000000",
                        "arrow-scale": 1,
                        "width": "data(width)",
                        "label": "data(label)",
                        "font-size": "10px",
                        "color": "#000",
                        "text-background-color": "#ffffff",
                        "text-background-opacity": 0,
                        "text-background-shape": "roundrectangle",
                        "text-margin-y": 10,
                    },
                },
            ],
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
