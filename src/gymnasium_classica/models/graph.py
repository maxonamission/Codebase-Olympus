"""Pydantic models for the knowledge graph: Node, PrerequisiteEdge, Item."""

import re
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator

from gymnasium_classica.schemas.id_schema import validate_knoop_id

# --- Enums ---


class Language(StrEnum):
    LAT = "lat"
    GRC = "grc"
    SHARED = "shared"


class NodeType(StrEnum):
    G = "G"  # Grammatica
    V = "V"  # Vocabulaire
    C = "C"  # Cultuur
    I = "I"  # Integratie  # noqa: E741 - enum uit ID-schema, niet te hernoemen


class BloomLevel(StrEnum):
    KENNIS = "kennis"
    BEGRIP = "begrip"
    TOEPASSING = "toepassing"
    ANALYSE = "analyse"
    SYNTHESE = "synthese"


class Phase(StrEnum):
    ONDERBOUW_1 = "onderbouw_1"
    ONDERBOUW_2 = "onderbouw_2"
    ONDERBOUW_3 = "onderbouw_3"
    BOVENBOUW_4 = "bovenbouw_4"
    BOVENBOUW_5 = "bovenbouw_5"
    BOVENBOUW_6 = "bovenbouw_6"


class EdgeType(StrEnum):
    PREREQUISITE = "prerequisite"
    ENRICHMENT = "enrichment"
    TRANSFER = "transfer"


class ItemType(StrEnum):
    HERKENNING = "herkenning"
    PRODUCTIE = "productie"
    ANALYSE = "analyse"
    SYNTHESE = "synthese"
    CONTEXTUEEL = "contextueel"
    OFFLINE_SCHRIJVEN = "offline_schrijven"
    LUISTER_HERKENNING = "luister_herkenning"
    LUISTER_PRODUCTIE = "luister_productie"


class VerificationMethod(StrEnum):
    SELF_REPORT = "self_report"
    OCR = "ocr"
    MENTOR_REVIEW = "mentor_review"


class Direction(StrEnum):
    RECEPTIEF = "receptief"
    PRODUCTIEF = "productief"


class Source(StrEnum):
    HANDMATIG = "handmatig"
    LLM_GEGENEREERD = "llm_gegenereerd"
    AUTHENTIEK = "authentiek"


# --- Models ---


class Item(BaseModel):
    """A single exercise item linked to one or more knowledge nodes."""

    id: str
    knoop_ids: list[str]
    type: ItemType
    richting: Direction
    moeilijkheid_initieel: float = Field(description="IRT b-parameter")
    discriminatie_initieel: float = Field(gt=0, description="IRT a-parameter, must be > 0")
    verwachte_tijd_sec: int = Field(gt=0)
    stimulus: str | dict[str, Any]
    antwoord: str | list[str]
    feedback: str
    bron: Source
    audio_ref: str | None = Field(
        default=None,
        description="Path to audio file in data/audio/, e.g. LAT-V-F01-ESSE.mp3",
    )
    verificatie_methode: VerificationMethod | None = Field(
        default=None,
        description="For offline_schrijven items: how the result is verified.",
    )
    verwacht_resultaat: str | None = Field(
        default=None,
        description="For offline_schrijven items: the expected written result (paradigm, translation, etc.).",
    )


class Node(BaseModel):
    """A single knowledge node (kennisatoom) in the graph."""

    id: str
    type: NodeType
    taal: Language
    titel_nl: str
    titel_terminologie: str | None = None
    beschrijving: str = Field(description="Short (1-2 sentences) identifying description")
    bloom_niveau: BloomLevel
    fase: Phase
    toetsbaar: bool = True
    pensum_jaren: list[int] = Field(default_factory=list)
    cevte_referentie: str | None = None
    content_ref: str | None = Field(
        default=None,
        description="Path to markdown content file in data/content/, e.g. LAT-G-MORF-NOM-D1.md",
    )
    pronunciation: str | None = Field(
        default=None,
        description="IPA phonetic transcription of the lemma/title, e.g. /pu.ˈel.la/",
    )
    semantisch_cluster: str | None = Field(
        default=None,
        description=(
            "Semantic cluster label for vocabulary nodes (type V). "
            "Lowercase alphanumeric, max 20 chars. Used by the scheduling engine "
            "for non-interference: items from the same cluster are spread apart."
        ),
    )
    items: list[Item] = Field(default_factory=list)

    @field_validator("semantisch_cluster")
    @classmethod
    def check_cluster_format(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not re.fullmatch(r"[a-z0-9_]{1,20}", v):
            raise ValueError(
                f"Invalid semantisch_cluster {v!r}. "
                "Must be lowercase alphanumeric/underscore, 1-20 chars."
            )
        return v

    @field_validator("id")
    @classmethod
    def check_id_format(cls, v: str) -> str:
        if not validate_knoop_id(v):
            raise ValueError(
                f"Invalid knoop ID {v!r}. "
                "Expected format: {{TAAL}}-{{TYPE}}-{{SEGMENT}}[-{{SEGMENT}}]... "
                "e.g. LAT-G-MORF-NOM-D1"
            )
        return v


class PrerequisiteEdge(BaseModel):
    """A directed edge between two knowledge nodes."""

    source_id: str
    target_id: str
    type: EdgeType
    encompassing_weight: float = Field(ge=0.0, le=1.0)


class GraphData(BaseModel):
    """Top-level wrapper for serializing/deserializing a knowledge graph JSON file."""

    knopen: list[Node]
    edges: list[PrerequisiteEdge]
