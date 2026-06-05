"""Tests for the method-mapping validator and User bijspijker fields (M1-03)."""

from pathlib import Path

import networkx as nx
import pytest
from pydantic import ValidationError

from gymnasium_classica.diagnostic.methode_profile import (
    load_methode_mapping,
    validate_methode_mapping,
)
from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.user import Modus, User

REPO_ROOT = Path(__file__).resolve().parent.parent


def _graph() -> nx.DiGraph:
    return load_graph(REPO_ROOT / "data" / "graph")


class TestRealMappingValidates:
    def test_shipped_mapping_is_valid(self):
        mapping = load_methode_mapping()
        errors = validate_methode_mapping(mapping, _graph())
        assert errors == [], errors

    def test_pallas_has_six_chapters(self):
        mapping = load_methode_mapping()
        pallas = mapping["methoden"]["pallas"]["hoofdstukken"]
        chapters = sorted(k for k in pallas if not k.startswith("_"))
        assert chapters == ["1", "2", "3", "4", "5", "6"]


class TestValidatorCatchesProblems:
    def _graph_with(self, *node_ids: str) -> nx.DiGraph:
        g = nx.DiGraph()
        for nid in node_ids:
            g.add_node(nid)
        return g

    def test_missing_node_flagged(self):
        mapping = {"methoden": {"x": {"hoofdstukken": {"1": {"node_ids": ["LAT-G-GHOST-INTRO"]}}}}}
        errors = validate_methode_mapping(mapping, self._graph_with("LAT-G-REAL-INTRO"))
        assert any("LAT-G-GHOST-INTRO" in e for e in errors)

    def test_duplicate_node_flagged(self):
        mapping = {
            "methoden": {
                "x": {
                    "hoofdstukken": {
                        "1": {"node_ids": ["LAT-G-A-INTRO"]},
                        "2": {"node_ids": ["LAT-G-A-INTRO"]},
                    }
                }
            }
        }
        errors = validate_methode_mapping(mapping, self._graph_with("LAT-G-A-INTRO"))
        assert any("meerdere hoofdstukken" in e for e in errors)

    def test_non_consecutive_chapters_flagged(self):
        mapping = {
            "methoden": {
                "x": {
                    "hoofdstukken": {
                        "1": {"node_ids": ["LAT-G-A-INTRO"]},
                        "3": {"node_ids": ["LAT-G-B-INTRO"]},
                    }
                }
            }
        }
        g = self._graph_with("LAT-G-A-INTRO", "LAT-G-B-INTRO")
        errors = validate_methode_mapping(mapping, g)
        assert any("opeenvolgend" in e for e in errors)

    def test_comment_keys_ignored(self):
        mapping = {
            "methoden": {
                "x": {
                    "_comment": "ignore me",
                    "hoofdstukken": {"_comment": "x", "1": {"node_ids": ["LAT-G-A-INTRO"]}},
                }
            }
        }
        errors = validate_methode_mapping(mapping, self._graph_with("LAT-G-A-INTRO"))
        assert errors == []


class TestUserBijspijkerFields:
    def test_default_mode_is_staatsexamen(self):
        user = User(email="x@example.com")
        assert user.modus == Modus.STAATSEXAMEN

    def test_staatsexamen_needs_no_method(self):
        user = User(email="x@example.com", modus=Modus.STAATSEXAMEN)
        assert user.huidige_methode_lat is None

    def test_bijspijker_requires_method_and_chapter(self):
        with pytest.raises(ValidationError):
            User(email="x@example.com", modus=Modus.BIJSPIJKER)

    def test_bijspijker_valid_with_one_language(self):
        user = User(
            email="x@example.com",
            modus=Modus.BIJSPIJKER,
            huidige_methode_grc="pallas",
            huidige_hoofdstuk_grc=4,
        )
        assert user.huidige_hoofdstuk_grc == 4

    def test_chapter_must_be_positive(self):
        with pytest.raises(ValidationError):
            User(
                email="x@example.com",
                modus=Modus.BIJSPIJKER,
                huidige_methode_lat="fortuna",
                huidige_hoofdstuk_lat=0,
            )

    def test_existing_user_json_deserializes_as_staatsexamen(self):
        # A record stored before M1-03 has no modus/method fields.
        legacy = '{"email": "old@example.com", "auth_provider": "local"}'
        user = User.model_validate_json(legacy)
        assert user.modus == Modus.STAATSEXAMEN
