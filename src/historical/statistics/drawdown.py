"""
Drawdown Calculator

Calculates drawdown statistics.

Author:
    AI Research Platform
"""

from __future__ import annotations

import pandas as pd


class DrawdownCalculator:

    # -----------------------------------------------------

    def calculate(
        self,
        df: pd.DataFrame,
    ) -> dict:

        close = df["Close"]

        rolling_max = close.cummax()

        drawdown = (
            close - rolling_max
        ) / rolling_max

        max_drawdown = float(
            drawdown.min()
        )

        current_drawdown = float(
            drawdown.iloc[-1]
        )

        average_drawdown = float(
            drawdown.mean()
        )

        duration = self.drawdown_duration(
            drawdown
        )

        recovery = self.recovery_days(
            drawdown
        )

        return {

            "max_drawdown": max_drawdown,

            "current_drawdown": current_drawdown,

            "average_drawdown": average_drawdown,

            "drawdown_duration": duration,

            "recovery_days": recovery,

            "drawdown_score": self.score(
                max_drawdown
            ),
        }

    # -----------------------------------------------------

    @staticmethod
    def drawdown_series(
        close: pd.Series,
    ) -> pd.Series:

        running_max = close.cummax()

        return (
            close - running_max
        ) / running_max

    # -----------------------------------------------------

    @staticmethod
    def drawdown_duration(
        drawdown: pd.Series,
    ) -> int:

        longest = 0
        current = 0

        for value in drawdown:

            if value < 0:

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
    def recovery_days(
        drawdown: pd.Series,
    ) -> int:

        current = 0

        total = 0

        periods = 0

        for value in drawdown:

            if value < 0:

                current += 1

            elif current > 0:

                total += current

                periods += 1

                current = 0

        if periods == 0:

            return 0

        return int(
            total / periods
        )

    # -----------------------------------------------------

    @staticmethod
    def score(
        max_drawdown: float,
    ) -> float:

        dd = abs(max_drawdown)

        if dd <= 0.05:
            return 100

        if dd <= 0.10:
            return 90

        if dd <= 0.15:
            return 80

        if dd <= 0.20:
            return 70

        if dd <= 0.30:
            return 55

        if dd <= 0.40:
            return 40

        return 20