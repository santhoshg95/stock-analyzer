import unittest
from types import SimpleNamespace

from src.application.platform import TradingPlatform
from src.options.services.strategy_selector import OptionStrategySelector


class OptionDirectionTests(unittest.TestCase):
    def test_bullish_watch_is_not_mapped_to_bearish(self):
        candidate = {
            "action": "WATCH",
            "analysis_report": {"analysis": {"trend": "STRONG BULLISH"}},
        }
        self.assertEqual(TradingPlatform._option_direction(candidate), "BULLISH")

    def test_bullish_direction_never_returns_bearish_strategy(self):
        selector = OptionStrategySelector()
        pcr = SimpleNamespace(sentiment="BEARISH")
        greeks = SimpleNamespace()
        for iv_status in ("LOW", "HIGH", "VERY_HIGH"):
            strategy = selector.select(
                pcr, SimpleNamespace(status=iv_status), greeks, direction="BULLISH"
            )
            self.assertIn(strategy, {"Cash Secured Put", "Bull Put Spread"})
            self.assertNotIn("Bear", strategy)

    def test_strong_bullish_direction_is_normalized_by_selector(self):
        selector = OptionStrategySelector()
        strategy = selector.select(
            SimpleNamespace(sentiment="BEARISH"),
            SimpleNamespace(status="LOW"),
            SimpleNamespace(),
            direction="STRONG_BULLISH",
        )
        self.assertEqual(strategy, "Cash Secured Put")


if __name__ == "__main__":
    unittest.main()
