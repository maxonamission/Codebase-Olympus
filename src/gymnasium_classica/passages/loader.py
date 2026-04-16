"""Load reading passages from JSON files in data/passages/."""

import json
from pathlib import Path

from gymnasium_classica.models.passage import Passage, PassageData


def load_passages(path: Path) -> list[Passage]:
    """Load passages from a JSON file or a directory of JSON files.

    When *path* is a file, it must contain a top-level key "passages".
    When *path* is a directory, all ``*.json`` files in it are loaded
    and merged into a single list.

    Returns:
        A list of validated Passage instances.

    Raises:
        FileNotFoundError: if *path* does not exist or directory is empty.
        json.JSONDecodeError: if any file is not valid JSON.
        pydantic.ValidationError: if any passage fails schema validation.
    """
    if path.is_dir():
        return _load_passages_directory(path)
    return _load_passages_file(path)


def _normalize_passage(raw: dict) -> dict:
    """Normalize a passage dict to match the Passage model schema.

    Handles alternative field names from different generation sessions:
    - titel_nl → titel
    - zinnen → tekst (joined)
    - niveau → moeilijkheid
    - complexiteit_label → ignored
    """
    if "titel" in raw and "taal" in raw and "tekst" in raw:
        return raw  # Already in correct format

    normalized = {"id": raw["id"], "knoop_ids": raw.get("knoop_ids", [])}

    # Title
    normalized["titel"] = raw.get("titel", raw.get("titel_nl", ""))

    # Language: infer from ID prefix
    pid = raw["id"]
    if pid.startswith("GRC"):
        normalized["taal"] = "grc"
    elif pid.startswith("LAT"):
        normalized["taal"] = "lat"
    else:
        normalized["taal"] = raw.get("taal", "lat")

    # Text: join zinnen if present
    if "tekst" in raw:
        normalized["tekst"] = raw["tekst"]
    elif "zinnen" in raw:
        zinnen = raw["zinnen"]
        if isinstance(zinnen, list):
            parts = []
            for z in zinnen:
                if isinstance(z, dict):
                    parts.append(z.get("latijn", z.get("grieks", z.get("tekst", ""))))
                else:
                    parts.append(str(z))
            normalized["tekst"] = " ".join(parts)
        else:
            normalized["tekst"] = str(zinnen)
    else:
        normalized["tekst"] = ""

    # Annotations: build from zinnen if available
    if "annotaties" in raw:
        normalized["annotaties"] = raw["annotaties"]
    elif "zinnen" in raw and isinstance(raw["zinnen"], list):
        annotations = []
        for z in raw["zinnen"]:
            if isinstance(z, dict) and "woorden" in z:
                for w in z["woorden"]:
                    annotations.append({
                        "woord": w.get("woord", w.get("vorm", "")),
                        "lemma": w.get("lemma", w.get("woord", "")),
                        "naamval": w.get("naamval", w.get("functie", None)),
                        "vertaling": w.get("vertaling", w.get("nl", "")),
                    })
        normalized["annotaties"] = annotations if annotations else [
            {"woord": "—", "lemma": "—", "vertaling": "—"}
        ]
    else:
        normalized["annotaties"] = [{"woord": "—", "lemma": "—", "vertaling": "—"}]

    # Difficulty
    normalized["moeilijkheid"] = raw.get("moeilijkheid", raw.get("niveau", 1))
    if not isinstance(normalized["moeilijkheid"], int):
        normalized["moeilijkheid"] = 1
    normalized["moeilijkheid"] = max(1, min(5, normalized["moeilijkheid"]))

    return normalized


def _load_passages_file(file_path: Path) -> list[Passage]:
    """Load passages from a single JSON file."""
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    # Normalize each passage before validation
    normalized = [_normalize_passage(p) for p in data.get("passages", [])]
    parsed = PassageData(passages=normalized)
    return parsed.passages


def _load_passages_directory(directory: Path) -> list[Passage]:
    """Load and merge all JSON passage files in *directory*."""
    json_files = sorted(directory.glob("*.json"))
    if not json_files:
        raise FileNotFoundError(f"No .json files found in {directory}")

    all_passages: list[Passage] = []
    seen_ids: set[str] = set()

    for file_path in json_files:
        passages = _load_passages_file(file_path)
        for p in passages:
            if p.id in seen_ids:
                raise ValueError(
                    f"Duplicate passage ID {p.id!r} found in {file_path}"
                )
            seen_ids.add(p.id)
            all_passages.append(p)

    return all_passages
