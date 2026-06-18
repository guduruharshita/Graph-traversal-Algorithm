# Graph Algorithm Library

[![CI](https://github.com/guduruharshita/graph-traversal-algorithm/actions/workflows/ci.yml/badge.svg)](https://github.com/guduruharshita/graph-traversal-algorithm/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](src/graph_algo/api/main.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Production-ready **graph algorithm library** with REST API. Implements fundamental graph algorithms from scratch in pure Python with zero non-standard dependencies in the core library.

## Algorithms

| Algorithm | Module | Time | Space | Notes |
|-----------|--------|------|-------|-------|
| BFS | `traversal.py` | O(V + E) | O(V) | Level-order, unweighted |
| DFS (iterative) | `traversal.py` | O(V + E) | O(V) | Explicit stack |
| DFS (recursive) | `traversal.py` | O(V + E) | O(V) | Call-stack |
| Connected Components | `traversal.py` | O(V + E) | O(V) | Undirected graphs |
| Dijkstra | `shortest_path.py` | O((V+E)logV) | O(V) | Non-negative weights, heapq |
| Bellman-Ford | `shortest_path.py` | O(V × E) | O(V) | Negative weights + cycle detection |
| Cycle Detection | `analysis.py` | O(V + E) | O(V) | DFS colouring |
| Topological Sort | `analysis.py` | O(V + E) | O(V) | Kahn's BFS algorithm |
| SCC (Kosaraju) | `analysis.py` | O(V + E) | O(V) | Two-pass DFS + transpose |

## Quick Start

```bash
pip install -e .
```

### Library usage

```python
from graph_algo.graph import Graph
from graph_algo.algorithms.traversal import bfs, dfs_recursive
from graph_algo.algorithms.shortest_path import dijkstra, reconstruct_path
from graph_algo.algorithms.analysis import topological_sort

# Build a weighted directed graph
g = Graph.from_edge_list([
    ("A", "B", 1),
    ("A", "C", 4),
    ("B", "C", 2),
    ("B", "D", 5),
    ("C", "D", 1),
], directed=True)

# Traversal
print(bfs(g, "A"))              # ['A', 'B', 'C', 'D']

# Shortest path
dist, prev = dijkstra(g, "A")
print(dist["D"])                # 4.0
print(reconstruct_path(prev, "D"))  # ['A', 'B', 'C', 'D']

# Analysis
print(topological_sort(g))      # ['A', 'B', 'C', 'D']
```

### REST API

```bash
uvicorn graph_algo.api.main:app --reload
# Docs: http://localhost:8000/docs
```

```bash
# BFS traversal
curl -X POST http://localhost:8000/api/graph/traverse \
  -H "Content-Type: application/json" \
  -d '{"graph": {"edges": [{"u":"A","v":"B"},{"u":"B","v":"C"}]}, "start": "A", "algorithm": "bfs"}'
# {"algorithm":"bfs","start":"A","traversal_order":["A","B","C"],"nodes_visited":3}

# Dijkstra shortest path
curl -X POST http://localhost:8000/api/graph/shortest-path \
  -H "Content-Type: application/json" \
  -d '{"graph": {"edges": [{"u":"A","v":"B","weight":1},{"u":"B","v":"C","weight":3}], "directed":true}, "source":"A","target":"C","algorithm":"dijkstra"}'
# {"distance":4.0,"path":["A","B","C"]}

# Graph analysis (cycle detection, topological sort, SCC)
curl -X POST http://localhost:8000/api/graph/analyze \
  -H "Content-Type: application/json" \
  -d '{"edges": [{"u":"A","v":"B"},{"u":"B","v":"C"}], "directed": true}'
```

### Docker

```bash
docker build -t graph-algo . && docker run -p 8000:8000 graph-algo
```

## Project Structure

```
graph-traversal-algorithm/
│
├── src/graph_algo/
│   ├── graph.py                  # Weighted adjacency-list Graph class
│   ├── algorithms/
│   │   ├── traversal.py          # BFS, DFS (iterative + recursive), connected components
│   │   ├── shortest_path.py      # Dijkstra, Bellman-Ford, path reconstruction
│   │   └── analysis.py           # Cycle detection, topological sort, SCC (Kosaraju)
│   └── api/
│       ├── main.py               # FastAPI app
│       └── routers/graphs.py     # POST /api/graph/traverse, /shortest-path, /analyze
│
├── tests/
│   ├── test_traversal.py         # 9 traversal tests
│   ├── test_shortest_path.py     # 7 shortest-path tests
│   ├── test_analysis.py          # 9 analysis tests
│   └── test_api.py               # 8 API tests
│
├── .github/workflows/ci.yml
├── pyproject.toml
└── Dockerfile
```

## Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

```
tests/test_traversal.py::test_bfs_order PASSED
tests/test_traversal.py::test_dfs_iterative_visits_all PASSED
tests/test_traversal.py::test_connected_components_multiple PASSED
tests/test_shortest_path.py::test_dijkstra_distances PASSED
tests/test_shortest_path.py::test_bellman_ford_negative_weight PASSED
tests/test_shortest_path.py::test_bellman_ford_negative_cycle_raises PASSED
tests/test_analysis.py::test_topological_sort_dag PASSED
tests/test_analysis.py::test_scc_simple PASSED
tests/test_api.py::test_dijkstra_shortest_path PASSED

33 passed
```

## Skills Demonstrated

| Skill | Evidence |
|-------|---------|
| **Graph Algorithms** | BFS, DFS, Dijkstra, Bellman-Ford, topological sort, Kosaraju SCC |
| **Data Structures** | Weighted adjacency list, binary heap (heapq), deque |
| **Algorithm Design** | DFS colouring, Kahn's BFS, two-pass transpose |
| **Complexity Analysis** | Time + space complexity documented for each algorithm |
| **Python Packaging** | `pyproject.toml` with `src/` layout, zero runtime dependencies in core |
| **FastAPI** | Typed Pydantic schemas, error handling (400, 404), REST design |
| **Testing** | 33 pytest tests covering correctness, edge cases, error paths |
| **Docker** | Single-stage lean image |
| **CI/CD** | GitHub Actions lint + test pipeline |
