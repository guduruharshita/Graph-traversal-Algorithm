# Graph Traversal Algorithms: BFS vs DFS

A comprehensive implementation and comparison of Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms with visualization and performance benchmarks.

## Features

- **Graph Class Implementation**: Create directed or undirected graphs
- **BFS (Breadth-First Search)**: Level-order traversal using queue
- **DFS (Depth-First Search)**: Both iterative and recursive implementations
- **Cycle Detection**: Check if a graph contains cycles
- **Performance Benchmarks**: Compare execution times of different algorithms
- **Visualization**: Visual representation using NetworkX and Matplotlib

## Usage

```python
from ADA collaborative project-1 import Graph, create_sample_graphs

# Create a graph
g = Graph()
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(2, 4)

# BFS traversal
print(g.bfs(0))  # [0, 1, 2, 3, 4]

# DFS traversal
print(g.dfs(0))  # [0, 1, 3, 2, 4]

# Check for cycles
print(g.has_cycle())  # False

# Visualize
g.visualize("My Graph")
```

## Requirements

- Python 3.x
- networkx
- matplotlib
- pandas
- IPython

## License

MIT

