import unittest

import pandas as pd

from src.candlestick.pattern_detector import PatternDetector


class CandlestickPatternTests(unittest.TestCase):
    def test_bullish_engulfing_with_volume_confirmation(self):
        frame = pd.DataFrame([
            {"Open": 110, "Close": 100, "High": 112, "Low": 98, "RVOL": 0.8},
            {"Open": 99, "Close": 113, "High": 114, "Low": 97, "RVOL": 1.8},
        ])
        result = PatternDetector.detect(frame)
        self.assertEqual(result["pattern"], "BULLISH ENGULFING")
        self.assertEqual(result["signal"], "BUY")
        self.assertGreater(result["strength"], 90)
