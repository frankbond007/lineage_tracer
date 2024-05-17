import plotly.graph_objs as go
from networkx.drawing.nx_pydot import graphviz_layout

def gen_graph_annotate(graph):
    pos = graphviz_layout(graph, prog='dot')

    # Prepare for edge & node traces
    edge_x = []
    edge_y = []
    annotations = []  # to hold edge annotations

    # Process edges to collect edge traces and prepare annotations
    for edge in graph.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]  # Define edge trace points
        edge_y += [y0, y1, None]

        # Calculate mid-point of the edge for placing the annotation
        mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
        transformation_id = edge[2].get('transformation_id', 'N/A')  # Get transformation_id for the edge
        annotations.append(dict(x=mid_x, y=mid_y, xref="x", yref="y",
                                text=transformation_id, showarrow=False, font=dict(size=10)))

    # Define edge trace
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=2, color='#888'),
                            hoverinfo='none', mode='lines')

    # Node trace setup
    node_x = []
    node_y = []
    node_text = []

    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f'<b>{node}</b>')

    node_trace = go.Scatter(x=node_x, y=node_y, text=node_text, mode='markers+text',
                            hoverinfo='text', textposition='top center',
                            marker=dict(showscale=True, colorscale='YlGnBu',
                                        reversescale=True, color=[], size=10,
                                        colorbar=dict(thickness=15,
                                                      title='Node Connections',
                                                      xanchor='left',
                                                      titleside='right'),
                                        line=dict(width=2)))

    # Create a figure and add annotations
    fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
        title='<br>Network graph made with Python',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        annotations=annotations + [{
            'text': "Python networkx library",
            'showarrow': False,
            'xref': "paper", 'yref': "paper",
            'x': 0.005, 'y': -0.002

        }],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    ))

    fig.show()
