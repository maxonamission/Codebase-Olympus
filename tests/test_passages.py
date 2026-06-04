"""Tests for Passage model and passage loader (E7-02)."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from gymnasium_classica.models.passage import Passage, PassageData, WordAnnotation
from gymnasium_classica.passages.loader import load_passages

# --- WordAnnotation tests ---


class TestWordAnnotation:
    def test_basic_construction(self):
        wa = WordAnnotation(
            word="puellam", lemma="puella", case="acc.sg", translation="het meisje"
        )
        assert wa.word == "puellam"
        assert wa.lemma == "puella"
        assert wa.case == "acc.sg"
        assert wa.translation == "het meisje"

    def test_naamval_optional(self):
        wa = WordAnnotation(word="in", lemma="in", translation="in")
        assert wa.case is None

    def test_naamval_explicit_none(self):
        wa = WordAnnotation(word="et", lemma="et", case=None, translation="en")
        assert wa.case is None


# --- Passage model tests ---


class TestPassage:
    def test_basic_construction(self):
        p = Passage(
            id="LAT-P-001",
            language="lat",
            title="Testpassage",
            text="Puella aquam portat.",
            annotations=[
                WordAnnotation(
                    word="Puella", lemma="puella", case="nom.sg", translation="het meisje"
                ),
                WordAnnotation(word="aquam", lemma="aqua", case="acc.sg", translation="water"),
                WordAnnotation(
                    word="portat",
                    lemma="portare",
                    case="praes.ind.act.3sg",
                    translation="draagt",
                ),
            ],
            node_ids=["LAT-G-MORF-NOM-D1", "LAT-G-MORF-ACC-D1"],
            difficulty=1,
        )
        assert p.id == "LAT-P-001"
        assert p.language == "lat"
        assert len(p.annotations) == 3
        assert len(p.node_ids) == 2
        assert p.difficulty == 1

    def test_moeilijkheid_range(self):
        """Difficulty must be 1-5."""
        base = dict(
            id="LAT-P-001",
            language="lat",
            title="Test",
            text="Puella.",
            annotations=[],
            node_ids=[],
        )
        for level in [1, 2, 3, 4, 5]:
            p = Passage(**base, difficulty=level)
            assert p.difficulty == level

    def test_moeilijkheid_too_low(self):
        with pytest.raises(ValidationError):
            Passage(
                id="LAT-P-001",
                language="lat",
                title="Test",
                text="Puella.",
                annotations=[],
                node_ids=[],
                difficulty=0,
            )

    def test_moeilijkheid_too_high(self):
        with pytest.raises(ValidationError):
            Passage(
                id="LAT-P-001",
                language="lat",
                title="Test",
                text="Puella.",
                annotations=[],
                node_ids=[],
                difficulty=6,
            )

    def test_taal_validation(self):
        with pytest.raises(ValidationError):
            Passage(
                id="LAT-P-001",
                language="frc",  # invalid
                title="Test",
                text="Puella.",
                annotations=[],
                node_ids=[],
                difficulty=1,
            )

    def test_serialization_roundtrip(self):
        p = Passage(
            id="LAT-P-001",
            language="lat",
            title="Test",
            text="Puella aquam portat.",
            annotations=[
                WordAnnotation(
                    word="Puella", lemma="puella", case="nom.sg", translation="het meisje"
                ),
            ],
            node_ids=["LAT-G-MORF-NOM-D1"],
            difficulty=2,
        )
        dumped = p.model_dump()
        p2 = Passage(**dumped)
        assert p2.id == p.id
        assert p2.annotations[0].lemma == "puella"


# --- PassageData tests ---


class TestPassageData:
    def test_wraps_passages(self):
        pd = PassageData(
            passages=[
                Passage(
                    id="LAT-P-001",
                    language="lat",
                    title="Test",
                    text="Puella.",
                    annotations=[],
                    node_ids=[],
                    difficulty=1,
                )
            ]
        )
        assert len(pd.passages) == 1

    def test_empty_list_allowed(self):
        pd = PassageData(passages=[])
        assert len(pd.passages) == 0


# --- Loader tests ---


@pytest.fixture
def passages_dir(tmp_path: Path) -> Path:
    """Create a temp directory with passage JSON files."""
    data = {
        "passages": [
            {
                "id": "LAT-P-T01",
                "language": "lat",
                "title": "Test 1",
                "text": "Puella cantat.",
                "annotations": [
                    {
                        "word": "Puella",
                        "lemma": "puella",
                        "case": "nom.sg",
                        "translation": "het meisje",
                    },
                    {
                        "word": "cantat",
                        "lemma": "cantare",
                        "case": "praes.ind.act.3sg",
                        "translation": "zingt",
                    },
                ],
                "node_ids": ["LAT-G-MORF-NOM-D1"],
                "difficulty": 1,
            }
        ]
    }
    f1 = tmp_path / "file1.json"
    f1.write_text(json.dumps(data), encoding="utf-8")

    data2 = {
        "passages": [
            {
                "id": "LAT-P-T02",
                "language": "lat",
                "title": "Test 2",
                "text": "Miles pugnat.",
                "annotations": [
                    {
                        "word": "Miles",
                        "lemma": "miles",
                        "case": "nom.sg",
                        "translation": "de soldaat",
                    },
                    {
                        "word": "pugnat",
                        "lemma": "pugnare",
                        "case": "praes.ind.act.3sg",
                        "translation": "vecht",
                    },
                ],
                "node_ids": ["LAT-G-MORF-NOM-D3"],
                "difficulty": 2,
            }
        ]
    }
    f2 = tmp_path / "file2.json"
    f2.write_text(json.dumps(data2), encoding="utf-8")

    return tmp_path


class TestPassageLoader:
    def test_load_single_file(self, passages_dir: Path):
        passages = load_passages(passages_dir / "file1.json")
        assert len(passages) == 1
        assert passages[0].id == "LAT-P-T01"
        assert passages[0].language == "lat"

    def test_load_directory(self, passages_dir: Path):
        passages = load_passages(passages_dir)
        assert len(passages) == 2
        ids = {p.id for p in passages}
        assert ids == {"LAT-P-T01", "LAT-P-T02"}

    def test_empty_directory_raises(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            load_passages(tmp_path)

    def test_duplicate_id_raises(self, passages_dir: Path):
        """Duplicate IDs across files should raise ValueError."""
        dup = {
            "passages": [
                {
                    "id": "LAT-P-T01",  # duplicate
                    "language": "lat",
                    "title": "Dup",
                    "text": "Dup.",
                    "annotations": [],
                    "node_ids": [],
                    "difficulty": 1,
                }
            ]
        }
        (passages_dir / "file3_dup.json").write_text(json.dumps(dup), encoding="utf-8")
        with pytest.raises(ValueError, match="Duplicate passage ID"):
            load_passages(passages_dir)

    def test_load_real_data(self):
        """Load the actual sample data in data/passages/."""
        data_dir = Path(__file__).parent.parent / "data" / "passages"
        if not data_dir.exists():
            pytest.skip("data/passages/ not found")
        passages = load_passages(data_dir)
        assert len(passages) >= 1
        for p in passages:
            assert p.difficulty >= 1
            assert p.difficulty <= 5
            assert len(p.text) > 0

    def test_annotaties_preserved(self, passages_dir: Path):
        passages = load_passages(passages_dir / "file1.json")
        p = passages[0]
        assert len(p.annotations) == 2
        assert p.annotations[0].word == "Puella"
        assert p.annotations[0].lemma == "puella"
        assert p.annotations[1].translation == "zingt"
