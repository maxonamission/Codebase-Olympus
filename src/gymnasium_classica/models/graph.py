"""Pydantic models for the knowledge graph: KennisKnoop, PrerequisiteEdge, Item."""

from enum import StrEnum
from typing import Optional, Union

import re

from pydantic import BaseModel, Field, field_validator

from gymnasium_classica.schemas.id_schema import validate_knoop_id


# --- Enums ---


class Taal(StrEnum):
    LAT = "lat"
    GRC = "grc"
    SHARED = "shared"


class KnoopType(StrEnum):
    G = "G"  # Grammatica
    V = "V"  # Vocabulaire
    C = "C"  # Cultuur
    I = "I"  # Integratie


class BloomNiveau(StrEnum):
    KENNIS = "kennis"
    BEGRIP = "begrip"
    TOEPASSING = "toepassing"
    ANALYSE = "analyse"
    SYNTHESE = "synthese"


class Fase(StrEnum):
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


class Richting(StrEnum):
    RECEPTIEF = "receptief"
    PRODUCTIEF = "productief"


class Bron(StrEnum):
    HANDMATIG = "handmatig"
    LLM_GEGENEREERD = "llm_gegenereerd"
    AUTHENTIEK = "authentiek"


# --- Models ---


class Item(BaseModel):
    """A single exercise item linked to one or more knowledge nodes."""

    id: str
    knoop_ids: list[str]
    type: ItemType
    richting: Richting
    moeilijkheid_initieel: float = Field(description="IRT b-parameter")
    discriminatie_initieel: float = Field(gt=0, description="IRT a-parameter, must be > 0")
    verwachte_tijd_sec: int = Field(gt=0)
    stimulus: Union[str, dict]
    antwoord: Union[str, list[str]]
    feedback: str
    bron: Bron


class KennisKnoop(BaseModel):
    """A single knowledge node (kennisatoom) in the graph."""

    id: str
    type: KnoopType
    taal: Taal
    titel_nl: str
    titel_terminologie: Optional[str] = None
    beschrijving: str = Field(description="Short (1-2 sentences) identifying description")
    bloom_niveau: BloomNiveau
    fase: Fase
    toetsbaar: bool = True
    pensum_jaren: list[int] = Field(default_factory=list)
    cevte_referentie: Optional[str] = None
    content_ref: Optional[str] = Field(
        default=None,
        description="Path to markdown content file in data/content/, e.g. LAT-G-MORF-NOM-D1.md",
    )
    semantisch_cluster: Optional[str] = Field(
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

    knopen: list[KennisKnoop]
    edges: list[PrerequisiteEdge]
