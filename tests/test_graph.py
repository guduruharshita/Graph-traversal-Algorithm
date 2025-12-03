import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from graph_traversal.graph import Graph
from graph_traversal.algorithms import bfs, dfs_iterative, dfs_recursive, has_cycle

def test_bfs_tree():
    g = Graph()
    for u, v in [(0,1),(0,2),(1,3),(1,4)]:
        g.add_edge(u, v)
    assert bfs(g, 0) == [0, 1, 2, 3, 4]

def test_dfs_iterative():
    g = Graph()
    for u, v in [(0,1),(0,2),(1,3)]:
        g.add_edge(u, v)
    result = dfs_iterative(g, 0)
    assert result[0] == 0
    assert set(result) == {0, 1, 2, 3}

def test_cycle_detection():
    acyclic = Graph()
    for u, v in [(0,1),(1,2),(2,3)]:
        acyclic.add_edge(u, v)
    assert not has_cycle(acyclic)

    cyclic = Graph()
    for u, v in [(0,1),(1,2),(2,0)]:
        cyclic.add_edge(u, v)
    assert has_cycle(cyclic)

def test_directed_graph():
    g = Graph(directed=True)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    assert 0 not in g.graph.get(1, [])

if __name__ == "__main__":
    test_bfs_tree()
    test_dfs_iterative()
    test_cycle_detection()
    test_directed_graph()
    print("All tests passed.")
