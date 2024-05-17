
# Data Lineage Tracing Application

## Overview
This application traces the lineage of data tables using metadata from an Excel sheet and visualizes the dependency graph using both Matplotlib and Plotly. It includes functionalities to build the graph, draw it using different layouts, and annotate it with transformation IDs.

## Files
- **`get_metadata.py`**: Contains the function to extract metadata from an Excel sheet.
- **`trace_lineage.py`**: Main script to build the dependency graph, draw it using Matplotlib, and find unique transformations.
- **`draw_plotly_with_annotation.py`**: Contains the function to draw the dependency graph using Plotly with annotations.

## Installation
To run this application, you need the following Python packages. You can install them using the `requirements.txt` file:
```sh
pip install -r requirements.txt
```

You also need to install Graphviz:
- On Ubuntu:
  ```sh
  sudo apt-get install graphviz
  ```
- On macOS:
  ```sh
  brew install graphviz
  ```
- On Windows, download and install Graphviz from [here](https://graphviz.org/download/).

## Usage

### Step 1: Extract Metadata
Use the `get_metadata.py` script to extract metadata from an Excel sheet. The metadata includes source tables, target tables, and transformation IDs.

#### Example:
```python
from get_metadata import get_metadata_from_sheet

metadata = get_metadata_from_sheet('sample.xlsx', 'Sheet1')
```

### Step 2: Trace Lineage and Draw Graphs
Use the `trace_lineage.py` script to build the dependency graph and visualize it using both Matplotlib and Plotly.

#### Example:
```python
import networkx as nx
from trace_lineage import build_graph, draw_graph
from get_metadata import get_metadata_from_sheet

metadata = get_metadata_from_sheet('sample.xlsx', 'Sheet1')
final_target = "p"
graph = build_graph(metadata, final_target)
draw_graph(graph)
```

### Step 3: Draw Plotly Graph with Annotations
Use the `draw_plotly_with_annotation.py` script to draw the dependency graph using Plotly with transformation ID annotations.

#### Example:
```python
from draw_plotly_with_annotation import gen_graph_annotate

gen_graph_annotate(graph)
```

## Example Workflow
1. Prepare an Excel file `sample.xlsx` with a sheet named `Sheet1` containing columns: `source_tables`, `target_table`, `transformation_id`.
2. Use `get_metadata.py` to extract metadata.
3. Use `trace_lineage.py` to build and visualize the dependency graph using Matplotlib.
4. Use `draw_plotly_with_annotation.py` to visualize the graph with Plotly.

5. Specify the configuration file and run the script using the command line:
```sh
python trace_lineage.py -c config.yaml
```

## Visual Example
Here is an example of a matplotlib dependency graph:

![Dependency Graph Example](samples/mplt_lib_example.png)

Here is an example of a plotly dependency graph:

![Dependency Graph Example](samples/plotly_example.png)
## License
This project is licensed under the MIT License.

## Acknowledgements
- [NetworkX](https://networkx.github.io/)
- [Matplotlib](https://matplotlib.org/)
- [Plotly](https://plotly.com/)
- [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)
- [PyYAML](https://pyyaml.org/)
