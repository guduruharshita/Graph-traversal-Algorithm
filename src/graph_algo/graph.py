"""Core Graph data structure — adjacency list with optional weighted edges."""
from __future__ import annotations

from typing import Any


class Graph:
    """Adjacency-list graph supporting directed/undirected and optional edge weights."""

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self._adj: dict[Any, dict[Any, float]] = {}  # node → {neighbor: weight}

    # ── Mutators ─────────────────────────────────────────────────────────────

    def add_node(self, node: Any) -> None:
        self._adj.setdefault(node, {})

    def add_edge(self, u: Any, v: Any, weight: float = 1.0) -> None:
        self.add_node(u)
        self.add_node(v)
        self._adj[u][v] = weight
        if not self.directed:
            self._adj[v][u] = weight

    def remove_edge(self, u: Any, v: Any) -> None:
        self._adj.get(u, {}).pop(v, None)
        if not self.directed:
            self._adj.get(v, {}).pop(u, None)

    # ── Accessors ─────────────────────────────────────────────────────────────

    @property
    def nodes(self) -> list[Any]:
        return list(self._adj)

    @property
    def edges(self) -> list[tuple[Any, Any, float]]:
        seen: set[frozenset] = set()
        result = []
        for u, neighbors in self._adj.items():
            for v, w in neighbors.items():
                key = frozenset({u, v}) if not self.directed else frozenset({(u, v)})
                if key not in seen:
                    seen.add(key)
                    result.append((u, v, w))
        return result

    def neighbors(self, node: Any) -> dict[Any, float]:
        return dict(self._adj.get(node, {}))

    def node_count(self) -> int:
        return len(self._adj)

    def edge_count(self) -> int:
        return len(self.edges)

    def has_node(self, node: Any) -> bool:
        return node in self._adj

    def has_edge(self, u: Any, v: Any) -> bool:
        return v in self._adj.get(u, {})

    def weight(self, u: Any, v: Any) -> float:
        return self._adj[u][v]

    @classmethod
    def from_edge_list(
        cls,
        edges: list[tuple],
        directed: bool = False,
    ) -> "Graph":
        """Build a Graph from a list of (u, v) or (u, v, weight) tuples."""
        g = cls(directed=directed)
        for edge in edges:
            if len(edge) == 3:
                g.add_edge(edge[0], edge[1], float(edge[2]))
            else:
                g.add_edge(edge[0], edge[1])
        return g
