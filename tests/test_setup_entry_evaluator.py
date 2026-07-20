import unittest
from types import SimpleNamespace

import pandas as pd

from src.decision.setup_entry_evaluator import SetupEntryEvaluator


def frame(confirmed=False):
    rows = []
    lows = [94, 95, 96, 97, 98, 98.5, 99, 99.2]
    for index, low in enumerate(lows):
        rows.append({"Close": 100, "Low": low, "EMA20": 99 if confirmed else 105,
                     "EMA50": 105, "EMA200": 95, "RSI": 29,
                     "MACD": -0.9, "MACD_SIGNAL": -1.0, "MACD_HISTOGRAM": .1,
                     "RVOL": 1.3 if confirmed else .4})
    return pd.DataFrame(rows)


class SetupEntryEvaluatorTests(unittest.TestCase):
    def test_oversold_is_candidate_not_trade(self):
        result = SetupEntryEvaluator.evaluate(
            frame(False), SimpleNamespace(score=65), {"support": 98, "risk_reward": 2},
            {"confirmed": False}, {"signal": "NEUTRAL"},
        )
        self.assertEqual(result["stage_1"]["category"], "REVERSAL CANDIDATE")
        self.assertEqual(result["momentum_label"], "EARLY_REVERSAL")
        self.assertFalse(result["stage_2"]["eligible"])

    def test_reversal_requires_every_confirmation(self):
        result = SetupEntryEvaluator.evaluate(
            frame(True), SimpleNamespace(score=65), {"support": 98, "risk_reward": 2},
            {"confirmed": False}, {"signal": "BUY"},
        )
        self.assertEqual(result["stage_1"]["category"], "REVERSAL CANDIDATE")
        self.assertTrue(result["stage_2"]["eligible"])
        self.assertEqual(result["stage_2"]["missing"], [])
