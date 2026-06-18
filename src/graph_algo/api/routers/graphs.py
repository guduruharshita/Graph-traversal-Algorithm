"""Graph algorithm REST endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from graph_algo.graph import Graph
from graph_algo.algorithms.traversal import bfs, dfs_iterative, dfs_recursive, connected_components
from graph_algo.algorithms.shortest_path import dijkstra, bellman_ford, reconstruct_path
from graph_algo.algorithms.analysis import has_cycle, topological_sort, strongly_connected_components

router = APIRouter(prefix="/api/graph", tags=["graph"])


class EdgeInput(BaseModel):
    u: str
    v: str
    weight: float = Field(default=1.0)


class GraphInput(BaseModel):
    edges: list[EdgeInput]
    directed: bool = False


class TraversalRequest(BaseModel):
    graph: GraphInput
    start: str
    algorithm: str = Field(default="bfs", pattern="^(bfs|dfs_iterative|dfs_recursive)$")


class ShortestPathRequest(BaseModel):
    graph: GraphInput
    source: str
    target: str
    algorithm: str = Field(default="dijkstra", pattern="^(dijkstra|bellman_ford)$")


def _build_graph(g_input: GraphInput) -> Graph:
    g = Graph(directed=g_input.directed)
    for e in g_input.edges:
        g.add_edge(e.u, e.v, e.weight)
    return g


@router.post("/traverse")
def traverse(req: TraversalRequest) -> dict:
    g = _build_graph(req.graph)
    if not g.has_node(req.start):
        raise HTTPException(400, f"Start node '{req.start}' not in graph")

    algo_map = {
        "bfs": bfs,
        "dfs_iterative": dfs_iterative,
        "dfs_recursive": dfs_recursive,
    }
    result = algo_map[req.algorithm](g, req.start)
    return {
        "algorithm": req.algorithm,
        "start": req.start,
        "traversal_order": result,
        "nodes_visited": len(result),
    }


@router.post("/shortest-path")
def shortest_path(req: ShortestPathRequest) -> dict:
    g = _build_graph(req.graph)
    for node in (req.source, req.target):
        if not g.has_node(node):
            raise HTTPException(400, f"Node '{node}' not in graph")

    try:
        if req.algorithm == "dijkstra":
            dist, prev = dijkstra(g, req.source)
        else:
            dist, prev = bellman_ford(g, req.source)
    except ValueError as e:
        raise HTTPException(400, str(e)) from e

    import math
    if dist[req.target] == math.inf:
        raise HTTPException(404, f"No path from '{req.source}' to '{req.target}'")

    path = reconstruct_path(prev, req.target)
    return {
        "algorithm": req.algorithm,
        "source": req.source,
        "target": req.target,
        "distance": dist[req.target],
        "path": path,
    }


@router.post("/analyze")
def analyze(g_input: GraphInput) -> dict:
    g = _build_graph(g_input)

    result: dict = {
        "node_count": g.node_count(),
        "edge_count": g.edge_count(),
        "directed": g_input.directed,
        "has_cycle": has_cycle(g),
    }

    if g_input.directed:
        try:
            result["topological_order"] = topological_sort(g)
        except ValueError:
            result["topological_order"] = None

        result["strongly_connected_components"] = strongly_connected_components(g)
    else:
        result["connected_components"] = connected_components(g)

    return result
