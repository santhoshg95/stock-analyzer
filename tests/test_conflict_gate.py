import unittest

from src.workflow.daily_trading_assistant import DailyTradingAssistant


class ConflictGateTests(unittest.TestCase):
    def test_null_option_rejection_is_normalized(self):
        self.assertEqual(DailyTradingAssistant._option_rejection({"rejection": None}), {})

    def test_bearish_pcr_and_negative_headline_exclude_bullish_trade(self):
        result = DailyTradingAssistant._conflict_gate(
            {"action": "BUY ON DIP"},
            {"available": True, "pcr": 0.69, "confidence": 31},
            {"sentiment": "NEUTRAL", "events": [], "headlines": [{"title": "Don't Buy COLPAL"}]},
        )
        self.assertFalse(result["approved"])
        self.assertIn("bearish PCR (0.69)", result["conflicts"])

    def test_oversized_option_lot_does_not_by_itself_reject_stock(self):
        result = DailyTradingAssistant._conflict_gate(
            {"action": "BUY"},
            {"available": False, "pcr": 1.05, "confidence": 60, "reason": "One lot exceeds risk."},
            {"sentiment": "NEUTRAL", "events": [], "headlines": []},
        )
        self.assertTrue(result["approved"])

    def test_option_entry_failure_does_not_reject_stock(self):
        result = DailyTradingAssistant._conflict_gate(
            {"action": "BUY"},
            {"available": False, "entry_validation": {"approved": False,
                                                        "reasons": ["option margin or entry check failed"]}},
            {"sentiment": "NEUTRAL", "events": [], "headlines": []},
        )
        self.assertTrue(result["approved"])
        self.assertIn("option margin or entry check failed", result["conflicts"])
