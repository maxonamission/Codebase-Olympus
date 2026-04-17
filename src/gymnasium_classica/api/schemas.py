"""Pydantic request/response models for the API."""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# -- Auth --


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    user_id: str
    token: str


# -- Session --


class ItemInfo(BaseModel):
    id: str
    type: str
    stimulus: str | dict
    feedback: str
    verwachte_tijd_sec: int


class VocabMetadata(BaseModel):
    """Structured lemma-metadata for V-knopen (F1-05).

    Mirrors :class:`VocabEntry` in ``vocab/loader.py`` but uses full-word
    field names so the frontend doesn't need to understand the compact
    JSON-source vocabulary (``pos`` → ``part_of_speech`` etc.).
    """

    lemma: str
    part_of_speech: str
    conjugation: Optional[str] = None
    forms: Optional[str] = Field(
        default=None,
        description=(
            "For nouns/adjectives: genitive form.  For verbs: stamtijden. "
            "For prepositions: governed case(s)."
        ),
    )
    meaning: str
    cluster: Optional[str] = Field(
        default=None,
        description="Semantisch cluster label, or None.",
    )


class QuestionResponse(BaseModel):
    knoop_id: str
    titel: str
    beschrijving: str
    stimulus: str | dict
    phase: str
    items: list[ItemInfo] = Field(default_factory=list)
    scaffolding_content: Optional[str] = Field(
        default=None,
        description="Markdown grammar explanation for context-first scaffolding",
    )
    vocab_metadata: Optional[VocabMetadata] = Field(
        default=None,
        description="Structured metadata for V-knopen (F1-05 — woordkaart).",
    )
    # Promoted from the first item so the frontend can read a flat shape
    # (question.item_type / question.options / ...) instead of digging into
    # items[0].stimulus.
    item_type: Optional[str] = None
    instruction: Optional[str] = None
    options: Optional[list[str]] = None
    hint: Optional[str] = None
    audio_ref: Optional[str] = None


class StartSessionResponse(BaseModel):
    session_id: str
    question: Optional[QuestionResponse] = None


class AnswerRequest(BaseModel):
    session_id: str
    response_time_ms: int = Field(ge=0)
    response: Optional[str] = Field(
        default=None,
        description=(
            "Self-assessment outcome: correct, incorrect, or slow_correct. "
            "Required when answer_text is not provided."
        ),
    )
    answer_text: Optional[str] = Field(
        default=None,
        description=(
            "Raw answer the learner typed or selected.  When provided, "
            "the server grades it against the current item and ignores "
            "response."
        ),
    )


class FeedbackResponse(BaseModel):
    knoop_id: str
    correct: bool
    response_type: str = Field(description="The original response: correct, slow_correct, or incorrect")
    mastery_before: float
    mastery_after: float


class AnswerResponse(BaseModel):
    feedback: FeedbackResponse
    next_question: Optional[QuestionResponse] = None
    session_finished: bool = False


# -- Session summary --


class MasteryChange(BaseModel):
    before: float
    after: float


class SessionSummaryResponse(BaseModel):
    session_id: str
    started_at: str
    ended_at: str
    total_items: int
    nodes_introduced: list[str]
    nodes_reviewed: list[str]
    mastery_changes: dict[str, MasteryChange]
    phases_completed: list[str]


# -- Progress --


class DomainProgress(BaseModel):
    total: int
    mastered: int
    in_progress: int
    unseen: int


class SessionMasteryEntry(BaseModel):
    """Mastery snapshot after a single session."""

    session_id: str
    timestamp: str
    learning_route: Optional[str] = None
    nodes_practiced: int
    mastered_after: int


class ProgressOverviewResponse(BaseModel):
    total_nodes: int
    mastered: int
    in_progress: int
    unseen: int
    domains: dict[str, DomainProgress]
    streak_days: int
    intake_completed: bool
    session_progression: list[SessionMasteryEntry] = Field(
        default_factory=list,
        description="Mastery progression per session, for route comparison",
    )


class ClusterProgress(BaseModel):
    """Progress in a single semantic vocabulary cluster."""

    label: str
    beschrijving: str
    total: int
    mastered: int
    in_progress: int
    unseen: int
    mastered_pct: float


class ClustersResponse(BaseModel):
    """Per-cluster vocabulary progress for the dashboard."""

    clusters: list[ClusterProgress]


class ItemHistoryEntry(BaseModel):
    timestamp: str
    item_id: str
    correct: bool
    response_time_ms: int


class KnoopProgressResponse(BaseModel):
    knoop_id: str
    titel: str
    type: str
    posterior_mastery: float
    easiness_factor: float
    interval_days: float
    repetitions: int
    last_review: Optional[str] = None
    source: str
    item_history: list[ItemHistoryEntry]


# -- Graph visualisation --


class GraphNode(BaseModel):
    id: str
    titel: str
    type: str
    taal: str
    mastery: float
    status: str  # "mastered", "in_progress", "unseen"


class GraphEdge(BaseModel):
    source: str
    target: str
    type: str  # "prerequisite", "enrichment", "transfer"


class GraphDataResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


# -- Intake --


class IntakeStartRequest(BaseModel):
    methode: Optional[str] = Field(
        default=None,
        description="Schoolmethode, bijv. 'fortuna', 'pallas'. Indien opgegeven samen met chapter.",
    )
    chapter: Optional[str] = Field(
        default=None,
        description="Laatst behandelde hoofdstuk, bijv. 'h03'.",
    )


class IntakeQuestionResponse(BaseModel):
    knoop_id: str
    titel: str
    beschrijving: str
    questions_asked: int
    max_questions: int


class IntakeStartResponse(BaseModel):
    intake_id: str
    question: Optional[IntakeQuestionResponse] = None
    already_completed: bool = False


class IntakeAnswerRequest(BaseModel):
    intake_id: str
    correct: bool


class IntakeAnswerResponse(BaseModel):
    questions_asked: int
    next_question: Optional[IntakeQuestionResponse] = None
    finished: bool = False
    converged: bool = False


# -- User settings --


class UpdateLearningRouteRequest(BaseModel):
    learning_route: str = Field(description="'grammar_first' or 'context_first'")


class UserProfileResponse(BaseModel):
    user_id: str
    email: str
    learning_route: str
