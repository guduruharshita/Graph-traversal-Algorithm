from collections import deque
from .graph import Graph


def bfs(graph: Graph, start) -> list:
    """Breadth-First Search — visits nodes level by level using a queue."""
    visited, queue, order = set(), deque([start]), []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            order.append(node)
            queue.extend(n for n in sorted(graph.neighbors(node)) if n not in visited)
    return order


def dfs_iterative(graph: Graph, start) -> list:
    """Depth-First Search using an explicit stack."""
    visited, stack, order = set(), [start], []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            stack.extend(reversed(sorted(graph.neighbors(node))))
    return order


def dfs_recursive(graph: Graph, start, _visited: set = None) -> list:
    """Depth-First Search using recursion."""
    if _visited is None:
        _visited = set()
    order = []
    if start not in _visited:
        _visited.add(start)
        order.append(start)
        for neighbor in sorted(graph.neighbors(start)):
            order += dfs_recursive(graph, neighbor, _visited)
    return order


def has_cycle(graph: Graph) -> bool:
    """Detect a cycle using DFS coloring (white/grey/black)."""
    visited, rec_stack = set(), set()

    def _dfs(node) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited and _dfs(neighbor):
                return True
            if neighbor in rec_stack:
                return True
        rec_stack.discard(node)
        return False

    return any(_dfs(n) for n in graph.graph if n not in visited)
