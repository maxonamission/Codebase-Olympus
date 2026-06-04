"""Mentor routes: diagnostics on behalf of linked learners (F2).

This module anchors the mentor-only surface introduced in F2-01. The
``GET /mentor/mentees`` endpoint lists the caller's linked learners and
``GET /mentor/{user_id}/profile`` proves the per-learner guard works.
Richer telemetry endpoints (last wrong answers, stumbling-block overview)
are layered on top in F2-02 and F2-03.
"""

import sqlite3

import networkx as nx
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from gymnasium_classica.api.auth import get_current_user_id, require_mentor_of
from gymnasium_classica.api.database import get_user, list_mentees, load_learner_model
from gymnasium_classica.api.schemas import (
    MenteeListResponse,
    MenteeSummary,
    MentorAttempt,
    MentorAttemptsResponse,
    MentorLearnerProfileResponse,
)
from gymnasium_classica.models.graph import Node
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


@router.get("/{user_id}/knoop/{knoop_id}/attempts", response_model=MentorAttemptsResponse)
async def get_node_attempts(
    user_id: str,
    knoop_id: str,
    request: Request,
    mentor_id: str = Depends(require_mentor_of),
    limit: int = Query(default=10, ge=1, le=100),
) -> MentorAttemptsResponse:
    """Return the learner's most recent *literal* attempts on one node.

    Newest first, capped at ``limit``. Self-assessment responses (no
    typed answer, ``answer_text is None``) are filtered out — a mentor
    coaching a concrete mistake needs the actual characters the learner
    produced, which those rows don't carry.

    Guarded by :func:`require_mentor_of`.
    """
    graph: nx.DiGraph = request.app.state.graph
    if knoop_id not in graph.nodes:
        raise HTTPException(status_code=404, detail=f"Knoop {knoop_id!r} not found")
    node: Node = graph.nodes[knoop_id]["node"]

    db: sqlite3.Connection = request.app.state.db
    learner = load_learner_model(db, user_id)

    attempts: list[MentorAttempt] = []
    if learner is not None:
        state = learner.node_states.get(knoop_id)
        if state is not None:
            literal = [ir for ir in state.item_history if ir.answer_text is not None]
            literal.sort(key=lambda ir: ir.timestamp, reverse=True)
            for ir in literal[:limit]:
                attempts.append(
                    MentorAttempt(
                        timestamp=ir.timestamp.isoformat(),
                        item_id=ir.item_id,
                        # answer_text is non-None here (filtered above)
                        answer_text=ir.answer_text or "",
                        correct_answer=ir.correct_answer,
                        correct=ir.correct,
                        response_time_ms=ir.response_time_ms,
                        item_type=ir.item_type,
                    )
                )

    return MentorAttemptsResponse(
        user_id=user_id,
        knoop_id=knoop_id,
        knoop_title=node.title_nl,
        attempts=attempts,
    )
