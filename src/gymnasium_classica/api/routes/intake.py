"""Intake routes: start and answer diagnostic placement questions."""

import networkx as nx
from fastapi import APIRouter, Depends, HTTPException, Request

from gymnasium_classica.api.auth import get_current_user_id
from gymnasium_classica.api.database import (
    get_user,
    load_learner_model,
    save_learner_model,
    update_user,
)
from gymnasium_classica.api.intake_manager import IntakeManager, IntakeQuestion
from gymnasium_classica.api.schemas import (
    BijspijkerIntakeRequest,
    BijspijkerIntakeResponse,
    IntakeAnswerRequest,
    IntakeAnswerResponse,
    IntakeQuestionResponse,
    IntakeStartRequest,
    IntakeStartResponse,
)
from gymnasium_classica.diagnostic.methode_profile import (
    apply_methode_profile,
    get_treated_node_ids,
    load_methode_mapping,
)
from gymnasium_classica.models.learner import LearnerModel, MasterySource, NodeState
from gymnasium_classica.models.user import Modus
from gymnasium_classica.scheduling.bijspijker import BijspijkerPlanner, BijspijkerTarget

router = APIRouter(prefix="/intake", tags=["intake"])

intake_manager = IntakeManager()


def _question_to_response(q: IntakeQuestion | None) -> IntakeQuestionResponse | None:
    if q is None:
        return None
    return IntakeQuestionResponse(
        node_id=q.node_id,
        title=q.title,
        description=q.description,
        questions_asked=q.questions_asked,
        max_questions=q.max_questions,
    )


@router.post("/start", response_model=IntakeStartResponse)
async def start_intake(
    request: Request,
    body: IntakeStartRequest | None = None,
    user_id: str = Depends(get_current_user_id),
) -> IntakeStartResponse:
    """Start a diagnostic intake. Optionally provide methode + chapter for priors."""
    db = request.app.state.db
    graph: nx.DiGraph = request.app.state.graph

    # Load or create learner model
    learner = load_learner_model(db, user_id)
    if learner is None:
        from uuid import UUID

        learner = LearnerModel(user_id=UUID(user_id))

    if learner.intake_completed:
        save_learner_model(db, learner)
        return IntakeStartResponse(
            intake_id="",
            already_completed=True,
        )

    # Apply methode profile if provided
    if body and body.methode and body.chapter:
        try:
            apply_methode_profile(learner, graph, body.methode, body.chapter)
        except (ValueError, FileNotFoundError) as err:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown methode {body.methode!r} or invalid chapter {body.chapter!r}",
            ) from err

    intake_id, question = intake_manager.start_intake(user_id, learner, graph)
    save_learner_model(db, learner)

    return IntakeStartResponse(
        intake_id=intake_id,
        question=_question_to_response(question),
    )


@router.post("/bijspijker", response_model=BijspijkerIntakeResponse)
async def start_bijspijker(
    body: BijspijkerIntakeRequest,
    request: Request,
    user_id: str = Depends(get_current_user_id),
) -> BijspijkerIntakeResponse:
    """Switch a user to bijspijker mode and plan a catch-up route (M1-03)."""
    db = request.app.state.db
    graph: nx.DiGraph = request.app.state.graph

    lat_ok = bool(body.methode_lat and body.hoofdstuk_lat)
    grc_ok = bool(body.methode_grc and body.hoofdstuk_grc)
    if not (lat_ok or grc_ok):
        raise HTTPException(
            status_code=400,
            detail="Geef voor minstens één taal methode + hoofdstuk op.",
        )

    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    mapping = load_methode_mapping()
    treated: set[str] = set()
    targets: list[BijspijkerTarget] = []
    try:
        if body.methode_lat and body.hoofdstuk_lat:
            treated |= get_treated_node_ids(mapping, body.methode_lat, str(body.hoofdstuk_lat))
            targets.append(BijspijkerTarget(body.methode_lat, body.hoofdstuk_lat))
        if body.methode_grc and body.hoofdstuk_grc:
            treated |= get_treated_node_ids(mapping, body.methode_grc, str(body.hoofdstuk_grc))
            targets.append(BijspijkerTarget(body.methode_grc, body.hoofdstuk_grc))
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err

    # Persist mode + method/chapter on the user (validator enforces consistency).
    user.modus = Modus.BIJSPIJKER
    user.huidige_methode_lat = body.methode_lat if lat_ok else None
    user.huidige_hoofdstuk_lat = body.hoofdstuk_lat if lat_ok else None
    user.huidige_methode_grc = body.methode_grc if grc_ok else None
    user.huidige_hoofdstuk_grc = body.hoofdstuk_grc if grc_ok else None
    update_user(db, user)

    # Set diagnostic priors over the union of treated nodes, then plan.
    from uuid import UUID

    learner = load_learner_model(db, user_id) or LearnerModel(user_id=UUID(user_id))
    for node_id in graph.nodes:
        prior = 0.70 if node_id in treated else 0.10
        learner.node_states[node_id] = NodeState(
            node_id=node_id,
            posterior_mastery=prior,
            source=MasterySource.DIAGNOSTIC,
        )
    save_learner_model(db, learner)

    plan = BijspijkerPlanner(graph, mapping).plan(learner, targets)
    return BijspijkerIntakeResponse(
        doelset_size=len(plan.doelset),
        diagnose_size=len(plan.diagnose),
        eta_dagen=plan.eta_dagen,
        fractie_bij=plan.fractie_bij,
        eerste_diagnose_node_ids=plan.diagnose[: plan.intro_per_sessie],
    )


@router.post("/answer", response_model=IntakeAnswerResponse)
async def submit_intake_answer(
    body: IntakeAnswerRequest,
    request: Request,
    user_id: str = Depends(get_current_user_id),
) -> IntakeAnswerResponse:
    """Submit an answer to an intake diagnostic question."""
    if not intake_manager.has_intake(body.intake_id):
        raise HTTPException(status_code=404, detail="Intake not found")

    state = intake_manager.get_intake_state(body.intake_id)
    if state.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your intake")

    try:
        result = intake_manager.submit_answer(body.intake_id, body.correct)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    # Persist learner model after each answer
    db = request.app.state.db
    save_learner_model(db, state.learner)

    return IntakeAnswerResponse(
        questions_asked=result.questions_asked,
        next_question=_question_to_response(result.next_question),
        finished=result.finished,
        converged=result.converged,
    )
