"""
Consistency Calculator

Calculates trading consistency and expectancy metrics.

Author:
    AI Research Platform
"""

from __future__ import annotations

import pandas as pd


class ConsistencyCalculator:

    # -----------------------------------------------------

    def calculate(
        self,
        df: pd.DataFrame,
    ) -> dict:

        returns = (
            df["Close"]
            .pct_change()
            .dropna()
        )

        winning = returns[returns > 0]

        losing = returns[returns < 0]

        total = len(returns)

        win_rate = (
            len(winning) / total
            if total
            else 0.0
        )

        loss_rate = (
            len(losing) / total
            if total
            else 0.0
        )

        avg_gain = (
            float(winning.mean())
            if not winning.empty
            else 0.0
        )

        avg_loss = (
            float(losing.mean())
            if not losing.empty
            else 0.0
        )

        expectancy = (
            (win_rate * avg_gain)
            +
            (loss_rate * avg_loss)
        )

        consecutive_wins = self.max_consecutive(
            returns,
            positive=True,
        )

        consecutive_losses = self.max_consecutive(
            returns,
            positive=False,
        )

        monthly_consistency = self.monthly_consistency(
            df
        )

        yearly_consistency = self.yearly_consistency(
            df
        )

        return {

            "winning_days": len(winning),

            "losing_days": len(losing),

            "win_rate": float(win_rate),

            "loss_rate": float(loss_rate),

            "average_gain": avg_gain,

            "average_loss": avg_loss,

            "expectancy": float(expectancy),

            "consecutive_wins": consecutive_wins,

            "consecutive_losses": consecutive_losses,

            "monthly_consistency": monthly_consistency,

            "yearly_consistency": yearly_consistency,

            "consistency_score": self.score(
                win_rate,
                expectancy,
            ),
        }

    # -----------------------------------------------------

    @staticmethod
    def max_consecutive(
        returns: pd.Series,
        positive: bool = True,
    ) -> int:

        longest = 0
        current = 0

        for value in returns:

            condition = (
                value > 0
                if positive
                else value < 0
            )

            if condition:

                current += 1

                longest = max(
                    longest,
                    current,
                )

            else:

                current = 0

        return longest

    # -----------------------------------------------------

    @staticmethod
    def monthly_consistency(
        df: pd.DataFrame,
    ) -> float:

        monthly = (

            df

            .set_index("Date")

            ["Close"]

            .resample("ME")

            .last()

            .pct_change()

            .dropna()

        )

        if monthly.empty:

            return 0.0

        return float(

            (monthly > 0).mean()

        )

    # -----------------------------------------------------

    @staticmethod
    def yearly_consistency(
        df: pd.DataFrame,
    ) -> float:

        yearly = (

            df

            .set_index("Date")

            ["Close"]

            .resample("YE")

            .last()

            .pct_change()

            .dropna()

        )

        if yearly.empty:

            return 0.0

        return float(

            (yearly > 0).mean()

        )

    # -----------------------------------------------------

    @staticmethod
    def score(
        win_rate: float,
        expectancy: float,
    ) -> float:

        score = 0.0

        score += min(
            win_rate * 70,
            70,
        )

        if expectancy > 0:

            score += min(
                expectancy * 5000,
                30,
            )

        return round(
            score,
            2,
        )