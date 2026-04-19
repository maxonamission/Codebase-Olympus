"""Load structured vocabulary metadata from ``data/vocab_sources/``.

Each file in that directory is a list of dicts with the shape::

    {
      "lemma": "sum",
      "id": "SUM",
      "pos": "verb",
      "conj": "irreg",
      "gen": "esse",
      "mean": "zijn",
      "cl": null
    }

The filename encodes ``{taal}_{frequentieband}_words.json`` (e.g.
``lat_f01_words.json``).  The V-knoop ID in the graph is assembled as
``{TAAL}-V-{BAND}-{id}`` (e.g. ``LAT-V-F01-SUM``) so we can build a
direct lookup table keyed on that knoop-ID.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field


class VocabEntry(BaseModel):
    """Structured metadata for a single vocabulary lemma."""

    lemma: str
    id: str = Field(description="Short lemma handle, uppercase, e.g. 'SUM'.")
    pos: str = Field(description="Part of speech: verb, noun, adj, pron, prep, ...")
    conj: str | None = Field(
        default=None,
        description="Conjugation or declension class, e.g. '1', '3b', 'irreg'.",
    )
    gen: str | None = Field(
        default=None,
        description=(
            "Genitive form (nouns/adjectives), stamtijden (verbs) or "
            "prepositional case (prep).  Free-text; see source-JSON."
        ),
    )
    mean: str = Field(description="Dutch translation(s), semicolon-separated.")
    cl: str | None = Field(
        default=None,
        description="Semantisch cluster label, or None.",
    )


def knoop_id_from_file_and_entry(filename: str, entry_id: str) -> str:
    """Compose the V-knoop ID from a vocab-source filename + entry id.

    ``lat_f01_words.json`` + ``SUM`` → ``LAT-V-F01-SUM``.
    """
    stem = filename.rsplit("_words", 1)[0]  # "lat_f01"
    taal, band = stem.split("_", 1)
    return f"{taal.upper()}-V-{band.upper()}-{entry_id}"


def load_vocab_metadata(path: Path) -> dict[str, VocabEntry]:
    """Load every ``*_words.json`` in *path* into a knoop-ID-keyed dict.

    Accepts a directory (loads all files) or a single file.

    Raises:
        FileNotFoundError: when *path* does not exist or the directory
            contains no ``*.json`` files.
        pydantic.ValidationError: when an entry fails schema validation.
        ValueError: when two files produce the same knoop ID.
    """
    if path.is_dir():
        return _load_directory(path)
    return _load_file(path)


def _load_file(file_path: Path) -> dict[str, VocabEntry]:
    with open(file_path, encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        raise ValueError(f"{file_path}: expected a JSON list of vocab entries")
    entries: dict[str, VocabEntry] = {}
    for item in raw:
        entry = VocabEntry(**item)
        knoop_id = knoop_id_from_file_and_entry(file_path.name, entry.id)
        if knoop_id in entries:
            raise ValueError(f"Duplicate vocab entry for {knoop_id!r} in {file_path}")
        entries[knoop_id] = entry
    return entries


def _load_directory(directory: Path) -> dict[str, VocabEntry]:
    files = sorted(directory.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"No .json files found in {directory}")

    merged: dict[str, VocabEntry] = {}
    for f in files:
        for knoop_id, entry in _load_file(f).items():
            if knoop_id in merged:
                raise ValueError(f"Duplicate knoop_id {knoop_id!r} across vocab_sources")
            merged[knoop_id] = entry
    return merged
