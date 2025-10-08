class Graph:
    def __init__(self, directed=False):
        self.graph = {}
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

    def node_count(self):
        return len(self.graph)

    def edge_count(self):
        total = sum(len(v) for v in self.graph.values())
        return total if self.directed else total // 2
