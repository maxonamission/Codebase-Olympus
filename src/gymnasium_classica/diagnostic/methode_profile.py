"""School-method profile: set BKT priors based on which textbook chapters
the learner has completed.

Mechanism 1 of the diagnostic intake system.
"""

import json
from pathlib import Path
from typing import Any

import networkx as nx

from gymnasium_classica.models.learner import LearnerModel, MasterySource, NodeState

# Default priors
PRIOR_TREATED = 0.70  # Chapters already covered → expected mastered, to be verified
PRIOR_UNTREATED = 0.10  # Not yet covered → expected unknown

MethodeMapping = dict[str, Any]  # raw parsed JSON structure


def load_methode_mapping(path: Path | None = None) -> MethodeMapping:
    """Load the method mapping from a JSON file.

    Falls back to ``data/methode_mapping.json`` relative to the project root.
    """
    if path is None:
        path = Path(__file__).resolve().parents[3] / "data" / "methode_mapping.json"
    with open(path, encoding="utf-8") as f:
        data: MethodeMapping = json.load(f)
    return data


def get_treated_node_ids(
    mapping: MethodeMapping,
    methode: str,
    up_to_chapter: str,
) -> set[str]:
    """Return all node IDs that are treated up to (and including) *up_to_chapter*.

    Chapters are accumulated: chapter 3 includes chapters 1, 2, and 3.
    """
    methode_data = mapping["methoden"].get(methode)
    if methode_data is None:
        raise ValueError(f"Unknown methode: {methode!r}")

    chapters = methode_data.get("hoofdstukken", {})
    treated: set[str] = set()

    for chapter_key in sorted(chapters.keys()):
        if chapter_key.startswith("_"):
            continue
        chapter_data = chapters[chapter_key]
        treated.update(chapter_data.get("node_ids", []))
        if chapter_key == up_to_chapter:
            break

    return treated


def validate_methode_mapping(
    mapping: MethodeMapping,
    graph: nx.DiGraph,
) -> list[str]:
    """Validate a method mapping against the knowledge graph (M1-03).

    Checks, per method:
      - every referenced node ID exists in the graph,
      - no node ID is listed in more than one chapter of the same method,
      - chapter numbers are consecutive starting at 1 (no gaps).

    Keys starting with ``_`` (e.g. ``_comment``) are ignored. Returns a list
    of error messages (empty if the mapping is valid).
    """
    errors: list[str] = []
    for methode, methode_data in mapping.get("methoden", {}).items():
        chapters = methode_data.get("hoofdstukken", {})
        chapter_keys = [k for k in chapters if not k.startswith("_")]

        # Consecutive chapter numbering starting at 1.
        try:
            numbers = sorted(int(k) for k in chapter_keys)
        except ValueError:
            errors.append(
                f"Methode '{methode}': niet-numerieke hoofdstuksleutel in {chapter_keys}"
            )
            numbers = []
        if numbers and numbers != list(range(1, len(numbers) + 1)):
            errors.append(
                f"Methode '{methode}': hoofdstukken niet opeenvolgend vanaf 1: {numbers}"
            )

        seen: set[str] = set()
        for key in chapter_keys:
            for node_id in chapters[key].get("node_ids", []):
                if node_id not in graph.nodes:
                    errors.append(
                        f"Methode '{methode}' hoofdstuk {key}: onbestaande knoop {node_id}"
                    )
                if node_id in seen:
                    errors.append(
                        f"Methode '{methode}': knoop {node_id} komt in meerdere hoofdstukken voor"
                    )
                seen.add(node_id)
    return errors


def apply_methode_profile(
    learner: LearnerModel,
    graph: nx.DiGraph,
    methode: str,
    up_to_chapter: str,
    mapping: MethodeMapping | None = None,
) -> LearnerModel:
    """Set BKT priors on a learner model based on a school-method profile.

    Nodes covered by the method up to *up_to_chapter* get
    ``posterior_mastery = 0.70`` (treated).  All other nodes get
    ``posterior_mastery = 0.10`` (untreated).

    Returns the mutated *learner* for convenience.
    """
    if mapping is None:
        mapping = load_methode_mapping()

    treated_ids = get_treated_node_ids(mapping, methode, up_to_chapter)

    for node_id in graph.nodes:
        prior = PRIOR_TREATED if node_id in treated_ids else PRIOR_UNTREATED
        learner.node_states[node_id] = NodeState(
            node_id=node_id,
            posterior_mastery=prior,
            source=MasterySource.DIAGNOSTIC,
        )

    learner.intake_method = methode
    return learner
