"""Mentor routes: diagnostics on behalf of linked learners (F2).

This module anchors the mentor-only surface introduced in F2-01. The
``GET /mentor/mentees`` endpoint lists the caller's linked learners and
``GET /mentor/{user_id}/profile`` proves the per-learner guard works.
Richer telemetry endpoints (last wrong answers, stumbling-block overview)
are layered on top in F2-02 and F2-03.
"""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Request

from gymnasium_classica.api.auth import get_current_user_id, require_mentor_of
from gymnasium_classica.api.database import get_user, list_mentees
from gymnasium_classica.api.schemas import (
    MenteeListResponse,
    MenteeSummary,
    MentorLearnerProfileResponse,
)
from gymnasium_classica.models.user import Role

router = APIRouter(prefix="/mentor", tags=["mentor"])


@router.get("/mentees", response_model=MenteeListResponse)
async def get_mentees(
    request: Request,
    mentor_id: str = Depends(get_current_user_id),
) -> MenteeListResponse:
    """List the learners linked to the authenticated mentor.

    Requires the MENTOR role. A learner calling this gets 403 even though
    they are authenticated, because the data is meaningless for them.
    """
    db: sqlite3.Connection = request.app.state.db
    mentor = get_user(db, mentor_id)
    if mentor is None or mentor.role != Role.MENTOR:
        raise HTTPException(status_code=403, detail="Mentor role required")

    summaries: list[MenteeSummary] = []
    for learner_id in list_mentees(db, mentor_id):
        learner = get_user(db, learner_id)
        if learner is not None:
            summaries.append(MenteeSummary(user_id=str(learner.id), email=learner.email))
    return MenteeListResponse(mentees=summaries)


@router.get("/{user_id}/profile", response_model=MentorLearnerProfileResponse)
async def get_learner_profile(
    user_id: str,
    request: Request,
    mentor_id: str = Depends(require_mentor_of),
) -> MentorLearnerProfileResponse:
    """Return a linked learner's basic profile.

    Guarded by :func:`require_mentor_of`: the caller must hold the MENTOR
    role *and* be assigned to ``user_id``, else 403.
    """
    db: sqlite3.Connection = request.app.state.db
    learner = get_user(db, user_id)
    if learner is None:
        raise HTTPException(status_code=404, detail="Learner not found")
    return MentorLearnerProfileResponse(
        user_id=str(learner.id),
        email=learner.email,
        role=learner.role.value,
    )
