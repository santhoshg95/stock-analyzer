import unittest

import pandas as pd

from src.historical.regime_performance import RegimePerformance


class RegimePerformanceTests(unittest.TestCase):
    def test_reports_current_regime_and_forward_samples(self):
        dates = pd.date_range("2018-01-01", periods=1500, freq="B")
        close = pd.Series(range(1000, 2500), index=dates, dtype=float)
        result = RegimePerformance.analyze(pd.DataFrame({"Close": close}), "BULLISH")
        self.assertEqual(result["regime"], "BULL")
        self.assertGreater(result["sample_count"], 20)
        self.assertEqual(result["win_rate_percent"], 100.0)
