"""Pydantic models for reading passages (leespassages).

A passage is a short Latin or Greek text (2-5 sentences) with per-word
annotations (lemma, case, translation). Each passage is linked to the
grammar and vocabulary nodes it exercises.
"""

from pydantic import BaseModel, Field

from gymnasium_classica.models.graph import Taal


class WordAnnotation(BaseModel):
    """Per-word annotation for a passage."""

    woord: str = Field(description="Surface form as it appears in the text")
    lemma: str = Field(description="Dictionary form (lemma)")
    naamval: str | None = Field(
        default=None,
        description="Grammatical case or form label, e.g. 'nom.sg', 'praes.ind.act.3sg'",
    )
    vertaling: str = Field(description="Dutch translation of this word in context")


class Passage(BaseModel):
    """A reading passage for contextual learning."""

    id: str = Field(description="Unique passage ID, e.g. 'LAT-P-001'")
    taal: Taal
    titel: str = Field(description="Short descriptive title in Dutch")
    tekst: str = Field(description="The Latin/Greek source text")
    annotaties: list[WordAnnotation] = Field(description="Per-word annotations for the passage")
    knoop_ids: list[str] = Field(
        description="IDs of grammar/vocabulary nodes this passage exercises"
    )
    moeilijkheid: int = Field(ge=1, le=5, description="Difficulty level 1-5 (ascending)")


class PassageData(BaseModel):
    """Top-level wrapper for serializing/deserializing a passages JSON file."""

    passages: list[Passage]
