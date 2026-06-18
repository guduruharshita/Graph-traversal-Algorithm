"""FastAPI application."""
from fastapi import FastAPI
from graph_algo.api.routers import graphs

app = FastAPI(
    title="Graph Algorithm API",
    version="2.0.0",
    description="BFS, DFS, Dijkstra, Bellman-Ford, topological sort, SCC via REST.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(graphs.router)


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "version": "2.0.0"}
