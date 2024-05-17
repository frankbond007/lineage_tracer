import argparse
import logging
import networkx as nx
from get_metadata import get_metadata_from_sheet, get_metadata_from_csv
from draw_plotly_with_annotation import gen_graph_annotate
from export_to_atlas_json import save_atlas_json
import tkinter as tk
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

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


def main(input_file, sheet_name, final_target, output_file, graph_type, input_type='excel'):
    logging.info("Starting the lineage tracing process...")
    if input_type == 'excel':
        metadata = get_metadata_from_sheet(input_file, sheet_name)
    elif input_type == 'csv':
        metadata = get_metadata_from_csv(input_file)
    else:
        logging.error("Invalid input type specified. Please use 'excel' or 'csv'.")
        return

    if not metadata:
        logging.error("Failed to load metadata.")
        return

    graph = build_graph(metadata, final_target)
    save_atlas_json(graph, 'my-namespace', output_file)

    if graph_type == 'matplotlib':
        draw_graph(graph)
    elif graph_type == 'plotly':
        gen_graph_annotate(graph)
    else:
        logging.error("Invalid graph type specified. Please use 'matplotlib' or 'plotly'.")
    logging.info("Lineage tracing process completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trace data lineage and export to Atlas JSON.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Path to the input Excel or CSV file.")
    parser.add_argument('-s', '--sheet', type=str,
                        help="Name of the sheet in the Excel file (required if input type is Excel).")
    parser.add_argument('-t', '--target', type=str, required=True, help="Name of the final target table.")
    parser.add_argument('-o', '--output', type=str, required=True, help="Path to the output JSON file.")
    parser.add_argument('-g', '--graph', type=str, choices=['matplotlib', 'plotly'], required=True,
                        help="Type of graph to generate (matplotlib or plotly).")
    parser.add_argument('--input-type', type=str, choices=['excel', 'csv'], default='excel',
                        help="Type of input file (excel or csv).")

    args = parser.parse_args()
    main(input_file=args.input, sheet_name=args.sheet, final_target=args.target, output_file=args.output,
         graph_type=args.graph, input_type=args.input_type)
