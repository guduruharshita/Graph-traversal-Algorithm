class Graph:
    """Adjacency-list graph supporting directed and undirected edges."""

    def __init__(self, directed: bool = False):
        self.graph: dict = {}
        self.directed = directed

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, u, v):
        self.add_node(u)
        self.add_node(v)
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)

    def node_count(self) -> int:
        return len(self.graph)

    def edge_count(self) -> int:
        total = sum(len(v) for v in self.graph.values())
        return total if self.directed else total // 2

    def neighbors(self, node) -> list:
        return self.graph.get(node, [])
