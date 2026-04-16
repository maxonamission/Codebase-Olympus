"""Auth routes: register, login, and settings."""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Request

from gymnasium_classica.api.auth import (
    generate_token,
    get_current_user_id,
    hash_password,
    verify_password,
)
from gymnasium_classica.api.database import (
    create_user,
    get_user,
    get_user_by_email,
    load_learner_model,
    save_learner_model,
    update_user,
)
from gymnasium_classica.api.schemas import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UpdateLearningRouteRequest,
    UserProfileResponse,
)
from gymnasium_classica.models.learner import LearnerModel, RouteSwitch
from gymnasium_classica.models.user import LearningRoute, User

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


@router.post("/settings", response_model=UserProfileResponse)
async def update_settings(
    body: UpdateLearningRouteRequest,
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """Update user settings (currently: learning_route).

    POST /auth/settings { learning_route: "grammar_first" | "context_first" }
    """
    db: sqlite3.Connection = request.app.state.db

    try:
        route = LearningRoute(body.learning_route)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid learning_route: {body.learning_route!r}. "
            "Must be 'grammar_first' or 'context_first'.",
        )

    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.learning_route = route
    update_user(db, user)

    # Track the route switch in the learner model
    from datetime import datetime
    from uuid import UUID

    learner = load_learner_model(db, user_id)
    if learner is None:
        learner = LearnerModel(user_id=UUID(user_id))
    learner.route_history.append(
        RouteSwitch(timestamp=datetime.now(), route=route.value)
    )
    save_learner_model(db, learner)

    return UserProfileResponse(
        user_id=str(user.id),
        email=user.email,
        learning_route=user.learning_route.value,
    )
