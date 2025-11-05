import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from graph_traversal import Graph, bfs, dfs_iterative, dfs_recursive, has_cycle


def test_bfs_level_order():
    g = Graph()
    for u, v in [(0, 1), (0, 2), (1, 3), (1, 4)]:
        g.add_edge(u, v)
    assert bfs(g, 0) == [0, 1, 2, 3, 4]


def test_dfs_visits_all_nodes():
    g = Graph()
    for u, v in [(0, 1), (0, 2), (1, 3)]:
        g.add_edge(u, v)
    result = dfs_iterative(g, 0)
    assert result[0] == 0 and set(result) == {0, 1, 2, 3}


def test_recursive_matches_iterative():
    g = Graph()
    for u, v in [(0, 1), (0, 2), (1, 3), (2, 4)]:
        g.add_edge(u, v)
    assert set(dfs_iterative(g, 0)) == set(dfs_recursive(g, 0))


def test_no_cycle_in_tree():
    g = Graph()
    for u, v in [(0, 1), (1, 2), (2, 3)]:
        g.add_edge(u, v)
    assert not has_cycle(g)


def test_cycle_detected():
    g = Graph()
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        g.add_edge(u, v)
    assert has_cycle(g)


def test_directed_no_back_edge():
    g = Graph(directed=True)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    assert 0 not in g.neighbors(1)


def test_node_and_edge_count():
    g = Graph()
    for u, v in [(0, 1), (1, 2), (2, 3)]:
        g.add_edge(u, v)
    assert g.node_count() == 4
    assert g.edge_count() == 3


if __name__ == "__main__":
    test_bfs_level_order()
    test_dfs_visits_all_nodes()
    test_recursive_matches_iterative()
    test_no_cycle_in_tree()
    test_cycle_detected()
    test_directed_no_back_edge()
    test_node_and_edge_count()
    print("All tests passed.")
