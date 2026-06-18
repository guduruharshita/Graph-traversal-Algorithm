import math
import pytest
from graph_algo.graph import Graph
from graph_algo.algorithms.shortest_path import dijkstra, bellman_ford, reconstruct_path


@pytest.fixture
def weighted_graph() -> Graph:
    g = Graph(directed=True)
    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 4)
    g.add_edge("B", "C", 2)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 1)
    return g


def test_dijkstra_distances(weighted_graph: Graph):
    dist, _ = dijkstra(weighted_graph, "A")
    assert dist["A"] == 0
    assert dist["B"] == 1
    assert dist["C"] == 3  # A→B→C
    assert dist["D"] == 4  # A→B→C→D


def test_dijkstra_path(weighted_graph: Graph):
    _, prev = dijkstra(weighted_graph, "A")
    path = reconstruct_path(prev, "D")
    assert path == ["A", "B", "C", "D"]


def test_dijkstra_unreachable():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_node("C")
    dist, _ = dijkstra(g, "A")
    assert dist["C"] == math.inf


def test_dijkstra_negative_weight_raises():
    g = Graph(directed=True)
    g.add_edge("A", "B", -1)
    with pytest.raises(ValueError, match="non-negative"):
        dijkstra(g, "A")


def test_bellman_ford_distances(weighted_graph: Graph):
    dist, _ = bellman_ford(weighted_graph, "A")
    assert dist["D"] == 4


def test_bellman_ford_negative_weight():
    g = Graph(directed=True)
    g.add_edge("A", "B", -1)
    g.add_edge("A", "C", 4)
    g.add_edge("B", "C", 2)
    dist, _ = bellman_ford(g, "A")
    assert dist["B"] == -1
    assert dist["C"] == 1  # A→B→C = -1 + 2


def test_bellman_ford_negative_cycle_raises():
    g = Graph(directed=True)
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", -3)
    g.add_edge("C", "A", 1)
    with pytest.raises(ValueError, match="negative-weight cycle"):
        bellman_ford(g, "A")
