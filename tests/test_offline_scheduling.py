"""Tests for B5-01: offline exercise scheduling integration."""

from datetime import datetime, timedelta
from uuid import uuid4

from gymnasium_classica.graph.loader import load_graph_from_dict
from gymnasium_classica.models.graph import KennisKnoop
from gymnasium_classica.models.learner import (
    LearnerModel,
    OfflineAssignment,
    ResponseType,
)
from gymnasium_classica.scheduling.session import (
    _collect_offline_items,
    _pending_follow_ups,
    run_session,
)


def _graph_with_offline_items() -> dict:
    """Small graph where one node has an offline_schrijven item."""
    return {
        "knopen": [
            {
                "id": "LAT-G-MORF-NAAMVAL-INTRO",
                "type": "G",
                "taal": "lat",
                "titel_nl": "Wat is een naamval?",
                "beschrijving": "Introductie van het concept naamval in het Latijn.",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
                "toetsbaar": True,
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL1-INTRO",
                "type": "G",
                "taal": "lat",
                "titel_nl": "De eerste declinatie",
                "beschrijving": "Overzicht van de 1e declinatie (a-stammen).",
                "bloom_niveau": "kennis",
                "fase": "onderbouw_1",
                "toetsbaar": True,
                "items": [
                    {
                        "id": "ITEM-OFFLINE-D1-001",
                        "knoop_ids": ["LAT-G-MORF-DECL1-INTRO"],
                        "type": "offline_schrijven",
                        "richting": "productief",
                        "moeilijkheid_initieel": 0.5,
                        "discriminatie_initieel": 1.0,
                        "verwachte_tijd_sec": 300,
                        "stimulus": "Schrijf het paradigma van puella, -ae (v.) op papier.",
                        "antwoord": "puella, puellae, puellae, puellam, puellā, puellā",
                        "feedback": "Vergelijk je antwoord met het paradigma.",
                        "bron": "handmatig",
                        "verificatie_methode": "self_report",
                        "verwacht_resultaat": "puella, puellae, puellae, puellam, puellā, puellā",
                    },
                    {
                        "id": "ITEM-ONLINE-D1-001",
                        "knoop_ids": ["LAT-G-MORF-DECL1-INTRO"],
                        "type": "herkenning",
                        "richting": "receptief",
                        "moeilijkheid_initieel": -0.5,
                        "discriminatie_initieel": 1.2,
                        "verwachte_tijd_sec": 20,
                        "stimulus": "Welke naamval is 'puellam'?",
                        "antwoord": "accusativus",
                        "feedback": "Puellam is accusativus enkelvoud.",
                        "bron": "handmatig",
                    },
                ],
            },
        ],
        "edges": [
            {
                "source_id": "LAT-G-MORF-NAAMVAL-INTRO",
                "target_id": "LAT-G-MORF-DECL1-INTRO",
                "type": "prerequisite",
                "encompassing_weight": 0.5,
            },
        ],
    }


def _always_correct(knoop_id: str, knoop: KennisKnoop) -> tuple[ResponseType, int]:
    return (ResponseType.CORRECT, 2000)


class TestCollectOfflineItems:
    """Tests for _collect_offline_items helper."""

    def test_finds_offline_items(self):
        graph = load_graph_from_dict(_graph_with_offline_items())
        now = datetime(2026, 4, 13)
        assignments = _collect_offline_items(graph, {"LAT-G-MORF-DECL1-INTRO"}, now)
        assert len(assignments) == 1
        assert assignments[0].knoop_id == "LAT-G-MORF-DECL1-INTRO"
        assert assignments[0].item_id == "ITEM-OFFLINE-D1-001"
        assert assignments[0].assigned_at == now
        assert assignments[0].completed is False

    def test_ignores_online_items(self):
        graph = load_graph_from_dict(_graph_with_offline_items())
        now = datetime(2026, 4, 13)
        assignments = _collect_offline_items(graph, {"LAT-G-MORF-DECL1-INTRO"}, now)
        item_ids = [a.item_id for a in assignments]
        assert "ITEM-ONLINE-D1-001" not in item_ids

    def test_empty_for_nodes_without_offline(self):
        graph = load_graph_from_dict(_graph_with_offline_items())
        now = datetime(2026, 4, 13)
        assignments = _collect_offline_items(graph, {"LAT-G-MORF-NAAMVAL-INTRO"}, now)
        assert assignments == []

    def test_empty_for_unknown_nodes(self):
        graph = load_graph_from_dict(_graph_with_offline_items())
        now = datetime(2026, 4, 13)
        assignments = _collect_offline_items(graph, {"NONEXISTENT"}, now)
        assert assignments == []


class TestPendingFollowUps:
    """Tests for _pending_follow_ups helper."""

    def test_returns_uncompleted(self):
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 13)
        learner.pending_offline_assignments = [
            OfflineAssignment(
                knoop_id="LAT-G-MORF-DECL1-INTRO",
                item_id="ITEM-OFFLINE-D1-001",
                assigned_at=now,
                completed=False,
            ),
        ]
        follow_ups = _pending_follow_ups(learner)
        assert len(follow_ups) == 1

    def test_excludes_completed(self):
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 13)
        learner.pending_offline_assignments = [
            OfflineAssignment(
                knoop_id="LAT-G-MORF-DECL1-INTRO",
                item_id="ITEM-OFFLINE-D1-001",
                assigned_at=now,
                completed=True,
            ),
        ]
        follow_ups = _pending_follow_ups(learner)
        assert follow_ups == []

    def test_empty_when_no_assignments(self):
        learner = LearnerModel(user_id=uuid4())
        follow_ups = _pending_follow_ups(learner)
        assert follow_ups == []


class TestOfflineInSession:
    """Integration tests: offline scheduling within run_session."""

    def test_offline_assignments_collected_at_session_end(self):
        graph = load_graph_from_dict(_graph_with_offline_items())
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 13)

        result = run_session(learner, graph, _always_correct, now=now)

        # The session should have practiced DECL1-INTRO (only root + child)
        practiced_ids = {item.knoop_id for item in result.items}
        if "LAT-G-MORF-DECL1-INTRO" in practiced_ids:
            assert len(result.offline_assignments) == 1
            assert result.offline_assignments[0].item_id == "ITEM-OFFLINE-D1-001"
            # Also stored on learner
            assert len(learner.pending_offline_assignments) == 1

    def test_no_duplicate_assignments_across_sessions(self):
        graph = load_graph_from_dict(_graph_with_offline_items())
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 13)

        # Pre-seed a pending assignment for the offline item
        learner.pending_offline_assignments.append(
            OfflineAssignment(
                knoop_id="LAT-G-MORF-DECL1-INTRO",
                item_id="ITEM-OFFLINE-D1-001",
                assigned_at=now - timedelta(days=1),
            )
        )

        # Run a session — the same item should not be duplicated
        result = run_session(learner, graph, _always_correct, now=now)
        assert len(learner.pending_offline_assignments) == 1
        # The result should not contain the duplicate either
        assert len(result.offline_assignments) == 0

    def test_follow_ups_surfaced_in_next_session(self):
        graph = load_graph_from_dict(_graph_with_offline_items())
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 13)

        # First session — creates offline assignments
        result1 = run_session(learner, graph, _always_correct, now=now)
        assert result1.follow_ups == []  # No pending at start of first session

        if learner.pending_offline_assignments:
            # Second session — follow-ups should be surfaced
            result2 = run_session(learner, graph, _always_correct, now=now + timedelta(days=1))
            assert len(result2.follow_ups) > 0
            assert result2.follow_ups[0].item_id == "ITEM-OFFLINE-D1-001"

    def test_completed_assignment_not_in_follow_ups(self):
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 13)

        # Manually add a completed assignment
        learner.pending_offline_assignments.append(
            OfflineAssignment(
                knoop_id="LAT-G-MORF-DECL1-INTRO",
                item_id="ITEM-OFFLINE-D1-001",
                assigned_at=now,
                completed=True,
            )
        )

        graph = load_graph_from_dict(_graph_with_offline_items())
        result = run_session(learner, graph, _always_correct, now=now + timedelta(days=1))
        assert result.follow_ups == []


class TestOfflineAssignmentModel:
    """Tests for the OfflineAssignment Pydantic model."""

    def test_defaults(self):
        now = datetime(2026, 4, 13)
        a = OfflineAssignment(
            knoop_id="LAT-G-MORF-DECL1-INTRO",
            item_id="ITEM-001",
            assigned_at=now,
        )
        assert a.completed is False

    def test_serialization_roundtrip(self):
        now = datetime(2026, 4, 13)
        a = OfflineAssignment(
            knoop_id="LAT-G-MORF-DECL1-INTRO",
            item_id="ITEM-001",
            assigned_at=now,
            completed=True,
        )
        data = a.model_dump()
        a2 = OfflineAssignment(**data)
        assert a2 == a
