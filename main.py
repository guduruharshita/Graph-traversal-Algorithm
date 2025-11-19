from graph_traversal.graph import Graph
from graph_traversal.algorithms import bfs, dfs_iterative, dfs_recursive, has_cycle
import timeit

def build_sample_graph():
    g = Graph()
    for u, v in [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]:
        g.add_edge(u, v)
    return g

def benchmark(graph, start, reps=500):
    return {
        "BFS":           timeit.timeit(lambda: bfs(graph, start), number=reps) / reps,
        "DFS Iterative": timeit.timeit(lambda: dfs_iterative(graph, start), number=reps) / reps,
        "DFS Recursive": timeit.timeit(lambda: dfs_recursive(graph, start), number=reps) / reps,
    }

if __name__ == "__main__":
    g = build_sample_graph()
    print("BFS:          ", bfs(g, 0))
    print("DFS Iterative:", dfs_iterative(g, 0))
    print("DFS Recursive:", dfs_recursive(g, 0))
    print("Has cycle:    ", has_cycle(g))
    print("\nBenchmarks:")
    for algo, t in benchmark(g, 0).items():
        print(f"  {algo}: {t*1e6:.2f} us")
