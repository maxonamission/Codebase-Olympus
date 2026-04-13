"""FastAPI application: startup, CORS, health endpoint."""

import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import networkx as nx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gymnasium_classica.api.database import init_db
from gymnasium_classica.api.routes.auth import router as auth_router
from gymnasium_classica.api.routes.intake import router as intake_router
from gymnasium_classica.api.routes.progress import router as progress_router
from gymnasium_classica.api.routes.session import router as session_router
from gymnasium_classica.graph.loader import load_graph

GRAPH_DIR = Path("data/graph")


def create_app(
    graph_dir: Path = GRAPH_DIR,
    db_path: Optional[Path] = None,
) -> FastAPI:
    """Create and configure the FastAPI application.

    Parameters:
        graph_dir: Path to directory with knowledge graph JSON files.
        db_path: Path to the SQLite database file. None uses the default.
    """

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        application.state.graph = load_graph(graph_dir)
        if db_path is not None:
            application.state.db = init_db(db_path)
        else:
            application.state.db = init_db()
        yield
        db: sqlite3.Connection = application.state.db
        db.close()

    application = FastAPI(
        title="Gymnasium Classica API",
        version="0.1.0",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(auth_router)
    application.include_router(session_router)
    application.include_router(progress_router)
    application.include_router(intake_router)

    @application.get("/health")
    async def health():
        """Health check: returns node/edge counts from the loaded graph."""
        graph: nx.DiGraph = application.state.graph
        return {
            "status": "ok",
            "graph_nodes": graph.number_of_nodes(),
            "graph_edges": graph.number_of_edges(),
        }

    return application


# Default app instance for uvicorn
app = create_app()
