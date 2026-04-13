"""SQLite database connection and schema management."""

import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path("data/gymnasium_classica.db")

_CREATE_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    data TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS learner_models (
    user_id TEXT PRIMARY KEY,
    data TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS auth_tokens (
    token TEXT PRIMARY KEY,
    user_id TEXT NOT NULL
);
"""


def get_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Create a SQLite connection with WAL mode and foreign keys enabled."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Initialise the database: create tables if they don't exist and return the connection."""
    conn = get_connection(db_path)
    conn.executescript(_CREATE_SCHEMA)
    conn.commit()
    return conn
