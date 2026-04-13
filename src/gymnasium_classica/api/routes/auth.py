"""Auth routes: register and login."""

import sqlite3

from fastapi import APIRouter, HTTPException, Request

from gymnasium_classica.api.auth import generate_token, hash_password, verify_password
from gymnasium_classica.api.database import create_user, get_user_by_email
from gymnasium_classica.api.schemas import AuthResponse, LoginRequest, RegisterRequest
from gymnasium_classica.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(body: RegisterRequest, request: Request):
    """Register a new user with email + password. Returns user_id and auth token."""
    db: sqlite3.Connection = request.app.state.db

    # Check for existing email
    existing = db.execute("SELECT id FROM users WHERE email = ?", (body.email,)).fetchone()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Create User model and persist via CRUD
    user = User(email=body.email)
    pw_hash = hash_password(body.password)
    create_user(db, user, pw_hash)

    # Generate and store token
    user_id = str(user.id)
    token = generate_token()
    db.execute("INSERT INTO auth_tokens (token, user_id) VALUES (?, ?)", (token, user_id))
    db.commit()

    return AuthResponse(user_id=user_id, token=token)


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest, request: Request):
    """Login with email + password. Returns user_id and auth token."""
    db: sqlite3.Connection = request.app.state.db

    row = db.execute(
        "SELECT id, password_hash FROM users WHERE email = ?", (body.email,)
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate a new token for this login session
    token = generate_token()
    db.execute("INSERT INTO auth_tokens (token, user_id) VALUES (?, ?)", (token, row["id"]))
    db.commit()

    return AuthResponse(user_id=row["id"], token=token)
