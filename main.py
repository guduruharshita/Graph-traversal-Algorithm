import timeit
from graph_traversal import Graph, bfs, dfs_iterative, dfs_recursive, has_cycle


def build_tree() -> Graph:
    g = Graph()
    for u, v in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]:
        g.add_edge(u, v)
    return g


def build_cyclic() -> Graph:
    g = Graph()
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 4)]:
        g.add_edge(u, v)
    return g


def build_social() -> Graph:
    g = Graph()
    for u, v in [("Alice", "Bob"), ("Alice", "Charlie"),
                 ("Bob", "Diana"), ("Diana", "Eve"), ("Eve", "Alice")]:
        g.add_edge(u, v)
    return g


def benchmark(graph: Graph, start, reps: int = 500) -> dict:
    return {
        "BFS":           timeit.timeit(lambda: bfs(graph, start), number=reps) / reps * 1e6,
        "DFS Iterative": timeit.timeit(lambda: dfs_iterative(graph, start), number=reps) / reps * 1e6,
        "DFS Recursive": timeit.timeit(lambda: dfs_recursive(graph, start), number=reps) / reps * 1e6,
    }


if __name__ == "__main__":
    tree   = build_tree()
    cyclic = build_cyclic()
    social = build_social()

    print("=== Tree (no cycle) ===")
    print(f"  BFS:           {bfs(tree, 0)}")
    print(f"  DFS Iterative: {dfs_iterative(tree, 0)}")
    print(f"  Has cycle:     {has_cycle(tree)}")

    print("\n=== Cyclic Graph ===")
    print(f"  BFS:       {bfs(cyclic, 0)}")
    print(f"  Has cycle: {has_cycle(cyclic)}")

    print("\n=== Social Network ===")
    print(f"  BFS from Alice: {bfs(social, 'Alice')}")

    print("\n=== Benchmarks (µs per call) ===")
    for algo, t in benchmark(tree, 0).items():
        print(f"  {algo:<18} {t:.2f} µs")
