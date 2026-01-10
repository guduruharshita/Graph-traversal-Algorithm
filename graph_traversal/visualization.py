try:
    import networkx as nx
    import matplotlib.pyplot as plt

    def draw_graph(graph, title="Graph Visualization", highlight_path=None):
        G = nx.DiGraph() if graph.directed else nx.Graph()
        for node, neighbors in graph.graph.items():
            G.add_node(node)
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(8, 6))
        nx.draw_networkx_nodes(G, pos, node_color="#89b4fa", node_size=600)
        nx.draw_networkx_labels(G, pos, font_color="white", font_weight="bold")
        if highlight_path:
            path_edges = set(zip(highlight_path, highlight_path[1:]))
            edge_colors = ["#f38ba8" if e in path_edges else "#585b70" for e in G.edges()]
        else:
            edge_colors = ["#585b70"] * G.number_of_edges()
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True, width=2)
        plt.title(title)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

except ImportError:
    def draw_graph(graph, title="Graph Visualization", highlight_path=None):
        print("networkx and matplotlib are required for visualization.")
        print("Install with: pip install networkx matplotlib")
