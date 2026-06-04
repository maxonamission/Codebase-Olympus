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


def get_treated_knoop_ids(
    mapping: MethodeMapping,
    methode: str,
    up_to_chapter: str,
) -> set[str]:
    """Return all knoop IDs that are treated up to (and including) *up_to_chapter*.

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
        treated.update(chapter_data.get("knoop_ids", []))
        if chapter_key == up_to_chapter:
            break

    return treated


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

    treated_ids = get_treated_knoop_ids(mapping, methode, up_to_chapter)

    for node_id in graph.nodes:
        prior = PRIOR_TREATED if node_id in treated_ids else PRIOR_UNTREATED
        learner.knoop_states[node_id] = NodeState(
            knoop_id=node_id,
            posterior_mastery=prior,
            source=MasterySource.DIAGNOSTIC,
        )

    learner.intake_method = methode
    return learner
