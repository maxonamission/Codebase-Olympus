"""FastAPI application: startup, CORS, health endpoint.

Start with: uvicorn gymnasium_classica.api.app:app --reload
"""

import json
import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import networkx as nx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from gymnasium_classica.api.database import init_db
from gymnasium_classica.api.routes.auth import router as auth_router
from gymnasium_classica.api.routes.intake import router as intake_router
from gymnasium_classica.api.routes.mentor import router as mentor_router
from gymnasium_classica.api.routes.progress import router as progress_router
from gymnasium_classica.api.routes.session import router as session_router
from gymnasium_classica.api.routes.user import router as user_router
from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.passages.loader import load_passages
from gymnasium_classica.vocab.loader import load_vocab_metadata

GRAPH_DIR = Path("data/graph")
PASSAGES_DIR = Path("data/passages")
AUDIO_DIR = Path("data/audio")
VOCAB_SOURCES_DIR = Path("data/vocab_sources")
CLUSTERS_FILE = Path("data/vocabulaire_clusters.json")

_AUDIO_MEDIA_TYPES = {
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
}


def _load_clusters(path: Path) -> list[dict[str, Any]]:
    """Load semantic vocabulary cluster definitions from JSON.

    Returns an empty list when the file is missing so tests and dev
    environments without the data file still start cleanly.
    """
    if not path.is_file():
        return []
    raw = json.loads(path.read_text("utf-8"))
    return list(raw.get("clusters", []))


def create_app(
    graph_dir: Path = GRAPH_DIR,
    db_path: Path | None = None,
    passages_dir: Path = PASSAGES_DIR,
    audio_dir: Path = AUDIO_DIR,
    vocab_sources_dir: Path = VOCAB_SOURCES_DIR,
    clusters_file: Path = CLUSTERS_FILE,
) -> FastAPI:
    """Create and configure the FastAPI application.

    Parameters:
        graph_dir: Path to directory with knowledge graph JSON files.
        db_path: Path to the SQLite database file. None uses the default.
        passages_dir: Path to directory with passage JSON files.
        audio_dir: Path to directory served as read-only audio on /audio.
        vocab_sources_dir: Path to directory with structured vocab metadata.
        clusters_file: Path to the semantic vocabulary clusters JSON file.
    """

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        application.state.graph = load_graph(graph_dir)
        if passages_dir.is_dir():
            application.state.passages = load_passages(passages_dir)
        else:
            application.state.passages = []
        if vocab_sources_dir.is_dir():
            application.state.vocab_metadata = load_vocab_metadata(vocab_sources_dir)
        else:
            application.state.vocab_metadata = {}
        application.state.clusters = _load_clusters(clusters_file)
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
        description="Adaptief leersysteem voor Latijn en Grieks",
        lifespan=lifespan,
    )

    # CORS: allow Vite dev server for development
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(auth_router)
    application.include_router(session_router)
    application.include_router(progress_router)
    application.include_router(intake_router)
    application.include_router(user_router)
    application.include_router(mentor_router)

    @application.get("/health")
    async def health() -> dict[str, Any]:
        """Health check: returns node/edge counts from the loaded graph."""
        graph: nx.DiGraph = application.state.graph
        return {
            "status": "ok",
            "graph_nodes": graph.number_of_nodes(),
            "graph_edges": graph.number_of_edges(),
        }

    @application.get("/audio/{filename}")
    async def serve_audio(filename: str) -> FileResponse:
        """Serve a read-only audio file from *audio_dir*.

        Restrictions:
          * Filename cannot contain path separators or ``..`` — blocks
            directory traversal.
          * Only ``.wav`` and ``.mp3`` extensions are served; other
            files return 404 even if present on disk.
          * Unknown files return 404.
        """
        if "/" in filename or "\\" in filename or ".." in filename:
            raise HTTPException(status_code=404)
        suffix = Path(filename).suffix.lower()
        media_type = _AUDIO_MEDIA_TYPES.get(suffix)
        if media_type is None:
            raise HTTPException(status_code=404)
        path = audio_dir / filename
        if not path.is_file():
            raise HTTPException(status_code=404)
        return FileResponse(path, media_type=media_type)

    return application


# Default app instance for uvicorn
app = create_app()
