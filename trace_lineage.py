import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from get_metadata import get_metadata_from_sheet
# from draw_plotly_graph import gen_graph
from draw_plotly_with_annotation import gen_graph_annotate
import tkinter as tk


#Need to install graphviz

def build_graph(metadata, final_target):

    graph = nx.DiGraph()
    print(f"metadata: \n {metadata}")
    for sources, target, transformation_id in metadata:
        for source in sources.split():
            #Add or update the edge with transformation_id as an attribute
            graph.add_edge(source, target, transformation_id=transformation_id)
    final_target_label = final_target

    subgraph_nodes = nx.ancestors(graph, final_target_label) | {final_target_label}
    subgraph = graph.subgraph(subgraph_nodes).copy()

    return subgraph
def draw_graph(graph):
    """Draws the graph with dot layout and autoscales UI elements according to
    the screen resolution"""

    root = tk.Tk()
    screen_width = root.winfo_screenmmwidth()
    screen_height = root.winfo_screenheight()
    root.destroy() # Closing tkinter window

    #Scale figure size based on screen resolution
    fig_width = screen_width / 100
    fig_height = screen_height / 100

    #Adjust font size dynamically
    font_size = max(fig_width / 2, 12) #ensure minimum font size for readability

    # Use dot layout from graphviz
    pos = graphviz_layout(graph, prog = 'dot')

    #Create figure with dynamic size
    plt.figure(figsize=(fig_width, fig_height))

    #Draw the graph with scaled font size
    nx.draw(graph, pos, with_labels=True, node_color = 'skyblue', node_size = 3000,
            edge_color = 'gray', linewidths = 1, font_size = font_size, font_weight = 'bold',
            arrows = True, arrowsize = 20)
    #Optional: if you are displaying wdf_dt_id on edges
    edge_labels = nx.get_edge_attributes(graph, 'transformation_id')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels,font_color='red', font_size = font_size)

    plt.title('Dependency graph with Transformations (Dot Layout)', size = font_size)
    plt.show()


def draw_spring_graph(graph):
    #k: optimal distance between nodes, iterations: number of iterations for the algorithm
    pos = nx.spring_layout(graph, k = 4, iterations = 50)
    plt.figure(figsize = (20, 20)) #increase the figure size
    nx.draw_networkx_nodes(graph, pos, node_color='skyblue', node_size=500)
    nx.draw_networkx_edges(graph, pos, edge_color='gray', width=1, alpha=0.5, style='dashed',
                           connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_labels(graph, pos, font_size=8, font_family='sans-serif') #Decrease font size
    plt.title('Dependency Graph', size=20)
    plt.axis('off') # Turn off axis
    plt.show()

metadata = get_metadata_from_sheet('sample.xlsx', 'Sheet1')
final_target = "z"

graph = build_graph(metadata, final_target)
def find_unique_transformations(graph, final_target):
    def dfs(node, path, transformations, visited):
        #Avoid cycles
        if node in visited:
            return
        visited.add(node)

        #Extend path and transformations
        path.append(node)
        if node != final_target: #Skip appending transformation for the final node itself
            for _, attr in graph[node].items():
                transformation_id = attr['transformation_id']
                if transformation_id not in transformations:
                    transformations.append(transformation_id)

        #Reached final target, record the path and transformations
        if node == final_target:
            unique_transformations.add(tuple(transformations))
        else:
            for successor in graph.successors(node):
                dfs(successor, path[:], transformations[:], visited.copy())
    unique_transformations = set()
    #start DFS from nodes that have paths to the final target
    for node in nx.ancestors(graph, final_target):
        dfs(node, [], [], set())

    #Print  unique sequences of transformations
    for sequence in unique_transformations:
        print(" -> ".join(sequence))
#After building the graph
#find_unique_transformations(graph, final_target)

#Draw the graph
draw_graph(graph)
gen_graph_annotate(graph)