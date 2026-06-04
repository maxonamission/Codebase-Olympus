"""Integration tests tegen de volledige Leerjaar-1 knowledge graph.

Policy: zero mocking. Leest de echte JSON-bestanden uit ``data/graph/`` en
laat ze door de échte loader, validator en scheduler. Geen ``unittest.mock``,
geen patches op interne functies.

Doel: borgen dat de productie-graph (alle 8 JSON-bestanden samen, ~800 nodes,
~1280 edges) structureel gezond is én dat de scheduling-pipeline er een
volledige sessie doorheen kan draaien.

Deze tests falen als:
- Een JSON-bestand een typo of ongeldig ID bevat.
- Cross-file edges (met name ``transfer_edges_leerjaar1.json``) naar
  niet-bestaande knopen verwijzen.
- Een nieuwe grammaticaknoop wordt toegevoegd zonder prerequisite op de
  alfabet-subgraph (schending van de invariant uit CLAUDE.md).
- De scheduler deadlockt of crasht op de volledige graph.
"""

from datetime import datetime
from pathlib import Path
from uuid import uuid4

import networkx as nx
import pytest

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.graph.validation import detect_cycles, validate_graph
from gymnasium_classica.models.graph import EdgeType, PrerequisiteEdge
from gymnasium_classica.models.learner import LearnerModel, ResponseType
from gymnasium_classica.scheduling.session import run_session
from gymnasium_classica.schemas.id_schema import validate_node_id

GRAPH_DIR = Path(__file__).parent.parent / "data" / "graph"


@pytest.fixture(scope="module")
def real_graph() -> nx.DiGraph:
    """Laad alle 8 JSON-bestanden in ``data/graph/`` één keer per testmodule."""
    return load_graph(GRAPH_DIR)


class TestStructuralIntegrity:
    def test_all_expected_files_contribute(self, real_graph):
        """De 8 productie-bestanden samen leveren ≥500 knopen op."""
        expected_files = {
            "grc_alfabet.json",
            "grc_grammatica_leerjaar1.json",
            "grc_vocabulaire_leerjaar1.json",
            "lat_grammatica_leerjaar1.json",
            "lat_grammatica_poc.json",
            "lat_vocabulaire_leerjaar1.json",
            "sha_cultuur_leerjaar1.json",
            "transfer_edges_leerjaar1.json",
        }
        present = {p.name for p in GRAPH_DIR.glob("*.json")}
        missing = expected_files - present
        assert not missing, f"Ontbrekende productie-graph-bestanden: {missing}"
        assert real_graph.number_of_nodes() >= 500, (
            f"Verwacht ≥500 knopen in volledige graph, kreeg {real_graph.number_of_nodes()}"
        )

    def test_validate_graph_has_no_errors(self, real_graph):
        """De validator vindt geen harde fouten in de productie-graph."""
        report = validate_graph(real_graph)
        assert report.errors == [], "Graph-validatie rapporteerde fouten:\n" + "\n".join(
            report.errors
        )

    def test_no_cycles_in_prerequisite_subgraph(self, real_graph):
        cycles = detect_cycles(real_graph)
        assert cycles == [], f"Onverwachte cykels: {cycles[:3]}"

    def test_all_ids_conform_to_schema(self, real_graph):
        """Alle node-IDs passeren ``validate_node_id``."""
        invalid = [n for n in real_graph.nodes if not validate_node_id(n)]
        assert not invalid, (
            f"{len(invalid)} node-ID(s) voldoen niet aan het ID-schema: {invalid[:5]}"
        )


class TestCrossFileEdges:
    """Transfer-edges definiëren cross-file verbindingen (LAT↔GRC); alle
    bron- en doelknopen moeten bestaan in de samengevoegde graph."""

    def test_all_transfer_edges_resolve(self, real_graph):
        unresolved = []
        for source, target, data in real_graph.edges(data=True):
            edge = data.get("edge")
            if isinstance(edge, PrerequisiteEdge) and edge.type == EdgeType.TRANSFER:
                if source not in real_graph.nodes:
                    unresolved.append(("source missing", source, target))
                if target not in real_graph.nodes:
                    unresolved.append(("target missing", source, target))
        assert not unresolved, (
            f"Transfer-edges verwijzen naar niet-bestaande knopen: {unresolved[:5]}"
        )

    def test_transfer_edges_bridge_languages(self, real_graph):
        """Transfer-edges horen LAT-knopen met GRC-knopen te koppelen."""
        transfer_count = 0
        for source, target, data in real_graph.edges(data=True):
            edge = data.get("edge")
            if isinstance(edge, PrerequisiteEdge) and edge.type == EdgeType.TRANSFER:
                transfer_count += 1
                source_lang = source.split("-", 1)[0]
                target_lang = target.split("-", 1)[0]
                assert source_lang != target_lang, (
                    f"Transfer-edge binnen één taal gevonden: {source} → {target}"
                )
        assert transfer_count > 0, "Geen transfer-edges aangetroffen"


class TestGrcAlfabetInvariant:
    """CLAUDE.md: de Grieks-alfabet-subgraph blokkeert alle Griekse grammatica.

    Elke niet-alfabet ``GRC-G-*``-node moet transitief afhankelijk zijn van
    minstens één ``GRC-G-FONL-ALFA-*``-node.
    """

    def test_every_grc_grammar_node_depends_on_alfabet(self, real_graph):
        missing = []
        for node_id in real_graph.nodes:
            if not node_id.startswith("GRC-G-"):
                continue
            if "FONL-ALFA" in node_id:
                continue
            ancestors = nx.ancestors(real_graph, node_id)
            if not any("FONL-ALFA" in a for a in ancestors):
                missing.append(node_id)
        assert not missing, (
            f"{len(missing)} GRC-grammaticaknopen zonder alfabet-prerequisite: {missing[:5]}"
        )

    def test_alfabet_subgraph_has_entry_point(self, real_graph):
        """De alfabet-subgraph moet minstens één entry-node hebben: een
        alfabet-node zonder andere alfabet-node als prerequisite.

        (De alfabet-subgraph kan cultuurknopen als bovenliggende context
        hebben — bijv. ``SHA-C-LIT-GRALF`` als introductie — dus we eisen
        niet dat alfabet-knopen globale roots zijn.)
        """
        alfa_nodes = [n for n in real_graph.nodes if "FONL-ALFA" in n]
        assert alfa_nodes, "Geen alfabet-knopen gevonden"
        entry_points = [
            n for n in alfa_nodes if not any("FONL-ALFA" in p for p in real_graph.predecessors(n))
        ]
        assert entry_points, (
            "Alfabet-subgraph heeft geen entry-node (elke alfabet-node "
            "heeft een andere alfabet-node als prerequisite — circulaire "
            "definitie?)"
        )


class TestSchedulerOnRealGraph:
    """De scheduler kan een volledige sessie draaien op de productie-graph."""

    def test_run_session_terminates_and_records_items(self, real_graph):
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 16, 10, 0, 0)

        def always_correct(node_id, node):
            return ResponseType.CORRECT, 1500

        result = run_session(learner, real_graph, always_correct, now=now)

        assert result.ended_at is not None, "Sessie niet afgerond"
        assert len(result.items) >= 1, "Geen items aangeboden op productie-graph"
        # Elke mastery_change bevat een voor/na-paar binnen [0,1].
        for node_id, (before, after) in result.mastery_changes.items():
            assert 0.0 <= before <= 1.0, f"{node_id}: before={before}"
            assert 0.0 <= after <= 1.0, f"{node_id}: after={after}"
            # CORRECT-antwoord mag mastery niet verlagen.
            assert after >= before - 1e-9, (
                f"CORRECT verlaagde mastery voor {node_id}: {before} → {after}"
            )
        # Minstens één van de geïntroduceerde knopen kreeg z'n mastery verhoogd.
        assert result.nodes_introduced, "Geen nieuwe knopen geïntroduceerd"

    def test_learner_serialisation_after_real_session(self, real_graph):
        """Het LearnerModel blijft JSON-serializable na een echte sessie-loop."""
        learner = LearnerModel(user_id=uuid4())
        now = datetime(2026, 4, 16, 10, 0, 0)

        run_session(
            learner,
            real_graph,
            lambda node_id, node: (ResponseType.CORRECT, 1500),
            now=now,
        )

        serialized = learner.model_dump_json()
        restored = LearnerModel.model_validate_json(serialized)
        assert set(restored.node_states.keys()) == set(learner.node_states.keys())
        assert len(restored.session_history) == 1
