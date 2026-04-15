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
            woord="puellam", lemma="puella", naamval="acc.sg", vertaling="het meisje"
        )
        assert wa.woord == "puellam"
        assert wa.lemma == "puella"
        assert wa.naamval == "acc.sg"
        assert wa.vertaling == "het meisje"

    def test_naamval_optional(self):
        wa = WordAnnotation(woord="in", lemma="in", vertaling="in")
        assert wa.naamval is None

    def test_naamval_explicit_none(self):
        wa = WordAnnotation(woord="et", lemma="et", naamval=None, vertaling="en")
        assert wa.naamval is None


# --- Passage model tests ---


class TestPassage:
    def test_basic_construction(self):
        p = Passage(
            id="LAT-P-001",
            taal="lat",
            titel="Testpassage",
            tekst="Puella aquam portat.",
            annotaties=[
                WordAnnotation(
                    woord="Puella", lemma="puella", naamval="nom.sg", vertaling="het meisje"
                ),
                WordAnnotation(
                    woord="aquam", lemma="aqua", naamval="acc.sg", vertaling="water"
                ),
                WordAnnotation(
                    woord="portat", lemma="portare", naamval="praes.ind.act.3sg", vertaling="draagt"
                ),
            ],
            knoop_ids=["LAT-G-MORF-NOM-D1", "LAT-G-MORF-ACC-D1"],
            moeilijkheid=1,
        )
        assert p.id == "LAT-P-001"
        assert p.taal == "lat"
        assert len(p.annotaties) == 3
        assert len(p.knoop_ids) == 2
        assert p.moeilijkheid == 1

    def test_moeilijkheid_range(self):
        """Difficulty must be 1-5."""
        base = dict(
            id="LAT-P-001",
            taal="lat",
            titel="Test",
            tekst="Puella.",
            annotaties=[],
            knoop_ids=[],
        )
        for level in [1, 2, 3, 4, 5]:
            p = Passage(**base, moeilijkheid=level)
            assert p.moeilijkheid == level

    def test_moeilijkheid_too_low(self):
        with pytest.raises(ValidationError):
            Passage(
                id="LAT-P-001",
                taal="lat",
                titel="Test",
                tekst="Puella.",
                annotaties=[],
                knoop_ids=[],
                moeilijkheid=0,
            )

    def test_moeilijkheid_too_high(self):
        with pytest.raises(ValidationError):
            Passage(
                id="LAT-P-001",
                taal="lat",
                titel="Test",
                tekst="Puella.",
                annotaties=[],
                knoop_ids=[],
                moeilijkheid=6,
            )

    def test_taal_validation(self):
        with pytest.raises(ValidationError):
            Passage(
                id="LAT-P-001",
                taal="frc",  # invalid
                titel="Test",
                tekst="Puella.",
                annotaties=[],
                knoop_ids=[],
                moeilijkheid=1,
            )

    def test_serialization_roundtrip(self):
        p = Passage(
            id="LAT-P-001",
            taal="lat",
            titel="Test",
            tekst="Puella aquam portat.",
            annotaties=[
                WordAnnotation(woord="Puella", lemma="puella", naamval="nom.sg", vertaling="het meisje"),
            ],
            knoop_ids=["LAT-G-MORF-NOM-D1"],
            moeilijkheid=2,
        )
        dumped = p.model_dump()
        p2 = Passage(**dumped)
        assert p2.id == p.id
        assert p2.annotaties[0].lemma == "puella"


# --- PassageData tests ---


class TestPassageData:
    def test_wraps_passages(self):
        pd = PassageData(
            passages=[
                Passage(
                    id="LAT-P-001",
                    taal="lat",
                    titel="Test",
                    tekst="Puella.",
                    annotaties=[],
                    knoop_ids=[],
                    moeilijkheid=1,
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
                "taal": "lat",
                "titel": "Test 1",
                "tekst": "Puella cantat.",
                "annotaties": [
                    {"woord": "Puella", "lemma": "puella", "naamval": "nom.sg", "vertaling": "het meisje"},
                    {"woord": "cantat", "lemma": "cantare", "naamval": "praes.ind.act.3sg", "vertaling": "zingt"},
                ],
                "knoop_ids": ["LAT-G-MORF-NOM-D1"],
                "moeilijkheid": 1,
            }
        ]
    }
    f1 = tmp_path / "file1.json"
    f1.write_text(json.dumps(data), encoding="utf-8")

    data2 = {
        "passages": [
            {
                "id": "LAT-P-T02",
                "taal": "lat",
                "titel": "Test 2",
                "tekst": "Miles pugnat.",
                "annotaties": [
                    {"woord": "Miles", "lemma": "miles", "naamval": "nom.sg", "vertaling": "de soldaat"},
                    {"woord": "pugnat", "lemma": "pugnare", "naamval": "praes.ind.act.3sg", "vertaling": "vecht"},
                ],
                "knoop_ids": ["LAT-G-MORF-NOM-D3"],
                "moeilijkheid": 2,
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
        assert passages[0].taal == "lat"

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
                    "taal": "lat",
                    "titel": "Dup",
                    "tekst": "Dup.",
                    "annotaties": [],
                    "knoop_ids": [],
                    "moeilijkheid": 1,
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
            assert p.moeilijkheid >= 1
            assert p.moeilijkheid <= 5
            assert len(p.tekst) > 0

    def test_annotaties_preserved(self, passages_dir: Path):
        passages = load_passages(passages_dir / "file1.json")
        p = passages[0]
        assert len(p.annotaties) == 2
        assert p.annotaties[0].woord == "Puella"
        assert p.annotaties[0].lemma == "puella"
        assert p.annotaties[1].vertaling == "zingt"
