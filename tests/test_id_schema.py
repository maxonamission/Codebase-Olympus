"""Tests for the knowledge node ID schema."""

import pytest

from gymnasium_classica.schemas.id_schema import parse_knoop_id, validate_knoop_id


class TestValidateKnoopId:
    """Tests for validate_knoop_id()."""

    @pytest.mark.parametrize(
        "knoop_id",
        [
            "LAT-G-MORF-NOM-D1",
            "LAT-G-MORF-DECL1-INTRO",
            "LAT-G-SYNT-ACI-INTRO",
            "LAT-G-MORF-PRAES-C1-ACT",
            "GRC-G-FONL-ALFABET",
            "SHA-C-FIL-STOA",
            "LAT-V-F01-ESSE",
            "LAT-I-VERT-PROZA-OB",
            "LAT-G-METR-HEX",
            "GRC-V-F15-EINAI",
        ],
    )
    def test_valid_ids(self, knoop_id: str):
        assert validate_knoop_id(knoop_id) is True

    @pytest.mark.parametrize(
        "knoop_id",
        [
            "",
            "lat-g-morf-nom-d1",  # lowercase
            "LAT-G",  # too few segments
            "LAT-G-MORF-NOM-D1-X-EXTRA-SEG",  # too many segments (>4 tail segs)
            "XXX-G-MORF-NOM",  # invalid language
            "LAT-X-MORF-NOM",  # invalid type
            "LAT-G-MORF-NOM D1",  # space in segment
            "LAT-G-MORF-NAAMVALLEN",  # segment too long (>8 chars)
            "LAT-G-MORF-",  # trailing dash
        ],
    )
    def test_invalid_ids(self, knoop_id: str):
        assert validate_knoop_id(knoop_id) is False


class TestParseKnoopId:
    """Tests for parse_knoop_id()."""

    def test_parse_grammar_id(self):
        result = parse_knoop_id("LAT-G-MORF-NOM-D1")
        assert result["taal"] == "LAT"
        assert result["type"] == "G"
        assert result["segments"] == ["MORF", "NOM", "D1"]

    def test_parse_vocab_id(self):
        result = parse_knoop_id("LAT-V-F01-ESSE")
        assert result["taal"] == "LAT"
        assert result["type"] == "V"
        assert result["segments"] == ["F01", "ESSE"]

    def test_parse_culture_id(self):
        result = parse_knoop_id("SHA-C-FIL-STOA")
        assert result["taal"] == "SHA"
        assert result["type"] == "C"
        assert result["segments"] == ["FIL", "STOA"]

    def test_parse_minimal_id(self):
        result = parse_knoop_id("LAT-G-MORF")
        assert result["segments"] == ["MORF"]

    def test_parse_invalid_raises(self):
        with pytest.raises(ValueError, match="Invalid knoop ID"):
            parse_knoop_id("invalid-id")
