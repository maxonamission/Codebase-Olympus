"""Progress routes: overview and per-node detail."""

from datetime import datetime, timedelta
from typing import Any

import networkx as nx
from fastapi import APIRouter, Depends, HTTPException, Request

from gymnasium_classica.api.auth import get_current_user_id
from gymnasium_classica.api.database import get_user, load_learner_model
from gymnasium_classica.api.schemas import (
    BijspijkerProgressResponse,
    BijspijkerTopic,
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
from gymnasium_classica.models.graph import Node, NodeType, PrerequisiteEdge
from gymnasium_classica.models.learner import LearnerModel
from gymnasium_classica.models.user import Modus
from gymnasium_classica.scheduling.bijspijker import BijspijkerPlanner, BijspijkerTarget
from gymnasium_classica.scheduling.priority import MASTERY_THRESHOLD

router = APIRouter(prefix="/progress", tags=["progress"])

# A node is "in progress" when it has a state but is not yet mastered
_IN_PROGRESS_FLOOR = 0.15  # Above default prior → learner has interacted


@router.get("/bijspijker", response_model=BijspijkerProgressResponse)
async def bijspijker_progress(
    request: Request,
    user_id: str = Depends(get_current_user_id),
) -> BijspijkerProgressResponse:
    """Catch-up progress: how much of the target set is green (M1-03)."""
    db = request.app.state.db
    graph: nx.DiGraph = request.app.state.graph

    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.modus != Modus.BIJSPIJKER:
        raise HTTPException(status_code=400, detail="Gebruiker staat niet in bijspijker-modus.")

    targets: list[BijspijkerTarget] = []
    if user.huidige_methode_lat and user.huidige_hoofdstuk_lat:
        targets.append(BijspijkerTarget(user.huidige_methode_lat, user.huidige_hoofdstuk_lat))
    if user.huidige_methode_grc and user.huidige_hoofdstuk_grc:
        targets.append(BijspijkerTarget(user.huidige_methode_grc, user.huidige_hoofdstuk_grc))
    if not targets:
        raise HTTPException(status_code=400, detail="Geen bijspijker-doel ingesteld.")

    from uuid import UUID

    learner = load_learner_model(db, user_id) or LearnerModel(user_id=UUID(user_id))
    plan = BijspijkerPlanner(graph, request.app.state.methode_mapping).plan(learner, targets)

    open_topics: list[BijspijkerTopic] = []
    for node_id in plan.diagnose[:20]:
        node_attr = graph.nodes.get(node_id, {}).get("node")
        state = learner.node_states.get(node_id)
        open_topics.append(
            BijspijkerTopic(
                node_id=node_id,
                title_nl=node_attr.title_nl if node_attr else node_id,
                mastery=state.posterior_mastery if state else 0.0,
            )
        )

    return BijspijkerProgressResponse(
        modus=user.modus.value,
        fractie_bij=plan.fractie_bij,
        is_bij=plan.is_bij,
        doelset_size=len(plan.doelset),
        diagnose_size=len(plan.diagnose),
        eta_dagen=plan.eta_dagen,
        suggest_chapter_bump=plan.suggest_chapter_bump,
        open_topics=open_topics,
    )


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
            state = learner.node_states.get(node_id)
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
            node: Node = graph.nodes[node_id]["node"]
            d = node.type.value
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
        node = graph.nodes[node_id]["node"]
        d = node.type.value
        if d not in domains:
            domains[d] = DomainProgress(total=0, mastered=0, in_progress=0, unseen=0)
        domains[d].total += 1

        state = learner.node_states.get(node_id)
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


@router.get("/node/{node_id}", response_model=KnoopProgressResponse)
async def node_progress(
    node_id: str,
    request: Request,
    user_id: str = Depends(get_current_user_id),
) -> KnoopProgressResponse:
    """Return detailed progress for a single knowledge node."""
    graph: nx.DiGraph = request.app.state.graph

    if node_id not in graph.nodes:
        raise HTTPException(status_code=404, detail=f"Knoop {node_id!r} not found")

    node: Node = graph.nodes[node_id]["node"]

    db = request.app.state.db
    learner = load_learner_model(db, user_id)

    state = None
    if learner is not None:
        state = learner.node_states.get(node_id)

    if state is None:
        return KnoopProgressResponse(
            node_id=node_id,
            title=node.title_nl,
            type=node.type.value,
            posterior_mastery=0.0,
            easiness_factor=2.5,
            interval_days=0.0,
            repetitions=0,
            last_review=None,
            source="practice",
            item_history=[],
        )

    return KnoopProgressResponse(
        node_id=node_id,
        title=node.title_nl,
        type=node.type.value,
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
    together with the count of V-nodes that carry the matching
    ``semantic_cluster`` label and the learner's mastery status
    for those nodes.
    """
    graph: nx.DiGraph = request.app.state.graph
    cluster_defs: list[dict[str, Any]] = getattr(request.app.state, "clusters", []) or []

    db = request.app.state.db
    learner = load_learner_model(db, user_id)

    nodes_per_cluster: dict[str, list[str]] = {c["label"]: [] for c in cluster_defs}
    for node_id in graph.nodes:
        node: Node = graph.nodes[node_id]["node"]
        if node.type != NodeType.V:
            continue
        label = node.semantic_cluster
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
                state = learner.node_states.get(node_id)
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
                description=c.get("description", ""),
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
        node: Node = graph.nodes[node_id]["node"]
        mastery = 0.0
        status = "unseen"
        if learner:
            state = learner.node_states.get(node_id)
            if state:
                mastery = state.posterior_mastery
                if mastery >= MASTERY_THRESHOLD:
                    status = "mastered"
                elif mastery >= _IN_PROGRESS_FLOOR:
                    status = "in_progress"
        nodes.append(
            GraphNode(
                id=node_id,
                title=node.title_nl,
                type=node.type.value,
                language=node.language.value
                if hasattr(node.language, "value")
                else str(node.language),
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
