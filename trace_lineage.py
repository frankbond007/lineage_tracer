import argparse
import yaml
import logging
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from get_metadata import get_metadata_from_sheet
from draw_plotly_with_annotation import gen_graph_annotate
import tkinter as tk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def build_graph(metadata, final_target):
    """
    Builds a directed graph from metadata.

    Parameters:
    metadata (list): List of tuples containing source tables, target table, and transformation ID.
    final_target (str): The final target table name.

    Returns:
    networkx.DiGraph: A directed graph representing the data lineage.
    """
    graph = nx.DiGraph()
    for sources, target, transformation_id in metadata:
        for source in sources.split():
            graph.add_edge(source, target, transformation_id=transformation_id)

    final_target_label = final_target
    subgraph_nodes = nx.ancestors(graph, final_target_label) | {final_target_label}
    subgraph = graph.subgraph(subgraph_nodes).copy()

    return subgraph


def draw_graph(graph):
    """
    Draws the graph using Matplotlib with dot layout.

    Parameters:
    graph (networkx.DiGraph): The graph to draw.
    """
    root = tk.Tk()
    screen_width = root.winfo_screenmmwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    fig_width = screen_width / 100
    fig_height = screen_height / 100
    font_size = max(fig_width / 2, 12)

    pos = graphviz_layout(graph, prog='dot')
    plt.figure(figsize=(fig_width, fig_height))

    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=3000,
            edge_color='gray', linewidths=1, font_size=font_size, font_weight='bold',
            arrows=True, arrowsize=20)

    edge_labels = nx.get_edge_attributes(graph, 'transformation_id')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red', font_size=font_size)

    plt.title('Dependency graph with Transformations (Dot Layout)', size=font_size)
    plt.show()


def main(config_path):
    # Load configuration
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    input_file = config.get('input_file')
    sheet_name = config.get('sheet_name')
    final_target = config.get('final_target')

    metadata = get_metadata_from_sheet(input_file, sheet_name)
    if not metadata:
        logging.error("Failed to load metadata.")
        return

    graph = build_graph(metadata, final_target)
    draw_graph(graph)
    gen_graph_annotate(graph)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trace data lineage and visualize dependency graph.")
    parser.add_argument('-c', '--config', type=str, required=True, help="Path to the configuration file.")

    args = parser.parse_args()
    main(args.config)
