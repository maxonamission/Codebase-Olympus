"""Pydantic models for user accounts and subscriptions."""

from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Plan(StrEnum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"


class SubscriptionStatus(StrEnum):
    TRIAL = "trial"
    ACTIVE = "active"
    EXPIRED = "expired"


class LearningRoute(StrEnum):
    GRAMMAR_FIRST = "grammar_first"
    CONTEXT_FIRST = "context_first"


class PronunciationLat(StrEnum):
    CLASSICAL = "classical"  # Restored classical pronunciation (default)
    ECCLESIASTICAL = "ecclesiastical"  # Church Latin


class PronunciationGrc(StrEnum):
    ERASMIAN = "erasmian"  # Standard on Dutch gymnasia (default)
    MODERN = "modern"  # Modern Greek pronunciation


class Subscription(BaseModel):
    """Subscription state for a user account."""

    plan: Plan = Plan.FREE
    status: SubscriptionStatus = SubscriptionStatus.TRIAL
    started_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime | None = None


class User(BaseModel):
    """A learner account."""

    id: UUID = Field(default_factory=uuid4)
    email: str
    auth_provider: str = "local"
    subscription: Subscription = Field(default_factory=Subscription)
    examenjaar_ltc: int | None = None
    examenjaar_gtc: int | None = None
    pronunciation_preference_lat: PronunciationLat = PronunciationLat.CLASSICAL
    pronunciation_preference_grc: PronunciationGrc = PronunciationGrc.ERASMIAN
    learning_route: LearningRoute = LearningRoute.GRAMMAR_FIRST
    show_grammar_scaffolding: bool = Field(
        default=True,
        description=(
            "Opt-in: grammar-first learners zien markdown-uitleg bij de "
            "eerste introductie van een G-node.  Context-first leerlingen "
            "krijgen altijd scaffolding na een passage — deze flag raakt "
            "alleen grammar-first.  Bestaande users krijgen True bij de "
            "eerste laad-actie dankzij de Pydantic-default."
        ),
    )
    created_at: datetime = Field(default_factory=datetime.now)
