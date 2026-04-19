"""SQLite database connection, schema management, and CRUD operations."""

import sqlite3
from pathlib import Path

from gymnasium_classica.models.learner import LearnerModel
from gymnasium_classica.models.user import User

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
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
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


# ---------------------------------------------------------------------------
# CRUD: Users
# ---------------------------------------------------------------------------


def create_user(conn: sqlite3.Connection, user: User, password_hash: str) -> None:
    """Insert a new user into the database."""
    conn.execute(
        "INSERT INTO users (id, email, password_hash, data) VALUES (?, ?, ?, ?)",
        (str(user.id), user.email, password_hash, user.model_dump_json()),
    )
    conn.commit()


def get_user(conn: sqlite3.Connection, user_id: str) -> User | None:
    """Load a user by ID, returning None if not found."""
    row = conn.execute("SELECT data FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        return None
    return User.model_validate_json(row["data"])


def get_user_by_email(conn: sqlite3.Connection, email: str) -> User | None:
    """Load a user by email address, returning None if not found."""
    row = conn.execute("SELECT data FROM users WHERE email = ?", (email,)).fetchone()
    if row is None:
        return None
    return User.model_validate_json(row["data"])


def update_user(conn: sqlite3.Connection, user: User) -> None:
    """Update an existing user's data column."""
    conn.execute(
        "UPDATE users SET data = ? WHERE id = ?",
        (user.model_dump_json(), str(user.id)),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# CRUD: LearnerModels
# ---------------------------------------------------------------------------


def save_learner_model(conn: sqlite3.Connection, model: LearnerModel) -> None:
    """Insert or replace the learner model for a user."""
    conn.execute(
        "INSERT OR REPLACE INTO learner_models (user_id, data) VALUES (?, ?)",
        (str(model.user_id), model.model_dump_json()),
    )
    conn.commit()


def load_learner_model(conn: sqlite3.Connection, user_id: str) -> LearnerModel | None:
    """Load the learner model for a user, returning None if not found."""
    row = conn.execute("SELECT data FROM learner_models WHERE user_id = ?", (user_id,)).fetchone()
    if row is None:
        return None
    return LearnerModel.model_validate_json(row["data"])
