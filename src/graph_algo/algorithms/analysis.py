"""Graph analysis: cycle detection, topological sort, strongly connected components.

Cycle detection:     O(V + E)
Topological sort:    O(V + E)  — Kahn's algorithm
SCC (Kosaraju):      O(V + E)
"""
from __future__ import annotations

from collections import deque
from typing import Any

from graph_algo.graph import Graph


def has_cycle(graph: Graph) -> bool:
    """Detect a cycle using DFS colouring.

    Works for both directed and undirected graphs.
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    colour: dict[Any, int] = {n: WHITE for n in graph.nodes}

    def dfs(node: Any, parent: Any | None) -> bool:
        colour[node] = GRAY
        for neighbor in graph.neighbors(node):
            if colour[neighbor] == GRAY:
                if graph.directed or neighbor != parent:
                    return True
            elif colour[neighbor] == WHITE:
                if dfs(neighbor, node):
                    return True
        colour[node] = BLACK
        return False

    return any(dfs(n, None) for n in graph.nodes if colour[n] == WHITE)


def topological_sort(graph: Graph) -> list[Any]:
    """Kahn's BFS-based topological sort for DAGs.

    Returns nodes in topological order.
    Raises:
        ValueError: if the graph contains a cycle.
    """
    if not graph.directed:
        raise ValueError("Topological sort is only defined for directed graphs")

    in_degree: dict[Any, int] = {n: 0 for n in graph.nodes}
    for u in graph.nodes:
        for v in graph.neighbors(u):
            in_degree[v] += 1

    queue: deque = deque(n for n, d in in_degree.items() if d == 0)
    result: list = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph.neighbors(node):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != graph.node_count():
        raise ValueError("Graph contains a cycle — topological sort impossible")

    return result


def strongly_connected_components(graph: Graph) -> list[list[Any]]:
    """Kosaraju's algorithm for SCCs (directed graphs only).

    Returns a list of strongly connected components (each a list of nodes).
    """
    if not graph.directed:
        raise ValueError("SCC is only defined for directed graphs")

    # Step 1: DFS on original graph, push to finish-order stack
    visited: set = set()
    finish_stack: list = []

    def dfs1(node: Any) -> None:
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                dfs1(neighbor)
        finish_stack.append(node)

    for node in graph.nodes:
        if node not in visited:
            dfs1(node)

    # Step 2: Build transpose graph
    transposed = Graph(directed=True)
    for u, v, w in graph.edges:
        transposed.add_edge(v, u, w)

    # Step 3: DFS on transposed graph in reverse finish order
    visited2: set = set()
    sccs: list[list] = []

    def dfs2(node: Any, component: list) -> None:
        visited2.add(node)
        component.append(node)
        for neighbor in transposed.neighbors(node):
            if neighbor not in visited2:
                dfs2(neighbor, component)

    while finish_stack:
        node = finish_stack.pop()
        if node not in visited2:
            component: list = []
            dfs2(node, component)
            sccs.append(component)

    return sccs
