# Graph Algorithm Library

[![CI](https://github.com/guduruharshita/graph-traversal-algorithm/actions/workflows/ci.yml/badge.svg)](https://github.com/guduruharshita/graph-traversal-algorithm/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](src/graph_algo/api/main.py)
[![Algorithms](https://img.shields.io/badge/Algorithms-9-brightgreen?logo=python)](src/graph_algo/algorithms/)
[![Tests](https://img.shields.io/badge/Tests-33%20passing-success?logo=pytest)](tests/)
[![Zero Dependencies](https://img.shields.io/badge/Core-Zero%20Dependencies-blue)](pyproject.toml)

Production-ready **graph algorithm library** with REST API. Implements 9 fundamental graph algorithms from scratch in pure Python — zero non-standard dependencies in the core library.

---

## Why This Library

Graph algorithms are the backbone of real systems: GPS routing uses Dijkstra, social network friend-of-friend queries use BFS, build tools use topological sort, and compiler dataflow analysis uses Kosaraju SCC. Most Python developers reach for `networkx` without understanding what's underneath. This library implements each algorithm from first principles so the mechanics are fully transparent and auditable — useful for learning, technical interviews, and as a reference implementation.

---

## Architecture

```
┌────────────────────────────────────────────────────────┐
│                  Graph Algorithm Library                 │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              graph.py (Core)                     │   │
│  │  Graph(directed, weighted)                       │   │
│  │  Weighted adjacency list: dict[node, list[Edge]] │   │
│  │  from_edge_list() · add_edge() · neighbors()     │   │
│  └───────────────┬──────────────────────────────────┘   │
│                  │                                       │
│  ┌───────────────▼──────────────────────────────────┐   │
│  │           algorithms/                            │   │
│  │  ┌─────────────┐ ┌──────────────┐ ┌───────────┐ │   │
│  │  │traversal.py │ │shortest_path │ │analysis.py│ │   │
│  │  │  BFS        │ │  Dijkstra    │ │  has_cycle│ │   │
│  │  │  DFS iter   │ │  Bellman-Ford│ │  topo_sort│ │   │
│  │  │  DFS recur  │ │  reconstruct │ │  SCC      │ │   │
│  │  │  conn comps │ │  _path()     │ │(Kosaraju) │ │   │
│  │  └─────────────┘ └──────────────┘ └───────────┘ │   │
│  └───────────────┬──────────────────────────────────┘   │
│                  │                                       │
│  ┌───────────────▼──────────────────────────────────┐   │
│  │           api/ (FastAPI REST Layer)              │   │
│  │  POST /api/graph/traverse                        │   │
│  │  POST /api/graph/shortest-path                   │   │
│  │  POST /api/graph/analyze                         │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```

---

## Algorithms

| Algorithm | Module | Time | Space | Notes |
|-----------|--------|------|-------|-------|
| BFS | `traversal.py` | O(V + E) | O(V) | Level-order, unweighted shortest path |
| DFS (iterative) | `traversal.py` | O(V + E) | O(V) | Explicit stack, avoids recursion limit |
| DFS (recursive) | `traversal.py` | O(V + E) | O(V) | Clean call-stack implementation |
| Connected Components | `traversal.py` | O(V + E) | O(V) | Undirected graphs via BFS |
| Dijkstra | `shortest_path.py` | O((V+E) log V) | O(V) | Binary heap (`heapq`), non-negative weights |
| Bellman-Ford | `shortest_path.py` | O(V × E) | O(V) | Negative weights + negative-cycle detection |
| Cycle Detection | `analysis.py` | O(V + E) | O(V) | DFS 3-colour (WHITE/GRAY/BLACK) |
| Topological Sort | `analysis.py` | O(V + E) | O(V) | Kahn's BFS — detects non-DAG graphs |
| SCC (Kosaraju) | `analysis.py` | O(V + E) | O(V) | Two-pass DFS on original + transposed graph |

### Algorithm Selection Guide

```
Need to visit all nodes?
├── Unweighted / level-by-level → BFS
└── Depth-first exploration     → DFS

Need shortest paths?
├── All weights ≥ 0 → Dijkstra     O((V+E) log V)
└── Negative weights / cycle check → Bellman-Ford  O(V·E)

Need to understand graph structure?
├── Has a cycle?               → has_cycle()       O(V+E)
├── Processing order for deps? → topological_sort() O(V+E)  (DAG only)
└── Clusters of mutual reach?  → scc_kosaraju()    O(V+E)
```

---

## Quick Start

```bash
pip install -e .
```

### Library Usage

```python
from graph_algo.graph import Graph
from graph_algo.algorithms.traversal import bfs, dfs_recursive
from graph_algo.algorithms.shortest_path import dijkstra, reconstruct_path
from graph_algo.algorithms.analysis import topological_sort, scc_kosaraju

# Build a weighted directed graph
g = Graph.from_edge_list([
    ("A", "B", 1),
    ("A", "C", 4),
    ("B", "C", 2),
    ("B", "D", 5),
    ("C", "D", 1),
], directed=True)

# Traversal
print(bfs(g, "A"))                     # ['A', 'B', 'C', 'D']
print(dfs_recursive(g, "A"))           # ['A', 'B', 'C', 'D']

# Shortest path — Dijkstra
dist, prev = dijkstra(g, "A")
print(dist["D"])                        # 4.0  (A→B→C→D)
print(reconstruct_path(prev, "D"))      # ['A', 'B', 'C', 'D']

# Strongly Connected Components
g2 = Graph.from_edge_list([("A","B"),("B","C"),("C","A"),("C","D")], directed=True)
print(scc_kosaraju(g2))                 # [{'A','B','C'}, {'D'}]
```

### REST API

```bash
uvicorn graph_algo.api.main:app --reload
# Interactive docs: http://localhost:8000/docs
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
  -d '{
    "graph": {"edges": [{"u":"A","v":"B","weight":1},{"u":"B","v":"C","weight":3}], "directed":true},
    "source": "A", "target": "C", "algorithm": "dijkstra"
  }'
# {"distance":4.0,"path":["A","B","C"]}

# Full graph analysis — cycle detection + topological sort + SCC
curl -X POST http://localhost:8000/api/graph/analyze \
  -H "Content-Type: application/json" \
  -d '{"edges": [{"u":"A","v":"B"},{"u":"B","v":"C"}], "directed": true}'
# {"has_cycle":false,"topological_order":["A","B","C"],"strongly_connected_components":[["A"],["B"],["C"]]}
```

### Docker

```bash
docker build -t graph-algo . && docker run -p 8000:8000 graph-algo
```

---

## Project Structure

```
graph-traversal-algorithm/
│
├── src/graph_algo/
│   ├── graph.py                  # Weighted adjacency-list Graph class
│   ├── algorithms/
│   │   ├── traversal.py          # BFS, DFS (iterative + recursive), connected_components
│   │   ├── shortest_path.py      # Dijkstra (heapq), Bellman-Ford, reconstruct_path
│   │   └── analysis.py           # has_cycle (DFS 3-colour), topological_sort (Kahn's),
│   │                             # scc_kosaraju (two-pass DFS + transpose)
│   └── api/
│       ├── main.py               # FastAPI app factory + lifespan
│       └── routers/graphs.py     # POST /traverse, /shortest-path, /analyze
│
├── tests/
│   ├── test_traversal.py         # 9 tests — order, disconnected graphs, cycles
│   ├── test_shortest_path.py     # 7 tests — Dijkstra distances, Bellman-Ford negative weights
│   ├── test_analysis.py          # 9 tests — cycle detection, topo sort, SCC components
│   └── test_api.py               # 8 API integration tests
│
├── .github/workflows/ci.yml      # Ruff lint + pytest on every push
├── pyproject.toml                # src/ layout, zero runtime deps in core
└── Dockerfile
```

---

## Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

```
tests/test_traversal.py::test_bfs_order PASSED
tests/test_traversal.py::test_bfs_disconnected_visits_only_component PASSED
tests/test_traversal.py::test_dfs_iterative_visits_all PASSED
tests/test_traversal.py::test_dfs_recursive_visits_all PASSED
tests/test_traversal.py::test_connected_components_multiple PASSED
tests/test_shortest_path.py::test_dijkstra_distances PASSED
tests/test_shortest_path.py::test_dijkstra_reconstruct_path PASSED
tests/test_shortest_path.py::test_bellman_ford_negative_weight PASSED
tests/test_shortest_path.py::test_bellman_ford_negative_cycle_raises PASSED
tests/test_analysis.py::test_cycle_detection_cyclic PASSED
tests/test_analysis.py::test_cycle_detection_acyclic PASSED
tests/test_analysis.py::test_topological_sort_dag PASSED
tests/test_analysis.py::test_topological_sort_cycle_raises PASSED
tests/test_analysis.py::test_scc_simple PASSED
tests/test_analysis.py::test_scc_all_separate PASSED
tests/test_api.py::test_bfs_traversal PASSED
tests/test_api.py::test_dfs_traversal PASSED
tests/test_api.py::test_dijkstra_shortest_path PASSED
tests/test_api.py::test_analyze_acyclic PASSED

33 passed in 0.8s
```

---

## Real-World Applications

| Algorithm | Where It's Used |
|-----------|----------------|
| **BFS** | Shortest path in unweighted networks, level-order tree processing, web crawlers |
| **DFS** | Maze solving, topological sort pre-computation, detecting back-edges |
| **Dijkstra** | GPS routing (Google Maps), network packet routing (OSPF), game pathfinding (A* variant) |
| **Bellman-Ford** | Currency arbitrage detection, routing protocols with negative-weight links (BGP) |
| **Topological Sort** | Build systems (Make, Gradle), task scheduling, import dependency resolution |
| **Kosaraju SCC** | Compiler dead-code analysis, web page link clustering, social network community detection |

---

## Skills Demonstrated

| Skill | Evidence |
|-------|---------|
| **Graph Algorithms** | BFS, DFS (×2), Dijkstra, Bellman-Ford, cycle detection, topological sort, Kosaraju SCC |
| **Data Structures** | Weighted adjacency list, binary heap (`heapq`), deque, DFS 3-colour state |
| **Algorithm Design** | Kahn's BFS for topo sort, two-pass transpose for SCC, negative-cycle detection |
| **Complexity Analysis** | Time + space complexity for each algorithm with practical notes |
| **Python Packaging** | `pyproject.toml`, `src/` layout, zero runtime dependencies in core library |
| **FastAPI** | Typed Pydantic schemas, 400/404 error handling, REST design |
| **Testing** | 33 pytest tests — correctness, edge cases (empty graph, single node, negative cycle) |
| **Docker** | Single-stage lean image |
| **CI/CD** | GitHub Actions: ruff lint + pytest on every push |

---

**Harshita Guduru** — [GitHub](https://github.com/guduruharshita) · [LinkedIn](https://linkedin.com/in/guduruharshita) · [Email](mailto:guduruharshita2001@gmail.com)
