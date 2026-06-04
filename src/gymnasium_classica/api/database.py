"""SQLite database connection, schema management, and CRUD operations."""

import sqlite3
from datetime import datetime
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

CREATE TABLE IF NOT EXISTS mentor_assignments (
    mentor_id TEXT NOT NULL,
    learner_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (mentor_id, learner_id),
    FOREIGN KEY (mentor_id) REFERENCES users(id),
    FOREIGN KEY (learner_id) REFERENCES users(id)
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


# ---------------------------------------------------------------------------
# CRUD: Mentor assignments (F2-01)
# ---------------------------------------------------------------------------


def create_mentor_assignment(conn: sqlite3.Connection, mentor_id: str, learner_id: str) -> None:
    """Link a mentor to a learner. Idempotent: re-linking is a no-op.

    The caller is responsible for ensuring ``mentor_id`` belongs to a user
    with the MENTOR role; this function only records the relationship.
    """
    conn.execute(
        "INSERT OR IGNORE INTO mentor_assignments (mentor_id, learner_id, created_at) "
        "VALUES (?, ?, ?)",
        (mentor_id, learner_id, datetime.now().isoformat()),
    )
    conn.commit()


def is_mentor_of(conn: sqlite3.Connection, mentor_id: str, learner_id: str) -> bool:
    """Return True if an assignment links *mentor_id* to *learner_id*."""
    row = conn.execute(
        "SELECT 1 FROM mentor_assignments WHERE mentor_id = ? AND learner_id = ?",
        (mentor_id, learner_id),
    ).fetchone()
    return row is not None


def list_mentees(conn: sqlite3.Connection, mentor_id: str) -> list[str]:
    """Return the learner IDs assigned to *mentor_id*, oldest link first."""
    rows = conn.execute(
        "SELECT learner_id FROM mentor_assignments WHERE mentor_id = ? ORDER BY created_at",
        (mentor_id,),
    ).fetchall()
    return [row["learner_id"] for row in rows]
