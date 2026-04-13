"""FastAPI application: startup, CORS, health endpoint."""

import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

import networkx as nx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gymnasium_classica.api.database import init_db
from gymnasium_classica.graph.loader import load_graph

GRAPH_DIR = Path("data/graph")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the knowledge graph and initialise the database on startup."""
    app.state.graph = load_graph(GRAPH_DIR)
    app.state.db = init_db()
    yield
    # Cleanup
    db: sqlite3.Connection = app.state.db
    db.close()


app = FastAPI(
    title="Gymnasium Classica API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Health check: returns node/edge counts from the loaded graph."""
    graph: nx.DiGraph = app.state.graph
    return {
        "status": "ok",
        "graph_nodes": graph.number_of_nodes(),
        "graph_edges": graph.number_of_edges(),
    }
