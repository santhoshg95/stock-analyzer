import unittest

from src.workflow.decision_policy import (
    classify_setup, market_alignment, normalize_market_regime,
    option_confidence_status, pcr_adjustment,
    market_risk_scale,
)


class DecisionPolicyTests(unittest.TestCase):
    def test_low_confidence_strong_bearish_is_uncertain(self):
        self.assertEqual(normalize_market_regime("STRONG_BEARISH", 40), "UNCERTAIN_BEARISH")
        self.assertEqual(market_alignment("UNCERTAIN_BEARISH", 40, "BULLISH")["status"], "UNCERTAIN")

    def test_pcr_is_a_bounded_score_adjustment(self):
        self.assertEqual(pcr_adjustment(.52, "BULLISH"), -7)
        self.assertEqual(pcr_adjustment(.52, "BEARISH"), 6)

    def test_option_confidence_tiers(self):
        self.assertEqual(option_confidence_status(70), "CONFIRMED")
        self.assertEqual(option_confidence_status(40), "CONFLICT")
        self.assertEqual(option_confidence_status(20), "UNRELIABLE")

    def test_pullback_classification(self):
        self.assertEqual(classify_setup("STRONG_BULLISH", "BEARISH"), "BULLISH_PULLBACK")

    def test_low_market_confidence_halves_risk(self):
        self.assertEqual(market_risk_scale(20), .5)
        self.assertEqual(market_risk_scale(60), .75)
        self.assertEqual(market_risk_scale(80), 1.0)
        self.assertEqual(market_risk_scale(0, available=False), 1.0)
