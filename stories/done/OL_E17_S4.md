---
type: story
project: GC
epic: E17
story_id: OL_E17_S4
legacy_id: D1-04
track: app
status: done
prioriteit: middel
---

# Story OL_E17_S4: SessionManager: stapsgewijs sessie-protocol

## Doel
Bridge tussen de API en de sessie-engine. Vervangt de synchrone answer_fn callback door een stap-voor-stap protocol: start_session() → Question, submit_answer() → AnswerResult, get_summary() → SessionSummary. In-memory state per sessie.

## Input
scheduling/session.py, scheduling/priority.py, scheduling/bkt.py, scheduling/sm2.py

## Acceptatiecriteria
- [x] Alle bestaande tests blijven groen
- [x] Nieuwe functionaliteit heeft eigen tests (backend) of is visueel geverifieerd (frontend)
- [x] Geen breaking changes in bestaande modules


<!-- legacy-bulk-checked: 2026-04-20 — AC retroactief afgevinkt door OL_E29_S7 cleanup -->

## Scope
api/session_manager.py: SessionManager class, Question/AnswerResult/SessionSummary dataclasses

## Geschat
—
