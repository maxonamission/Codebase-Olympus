#!/usr/bin/env python3
"""Seed the development database with a test user.

Creates:
- A test user (demo@gymnasium.nl / wachtwoord123)
- Fortuna chapter 3 intake profile
- 20 nodes promoted to full mastery (posterior >= 0.80)
- Some session history for streak display

Usage:
    python scripts/seed_dev.py
"""

import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from gymnasium_classica.diagnostic.methode_profile import apply_methode_profile
from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.learner import (
    LearnerModel,
    MasterySource,
    SessionRecord,
)
from gymnasium_classica.models.user import User
from gymnasium_classica.scheduling.priority import MASTERY_THRESHOLD

DB_PATH = PROJECT_ROOT / "data" / "gymnasium_classica.db"
DEMO_EMAIL = "demo@gymnasium.nl"
DEMO_PASSWORD = "wachtwoord123"


def init_db(conn: sqlite3.Connection) -> None:
    """Create tables if they don't exist."""
    conn.executescript("""
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
    """)


def hash_password(password: str) -> str:
    """Hash password for the dev seed.

    Uses bcrypt directly if available, falls back to hashlib.
    The backend auth module determines the canonical hashing strategy.
    """
    try:
        import bcrypt

        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    except Exception:
        import hashlib
        import os

        salt = os.urandom(16).hex()
        hashed = hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()
        return f"sha256:{salt}:{hashed}"


def main() -> None:
    print("=== Gymnasium Classica: Seed Dev Database ===\n")

    # Load graph
    graph_dir = PROJECT_ROOT / "data" / "graph"
    graph = load_graph(graph_dir)
    print(f"Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")

    # Create user
    user_id = uuid4()
    user = User(id=user_id, email=DEMO_EMAIL)
    print(f"User: {DEMO_EMAIL} / {DEMO_PASSWORD}")
    print(f"  ID: {user_id}")

    # Create learner model with Fortuna chapter 3 profile
    learner = LearnerModel(user_id=user_id)
    apply_methode_profile(learner, graph, "fortuna", "3")
    learner.intake_completed = True

    treated = sum(1 for s in learner.node_states.values() if s.posterior_mastery >= 0.50)
    print(f"  Intake: Fortuna hfst. 3 → {treated} treated nodes (prior 0.70)")

    # Promote 20 nodes to full mastery
    promoted = 0
    now = datetime.now()
    for _node_id, state in learner.node_states.items():
        if promoted >= 20:
            break
        if state.posterior_mastery >= 0.50:
            state.posterior_mastery = 0.85
            state.source = MasterySource.PRACTICE
            state.repetitions = 3
            state.interval_days = 7.0
            state.last_review = now - timedelta(days=1)
            promoted += 1

    print(f"  Promoted {promoted} nodes to mastery (>= {MASTERY_THRESHOLD})")

    # Add session history (3 days streak)
    for days_ago in [3, 2, 1]:
        session_time = now - timedelta(days=days_ago)
        learner.session_history.append(
            SessionRecord(
                session_id=str(uuid4())[:8],
                started_at=session_time,
                ended_at=session_time + timedelta(minutes=30),
                items_reviewed=[],
            )
        )
    print(f"  Session history: {len(learner.session_history)} sessions (3-day streak)")

    # Write to SQLite
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    init_db(conn)

    # Remove existing demo user
    conn.execute("DELETE FROM users WHERE email = ?", (DEMO_EMAIL,))
    conn.execute("DELETE FROM learner_models WHERE user_id = ?", (str(user_id),))

    password_hash = hash_password(DEMO_PASSWORD)

    conn.execute(
        "INSERT INTO users (id, email, password_hash, data) VALUES (?, ?, ?, ?)",
        (str(user_id), DEMO_EMAIL, password_hash, user.model_dump_json()),
    )
    conn.execute(
        "INSERT INTO learner_models (user_id, data) VALUES (?, ?)",
        (str(user_id), learner.model_dump_json()),
    )
    conn.commit()
    conn.close()

    print(f"\nDatabase: {DB_PATH}")
    print("Done! Start the app with: python scripts/run_dev.py")


if __name__ == "__main__":
    main()
