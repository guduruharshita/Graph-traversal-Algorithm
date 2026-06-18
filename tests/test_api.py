from fastapi.testclient import TestClient
from graph_algo.api.main import app

client = TestClient(app)

SIMPLE_GRAPH = {
    "edges": [
        {"u": "A", "v": "B", "weight": 1},
        {"u": "A", "v": "C", "weight": 4},
        {"u": "B", "v": "C", "weight": 2},
        {"u": "B", "v": "D", "weight": 5},
        {"u": "C", "v": "D", "weight": 1},
    ],
    "directed": True,
}


def test_health():
    res = client.get("/health")
    assert res.status_code == 200


def test_bfs_traversal():
    res = client.post("/api/graph/traverse", json={"graph": SIMPLE_GRAPH, "start": "A", "algorithm": "bfs"})
    assert res.status_code == 200
    data = res.json()
    assert data["traversal_order"][0] == "A"


def test_dfs_traversal():
    res = client.post("/api/graph/traverse", json={"graph": SIMPLE_GRAPH, "start": "A", "algorithm": "dfs_iterative"})
    assert res.status_code == 200


def test_traverse_unknown_start():
    res = client.post("/api/graph/traverse", json={"graph": SIMPLE_GRAPH, "start": "Z", "algorithm": "bfs"})
    assert res.status_code == 400


def test_dijkstra_shortest_path():
    res = client.post(
        "/api/graph/shortest-path",
        json={"graph": SIMPLE_GRAPH, "source": "A", "target": "D", "algorithm": "dijkstra"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["distance"] == 4.0
    assert data["path"] == ["A", "B", "C", "D"]


def test_shortest_path_no_route():
    isolated = {"edges": [{"u": "A", "v": "B"}], "directed": True}
    isolated["directed"] = True
    res = client.post(
        "/api/graph/shortest-path",
        json={"graph": isolated, "source": "B", "target": "A", "algorithm": "dijkstra"},
    )
    assert res.status_code == 404


def test_analyze_graph():
    res = client.post("/api/graph/analyze", json=SIMPLE_GRAPH)
    assert res.status_code == 200
    data = res.json()
    assert data["node_count"] == 4
    assert "topological_order" in data
