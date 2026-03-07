#!/usr/bin/env python
# coding: utf-8

# In[10]:


# Graph Traversal Algorithms: BFS vs. DFS
# Complete ready-to-run implementation with visualization

from collections import deque
import timeit
import random
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, clear_output

plt.style.use('seaborn')

# ====================== GRAPH CLASS IMPLEMENTATION ======================
class Graph:
    def __init__(self, directed=False):
        self.graph = {}
        self.directed = directed
    
    def add_node(self, node):
        """Add a node to the graph"""
        if node not in self.graph:
            self.graph[node] = []
    
    def add_edge(self, u, v):
        """Add an edge between nodes u and v (directed or undirected)"""
        self.add_node(u)
        self.add_node(v)
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)
    
    def bfs(self, start):
        """Breadth-First Search using queue"""
        visited = set()
        queue = deque([start])
        traversal = []
        
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                traversal.append(node)
                # Add neighbors in alphabetical/numerical order
                queue.extend(sorted(n for n in self.graph.get(node, []) 
                             if n not in visited))
        return traversal
    
    def dfs(self, start, method='iterative'):
        """Depth-First Search (iterative or recursive)"""
        if method == 'iterative':
            return self._dfs_iterative(start)
        elif method == 'recursive':
            return self._dfs_recursive(start, set())
        else:
            raise ValueError("Method must be 'iterative' or 'recursive'")
    
    def _dfs_iterative(self, start):
        """DFS using explicit stack"""
        visited = set()
        stack = [start]
        traversal = []
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                traversal.append(node)
                # Reverse to match recursive order
                stack.extend(reversed(sorted(self.graph.get(node, []))))
        return traversal
    
    def _dfs_recursive(self, node, visited):
        """DFS using recursion"""
        traversal = []
        if node not in visited:
            visited.add(node)
            traversal.append(node)
            # Process neighbors in order
            for neighbor in sorted(self.graph.get(node, [])):
                traversal += self._dfs_recursive(neighbor, visited)
        return traversal
    
    def has_cycle(self):
        """Check if graph contains a cycle using DFS"""
        visited = set()
        recursion_stack = set()
        
        def dfs_cycle(node):
            visited.add(node)
            recursion_stack.add(node)
            
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if dfs_cycle(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True
            
            recursion_stack.remove(node)
            return False
        
        for node in self.graph:
            if node not in visited:
                if dfs_cycle(node):
                    return True
        return False
    
    def benchmark(self, start, reps=1000):
        """Compare BFS vs DFS performance"""
        results = {
            'BFS': timeit.timeit(lambda: self.bfs(start), number=reps)/reps,
            'DFS (Iterative)': timeit.timeit(lambda: self.dfs(start, 'iterative'), number=reps)/reps,
            'DFS (Recursive)': timeit.timeit(lambda: self.dfs(start, 'recursive'), number=reps)/reps
        }
        return results
    
    def visualize(self, title="Graph", figsize=(8,6)):
        """Visualize using NetworkX"""
        G = nx.DiGraph() if self.directed else nx.Graph()
        for node in self.graph:
            G.add_node(node)
            for neighbor in self.graph[node]:
                G.add_edge(node, neighbor)
        
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(G, seed=42)  # Consistent layout
        nx.draw(G, pos, with_labels=True, node_color='skyblue', 
                node_size=800, edge_color='gray', arrows=self.directed,
                font_weight='bold', arrowstyle='->', arrowsize=15)
        plt.title(title, fontsize=14)
        plt.show()

# ====================== DEMONSTRATION EXAMPLES ======================
def create_sample_graphs():
    """Create and return example graphs"""
    # Example 1: Undirected acyclic graph (Tree)
    tree = Graph()
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    for u, v in edges:
        tree.add_edge(u, v)
    
    # Example 2: Undirected cyclic graph
    cyclic = Graph()
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 4)]
    for u, v in edges:
        cyclic.add_edge(u, v)
    
    # Example 3: Directed acyclic graph (DAG)
    dag = Graph(directed=True)
    dag_edges = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5)]
    for u, v in dag_edges:
        dag.add_edge(u, v)
    
    # Example 4: Directed cyclic graph
    dcg = Graph(directed=True)
    dcg_edges = [(0, 1), (1, 2), (2, 3), (3, 0), (1, 3), (2, 4)]
    for u, v in dcg_edges:
        dcg.add_edge(u, v)
    
    # Example 5: Social network
    social = Graph()
    social_edges = [("Alice", "Bob"), ("Alice", "Charlie"), 
                   ("Bob", "Diana"), ("Diana", "Eve"), ("Eve", "Alice")]
    for u, v in social_edges:
        social.add_edge(u, v)
    
    return tree, cyclic, dag, dcg, social

# ====================== PERFORMANCE ANALYSIS ======================
def run_performance_tests():
    """Run benchmarks on all sample graphs"""
    tree, cyclic, dag, dcg, social = create_sample_graphs()
    results = []
    
    graphs = [
        ("Undirected Acyclic (Tree)", tree),
        ("Undirected Cyclic", cyclic),
        ("Directed Acyclic (DAG)", dag),
        ("Directed Cyclic", dcg),
        ("Social Network", social)
    ]
    
    for name, graph in graphs:
        start_node = list(graph.graph.keys())[0]
        res = graph.benchmark(start_node, reps=100)
        res['Graph Type'] = name
        res['Nodes'] = len(graph.graph)
        res['Edges'] = sum(len(v) for v in graph.graph.values()) // (1 if graph.directed else 2)
        res['Has Cycle'] = graph.has_cycle()
        results.append(res)
    
    return pd.DataFrame(results)

# ====================== VISUALIZATION ======================
def show_traversal_comparison():
    """Visual comparison of BFS vs DFS traversal"""
    _, cyclic, _, _, _ = create_sample_graphs()
    
    plt.figure(figsize=(12, 5))
    
    # BFS visualization
    plt.subplot(1, 2, 1)
    G = nx.Graph(cyclic.graph)
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=800)
    plt.title("BFS Traversal (Level Order)", fontsize=12)
    
    # DFS visualization
    plt.subplot(1, 2, 2)
    nx.draw(G, pos, with_labels=True, node_color='salmon', node_size=800)
    plt.title("DFS Traversal (Depth Priority)", fontsize=12)
    
    plt.tight_layout()
    plt.show()

# ====================== MAIN EXECUTION ======================
if __name__ == "__main__":
    # Create sample graphs
    tree, cyclic, dag, dcg, social = create_sample_graphs()
    
    print("=== UNDIRECTED ACYCLIC GRAPH (TREE) ===")
    print("BFS:", tree.bfs(0))
    print("DFS (Iterative):", tree.dfs(0))
    print("Contains cycle:", tree.has_cycle())
    tree.visualize("Undirected Acyclic Graph (Tree)")
    
    print("\n=== UNDIRECTED CYCLIC GRAPH ===")
    print("BFS:", cyclic.bfs(0))
    print("DFS (Iterative):", cyclic.dfs(0))
    print("Contains cycle:", cyclic.has_cycle())
    cyclic.visualize("Undirected Cyclic Graph")
    
    print("\n=== DIRECTED ACYCLIC GRAPH (DAG) ===")
    print("BFS:", dag.bfs(0))
    print("DFS (Iterative):", dag.dfs(0))
    print("Contains cycle:", dag.has_cycle())
    dag.visualize("Directed Acyclic Graph (DAG)")
    
    print("\n=== DIRECTED CYCLIC GRAPH ===")
    print("BFS:", dcg.bfs(0))
    print("DFS (Iterative):", dcg.dfs(0))
    print("Contains cycle:", dcg.has_cycle())
    dcg.visualize("Directed Cyclic Graph")
    
    print("\n=== SOCIAL NETWORK ===")
    print("BFS (Alice's connections):", social.bfs("Alice"))
    print("DFS (Iterative):", social.dfs("Alice"))
    print("Contains cycle:", social.has_cycle())
    social.visualize("Social Network", figsize=(7,5))
    
    # Performance analysis
    print("\n=== PERFORMANCE BENCHMARKS ===")
    performance_df = run_performance_tests()
    
    # Create a styled DataFrame without using float formatting on strings
    styled_df = (
        performance_df[['Graph Type', 'Nodes', 'Edges', 'Has Cycle', 'BFS', 'DFS (Iterative)', 'DFS (Recursive)']]
        .style.set_caption("Traversal Algorithm Performance (seconds per traversal)")
    )
    
    # Format only the numeric columns
    numeric_cols = ['BFS', 'DFS (Iterative)', 'DFS (Recursive)']
    for col in numeric_cols:
        styled_df = styled_df.format("{:.6f}", subset=[col])
    
    display(styled_df)
    
    # Traversal comparison
    print("\n=== BFS vs DFS VISUAL COMPARISON ===")
    show_traversal_comparison()


# In[ ]:




