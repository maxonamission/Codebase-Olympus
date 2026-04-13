"""Tests for D1-08: Intake endpoints (start + answer)."""

import tempfile
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from gymnasium_classica.api.intake_manager import IntakeManager
from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.learner import KnoopState, LearnerModel, MasterySource


# -- Unit tests for IntakeManager --


@pytest.fixture
def poc_graph():
    """Load the 50-node PoC graph (no transfer edges, DAG)."""
    path = Path(__file__).parent.parent / "data" / "graph" / "lat_grammatica_poc.json"
    if not path.exists():
        pytest.skip("PoC graph not found")
    return load_graph(path)


def _apply_partial_mastery(learner: LearnerModel, graph, fraction: float = 0.3):
    """Set the first fraction of topo-ordered nodes to mastery 0.70 (treated).

    This simulates a methode profile creating a frontier for the diagnostic
    to explore.
    """
    import networkx as nx

    topo = list(nx.topological_sort(graph))
    n_treated = max(1, int(len(topo) * fraction))
    for node_id in topo[:n_treated]:
        learner.knoop_states[node_id] = KnoopState(
            knoop_id=node_id, posterior_mastery=0.70, source=MasterySource.DIAGNOSTIC
        )


class TestIntakeManager:
    def test_start_with_frontier_returns_question(self, poc_graph):
        learner = LearnerModel(user_id=uuid4())
        _apply_partial_mastery(learner, poc_graph)
        mgr = IntakeManager()
        intake_id, q = mgr.start_intake("user1", learner, poc_graph)
        assert isinstance(intake_id, str)
        assert q is not None
        assert q.knoop_id in poc_graph.nodes

    def test_start_all_unmastered_no_frontier(self, poc_graph):
        """Fresh learner: all at 0.10 ≤ 0.25 = resolved unmastered → no questions."""
        learner = LearnerModel(user_id=uuid4())
        mgr = IntakeManager()
        intake_id, q = mgr.start_intake("user1", learner, poc_graph)
        # All nodes resolve immediately as unmastered, intake finishes
        state = mgr.get_intake_state(intake_id)
        assert state.finished

    def test_intake_eventually_finishes(self, poc_graph):
        learner = LearnerModel(user_id=uuid4())
        _apply_partial_mastery(learner, poc_graph, fraction=0.5)
        mgr = IntakeManager()
        intake_id, q = mgr.start_intake("user1", learner, poc_graph)

        steps = 0
        while q is not None and steps < 40:
            result = mgr.submit_answer(intake_id, correct=True)
            q = result.next_question
            steps += 1
            if result.finished:
                break

        assert steps < 40
        assert learner.intake_completed

    def test_incorrect_answers_handled(self, poc_graph):
        learner = LearnerModel(user_id=uuid4())
        _apply_partial_mastery(learner, poc_graph)
        mgr = IntakeManager()
        intake_id, q = mgr.start_intake("user1", learner, poc_graph)
        assert q is not None

        result = mgr.submit_answer(intake_id, correct=False)
        assert result.questions_asked == 1

    def test_finished_intake_raises(self, poc_graph):
        learner = LearnerModel(user_id=uuid4())
        _apply_partial_mastery(learner, poc_graph)
        mgr = IntakeManager()
        intake_id, q = mgr.start_intake("user1", learner, poc_graph)

        while q is not None:
            result = mgr.submit_answer(intake_id, correct=True)
            q = result.next_question
            if result.finished:
                break

        with pytest.raises(ValueError, match="already finished"):
            mgr.submit_answer(intake_id, correct=True)


# -- API integration tests --


@pytest.fixture()
def client():
    from gymnasium_classica.api.app import create_app

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        test_app = create_app(db_path=db_path)
        with TestClient(test_app) as c:
            yield c


def _auth_header(client, email="intake@example.nl"):
    resp = client.post("/auth/register", json={"email": email, "password": "pw1234"})
    return resp.json()["user_id"], {"Authorization": f"Bearer {resp.json()['token']}"}


class TestIntakeStartEndpoint:
    def test_start_with_methode(self, client):
        """Start intake with Fortuna methode → priors set, questions available."""
        _, headers = _auth_header(client, "methode@example.nl")
        resp = client.post(
            "/intake/start",
            json={"methode": "fortuna", "chapter": "3"},
            headers=headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["already_completed"] is False
        assert data["intake_id"] != ""
        if data["question"] is not None:
            assert "knoop_id" in data["question"]
            assert "questions_asked" in data["question"]
            assert "max_questions" in data["question"]

    def test_start_without_methode(self, client):
        """Start without methode: all nodes at default 0.10 → resolved immediately."""
        _, headers = _auth_header(client)
        resp = client.post("/intake/start", headers=headers)
        assert resp.status_code == 200

    def test_start_requires_auth(self, client):
        resp = client.post("/intake/start")
        assert resp.status_code == 422

    def test_start_invalid_methode(self, client):
        _, headers = _auth_header(client, "bad_methode@example.nl")
        resp = client.post(
            "/intake/start",
            json={"methode": "nonexistent", "chapter": "1"},
            headers=headers,
        )
        assert resp.status_code == 400


class TestIntakeAnswerEndpoint:
    def test_answer_correct(self, client):
        _, headers = _auth_header(client, "answer@example.nl")
        start = client.post(
            "/intake/start",
            json={"methode": "fortuna", "chapter": "3"},
            headers=headers,
        ).json()
        intake_id = start["intake_id"]

        if start["question"] is None:
            pytest.skip("No intake question available")

        resp = client.post(
            "/intake/answer",
            json={"intake_id": intake_id, "correct": True},
            headers=headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["questions_asked"] == 1

    def test_answer_unknown_intake(self, client):
        _, headers = _auth_header(client, "unknown@example.nl")
        resp = client.post(
            "/intake/answer",
            json={"intake_id": "nonexistent", "correct": True},
            headers=headers,
        )
        assert resp.status_code == 404

    def test_answer_wrong_user(self, client):
        _, h1 = _auth_header(client, "intake1@example.nl")
        start = client.post(
            "/intake/start",
            json={"methode": "fortuna", "chapter": "3"},
            headers=h1,
        ).json()
        intake_id = start["intake_id"]

        _, h2 = _auth_header(client, "intake2@example.nl")
        resp = client.post(
            "/intake/answer",
            json={"intake_id": intake_id, "correct": True},
            headers=h2,
        )
        assert resp.status_code == 403

    def test_full_intake_flow(self, client):
        """Run through a complete intake with methode profile."""
        _, headers = _auth_header(client, "flow@example.nl")
        start = client.post(
            "/intake/start",
            json={"methode": "fortuna", "chapter": "3"},
            headers=headers,
        ).json()
        intake_id = start["intake_id"]
        q = start["question"]

        steps = 0
        max_steps = 35
        while q is not None and steps < max_steps:
            resp = client.post(
                "/intake/answer",
                json={"intake_id": intake_id, "correct": True},
                headers=headers,
            ).json()
            q = resp.get("next_question")
            steps += 1
            if resp["finished"]:
                break

        assert steps < max_steps

    def test_already_completed_blocks_restart(self, client):
        """After completing intake, starting again returns already_completed."""
        _, headers = _auth_header(client, "twice@example.nl")
        start = client.post(
            "/intake/start",
            json={"methode": "fortuna", "chapter": "3"},
            headers=headers,
        ).json()
        intake_id = start["intake_id"]
        q = start["question"]

        while q is not None:
            resp = client.post(
                "/intake/answer",
                json={"intake_id": intake_id, "correct": True},
                headers=headers,
            ).json()
            q = resp.get("next_question")
            if resp["finished"]:
                break

        # Try to start again
        start2 = client.post(
            "/intake/start",
            json={"methode": "fortuna", "chapter": "3"},
            headers=headers,
        ).json()
        assert start2["already_completed"] is True
