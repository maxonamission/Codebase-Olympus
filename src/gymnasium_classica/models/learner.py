"""Pydantic models for the learner model: knowledge state and session history."""

from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


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


class KnoopState(BaseModel):
    """Per-node mastery state for a learner, combining BKT posterior and SM-2 scheduling."""

    knoop_id: str
    posterior_mastery: float = Field(ge=0.0, le=1.0, default=0.0)
    easiness_factor: float = Field(gt=0.0, default=2.5)
    interval_days: float = Field(ge=0.0, default=0.0)
    repetitions: int = Field(ge=0, default=0)
    last_review: Optional[datetime] = None
    last_response: Optional[ResponseType] = None
    source: MasterySource = MasterySource.PRACTICE
    item_history: list[ItemResponse] = Field(default_factory=list)


class OfflineAssignment(BaseModel):
    """A pending offline writing assignment scheduled at the end of a session."""

    knoop_id: str
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
    ended_at: Optional[datetime] = None
    items_reviewed: list[str] = Field(
        default_factory=list, description="List of item IDs reviewed in this session"
    )
    learning_route: Optional[str] = Field(
        default=None,
        description="The learning route active during this session",
    )


class LearnerModel(BaseModel):
    """Complete learner model for one user: mastery states and session history."""

    user_id: UUID
    knoop_states: dict[str, KnoopState] = Field(default_factory=dict)
    session_history: list[SessionRecord] = Field(default_factory=list)
    pending_offline_assignments: list[OfflineAssignment] = Field(default_factory=list)
    route_history: list[RouteSwitch] = Field(default_factory=list)
    self_report_count: int = Field(default=0, ge=0)
    ocr_verified_count: int = Field(default=0, ge=0)
    intake_completed: bool = False
    intake_method: Optional[str] = Field(
        default=None,
        description="School method used during intake, e.g. 'fortuna', 'pallas'.",
    )
