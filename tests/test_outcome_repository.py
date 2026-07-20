import tempfile
import unittest
from pathlib import Path

from src.learning.outcome_repository import OutcomeRepository


class OutcomeRepositoryTests(unittest.TestCase):
    def test_records_and_calibrates_completed_outcomes(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = OutcomeRepository(Path(directory) / "outcomes.json")
            ids = [repository.record_recommendation({"symbol": "SBIN", "strategy": "BUY", "ai_score": 80, "probability": 70}) for _ in range(20)]
            for index, identifier in enumerate(ids):
                self.assertTrue(repository.record_outcome(identifier, won=index < 15))
            self.assertEqual(repository.calibrated_probability("BUY"), 75.0)

    def test_records_and_calibrates_option_strategy_independently(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = OutcomeRepository(Path(directory) / "outcomes.json")
            trade = {
                "symbol": "SBIN", "strategy": "BUY", "ai_score": 80, "probability": 70,
                "short_put_strategy": {
                    "available": True, "strategy": "BULL_PUT_SPREAD", "net_credit": 2.5,
                    "candidate": {"expiry": "2026-08-27", "sold_put_strike": 750,
                                  "delta": -.2, "implied_volatility": 24,
                                  "probability_otm": 80},
                },
            }
            identifiers = [repository.record_recommendation(trade) for _ in range(20)]
            for index, identifier in enumerate(identifiers):
                repository.record_outcome(identifier, won=index < 16)
            self.assertEqual(repository.option_calibrated_probability("BULL_PUT_SPREAD"), 80.0)
