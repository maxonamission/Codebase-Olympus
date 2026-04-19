"""Progress routes: overview and per-knoop detail."""

from datetime import datetime, timedelta
from typing import Any

import networkx as nx
from fastapi import APIRouter, Depends, HTTPException, Request

from gymnasium_classica.api.auth import get_current_user_id
from gymnasium_classica.api.database import load_learner_model
from gymnasium_classica.api.schemas import (
    ClusterProgress,
    ClustersResponse,
    DomainProgress,
    GraphDataResponse,
    GraphEdge,
    GraphNode,
    ItemHistoryEntry,
    KnoopProgressResponse,
    ProgressOverviewResponse,
    SessionMasteryEntry,
)
from gymnasium_classica.models.graph import KennisKnoop, KnoopType, PrerequisiteEdge
from gymnasium_classica.models.learner import LearnerModel
from gymnasium_classica.scheduling.priority import MASTERY_THRESHOLD

router = APIRouter(prefix="/progress", tags=["progress"])

# A node is "in progress" when it has a state but is not yet mastered
_IN_PROGRESS_FLOOR = 0.15  # Above default prior → learner has interacted


def _compute_streak(learner: LearnerModel) -> int:
    """Compute the current study streak in consecutive days (up to today)."""
    if not learner.session_history:
        return 0

    # Collect unique dates of sessions
    session_dates: set[str] = set()
    for rec in learner.session_history:
        if rec.started_at:
            session_dates.add(rec.started_at.date().isoformat())

    if not session_dates:
        return 0

    today = datetime.now().date()
    streak = 0
    day = today
    while day.isoformat() in session_dates:
        streak += 1
        day -= timedelta(days=1)

    return streak


def _compute_session_progression(
    learner: LearnerModel,
    graph: nx.DiGraph,
) -> list[SessionMasteryEntry]:
    """Compute mastery progression per session for route comparison.

    For each session in the learner's history, counts how many nodes
    were practiced and how many total nodes are mastered at that point
    in time (cumulative).  The learning_route field allows filtering
    by route on the frontend/analytics side.
    """
    entries: list[SessionMasteryEntry] = []
    # Track cumulative mastered count by replaying session order.
    # Since we don't have per-session snapshots of all posteriors,
    # we use the current mastery state and the session's items_reviewed
    # as a proxy: nodes_practiced = len(items_reviewed).
    # mastered_after = cumulative mastered nodes up to and including this session.
    seen_mastered: set[str] = set()

    for rec in learner.session_history:
        for node_id in rec.items_reviewed:
            state = learner.knoop_states.get(node_id)
            if state and state.posterior_mastery >= MASTERY_THRESHOLD:
                seen_mastered.add(node_id)

        entries.append(
            SessionMasteryEntry(
                session_id=rec.session_id,
                timestamp=rec.started_at.isoformat() if rec.started_at else "",
                learning_route=rec.learning_route,
                nodes_practiced=len(rec.items_reviewed),
                mastered_after=len(seen_mastered),
            )
        )

    return entries


@router.get("/overview", response_model=ProgressOverviewResponse)
async def progress_overview(
    request: Request,
    user_id: str = Depends(get_current_user_id),
) -> ProgressOverviewResponse:
    """Return a progress overview: nodes per status, per domain, and streak."""
    db = request.app.state.db
    graph: nx.DiGraph = request.app.state.graph

    learner = load_learner_model(db, user_id)
    if learner is None:
        # No learner model yet — everything is unseen
        total = graph.number_of_nodes()
        domains: dict[str, DomainProgress] = {}
        for node_id in graph.nodes:
            knoop: KennisKnoop = graph.nodes[node_id]["knoop"]
            d = knoop.type.value
            if d not in domains:
                domains[d] = DomainProgress(total=0, mastered=0, in_progress=0, unseen=0)
            domains[d].total += 1
            domains[d].unseen += 1
        return ProgressOverviewResponse(
            total_nodes=total,
            mastered=0,
            in_progress=0,
            unseen=total,
            domains=domains,
            streak_days=0,
            intake_completed=False,
        )

    mastered = 0
    in_progress = 0
    unseen = 0
    domains = {}

    for node_id in graph.nodes:
        knoop = graph.nodes[node_id]["knoop"]
        d = knoop.type.value
        if d not in domains:
            domains[d] = DomainProgress(total=0, mastered=0, in_progress=0, unseen=0)
        domains[d].total += 1

        state = learner.knoop_states.get(node_id)
        if state is None or state.posterior_mastery < _IN_PROGRESS_FLOOR:
            unseen += 1
            domains[d].unseen += 1
        elif state.posterior_mastery >= MASTERY_THRESHOLD:
            mastered += 1
            domains[d].mastered += 1
        else:
            in_progress += 1
            domains[d].in_progress += 1

    # Build session mastery progression for route comparison
    session_progression = _compute_session_progression(learner, graph)

    return ProgressOverviewResponse(
        total_nodes=graph.number_of_nodes(),
        mastered=mastered,
        in_progress=in_progress,
        unseen=unseen,
        domains=domains,
        streak_days=_compute_streak(learner),
        intake_completed=learner.intake_completed,
        session_progression=session_progression,
    )


@router.get("/knoop/{knoop_id}", response_model=KnoopProgressResponse)
async def knoop_progress(
    knoop_id: str,
    request: Request,
    user_id: str = Depends(get_current_user_id),
) -> KnoopProgressResponse:
    """Return detailed progress for a single knowledge node."""
    graph: nx.DiGraph = request.app.state.graph

    if knoop_id not in graph.nodes:
        raise HTTPException(status_code=404, detail=f"Knoop {knoop_id!r} not found")

    knoop: KennisKnoop = graph.nodes[knoop_id]["knoop"]

    db = request.app.state.db
    learner = load_learner_model(db, user_id)

    state = None
    if learner is not None:
        state = learner.knoop_states.get(knoop_id)

    if state is None:
        return KnoopProgressResponse(
            knoop_id=knoop_id,
            titel=knoop.titel_nl,
            type=knoop.type.value,
            posterior_mastery=0.0,
            easiness_factor=2.5,
            interval_days=0.0,
            repetitions=0,
            last_review=None,
            source="practice",
            item_history=[],
        )

    return KnoopProgressResponse(
        knoop_id=knoop_id,
        titel=knoop.titel_nl,
        type=knoop.type.value,
        posterior_mastery=state.posterior_mastery,
        easiness_factor=state.easiness_factor,
        interval_days=state.interval_days,
        repetitions=state.repetitions,
        last_review=state.last_review.isoformat() if state.last_review else None,
        source=state.source.value,
        item_history=[
            ItemHistoryEntry(
                timestamp=ir.timestamp.isoformat(),
                item_id=ir.item_id,
                correct=ir.correct,
                response_time_ms=ir.response_time_ms,
            )
            for ir in state.item_history
        ],
    )


@router.get("/clusters", response_model=ClustersResponse)
async def progress_clusters(
    request: Request,
    user_id: str = Depends(get_current_user_id),
) -> ClustersResponse:
    """Return vocabulary progress grouped by semantic cluster.

    Each cluster from ``data/vocabulaire_clusters.json`` is returned
    together with the count of V-knopen that carry the matching
    ``semantisch_cluster`` label and the learner's mastery status
    for those nodes.
    """
    graph: nx.DiGraph = request.app.state.graph
    cluster_defs: list[dict[str, Any]] = getattr(request.app.state, "clusters", []) or []

    db = request.app.state.db
    learner = load_learner_model(db, user_id)

    nodes_per_cluster: dict[str, list[str]] = {c["label"]: [] for c in cluster_defs}
    for node_id in graph.nodes:
        knoop: KennisKnoop = graph.nodes[node_id]["knoop"]
        if knoop.type != KnoopType.V:
            continue
        label = knoop.semantisch_cluster
        if not label or label not in nodes_per_cluster:
            continue
        nodes_per_cluster[label].append(node_id)

    results: list[ClusterProgress] = []
    for c in cluster_defs:
        label = c["label"]
        node_ids = nodes_per_cluster.get(label, [])
        total = len(node_ids)
        mastered = 0
        in_progress = 0
        for node_id in node_ids:
            state = None
            if learner is not None:
                state = learner.knoop_states.get(node_id)
            if state is None or state.posterior_mastery < _IN_PROGRESS_FLOOR:
                continue
            if state.posterior_mastery >= MASTERY_THRESHOLD:
                mastered += 1
            else:
                in_progress += 1
        unseen = total - mastered - in_progress
        pct = round(100.0 * mastered / total, 1) if total > 0 else 0.0
        results.append(
            ClusterProgress(
                label=label,
                beschrijving=c.get("beschrijving", ""),
                total=total,
                mastered=mastered,
                in_progress=in_progress,
                unseen=unseen,
                mastered_pct=pct,
            )
        )

    return ClustersResponse(clusters=results)


@router.get("/graph", response_model=GraphDataResponse)
async def graph_data(
    request: Request,
    user_id: str = Depends(get_current_user_id),
) -> GraphDataResponse:
    """Return the full knowledge graph with per-node mastery for visualisation."""
    db = request.app.state.db
    graph: nx.DiGraph = request.app.state.graph
    learner = load_learner_model(db, user_id)

    nodes = []
    for node_id in graph.nodes:
        knoop: KennisKnoop = graph.nodes[node_id]["knoop"]
        mastery = 0.0
        status = "unseen"
        if learner:
            state = learner.knoop_states.get(node_id)
            if state:
                mastery = state.posterior_mastery
                if mastery >= MASTERY_THRESHOLD:
                    status = "mastered"
                elif mastery >= _IN_PROGRESS_FLOOR:
                    status = "in_progress"
        nodes.append(
            GraphNode(
                id=node_id,
                titel=knoop.titel_nl,
                type=knoop.type.value,
                taal=knoop.taal.value if hasattr(knoop.taal, "value") else str(knoop.taal),
                mastery=round(mastery, 3),
                status=status,
            )
        )

    edges = []
    for u, v in graph.edges:
        edge_data = graph.edges[u, v].get("edge")
        edge_type = "prerequisite"
        if isinstance(edge_data, PrerequisiteEdge):
            edge_type = edge_data.type.value
        edges.append(GraphEdge(source=u, target=v, type=edge_type))

    return GraphDataResponse(nodes=nodes, edges=edges)
