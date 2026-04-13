#!/usr/bin/env python3
"""CLI script: run an interactive or simulated learning session."""

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from gymnasium_classica.diagnostic.methode_profile import (
    apply_methode_profile,
    load_methode_mapping,
)
from gymnasium_classica.diagnostic.placement import run_diagnostic
from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.graph import KennisKnoop
from gymnasium_classica.models.learner import LearnerModel, ResponseType
from gymnasium_classica.scheduling.session import run_session


def load_learner(path: Path) -> LearnerModel:
    """Load a LearnerModel from a JSON file, or create a fresh one."""
    if path.exists():
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return LearnerModel(**data)
    return LearnerModel(user_id=uuid4())


def save_learner(learner: LearnerModel, path: Path) -> None:
    """Save a LearnerModel to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(learner.model_dump(), f, indent=2, default=str, ensure_ascii=False)


def interactive_answer_fn(knoop_id: str, knoop: KennisKnoop) -> tuple[ResponseType, int]:
    """Prompt the user for an answer via stdin."""
    print(f"\n  [{knoop.type.value}] {knoop.titel_nl}")
    print(f"  {knoop.beschrijving}")
    while True:
        choice = input("  Antwoord — (c)orrect, (s)low, (i)ncorrect: ").strip().lower()
        if choice in ("c", "correct"):
            return (ResponseType.CORRECT, 2000)
        elif choice in ("s", "slow"):
            return (ResponseType.SLOW_CORRECT, 4000)
        elif choice in ("i", "incorrect"):
            return (ResponseType.INCORRECT, 6000)
        print("  Kies c, s, of i.")


def make_simulated_answer_fn(learner: LearnerModel):
    """Return an answer_fn that simulates responses based on mastery + noise."""

    def answer(knoop_id: str, knoop: KennisKnoop) -> tuple[ResponseType, int]:
        state = learner.knoop_states.get(knoop_id)
        posterior = state.posterior_mastery if state else 0.10

        # Add 10% noise
        if random.random() < 0.10:
            posterior = 1.0 - posterior

        if posterior >= 0.75:
            return (ResponseType.CORRECT, 1500)
        elif posterior >= 0.40:
            return (ResponseType.SLOW_CORRECT, 4000)
        else:
            return (ResponseType.INCORRECT, 6000)

    return answer


def print_session_summary(result) -> None:
    """Print a formatted summary of the session to stdout."""
    print(f"\n{'=' * 50}")
    print(f"Sessie {result.session_id} — samenvatting")
    print(f"{'=' * 50}")
    print(f"Items:        {len(result.items)}")
    print(f"Nieuwe stof:  {len(result.nodes_introduced)}")
    print(f"Review:       {len(result.nodes_reviewed)}")

    if result.mastery_changes:
        print(f"\nMastery-veranderingen:")
        for knoop_id, (before, after) in sorted(result.mastery_changes.items()):
            direction = "↑" if after > before else "↓" if after < before else "="
            print(f"  {direction} {knoop_id}: {before:.2f} → {after:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gymnasium Classica — sessie draaien")
    parser.add_argument("graph_path", type=Path, help="Pad naar graph JSON of directory")
    parser.add_argument("--learner", type=Path, default=Path("learner.json"),
                        help="Pad naar learner JSON (aangemaakt als afwezig)")
    parser.add_argument("--simulate", action="store_true",
                        help="Gebruik gesimuleerde antwoorden")
    parser.add_argument("--intake", nargs=2, metavar=("METHODE", "HOOFDSTUK"),
                        help="Voer eerst diagnostische intake uit")

    args = parser.parse_args()

    graph = load_graph(args.graph_path)
    learner = load_learner(args.learner)

    print(f"Graph geladen: {graph.number_of_nodes()} knopen, {graph.number_of_edges()} edges")
    print(f"Learner: {'bestaand' if args.learner.exists() else 'nieuw aangemaakt'}")

    # Optional diagnostic intake
    if args.intake and not learner.intake_completed:
        methode, chapter = args.intake
        print(f"\n--- Diagnostische intake: {methode} t/m hoofdstuk {chapter} ---")

        mapping = load_methode_mapping()
        apply_methode_profile(learner, graph, methode, chapter, mapping)

        if args.simulate:
            answer_fn = make_simulated_answer_fn(learner)
            diag_answer = lambda kid: answer_fn(kid, graph.nodes[kid]["knoop"])[0] == ResponseType.CORRECT
        else:
            def diag_answer(kid):
                knoop = graph.nodes[kid]["knoop"]
                resp, _ = interactive_answer_fn(kid, knoop)
                return resp in (ResponseType.CORRECT, ResponseType.SLOW_CORRECT)

        diag_result = run_diagnostic(learner, graph, diag_answer)
        print(f"Intake compleet: {diag_result.questions_asked} vragen, "
              f"geconvergeerd: {diag_result.converged}")

    # Run session
    print(f"\n--- Sessie starten (30 min) ---")

    if args.simulate:
        answer_fn = make_simulated_answer_fn(learner)
    else:
        answer_fn = interactive_answer_fn

    result = run_session(learner, graph, answer_fn)
    print_session_summary(result)

    # Save learner state
    save_learner(learner, args.learner)
    print(f"\nLeerling-status opgeslagen: {args.learner}")


if __name__ == "__main__":
    main()
