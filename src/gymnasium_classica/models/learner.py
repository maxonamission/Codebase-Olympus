"""Pydantic models for the learner model: knowledge state and session history."""

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field

from gymnasium_classica.models.graph import Direction


class ResponseType(StrEnum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    SLOW_CORRECT = "slow_correct"


class SelfReportResponse(StrEnum):
    """Self-reported outcome for an offline writing assignment."""

    CORRECT = "correct"
    PARTIAL = "partial"
    INCORRECT = "incorrect"


class MasterySource(StrEnum):
    """How the current posterior mastery was established."""

    DIAGNOSTIC = "diagnostic"  # Set during intake placement test
    PRACTICE = "practice"  # Updated through regular exercises
    REVIEW = "review"  # Updated through fallback / conditional-completion review
    SELF_REPORT = "self_report"  # Updated through self-reported offline work


class ItemResponse(BaseModel):
    """A single recorded response to an exercise item."""

    timestamp: datetime
    item_id: str
    correct: bool
    response_time_ms: int = Field(ge=0)
    answer_text: str | None = Field(
        default=None,
        description=(
            "Raw answer the learner typed or selected.  None when the "
            "response came from self-assessment (no literal answer)."
        ),
    )
    correct_answer: str | None = Field(
        default=None,
        description=(
            "Snapshot of the expected answer at the time of the attempt, "
            "so later analysis doesn't break when items are rewritten."
        ),
    )
    item_type: str | None = Field(
        default=None,
        description="ItemType value at attempt-time (herkenning, productie, ...).",
    )
    # --- L1-01 meetlaag: verplichte velden voor retentie- en effectgrootte-analyse ---
    node_id: str = Field(
        description="Knoop waartoe dit antwoord hoort; maakt de respons zelf-beschrijvend voor platte analyse en export.",
    )
    direction: str | None = Field(
        description=(
            "Direction (Direction-value: 'receptive'/'productive') van het item, "
            "gesnapshot op moment van antwoorden. None bij self-assessment zonder item."
        ),
    )
    mastery_before: float = Field(
        ge=0.0,
        le=1.0,
        description="BKT-posterior mastery vlak vóór deze poging; basis voor leerwinst/effectgrootte.",
    )


class NodeState(BaseModel):
    """Per-node mastery state for a learner, combining BKT posterior and SM-2 scheduling."""

    node_id: str
    posterior_mastery: float = Field(ge=0.0, le=1.0, default=0.0)
    receptive_mastery: float = Field(
        ge=0.0,
        le=1.0,
        default=0.0,
        description="BKT-posterior voor receptieve items (herkennen). L2-01.",
    )
    productive_mastery: float = Field(
        ge=0.0,
        le=1.0,
        default=0.0,
        description="BKT-posterior voor productieve items (zelf produceren). L2-01.",
    )
    easiness_factor: float = Field(gt=0.0, default=2.5)
    interval_days: float = Field(ge=0.0, default=0.0)
    repetitions: int = Field(ge=0, default=0)
    last_review: datetime | None = None
    last_response: ResponseType | None = None
    source: MasterySource = MasterySource.PRACTICE
    item_history: list[ItemResponse] = Field(default_factory=list)

    def mastery_for(self, direction: Direction | None) -> float:
        """Mastery voor een richting; ``None`` geeft de overall posterior.

        Vormt de interface waarmee scheduler/diagnostiek optioneel per
        richting kan redeneren (L2-01).
        """
        if direction == Direction.RECEPTIVE:
            return self.receptive_mastery
        if direction == Direction.PRODUCTIVE:
            return self.productive_mastery
        return self.posterior_mastery

    @property
    def combined_mastery(self) -> float:
        """Strenge afgeleide overall-mastery: min van receptief en productief.

        Beschikbaar voor diagnostiek die 'beide richtingen beheerst' wil
        weten; ``posterior_mastery`` blijft de reguliere overall-trajectorie.
        """
        return min(self.receptive_mastery, self.productive_mastery)


class OfflineAssignment(BaseModel):
    """A pending offline writing assignment scheduled at the end of a session."""

    node_id: str
    item_id: str
    assigned_at: datetime
    completed: bool = False


class RouteSwitch(BaseModel):
    """A record of a learning route change."""

    timestamp: datetime
    route: str = Field(description="'grammar_first' or 'context_first'")


class SessionRecord(BaseModel):
    """A record of a single study session."""

    session_id: str
    started_at: datetime
    ended_at: datetime | None = None
    items_reviewed: list[str] = Field(
        default_factory=list, description="List of item IDs reviewed in this session"
    )
    learning_route: str | None = Field(
        default=None,
        description="The learning route active during this session",
    )


class BaselineSnapshot(BaseModel):
    """Mastery-nulpunt vastgelegd bij afronding van de intake.

    Dient als referentie om voortgang en effectgrootte tegen af te zetten
    (L1-02). Apart herkenbaar van latere metingen via ``captured_at``.
    """

    captured_at: datetime
    mastery: dict[str, float] = Field(
        default_factory=dict,
        description="node_id -> posterior_mastery op het baseline-moment.",
    )


class LearnerModel(BaseModel):
    """Complete learner model for one user: mastery states and session history."""

    user_id: UUID
    node_states: dict[str, NodeState] = Field(default_factory=dict)
    session_history: list[SessionRecord] = Field(default_factory=list)
    pending_offline_assignments: list[OfflineAssignment] = Field(default_factory=list)
    route_history: list[RouteSwitch] = Field(default_factory=list)
    self_report_count: int = Field(default=0, ge=0)
    ocr_verified_count: int = Field(default=0, ge=0)
    intake_completed: bool = False
    intake_method: str | None = Field(
        default=None,
        description="School method used during intake, e.g. 'fortuna', 'pallas'.",
    )
    baseline: BaselineSnapshot | None = Field(
        default=None,
        description="Mastery-nulpunt vastgelegd bij intake-afronding (L1-02).",
    )
    experiment_arms: dict[str, str] = Field(
        default_factory=dict,
        description="Toegewezen experiment-varianten (experiment-naam -> arm-naam), "
        "zodat metriek per variant uitgesplitst kan worden (L1-03).",
    )
    learning_rate: float = Field(
        default=1.0,
        gt=0.0,
        description="Learner-niveau leersnelheid: modifier op de BKT-transitie "
        "P(T). 1.0 = neutraal (huidig gedrag); geschat uit de "
        "observatiegeschiedenis (L2-03).",
    )
