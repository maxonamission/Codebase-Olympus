"""FastAPI application entry point.

Start with: uvicorn gymnasium_classica.api.app:app --reload
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gymnasium_classica.graph.loader import load_graph

DATA_DIR = Path(__file__).resolve().parents[3] / "data"

app = FastAPI(
    title="Gymnasium Classica API",
    version="0.1.0",
    description="Adaptief leersysteem voor Latijn en Grieks",
)

# CORS: allow Vite dev server (localhost:5173) and same-origin production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Load knowledge graph into app state at startup."""
    graph_dir = DATA_DIR / "graph"
    app.state.graph = load_graph(graph_dir)
    node_count = app.state.graph.number_of_nodes()
    edge_count = app.state.graph.number_of_edges()
    print(f"Graph loaded: {node_count} nodes, {edge_count} edges")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
