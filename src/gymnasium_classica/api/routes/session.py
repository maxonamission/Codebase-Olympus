"""Session routes: start, answer, summary."""

import networkx as nx
from fastapi import APIRouter, Depends, HTTPException, Request

from gymnasium_classica.api.auth import get_current_user_id
from gymnasium_classica.api.database import get_user, load_learner_model, save_learner_model
from gymnasium_classica.api.schemas import (
    AnswerRequest,
    AnswerResponse,
    FeedbackResponse,
    ItemInfo,
    MasteryChange,
    QuestionResponse,
    SessionSummaryResponse,
    StartSessionResponse,
    VocabMetadata,
)
from gymnasium_classica.api.session_manager import Question, SessionManager
from gymnasium_classica.models.learner import LearnerModel, ResponseType
from gymnasium_classica.vocab.loader import VocabEntry

router = APIRouter(prefix="/session", tags=["session"])

# Module-level session manager (shared across requests)
session_manager = SessionManager()


def _vocab_entry_to_metadata(entry: VocabEntry) -> VocabMetadata:
    """Map compact VocabEntry fields to the self-explanatory wire schema."""
    return VocabMetadata(
        lemma=entry.lemma,
        part_of_speech=entry.pos,
        conjugation=entry.conj,
        forms=entry.gen,
        meaning=entry.mean,
        cluster=entry.cl,
    )


def _question_to_response(
    q: Question | None,
    vocab_metadata: dict[str, VocabEntry] | None = None,
) -> QuestionResponse | None:
    """Convert internal Question to API QuestionResponse.

    *vocab_metadata* is the knoop-ID-keyed lookup from
    :func:`gymnasium_classica.vocab.loader.load_vocab_metadata`.  When
    the question is about a V-knoop and a matching entry exists, the
    structured metadata is attached on ``vocab_metadata``.
    """
    if q is None:
        return None
    metadata: VocabMetadata | None = None
    if vocab_metadata:
        entry = vocab_metadata.get(q.knoop_id)
        if entry is not None:
            metadata = _vocab_entry_to_metadata(entry)
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
        scaffolding_content=q.scaffolding_content,
        vocab_metadata=metadata,
        item_type=q.item_type,
        instruction=q.instruction,
        options=q.options,
        hint=q.hint,
        audio_ref=q.audio_ref,
    )


@router.post("/start", response_model=StartSessionResponse)
async def start_session(
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """Start a new learning session. Returns session_id and the first question.

    Automatically uses the user's learning_route preference and loads
    passages from the server when the route is context_first.
    """
    db = request.app.state.db
    graph: nx.DiGraph = request.app.state.graph
    passages = getattr(request.app.state, "passages", [])

    # Load or create learner model
    learner = load_learner_model(db, user_id)
    if learner is None:
        from uuid import UUID

        learner = LearnerModel(user_id=UUID(user_id))

    # Read the user's learning route preference
    from gymnasium_classica.models.user import LearningRoute

    user = get_user(db, user_id)
    learning_route = user.learning_route if user is not None else LearningRoute.GRAMMAR_FIRST
    show_grammar_scaffolding = user.show_grammar_scaffolding if user is not None else True

    session_id, question = session_manager.start_session(
        user_id,
        learner,
        graph,
        learning_route=learning_route,
        passages=passages,
        show_grammar_scaffolding=show_grammar_scaffolding,
    )

    # Persist learner model after session start
    save_learner_model(db, learner)

    vocab_metadata = getattr(request.app.state, "vocab_metadata", {})
    return StartSessionResponse(
        session_id=session_id,
        question=_question_to_response(question, vocab_metadata),
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

    # Either answer_text (server grades) or response (self-assess) is required.
    if body.answer_text is None and body.response is None:
        raise HTTPException(
            status_code=422,
            detail="Either 'answer_text' or 'response' must be provided.",
        )

    response: ResponseType | None = None
    if body.response is not None:
        try:
            response = ResponseType(body.response)
        except ValueError as err:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Invalid response: {body.response!r}. "
                    "Must be correct, incorrect, or slow_correct."
                ),
            ) from err

    try:
        result = session_manager.submit_answer(
            body.session_id,
            response,
            body.response_time_ms,
            answer_text=body.answer_text,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    # Persist learner model after each answer
    db = request.app.state.db
    save_learner_model(db, state.learner)

    vocab_metadata = getattr(request.app.state, "vocab_metadata", {})
    return AnswerResponse(
        feedback=FeedbackResponse(
            knoop_id=result.feedback.knoop_id,
            correct=result.feedback.correct,
            response_type=result.feedback.response_type,
            mastery_before=result.feedback.mastery_before,
            mastery_after=result.feedback.mastery_after,
        ),
        next_question=_question_to_response(result.next_question, vocab_metadata),
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
            k: MasteryChange(before=v[0], after=v[1]) for k, v in summary.mastery_changes.items()
        },
        phases_completed=summary.phases_completed,
    )
