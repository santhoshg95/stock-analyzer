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
