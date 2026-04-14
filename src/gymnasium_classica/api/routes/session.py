"""Session routes: start, answer, summary."""

import networkx as nx
from fastapi import APIRouter, Depends, HTTPException, Request

from gymnasium_classica.api.auth import get_current_user_id
from gymnasium_classica.api.database import load_learner_model, save_learner_model
from gymnasium_classica.api.schemas import (
    AnswerRequest,
    AnswerResponse,
    FeedbackResponse,
    ItemInfo,
    MasteryChange,
    QuestionResponse,
    SessionSummaryResponse,
    StartSessionResponse,
)
from gymnasium_classica.api.session_manager import Question, SessionManager
from gymnasium_classica.models.learner import LearnerModel, ResponseType

router = APIRouter(prefix="/session", tags=["session"])

# Module-level session manager (shared across requests)
session_manager = SessionManager()


def _question_to_response(q: Question | None) -> QuestionResponse | None:
    """Convert internal Question to API QuestionResponse."""
    if q is None:
        return None
    return QuestionResponse(
        knoop_id=q.knoop_id,
        titel=q.titel,
        beschrijving=q.beschrijving,
        stimulus=q.stimulus,
        phase=q.phase,
        items=[
            ItemInfo(
                id=item["id"],
                type=item["type"],
                stimulus=item["stimulus"],
                feedback=item["feedback"],
                verwachte_tijd_sec=item["verwachte_tijd_sec"],
            )
            for item in q.items
        ],
    )


@router.post("/start", response_model=StartSessionResponse)
async def start_session(
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """Start a new learning session. Returns session_id and the first question."""
    db = request.app.state.db
    graph: nx.DiGraph = request.app.state.graph

    # Load or create learner model
    learner = load_learner_model(db, user_id)
    if learner is None:
        from uuid import UUID

        learner = LearnerModel(user_id=UUID(user_id))

    session_id, question = session_manager.start_session(user_id, learner, graph)

    # Persist learner model after session start
    save_learner_model(db, learner)

    return StartSessionResponse(
        session_id=session_id,
        question=_question_to_response(question),
    )


@router.post("/answer", response_model=AnswerResponse)
async def submit_answer(
    body: AnswerRequest,
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """Submit an answer to the current question. Returns feedback and the next question."""
    if not session_manager.has_session(body.session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    # Validate that this user owns the session
    state = session_manager.get_session_state(body.session_id)
    if state.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your session")

    # Validate response type
    try:
        response = ResponseType(body.response)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid response: {body.response!r}. Must be correct, incorrect, or slow_correct.",
        )

    try:
        result = session_manager.submit_answer(
            body.session_id, response, body.response_time_ms
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Persist learner model after each answer
    db = request.app.state.db
    save_learner_model(db, state.learner)

    return AnswerResponse(
        feedback=FeedbackResponse(
            knoop_id=result.feedback.knoop_id,
            correct=result.feedback.correct,
            mastery_before=result.feedback.mastery_before,
            mastery_after=result.feedback.mastery_after,
        ),
        next_question=_question_to_response(result.next_question),
        session_finished=result.session_finished,
    )


@router.get("/{session_id}/summary", response_model=SessionSummaryResponse)
async def get_session_summary(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Return a summary of a completed (or in-progress) session."""
    if not session_manager.has_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    state = session_manager.get_session_state(session_id)
    if state.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your session")

    summary = session_manager.get_summary(session_id)
    return SessionSummaryResponse(
        session_id=summary.session_id,
        started_at=summary.started_at,
        ended_at=summary.ended_at,
        total_items=summary.total_items,
        nodes_introduced=summary.nodes_introduced,
        nodes_reviewed=summary.nodes_reviewed,
        mastery_changes={
            k: MasteryChange(before=v[0], after=v[1])
            for k, v in summary.mastery_changes.items()
        },
        phases_completed=summary.phases_completed,
    )
