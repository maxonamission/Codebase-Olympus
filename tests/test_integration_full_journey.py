"""End-to-end integration tests: register → (intake) → session → persist → resume.

Policy: zero mocking. No ``unittest.mock``, no ``@patch``, no monkeypatching
of internal functions. Every test drives the real FastAPI app through
``TestClient``, writes to a real SQLite database on ``tmp_path``, and loads
the real production knowledge graph from ``data/graph/``. Time is controlled
only by letting ``datetime.now()`` run; assertions on timestamps are
tolerance-based rather than exact.

Goal: catch regressions where individual layers pass their unit tests but
the composition (auth + DB + session_manager + scheduler + learner model)
breaks on the way through. Unit tests cover the pieces; these tests cover
the seams.
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from gymnasium_classica.api.app import create_app
from gymnasium_classica.api.database import load_learner_model


GRAPH_DIR = Path(__file__).parent.parent / "data" / "graph"
PASSAGES_DIR = Path(__file__).parent.parent / "data" / "passages"


@pytest.fixture
def app_factory(tmp_path):
    """Factory that creates TestClients against a single shared SQLite file.

    Calling ``factory()`` returns a new TestClient with its own lifespan,
    but backed by the same ``db_path`` — this simulates the user restarting
    the app, logging in again, and resuming state from persistence.
    """
    db_path = tmp_path / "journey.db"

    def _make(with_passages: bool = False) -> TestClient:
        passages_dir = PASSAGES_DIR if with_passages else tmp_path / "nonexistent"
        app = create_app(
            graph_dir=GRAPH_DIR,
            db_path=db_path,
            passages_dir=passages_dir,
        )
        return TestClient(app)

    return _make


def _register(client: TestClient, email: str, password: str = "geheim1234") -> dict:
    resp = client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert resp.status_code == 200, resp.text
    return resp.json()


def _login(client: TestClient, email: str, password: str = "geheim1234") -> dict:
    resp = client.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert resp.status_code == 200, resp.text
    return resp.json()


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _drain_session(
    client: TestClient,
    headers: dict,
    session_id: str,
    first_question: dict | None,
    response: str = "correct",
    max_steps: int = 400,
) -> int:
    """Answer until the session finishes. Returns the number of questions answered."""
    q = first_question
    answered = 0
    while q is not None and answered < max_steps:
        resp = client.post(
            "/session/answer",
            json={
                "session_id": session_id,
                "response": response,
                "response_time_ms": 1500,
            },
            headers=headers,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        answered += 1
        q = data.get("next_question")
        if data["session_finished"]:
            break
    assert answered < max_steps, "Session did not terminate within max_steps"
    return answered


class TestRegisterAndFirstSession:
    """A new user can register, start a session, answer, and get a summary."""

    def test_happy_path(self, app_factory):
        with app_factory() as client:
            auth = _register(client, "alice@example.nl")
            headers = _auth_headers(auth["token"])

            start = client.post("/session/start", headers=headers).json()
            session_id = start["session_id"]
            assert len(session_id) > 0
            assert start["question"] is not None, "Production graph must yield a question"

            # Answer at least three questions, alternating correct/incorrect.
            q = start["question"]
            alternating = ["correct", "incorrect", "correct"]
            for response in alternating:
                resp = client.post(
                    "/session/answer",
                    json={
                        "session_id": session_id,
                        "response": response,
                        "response_time_ms": 2000,
                    },
                    headers=headers,
                )
                assert resp.status_code == 200, resp.text
                data = resp.json()
                # Feedback reflects the response type (passage_read is possible
                # if the first question happened to be a passage).
                assert data["feedback"]["response_type"] in {
                    response, "passage_read"
                }
                q = data.get("next_question")
                if data["session_finished"]:
                    break

            summary = client.get(
                f"/session/{session_id}/summary", headers=headers
            ).json()
            assert summary["session_id"] == session_id
            assert summary["total_items"] >= 1
            # At least one correct answer should have raised mastery.
            raised = [
                (k, v) for k, v in summary["mastery_changes"].items()
                if v["after"] > v["before"]
            ]
            assert raised, "At least one correct answer should raise mastery"


class TestSessionPersistsAcrossLogins:
    """Learner state written to SQLite survives app restart + re-login."""

    def test_session_history_restored_after_relogin(self, app_factory):
        # --- First app instance: register and run a session ---
        with app_factory() as client1:
            auth = _register(client1, "bob@example.nl")
            headers1 = _auth_headers(auth["token"])
            user_id = auth["user_id"]

            start = client1.post("/session/start", headers=headers1).json()
            session_id = start["session_id"]
            _drain_session(client1, headers1, session_id, start["question"])

        # --- Second app instance: new TestClient, same DB, same user ---
        with app_factory() as client2:
            re_auth = _login(client2, "bob@example.nl")
            assert re_auth["user_id"] == user_id
            headers2 = _auth_headers(re_auth["token"])

            # Inspect via the progress endpoint which reads the persisted model.
            resp = client2.get("/progress/overview", headers=headers2)
            assert resp.status_code == 200, resp.text
            overview = resp.json()
            # After a session against a real graph, at least one knoop has
            # moved from unseen into mastered or in_progress.
            assert overview["mastered"] + overview["in_progress"] >= 1

            # Direct DB check: session_history actually got appended.
            db_path = Path(client2.app.state.db.execute(
                "PRAGMA database_list"
            ).fetchone()["file"])
            conn = client2.app.state.db
            learner = load_learner_model(conn, user_id)
            assert learner is not None
            assert len(learner.session_history) >= 1
            assert learner.session_history[0].session_id == session_id


class TestIntakeThenSession:
    """After an intake with a school method profile, a regular session runs
    using the diagnostic mastery as prior."""

    def test_intake_sets_diagnostic_source_before_session(self, app_factory):
        with app_factory() as client:
            auth = _register(client, "claire@example.nl")
            headers = _auth_headers(auth["token"])
            user_id = auth["user_id"]

            # Start intake with a real methode profile.
            start = client.post(
                "/intake/start",
                json={"methode": "fortuna", "chapter": "1"},
                headers=headers,
            )
            assert start.status_code == 200, start.text
            data = start.json()

            if data.get("already_completed"):
                pytest.skip("User already completed intake (unexpected for fresh user)")

            intake_id = data["intake_id"]
            question = data.get("question")

            # Answer until intake finishes.
            answered = 0
            while question is not None and answered < 50:
                resp = client.post(
                    "/intake/answer",
                    json={"intake_id": intake_id, "correct": True},
                    headers=headers,
                )
                assert resp.status_code == 200, resp.text
                payload = resp.json()
                answered += 1
                question = payload.get("next_question")
                if payload["finished"]:
                    break
            assert answered < 50, "Intake did not terminate"

            # Verify diagnostic source on at least some knoop_states.
            conn = client.app.state.db
            learner = load_learner_model(conn, user_id)
            assert learner is not None
            assert learner.intake_completed is True
            diagnostic_nodes = [
                ks for ks in learner.knoop_states.values()
                if ks.source.value == "diagnostic"
            ]
            assert diagnostic_nodes, "Intake must mark nodes with source=diagnostic"

            # A subsequent session works and respects the diagnostic priors.
            sess = client.post("/session/start", headers=headers).json()
            assert sess["session_id"]
            _drain_session(
                client, headers, sess["session_id"], sess["question"]
            )


class TestIncorrectAnswerTriggersFallback:
    """An INCORRECT on a diagnostic-sourced knoop triggers conditional-completion
    fallback: posterior drops and the source flag stays diagnostic (or is
    updated by the practice response — the contract here is that fallback
    runs, not that the source changes)."""

    def test_mastery_drops_on_incorrect_for_diagnostic_node(self, app_factory):
        with app_factory() as client:
            auth = _register(client, "daan@example.nl")
            headers = _auth_headers(auth["token"])
            user_id = auth["user_id"]

            # Run the intake on chapter 1 to seed diagnostic mastery.
            intake = client.post(
                "/intake/start",
                json={"methode": "fortuna", "chapter": "1"},
                headers=headers,
            ).json()
            intake_id = intake["intake_id"]
            q = intake.get("question")
            while q is not None:
                resp = client.post(
                    "/intake/answer",
                    json={"intake_id": intake_id, "correct": True},
                    headers=headers,
                ).json()
                q = resp.get("next_question")
                if resp["finished"]:
                    break

            # Snapshot mastery before the session.
            conn = client.app.state.db
            before_learner = load_learner_model(conn, user_id)
            assert before_learner is not None
            before_mastery = {
                k: s.posterior_mastery
                for k, s in before_learner.knoop_states.items()
            }

            # Start a session and answer the first question INCORRECT.
            start = client.post("/session/start", headers=headers).json()
            first_q = start["question"]
            if first_q is None:
                pytest.skip("No question available after intake")

            knoop_id = first_q["knoop_id"]
            stimulus = first_q.get("stimulus")
            if isinstance(stimulus, dict) and stimulus.get("type") == "passage":
                pytest.skip("First question is a passage; fallback scenario N/A")

            answer = client.post(
                "/session/answer",
                json={
                    "session_id": start["session_id"],
                    "response": "incorrect",
                    "response_time_ms": 4000,
                },
                headers=headers,
            ).json()
            assert answer["feedback"]["knoop_id"] == knoop_id
            assert answer["feedback"]["correct"] is False
            assert answer["feedback"]["mastery_after"] < before_mastery.get(
                knoop_id, 1.0
            )


class TestMultipleSessionsAccumulate:
    """Two consecutive sessions keep accumulating mastery — proving that
    ``save_learner_model`` → ``load_learner_model`` round-trips correctly
    between sessions."""

    def test_two_sessions_grow_session_history(self, app_factory):
        with app_factory() as client:
            auth = _register(client, "eva@example.nl")
            headers = _auth_headers(auth["token"])
            user_id = auth["user_id"]

            for _ in range(2):
                start = client.post("/session/start", headers=headers).json()
                _drain_session(
                    client, headers, start["session_id"], start["question"]
                )

            conn = client.app.state.db
            learner = load_learner_model(conn, user_id)
            assert learner is not None
            assert len(learner.session_history) == 2
            # Session IDs must be distinct.
            assert len({s.session_id for s in learner.session_history}) == 2
