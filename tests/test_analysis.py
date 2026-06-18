import pytest
from graph_algo.graph import Graph
from graph_algo.algorithms.analysis import has_cycle, topological_sort, strongly_connected_components


@pytest.fixture
def dag() -> Graph:
    g = Graph(directed=True)
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]:
        g.add_edge(u, v)
    return g


@pytest.fixture
def cyclic_directed() -> Graph:
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    return g


def test_has_cycle_dag_no_cycle(dag: Graph):
    assert not has_cycle(dag)


def test_has_cycle_directed_cycle(cyclic_directed: Graph):
    assert has_cycle(cyclic_directed)


def test_has_cycle_undirected_with_cycle():
    g = Graph(directed=False)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 1)
    assert has_cycle(g)


def test_has_cycle_undirected_tree():
    g = Graph(directed=False)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    assert not has_cycle(g)


def test_topological_sort_dag(dag: Graph):
    order = topological_sort(dag)
    assert order.index("A") < order.index("B")
    assert order.index("A") < order.index("C")
    assert order.index("B") < order.index("D")
    assert order.index("D") < order.index("E")


def test_topological_sort_cycle_raises(cyclic_directed: Graph):
    with pytest.raises(ValueError, match="cycle"):
        topological_sort(cyclic_directed)


def test_topological_sort_undirected_raises():
    g = Graph(directed=False)
    g.add_edge(1, 2)
    with pytest.raises(ValueError):
        topological_sort(g)


def test_scc_simple():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    g.add_edge("C", "D")
    sccs = strongly_connected_components(g)
    # A, B, C form one SCC; D is its own
    scc_sets = [set(s) for s in sccs]
    assert {"A", "B", "C"} in scc_sets
    assert {"D"} in scc_sets


def test_scc_undirected_raises():
    g = Graph(directed=False)
    g.add_edge(1, 2)
    with pytest.raises(ValueError):
        strongly_connected_components(g)
