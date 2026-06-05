"""Pydantic request/response models for the API."""

from typing import Any

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
    stimulus: str | dict[str, Any]
    feedback: str
    expected_time_sec: int


class VocabMetadata(BaseModel):
    """Structured lemma-metadata for V-nodes (F1-05).

    Mirrors :class:`VocabEntry` in ``vocab/loader.py`` but uses full-word
    field names so the frontend doesn't need to understand the compact
    JSON-source vocabulary (``pos`` → ``part_of_speech`` etc.).
    """

    lemma: str
    part_of_speech: str
    conjugation: str | None = None
    forms: str | None = Field(
        default=None,
        description=(
            "For nouns/adjectives: genitive form.  For verbs: stamtijden. "
            "For prepositions: governed case(s)."
        ),
    )
    meaning: str
    cluster: str | None = Field(
        default=None,
        description="Semantisch cluster label, or None.",
    )


class QuestionResponse(BaseModel):
    node_id: str
    title: str
    description: str
    stimulus: str | dict[str, Any]
    phase: str
    items: list[ItemInfo] = Field(default_factory=list)
    scaffolding_content: str | None = Field(
        default=None,
        description="Markdown grammar explanation for context-first scaffolding",
    )
    vocab_metadata: VocabMetadata | None = Field(
        default=None,
        description="Structured metadata for V-nodes (F1-05 — woordkaart).",
    )
    # Promoted from the first item so the frontend can read a flat shape
    # (question.item_type / question.options / ...) instead of digging into
    # items[0].stimulus.
    item_type: str | None = None
    instruction: str | None = None
    options: list[str] | None = None
    hint: str | None = None
    audio_ref: str | None = None


class StartSessionResponse(BaseModel):
    session_id: str
    question: QuestionResponse | None = None


class AnswerRequest(BaseModel):
    session_id: str
    response_time_ms: int = Field(ge=0)
    response: str | None = Field(
        default=None,
        description=(
            "Self-assessment outcome: correct, incorrect, or slow_correct. "
            "Required when answer_text is not provided."
        ),
    )
    answer_text: str | None = Field(
        default=None,
        description=(
            "Raw answer the learner typed or selected.  When provided, "
            "the server grades it against the current item and ignores "
            "response."
        ),
    )


class FeedbackResponse(BaseModel):
    node_id: str
    correct: bool
    response_type: str = Field(
        description="The original response: correct, slow_correct, or incorrect"
    )
    mastery_before: float
    mastery_after: float


class AnswerResponse(BaseModel):
    feedback: FeedbackResponse
    next_question: QuestionResponse | None = None
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
    learning_route: str | None = None
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
    description: str
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
    node_id: str
    title: str
    type: str
    posterior_mastery: float
    easiness_factor: float
    interval_days: float
    repetitions: int
    last_review: str | None = None
    source: str
    item_history: list[ItemHistoryEntry]


# -- Graph visualisation --


class GraphNode(BaseModel):
    id: str
    title: str
    type: str
    language: str
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
    methode: str | None = Field(
        default=None,
        description="Schoolmethode, bijv. 'fortuna', 'pallas'. Indien opgegeven samen met chapter.",
    )
    chapter: str | None = Field(
        default=None,
        description="Laatst behandelde hoofdstuk, bijv. 'h03'.",
    )


class IntakeQuestionResponse(BaseModel):
    node_id: str
    title: str
    description: str
    questions_asked: int
    max_questions: int


class IntakeStartResponse(BaseModel):
    intake_id: str
    question: IntakeQuestionResponse | None = None
    already_completed: bool = False


class IntakeAnswerRequest(BaseModel):
    intake_id: str
    correct: bool


class IntakeAnswerResponse(BaseModel):
    questions_asked: int
    next_question: IntakeQuestionResponse | None = None
    finished: bool = False
    converged: bool = False


# -- Bijspijker mode (M1-03) --


class BijspijkerIntakeRequest(BaseModel):
    methode_lat: str | None = Field(default=None, description="Latijnse methode, bijv. 'fortuna'.")
    hoofdstuk_lat: int | None = Field(default=None, ge=1)
    methode_grc: str | None = Field(default=None, description="Griekse methode, bijv. 'pallas'.")
    hoofdstuk_grc: int | None = Field(default=None, ge=1)
    reset_priors: bool = Field(
        default=True,
        description="True bij eerste intake (zet diagnose-priors). False bij een "
        "hoofdstuk-bump: behoudt bestaande voortgang.",
    )


class BijspijkerIntakeResponse(BaseModel):
    doelset_size: int = Field(description="Aantal knopen in de catch-up-doelset.")
    diagnose_size: int = Field(description="Aantal nog in te halen knopen.")
    eta_dagen: int = Field(description="Schatting dagen tot 'bij' bij 30 min/dag.")
    fractie_bij: float = Field(description="Fractie van de doelset die al groen is.")
    eerste_diagnose_node_ids: list[str] = Field(
        default_factory=list, description="Knopen voor de eerste diagnose-sessie."
    )


class BijspijkerTopic(BaseModel):
    node_id: str
    title_nl: str
    mastery: float


class BijspijkerProgressResponse(BaseModel):
    modus: str
    fractie_bij: float
    is_bij: bool
    doelset_size: int
    diagnose_size: int
    eta_dagen: int
    suggest_chapter_bump: bool
    methode_lat: str | None = None
    hoofdstuk_lat: int | None = None
    methode_grc: str | None = None
    hoofdstuk_grc: int | None = None
    open_topics: list[BijspijkerTopic] = Field(default_factory=list)


# -- User settings --


class UpdateLearningRouteRequest(BaseModel):
    learning_route: str = Field(description="'grammar_first' or 'context_first'")


class UserProfileResponse(BaseModel):
    user_id: str
    email: str
    learning_route: str


class MenteeSummary(BaseModel):
    """One learner linked to the requesting mentor."""

    user_id: str
    email: str


class MenteeListResponse(BaseModel):
    """The mentees assigned to the authenticated mentor."""

    mentees: list[MenteeSummary]


class MentorLearnerProfileResponse(BaseModel):
    """Basic profile of a learner, viewed through the mentor guard."""

    user_id: str
    email: str
    role: str


class MentorAttempt(BaseModel):
    """One concrete wrong/right attempt the learner made on a node (F2-02)."""

    timestamp: str
    item_id: str
    answer_text: str
    correct_answer: str | None
    correct: bool
    response_time_ms: int
    item_type: str | None


class MentorAttemptsResponse(BaseModel):
    """The most recent literal attempts on one node, newest first."""

    user_id: str
    knoop_id: str
    knoop_title: str
    attempts: list[MentorAttempt]


class StruikelpuntEntry(BaseModel):
    """Aggregated difficulty signal for one node (F2-03)."""

    knoop_id: str
    knoop_title: str
    total_attempts: int
    wrong_attempts: int
    error_rate: float
    last_attempt: str | None
    mastery: float


class StruikelpuntenResponse(BaseModel):
    """Per-node stumbling-block overview for one learner, worst first."""

    user_id: str
    struikelpunten: list[StruikelpuntEntry]
