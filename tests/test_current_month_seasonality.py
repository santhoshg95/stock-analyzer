import unittest
from datetime import date

import pandas as pd

from src.historical.current_month_seasonality import CurrentMonthSeasonality


class CurrentMonthSeasonalityTests(unittest.TestCase):
    def test_compares_current_mtd_with_same_month_history(self):
        dates = pd.date_range("2016-12-31", "2026-06-30", freq="ME")
        values, close = [], 100.0
        for item in dates:
            if item.month == 7:
                close *= 1.10
            values.append(close)
        df = pd.DataFrame({"Close": values}, index=dates)
        df.loc[pd.Timestamp("2026-07-20"), "Close"] = close * 1.05

        result = CurrentMonthSeasonality.analyze(df, as_of=date(2026, 7, 20))

        self.assertEqual(result["month_name"], "JULY")
        self.assertEqual(result["sample_years"], 9)
        self.assertEqual(result["sample_quality"], "ROBUST")
        self.assertAlmostEqual(result["average_return_percent"], 10.0)
        self.assertAlmostEqual(result["current_mtd_return_percent"], 5.0)
        self.assertEqual(result["versus_history"], "UNDERPERFORMING")

    def test_short_history_is_labelled_insufficient(self):
        df = pd.DataFrame({"Date": ["2025-06-30", "2025-07-31"], "Close": [100, 105]})
        result = CurrentMonthSeasonality.analyze(df, as_of=date(2026, 7, 20))
        self.assertEqual(result["sample_quality"], "INSUFFICIENT")
