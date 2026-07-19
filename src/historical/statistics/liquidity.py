"""
Liquidity Calculator

Calculates liquidity, trading activity and volume metrics.

Author:
    AI Research Platform
"""

from __future__ import annotations

import pandas as pd


class LiquidityCalculator:

    # -----------------------------------------------------

    def calculate(
        self,
        df: pd.DataFrame,
    ) -> dict:

        data = df.copy()

        avg_volume = float(
            data["Volume"].mean()
        )

        median_volume = float(
            data["Volume"].median()
        )

        max_volume = float(
            data["Volume"].max()
        )

        min_volume = float(
            data["Volume"].min()
        )

        volume_std = float(
            data["Volume"].std()
        )

        traded_value = (
            data["Close"]
            * data["Volume"]
        )

        average_traded_value = float(
            traded_value.mean()
        )

        latest_volume = float(
            data["Volume"].iloc[-1]
        )

        average_20 = float(
            data["Volume"]
            .tail(20)
            .mean()
        )

        relative_volume = (
            latest_volume / average_20
            if average_20 > 0
            else 0.0
        )

        turnover_ratio = (
            volume_std / avg_volume
            if avg_volume > 0
            else 0.0
        )

        return {

            "average_volume": avg_volume,

            "median_volume": median_volume,

            "maximum_volume": max_volume,

            "minimum_volume": min_volume,

            "volume_standard_deviation": volume_std,

            "average_traded_value": average_traded_value,

            "latest_volume": latest_volume,

            "relative_volume": float(
                relative_volume
            ),

            "turnover_ratio": float(
                turnover_ratio
            ),

            "liquidity_score": self.score(
                average_traded_value,
                relative_volume,
            ),
        }

    # -----------------------------------------------------

    @staticmethod
    def score(
        traded_value: float,
        relative_volume: float,
    ) -> float:

        score = 0.0

        # Daily traded value
        if traded_value >= 500_000_000:
            score += 60

        elif traded_value >= 200_000_000:
            score += 50

        elif traded_value >= 100_000_000:
            score += 40

        elif traded_value >= 50_000_000:
            score += 30

        elif traded_value >= 10_000_000:
            score += 20

        else:
            score += 10

        # Relative volume
        if relative_volume >= 2.0:
            score += 40

        elif relative_volume >= 1.5:
            score += 35

        elif relative_volume >= 1.2:
            score += 30

        elif relative_volume >= 1.0:
            score += 20

        elif relative_volume >= 0.8:
            score += 10

        return float(score)

    # -----------------------------------------------------

    @staticmethod
    def classify(
        liquidity_score: float,
    ) -> str:

        if liquidity_score >= 85:
            return "EXCELLENT"

        if liquidity_score >= 70:
            return "HIGH"

        if liquidity_score >= 50:
            return "MEDIUM"

        if liquidity_score >= 30:
            return "LOW"

        return "VERY_LOW"