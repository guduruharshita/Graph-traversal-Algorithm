from collections import deque
from .graph import Graph

def bfs(graph: Graph, start):
    """Breadth-First Search -- visits nodes level by level."""
    visited, queue, traversal = set(), deque([start]), []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            traversal.append(node)
            queue.extend(sorted(n for n in graph.graph.get(node, []) if n not in visited))
    return traversal

def dfs_iterative(graph: Graph, start):
    """Depth-First Search using an explicit stack."""
    visited, stack, traversal = set(), [start], []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            traversal.append(node)
            stack.extend(reversed(sorted(graph.graph.get(node, []))))
    return traversal

def dfs_recursive(graph: Graph, start, visited=None):
    """Depth-First Search using recursion."""
    if visited is None:
        visited = set()
    traversal = []
    if start not in visited:
        visited.add(start)
        traversal.append(start)
        for neighbor in sorted(graph.graph.get(start, [])):
            traversal += dfs_recursive(graph, neighbor, visited)
    return traversal

def has_cycle(graph: Graph):
    """Detect cycle using DFS coloring."""
    visited, rec_stack = set(), set()
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.graph.get(node, []):
            if neighbor not in visited and dfs(neighbor):
                return True
            if neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False
    return any(dfs(n) for n in graph.graph if n not in visited)
