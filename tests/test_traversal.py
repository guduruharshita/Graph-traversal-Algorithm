import pytest
from graph_algo.graph import Graph
from graph_algo.algorithms.traversal import bfs, dfs_iterative, dfs_recursive, connected_components


@pytest.fixture
def simple_graph() -> Graph:
    g = Graph(directed=False)
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]:
        g.add_edge(u, v)
    return g


@pytest.fixture
def directed_dag() -> Graph:
    g = Graph(directed=True)
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]:
        g.add_edge(u, v)
    return g


def test_bfs_order(simple_graph: Graph):
    result = bfs(simple_graph, "A")
    assert result[0] == "A"
    assert set(result) == {"A", "B", "C", "D", "E"}


def test_bfs_unknown_start(simple_graph: Graph):
    assert bfs(simple_graph, "Z") == []


def test_dfs_iterative_visits_all(simple_graph: Graph):
    result = dfs_iterative(simple_graph, "A")
    assert set(result) == {"A", "B", "C", "D", "E"}


def test_dfs_recursive_visits_all(simple_graph: Graph):
    result = dfs_recursive(simple_graph, "A")
    assert set(result) == {"A", "B", "C", "D", "E"}


def test_dfs_starts_with_source(simple_graph: Graph):
    for algo in (dfs_iterative, dfs_recursive):
        assert algo(simple_graph, "A")[0] == "A"


def test_connected_components_single(simple_graph: Graph):
    components = connected_components(simple_graph)
    assert len(components) == 1
    assert set(components[0]) == {"A", "B", "C", "D", "E"}


def test_connected_components_multiple():
    g = Graph(directed=False)
    g.add_edge(1, 2)
    g.add_edge(3, 4)
    components = connected_components(g)
    assert len(components) == 2
