"""Shortest-path algorithms: Dijkstra and Bellman-Ford.

Dijkstra:     O((V + E) log V)  — non-negative weights only
Bellman-Ford: O(V × E)          — handles negative weights, detects negative cycles
"""
from __future__ import annotations

import heapq
import math
from typing import Any

from graph_algo.graph import Graph

_INF = math.inf


def dijkstra(graph: Graph, source: Any) -> tuple[dict[Any, float], dict[Any, Any | None]]:
    """Single-source shortest paths (non-negative weights).

    Returns:
        dist:  {node: shortest distance from source}
        prev:  {node: predecessor on shortest path}
    """
    dist: dict[Any, float] = {n: _INF for n in graph.nodes}
    prev: dict[Any, Any | None] = {n: None for n in graph.nodes}
    dist[source] = 0.0
    heap: list[tuple[float, Any]] = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph.neighbors(u).items():
            if w < 0:
                raise ValueError("Dijkstra requires non-negative edge weights")
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))

    return dist, prev


def bellman_ford(
    graph: Graph, source: Any
) -> tuple[dict[Any, float], dict[Any, Any | None]]:
    """Single-source shortest paths supporting negative weights.

    Raises:
        ValueError: if a negative-weight cycle is reachable from source.
    """
    dist: dict[Any, float] = {n: _INF for n in graph.nodes}
    prev: dict[Any, Any | None] = {n: None for n in graph.nodes}
    dist[source] = 0.0

    n = graph.node_count()
    edges = graph.edges  # list of (u, v, w)

    # Relax edges V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

    # Detect negative cycles
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    return dist, prev


def reconstruct_path(prev: dict[Any, Any | None], target: Any) -> list[Any]:
    """Reconstruct shortest path from source to target using prev map."""
    path: list = []
    node: Any | None = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path
