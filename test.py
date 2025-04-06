import dash
import dash_cytoscape as cyto
from dash import html

app = dash.Dash(__name__)

stylesheet = [
    # Default style for all edges
    {
        "selector": "edge",
        "style": {
            "curve-style": "bezier",  # Default for directed edges
            "target-arrow-shape": "triangle",
            "width": 2,
            "line-color": "#ccc",  # Gray for ordinary edges
            "loop-direction": "0deg",  # Ignored unless a loop
            "loop-sweep": "0deg",  # Ignored unless a loop
        },
    },
    # Specific style for self-loops
    {
        "selector": "edge[data('source') == data('target')]",
        "style": {
            "curve-style": "unbundled-bezier",  # Distinct for self-loops
            "loop-direction": "45deg",  # Angle of the loop
            "loop-sweep": "90deg",  # Larger arc for visibility
            "control-point-distances": 30,  # Distance from node
            "control-point-weights": 0.5,  # Midpoint of the curve
            "width": 3,  # Thicker for self-loops
            "line-color": "#ff5555",  # Red for self-loops
            "target-arrow-shape": "none",  # Optional: remove arrow for loops
        },
    },
    # Node style
    {
        "selector": "node",
        "style": {
            "label": "data(id)",
            "width": 20,
            "height": 20,
            "background-color": "#666",
        },
    },
]

# Graph with one self-loop and one ordinary edge
elements = [
    {"data": {"id": "A"}},
    {"data": {"id": "B"}},
    {"data": {"source": "A", "target": "A"}},  # Self-loop
    {"data": {"source": "A", "target": "B"}},  # Ordinary edge
]

app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape-graph",
            elements=elements,
            stylesheet=stylesheet,
            layout={"name": "grid"},
            style={"width": "100%", "height": "500px"},
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
