"""Regression tests for the public final-report workflow."""

import unittest
from unittest.mock import patch

from src.application.platform import TradingPlatform
from src.application.settings import PlatformSettings
from src.presenter.daily_report import DailyReportPresenter


class DailyReportContractTests(unittest.TestCase):
    @patch("src.workflow.daily_trading_assistant.OutcomeRepository")
    def test_cache_report_contains_actionable_trade_fields(self, outcome_repository):
        outcome_repository.return_value.calibrated_probability.return_value = None
        outcome_repository.return_value.record_recommendation.return_value = "test-recommendation"
        platform = TradingPlatform(
            settings=PlatformSettings(market_data_source="cache", capital=100_000, risk_percent=1)
        )
        report = platform.daily_report(limit=1, minimum_score=40)

        self.assertEqual(report["report_type"], "daily_trading_assistant")
        self.assertEqual(len(report["trades"]), 1)
        trade = report["trades"][0]
        self.assertIn("levels", trade)
        self.assertIn("risk", trade)
        self.assertIn("option_strategy", trade)
        self.assertIn("stock_liquidity", trade)
        self.assertIn("trust", trade)
        self.assertIn("TODAY'S MARKET SUMMARY", DailyReportPresenter.render(report))
