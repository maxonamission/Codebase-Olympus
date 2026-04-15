"""Pydantic models for user accounts and subscriptions."""

from datetime import datetime
from enum import StrEnum
from typing import Optional
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
    expires_at: Optional[datetime] = None


class User(BaseModel):
    """A learner account."""

    id: UUID = Field(default_factory=uuid4)
    email: str
    auth_provider: str = "local"
    subscription: Subscription = Field(default_factory=Subscription)
    examenjaar_ltc: Optional[int] = None
    examenjaar_gtc: Optional[int] = None
    pronunciation_preference_lat: PronunciationLat = PronunciationLat.CLASSICAL
    pronunciation_preference_grc: PronunciationGrc = PronunciationGrc.ERASMIAN
    learning_route: LearningRoute = LearningRoute.GRAMMAR_FIRST
    created_at: datetime = Field(default_factory=datetime.now)
