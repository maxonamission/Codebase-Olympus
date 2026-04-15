"""User settings routes: profile and learning route."""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Request

from gymnasium_classica.api.auth import get_current_user_id
from gymnasium_classica.api.database import get_user, update_user
from gymnasium_classica.api.schemas import (
    UpdateLearningRouteRequest,
    UserProfileResponse,
)
from gymnasium_classica.models.user import LearningRoute

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """Return the current user's profile including learning route."""
    db: sqlite3.Connection = request.app.state.db
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfileResponse(
        user_id=str(user.id),
        email=user.email,
        learning_route=user.learning_route.value,
    )


@router.put("/learning-route", response_model=UserProfileResponse)
async def update_learning_route(
    body: UpdateLearningRouteRequest,
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """Update the user's learning route preference.

    Accepts 'grammar_first' or 'context_first'.
    """
    db: sqlite3.Connection = request.app.state.db

    # Validate the route value
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

    return UserProfileResponse(
        user_id=str(user.id),
        email=user.email,
        learning_route=user.learning_route.value,
    )
