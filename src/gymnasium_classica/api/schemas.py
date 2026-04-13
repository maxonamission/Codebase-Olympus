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


class QuestionResponse(BaseModel):
    knoop_id: str
    titel: str
    beschrijving: str
    stimulus: str | dict
    phase: str
    items: list[ItemInfo] = Field(default_factory=list)


class StartSessionResponse(BaseModel):
    session_id: str
    question: Optional[QuestionResponse] = None


class AnswerRequest(BaseModel):
    session_id: str
    response: str = Field(description="correct, incorrect, or slow_correct")
    response_time_ms: int = Field(ge=0)


class FeedbackResponse(BaseModel):
    knoop_id: str
    correct: bool
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
