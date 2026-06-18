"""BFS and DFS traversal algorithms.

Time complexity:  O(V + E)
Space complexity: O(V)
"""
from __future__ import annotations

from collections import deque
from typing import Any

from graph_algo.graph import Graph


def bfs(graph: Graph, start: Any) -> list[Any]:
    """Breadth-First Search — level-order traversal.

    Returns visited nodes in BFS order.
    """
    if not graph.has_node(start):
        return []

    visited: set = set()
    queue: deque = deque([start])
    result: list = []

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        result.append(node)
        for neighbor in sorted(graph.neighbors(node)):
            if neighbor not in visited:
                queue.append(neighbor)

    return result


def dfs_iterative(graph: Graph, start: Any) -> list[Any]:
    """Depth-First Search using an explicit stack."""
    if not graph.has_node(start):
        return []

    visited: set = set()
    stack: list = [start]
    result: list = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        result.append(node)
        for neighbor in reversed(sorted(graph.neighbors(node))):
            if neighbor not in visited:
                stack.append(neighbor)

    return result


def dfs_recursive(graph: Graph, start: Any, _visited: set | None = None) -> list[Any]:
    """Depth-First Search using recursion."""
    if not graph.has_node(start):
        return []

    if _visited is None:
        _visited = set()

    result: list = []
    if start not in _visited:
        _visited.add(start)
        result.append(start)
        for neighbor in sorted(graph.neighbors(start)):
            result.extend(dfs_recursive(graph, neighbor, _visited))

    return result


def connected_components(graph: Graph) -> list[list[Any]]:
    """Find all connected components (undirected graph).

    Returns a list of lists, each being one component.
    """
    visited: set = set()
    components: list[list] = []

    for node in graph.nodes:
        if node not in visited:
            component = bfs(graph, node)
            components.append(component)
            visited.update(component)

    return components
