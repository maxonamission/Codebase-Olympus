"""Authentication helpers: password hashing, token generation, current-user dependency."""

import hashlib
import os
import sqlite3
from uuid import uuid4

from fastapi import Depends, Header, HTTPException, Request

from gymnasium_classica.api.database import get_user, is_mentor_of
from gymnasium_classica.models.user import Role


def hash_password(plain: str) -> str:
    """Hash a plaintext password with PBKDF2-SHA256."""
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", plain.encode(), salt, iterations=260_000)
    return f"{salt.hex()}${dk.hex()}"


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against a PBKDF2-SHA256 hash."""
    salt_hex, dk_hex = hashed.split("$", 1)
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", plain.encode(), salt, iterations=260_000)
    return dk.hex() == dk_hex


def generate_token() -> str:
    """Generate a random UUID-based auth token."""
    return uuid4().hex


def get_current_user_id(
    request: Request,
    authorization: str = Header(..., description="Bearer <token>"),
) -> str:
    """FastAPI dependency: extract and validate the auth token, return user_id."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.removeprefix("Bearer ")
    db: sqlite3.Connection = request.app.state.db
    row = db.execute("SELECT user_id FROM auth_tokens WHERE token = ?", (token,)).fetchone()
    if row is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id: str = row["user_id"]
    return user_id


def require_mentor_of(
    user_id: str,
    request: Request,
    mentor_id: str = Depends(get_current_user_id),
) -> str:
    """FastAPI dependency: authorise the caller as a mentor of *user_id*.

    The path parameter ``user_id`` identifies the learner being viewed.
    Returns the authenticated mentor's ID on success. Raises 403 when the
    caller lacks the MENTOR role or has no assignment to that learner —
    the two failure modes are deliberately indistinguishable to avoid
    leaking which learners exist.
    """
    db: sqlite3.Connection = request.app.state.db
    mentor = get_user(db, mentor_id)
    if mentor is None or mentor.role != Role.MENTOR:
        raise HTTPException(status_code=403, detail="Mentor role required")
    if not is_mentor_of(db, mentor_id, user_id):
        raise HTTPException(status_code=403, detail="Not assigned to this learner")
    return mentor_id
