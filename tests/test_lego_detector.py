"""Tests for the Lego-vertaler detection heuristic (M1-02)."""

from uuid import uuid4

from gymnasium_classica.models.learner import LearnerModel, NodeState
from gymnasium_classica.scheduling.misconceptie_detectie import (
    DEFAULT_LEGO_CONFIG,
    LegoDetectorConfig,
    detect_lego_translator,
    evaluate_lego_translator,
)


def make_learner(masteries: dict[str, float]) -> LearnerModel:
    return LearnerModel(
        user_id=uuid4(),
        node_states={
            node_id: NodeState(node_id=node_id, posterior_mastery=m)
            for node_id, m in masteries.items()
        },
    )


# Vocabulary high, morphology low, translation low -> classic Lego profile.
PROFILE = {
    "LAT-V-F01-ESSE": 0.85,
    "LAT-V-F02-AMARE": 0.80,
    "LAT-G-MORF-NAAMVAL-INTRO": 0.40,
    "LAT-G-MORF-CONJ-INTRO": 0.30,
    "LAT-I-VERT-NAAMVAL": 0.30,
    "GRC-I-VERT-NAAMVAL": 0.25,
}


class TestDetectLegoTranslator:
    def test_profile_detected(self):
        assert detect_lego_translator(make_learner(PROFILE)) is True

    def test_flag_carries_scores_and_reason(self):
        flag = evaluate_lego_translator(make_learner(PROFILE))
        assert flag.code == "LEGO_VERTALEN"
        assert flag.active is True
        assert flag.avg_v is not None and flag.avg_v >= 0.70
        assert flag.avg_g_morf is not None and flag.avg_g_morf < 0.50
        assert flag.avg_i_vert is not None and flag.avg_i_vert < 0.40
        assert "Lego-vertaler" in flag.reason

    def test_weak_everywhere_not_detected(self):
        learner = make_learner(
            {
                "LAT-V-F01-ESSE": 0.40,
                "LAT-G-MORF-NAAMVAL-INTRO": 0.40,
                "LAT-I-VERT-NAAMVAL": 0.30,
            }
        )
        flag = evaluate_lego_translator(learner)
        assert flag.active is False
        assert "woordenschat" in flag.reason.lower()

    def test_strong_everywhere_not_detected(self):
        learner = make_learner(
            {
                "LAT-V-F01-ESSE": 0.90,
                "LAT-G-MORF-NAAMVAL-INTRO": 0.85,
                "LAT-I-VERT-NAAMVAL": 0.82,
            }
        )
        flag = evaluate_lego_translator(learner)
        assert flag.active is False
        assert "morfologie" in flag.reason.lower()

    def test_insufficient_data_not_detected(self):
        # Only vocabulary observed; no morphology or translation states.
        learner = make_learner({"LAT-V-F01-ESSE": 0.90})
        flag = evaluate_lego_translator(learner)
        assert flag.active is False
        assert "onvoldoende" in flag.reason.lower()


class TestThresholdBoundaries:
    def _learner(self, v: float, g: float, i: float) -> LearnerModel:
        return make_learner(
            {
                "LAT-V-F01-ESSE": v,
                "LAT-G-MORF-NAAMVAL-INTRO": g,
                "LAT-I-VERT-NAAMVAL": i,
            }
        )

    def test_v_exactly_at_threshold_is_inclusive(self):
        # avg_v >= 0.70 -> 0.70 should still qualify
        assert detect_lego_translator(self._learner(0.70, 0.30, 0.30)) is True

    def test_v_just_below_threshold_fails(self):
        assert detect_lego_translator(self._learner(0.69, 0.30, 0.30)) is False

    def test_g_exactly_at_threshold_fails(self):
        # avg_g_morf < 0.50 -> 0.50 must NOT qualify
        assert detect_lego_translator(self._learner(0.90, 0.50, 0.30)) is False

    def test_g_just_below_threshold_qualifies(self):
        assert detect_lego_translator(self._learner(0.90, 0.499, 0.30)) is True

    def test_i_exactly_at_threshold_fails(self):
        assert detect_lego_translator(self._learner(0.90, 0.30, 0.40)) is False

    def test_i_just_below_threshold_qualifies(self):
        assert detect_lego_translator(self._learner(0.90, 0.30, 0.399)) is True


class TestConfigurableThresholds:
    def test_custom_config_changes_outcome(self):
        learner = make_learner(
            {
                "LAT-V-F01-ESSE": 0.60,
                "LAT-G-MORF-NAAMVAL-INTRO": 0.30,
                "LAT-I-VERT-NAAMVAL": 0.30,
            }
        )
        # Default requires V >= 0.70 -> not active.
        assert detect_lego_translator(learner, DEFAULT_LEGO_CONFIG) is False
        # Relaxed vocabulary threshold -> now active.
        relaxed = LegoDetectorConfig(min_avg_v=0.55)
        assert detect_lego_translator(learner, relaxed) is True
