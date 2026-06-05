"""Pydantic models for user accounts and subscriptions."""

from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


class Role(StrEnum):
    """Account role. Determines which endpoints a user may access.

    Existing accounts default to ``LEARNER`` via the Pydantic default,
    so the field is backward-compatible with users stored before F2-01.
    """

    LEARNER = "learner"
    MENTOR = "mentor"


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


class Modus(StrEnum):
    """User mode: which optimisation goal the scheduler plans towards.

    - ``STAATSEXAMEN``: long-horizon mastery of the exam end-terms.
    - ``BIJSPIJKER``: short-horizon catch-up towards a school method/chapter.

    The Pydantic default is ``STAATSEXAMEN`` so accounts stored before M1-03
    deserialize unchanged (backward-compatible, no migration needed). New
    accounts are steered to ``BIJSPIJKER`` by the onboarding flow, which sets
    the mode together with method + chapter so the validator below is met.
    """

    STAATSEXAMEN = "staatsexamen"
    BIJSPIJKER = "bijspijker"


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
    role: Role = Role.LEARNER
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
    modus: Modus = Modus.STAATSEXAMEN
    huidige_methode_lat: str | None = Field(
        default=None, description='Active Latin school method, e.g. "fortuna".'
    )
    huidige_hoofdstuk_lat: int | None = Field(default=None, ge=1)
    huidige_methode_grc: str | None = Field(
        default=None, description='Active Greek school method, e.g. "pallas".'
    )
    huidige_hoofdstuk_grc: int | None = Field(default=None, ge=1)
    created_at: datetime = Field(default_factory=datetime.now)

    @model_validator(mode="after")
    def _check_bijspijker_config(self) -> "User":
        """In BIJSPIJKER mode at least one language needs method + chapter.

        Only enforced for BIJSPIJKER, so STAATSEXAMEN users (including all
        pre-M1-03 accounts deserialized with the default) are unaffected.
        """
        if self.modus == Modus.BIJSPIJKER:
            lat_ok = (
                self.huidige_methode_lat is not None and self.huidige_hoofdstuk_lat is not None
            )
            grc_ok = (
                self.huidige_methode_grc is not None and self.huidige_hoofdstuk_grc is not None
            )
            if not (lat_ok or grc_ok):
                raise ValueError(
                    "BIJSPIJKER-modus vereist huidige_methode + huidige_hoofdstuk "
                    "voor minstens één taal (Latijn of Grieks)."
                )
        return self
