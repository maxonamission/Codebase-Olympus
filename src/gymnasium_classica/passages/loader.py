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


def _load_passages_file(file_path: Path) -> list[Passage]:
    """Load passages from a single JSON file."""
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    parsed = PassageData(**data)
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
                raise ValueError(f"Duplicate passage ID {p.id!r} found in {file_path}")
            seen_ids.add(p.id)
            all_passages.append(p)

    return all_passages
