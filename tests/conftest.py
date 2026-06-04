"""Shared test fixtures for Gymnasium Classica tests."""

from pathlib import Path

import pytest


@pytest.fixture
def sample_node_data() -> dict:
    """A minimal valid Node as a dict."""
    return {
        "id": "LAT-G-MORF-NOM-D1",
        "type": "G",
        "language": "lat",
        "title_nl": "Nominativus 1e declinatie",
        "description": "De nominativus enkelvoud en meervoud van de 1e declinatie (-a).",
        "bloom_level": "kennis",
        "phase": "onderbouw_1",
        "testable": True,
        "pensum_years": [],
        "items": [],
    }


@pytest.fixture
def sample_edge_data() -> dict:
    """A minimal valid PrerequisiteEdge as a dict."""
    return {
        "source_id": "LAT-G-MORF-DECL1-INTRO",
        "target_id": "LAT-G-MORF-NOM-D1",
        "type": "prerequisite",
        "encompassing_weight": 0.3,
    }


@pytest.fixture
def sample_graph_data() -> dict:
    """A small valid graph (5 nodes, 4 edges) for testing."""
    return {
        "nodes": [
            {
                "id": "LAT-G-MORF-NAAMVAL-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "Wat is een naamval?",
                "description": "Introductie van het concept naamval in het Latijn.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "Wat is een declinatie?",
                "description": "Introductie van het concept declinatie.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL1-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "De eerste declinatie",
                "description": "Overzicht van de 1e declinatie (a-stammen).",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
            {
                "id": "LAT-G-MORF-NOM-D1",
                "type": "G",
                "language": "lat",
                "title_nl": "Nominativus 1e declinatie",
                "description": "De nominativus enkelvoud en meervoud van de 1e declinatie.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
            {
                "id": "LAT-G-MORF-ACC-D1",
                "type": "G",
                "language": "lat",
                "title_nl": "Accusativus 1e declinatie",
                "description": "De accusativus enkelvoud en meervoud van de 1e declinatie.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
        ],
        "edges": [
            {
                "source_id": "LAT-G-MORF-NAAMVAL-INTRO",
                "target_id": "LAT-G-MORF-DECL-INTRO",
                "type": "prerequisite",
                "encompassing_weight": 0.5,
            },
            {
                "source_id": "LAT-G-MORF-DECL-INTRO",
                "target_id": "LAT-G-MORF-DECL1-INTRO",
                "type": "prerequisite",
                "encompassing_weight": 0.4,
            },
            {
                "source_id": "LAT-G-MORF-DECL1-INTRO",
                "target_id": "LAT-G-MORF-NOM-D1",
                "type": "prerequisite",
                "encompassing_weight": 0.3,
            },
            {
                "source_id": "LAT-G-MORF-DECL1-INTRO",
                "target_id": "LAT-G-MORF-ACC-D1",
                "type": "prerequisite",
                "encompassing_weight": 0.3,
            },
        ],
    }


@pytest.fixture
def cyclic_graph_data() -> dict:
    """A graph with a cycle (A -> B -> C -> A) for negative testing."""
    return {
        "nodes": [
            {
                "id": "LAT-G-MORF-NOM-D1",
                "type": "G",
                "language": "lat",
                "title_nl": "Knoop A",
                "description": "Test node A.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
            {
                "id": "LAT-G-MORF-NOM-D2",
                "type": "G",
                "language": "lat",
                "title_nl": "Knoop B",
                "description": "Test node B.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
            {
                "id": "LAT-G-MORF-NOM-D3",
                "type": "G",
                "language": "lat",
                "title_nl": "Knoop C",
                "description": "Test node C.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
        ],
        "edges": [
            {
                "source_id": "LAT-G-MORF-NOM-D1",
                "target_id": "LAT-G-MORF-NOM-D2",
                "type": "prerequisite",
                "encompassing_weight": 0.5,
            },
            {
                "source_id": "LAT-G-MORF-NOM-D2",
                "target_id": "LAT-G-MORF-NOM-D3",
                "type": "prerequisite",
                "encompassing_weight": 0.5,
            },
            {
                "source_id": "LAT-G-MORF-NOM-D3",
                "target_id": "LAT-G-MORF-NOM-D1",
                "type": "prerequisite",
                "encompassing_weight": 0.5,
            },
        ],
    }


@pytest.fixture
def bidirectional_transfer_graph_data() -> dict:
    """A graph with bidirectional transfer edges (should NOT count as cycles)."""
    return {
        "nodes": [
            {
                "id": "LAT-G-MORF-NAAMVAL-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "Naamval LAT",
                "description": "Naamval introductie Latijn.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
            {
                "id": "LAT-G-MORF-DECL-INTRO",
                "type": "G",
                "language": "lat",
                "title_nl": "Declinatie LAT",
                "description": "Declinatie introductie Latijn.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
            {
                "id": "GRC-G-MORF-NAAMVAL-INTRO",
                "type": "G",
                "language": "grc",
                "title_nl": "Naamval GRC",
                "description": "Naamval introductie Grieks.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
            {
                "id": "GRC-G-MORF-DECL-INTRO",
                "type": "G",
                "language": "grc",
                "title_nl": "Declinatie GRC",
                "description": "Declinatie introductie Grieks.",
                "bloom_level": "kennis",
                "phase": "onderbouw_1",
                "testable": True,
                "items": [],
            },
        ],
        "edges": [
            # Prerequisite edges (acyclic)
            {
                "source_id": "LAT-G-MORF-NAAMVAL-INTRO",
                "target_id": "LAT-G-MORF-DECL-INTRO",
                "type": "prerequisite",
                "encompassing_weight": 0.5,
            },
            {
                "source_id": "GRC-G-MORF-NAAMVAL-INTRO",
                "target_id": "GRC-G-MORF-DECL-INTRO",
                "type": "prerequisite",
                "encompassing_weight": 0.5,
            },
            # Bidirectional transfer edges (would be cycles if counted)
            {
                "source_id": "LAT-G-MORF-NAAMVAL-INTRO",
                "target_id": "GRC-G-MORF-NAAMVAL-INTRO",
                "type": "transfer",
                "encompassing_weight": 0.7,
            },
            {
                "source_id": "GRC-G-MORF-NAAMVAL-INTRO",
                "target_id": "LAT-G-MORF-NAAMVAL-INTRO",
                "type": "transfer",
                "encompassing_weight": 0.5,
            },
            {
                "source_id": "LAT-G-MORF-DECL-INTRO",
                "target_id": "GRC-G-MORF-DECL-INTRO",
                "type": "transfer",
                "encompassing_weight": 0.6,
            },
            {
                "source_id": "GRC-G-MORF-DECL-INTRO",
                "target_id": "LAT-G-MORF-DECL-INTRO",
                "type": "transfer",
                "encompassing_weight": 0.4,
            },
        ],
    }


@pytest.fixture
def poc_graph_path() -> Path:
    """Path to the PoC JSON file."""
    return Path(__file__).parent.parent / "data" / "graph" / "lat_grammatica_poc.json"
