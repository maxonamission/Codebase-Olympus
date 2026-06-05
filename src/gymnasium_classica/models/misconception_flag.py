"""Result object for misconception detection (M1-02).

A :class:`MisconceptionFlag` carries not just a boolean but the three
aggregate scores and a human-readable reason, so a mentor dashboard or
session summary can explain *why* a profile was (not) detected.
"""

from pydantic import BaseModel, Field


class MisconceptionFlag(BaseModel):
    """Outcome of evaluating one misconception heuristic for a learner."""

    code: str = Field(description='Misconception code, e.g. "LEGO_VERTALEN".')
    active: bool = Field(description="Whether the profile is currently detected.")
    avg_v: float | None = Field(
        default=None,
        description="Mean vocabulary (F01-F02) mastery; None if no data.",
    )
    avg_g_morf: float | None = Field(
        default=None,
        description="Mean morphology-concept mastery; None if no data.",
    )
    avg_i_vert: float | None = Field(
        default=None,
        description="Mean translation-integration mastery; None if no data.",
    )
    reason: str = Field(description="Human-readable explanation of the outcome.")
