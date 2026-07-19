"""
Gap Statistics Calculator

Calculates opening gap statistics.

Author:
    AI Research Platform
"""

from __future__ import annotations

import pandas as pd


class GapCalculator:

    # -----------------------------------------------------

    def calculate(
        self,
        df: pd.DataFrame,
    ) -> dict:

        data = df.copy()

        previous_close = data["Close"].shift(1)

        gaps = (
            data["Open"] - previous_close
        ) / previous_close

        gaps = gaps.dropna()

        gap_up = gaps[gaps > 0]

        gap_down = gaps[gaps < 0]

        return {

            "average_gap": float(
                gaps.mean()
            ),

            "average_gap_up": float(
                gap_up.mean()
            ) if not gap_up.empty else 0.0,

            "average_gap_down": float(
                gap_down.mean()
            ) if not gap_down.empty else 0.0,

            "largest_gap_up": float(
                gap_up.max()
            ) if not gap_up.empty else 0.0,

            "largest_gap_down": float(
                gap_down.min()
            ) if not gap_down.empty else 0.0,

            "gap_up_frequency": float(
                len(gap_up) / len(gaps)
            ),

            "gap_down_frequency": float(
                len(gap_down) / len(gaps)
            ),

            "gap_score": self.score(gaps),
        }

    # -----------------------------------------------------

    @staticmethod
    def score(
        gaps: pd.Series,
    ) -> float:

        average_gap = abs(
            gaps.mean()
        )

        if average_gap <= 0.002:
            return 100

        if average_gap <= 0.004:
            return 90

        if average_gap <= 0.006:
            return 80

        if average_gap <= 0.01:
            return 70

        if average_gap <= 0.015:
            return 55

        if average_gap <= 0.02:
            return 40

        return 20

    # -----------------------------------------------------

    @staticmethod
    def classify(
        average_gap: float,
    ) -> str:

        gap = abs(average_gap)

        if gap <= 0.003:
            return "LOW"

        if gap <= 0.008:
            return "MEDIUM"

        return "HIGH"