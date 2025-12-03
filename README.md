# Graph Traversal Algorithms — BFS & DFS

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)

A clean, well-tested Python implementation of Breadth-First Search (BFS) and Depth-First Search (DFS) with cycle detection, benchmarking, and support for directed/undirected graphs.

## What It Does

- **BFS** — level-order traversal using a queue
- **DFS** — both iterative (stack) and recursive implementations
- **Cycle Detection** — DFS-based coloring algorithm
- **Benchmarking** — microsecond-level performance comparison
- **Modular package** — importable `graph_traversal` module with full test coverage

## Project Structure

```
├── graph_traversal/
│   ├── __init__.py
│   ├── graph.py          # Graph class (directed/undirected)
│   └── algorithms.py     # BFS, DFS, cycle detection
├── tests/
│   └── test_graph.py     # Unit tests
├── main.py               # Demo runner with benchmarks
└── requirements.txt
```

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

**Sample output:**
```
=== Tree (no cycle) ===
  BFS:           [0, 1, 2, 3, 4, 5, 6]
  DFS Iterative: [0, 1, 3, 4, 2, 5, 6]
  Has cycle:     False

=== Benchmarks (µs per call) ===
  BFS                1.82 µs
  DFS Iterative      2.14 µs
  DFS Recursive      2.31 µs
```

## Usage

```python
from graph_traversal import Graph, bfs, dfs_iterative, has_cycle

g = Graph()
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)

print(bfs(g, 0))           # [0, 1, 2, 3]
print(dfs_iterative(g, 0)) # [0, 1, 3, 2]
print(has_cycle(g))        # False
```

## Tests

```bash
python tests/test_graph.py
```

## Author

**Harshita Guduru** — [GitHub](https://github.com/guduruharshita) · [LinkedIn](https://linkedin.com/in/harshita-guduru)
