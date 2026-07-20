import tempfile
import unittest
from pathlib import Path

from src.learning.outcome_repository import OutcomeRepository


class HistoricalLearningTests(unittest.TestCase):
    def test_groups_completed_results_by_symbol_setup_and_regime(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = OutcomeRepository(Path(directory) / "outcomes.json")
            trade = {"symbol": "TEST", "strategy": "BUY", "setup": "BULLISH_PULLBACK",
                     "market_context": {"regime": "BULLISH"}, "sector": "BANKING",
                     "recommendation": "BUY", "ai_score": 70, "probability": 65}
            first = repository.record_recommendation(trade)
            second = repository.record_recommendation(trade)
            repository.record_outcome(first, True, 2.0)
            repository.record_outcome(second, False, -1.0)

            summary = repository.learning_summary()

            self.assertEqual(summary["completed_outcomes"], 2)
            self.assertEqual(summary["by_symbol"][0]["win_rate_percent"], 50.0)
            self.assertEqual(summary["by_setup_and_regime"][0]["market_regime"], "BULLISH")
