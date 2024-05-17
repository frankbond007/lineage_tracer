import json
import networkx as nx


def graph_to_atlas(graph, namespace):
    """
    Converts a NetworkX graph to Atlas JSON format.

    Parameters:
    graph (networkx.DiGraph): The graph to convert.
    namespace (str): The namespace for the Atlas entities.

    Returns:
    dict: The Atlas JSON data.
    """
    entities = []
    relationships = []

    def create_entity(name, typeName="Table"):
        return {
            "typeName": typeName,
            "attributes": {
                "qualifiedName": f"{namespace}.{name}",
                "name": name
            }
        }

    def create_process(name, inputs, outputs):
        return {
            "typeName": "Process",
            "attributes": {
                "qualifiedName": f"{namespace}.{name}",
                "name": name,
                "inputs": inputs,
                "outputs": outputs,
                "operationType": "TRANSFORM"
            }
        }

    for node in graph.nodes:
        entities.append(create_entity(node))

    for source, target, data in graph.edges(data=True):
        transformation_id = data.get('transformation_id', 'transformation')
        process_name = f"{source}_to_{target}_{transformation_id}"
        inputs = [{"uniqueAttributes": {"qualifiedName": f"{namespace}.{source}"}}]
        outputs = [{"uniqueAttributes": {"qualifiedName": f"{namespace}.{target}"}}]
        entities.append(create_process(process_name, inputs, outputs))

    return {
        "entities": entities,
        "relationships": relationships
    }


def save_atlas_json(graph, namespace, output_file):
    """
    Saves the Atlas JSON data to a file.

    Parameters:
    graph (networkx.DiGraph): The graph to convert.
    namespace (str): The namespace for the Atlas entities.
    output_file (str): The file to save the JSON data to.
    """
    atlas_data = graph_to_atlas(graph, namespace)
    with open(output_file, 'w') as f:
        json.dump(atlas_data, f, indent=2)

# Example usage:
# graph = build_graph(metadata, final_target)
# save_atlas_json(graph, 'my-namespace', 'lineage.json')
