"""
Risk Calculator

Calculates all volatility and risk related metrics.

Author:
    AI Research Platform
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class RiskCalculator:

    TRADING_DAYS = 252

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

        volatility = self.volatility(returns)

        downside = self.downside_volatility(
            returns
        )

        variance = float(
            returns.var()
        )

        std_dev = float(
            returns.std()
        )

        rolling = self.rolling_volatility(
            returns
        )

        return {

            "volatility": volatility,

            "downside_volatility": downside,

            "variance": variance,

            "standard_deviation": std_dev,

            "rolling_volatility": rolling,

            "risk_score": self.risk_score(
                volatility
            ),
        }

    # -----------------------------------------------------

    def volatility(
        self,
        returns: pd.Series,
    ) -> float:

        return float(

            returns.std()

            * np.sqrt(
                self.TRADING_DAYS
            )

        )

    # -----------------------------------------------------

    def downside_volatility(
        self,
        returns: pd.Series,
    ) -> float:

        downside = returns[
            returns < 0
        ]

        if downside.empty:

            return 0.0

        return float(

            downside.std()

            * np.sqrt(
                self.TRADING_DAYS
            )

        )

    # -----------------------------------------------------

    def rolling_volatility(
        self,
        returns: pd.Series,
        window: int = 21,
    ) -> float:

        if len(returns) < window:

            return 0.0

        rolling = (

            returns

            .rolling(window)

            .std()

            * np.sqrt(
                self.TRADING_DAYS
            )

        )

        return float(
            rolling.iloc[-1]
        )

    # -----------------------------------------------------

    def historical_volatility(
        self,
        returns: pd.Series,
        window: int = 252,
    ) -> float:

        if len(returns) < window:

            window = len(returns)

        hv = (

            returns.tail(window)

            .std()

            * np.sqrt(
                self.TRADING_DAYS
            )

        )

        return float(hv)

    # -----------------------------------------------------

    @staticmethod
    def classify(
        volatility: float,
    ) -> str:

        if volatility < 0.20:

            return "LOW"

        if volatility < 0.35:

            return "MEDIUM"

        return "HIGH"

    # -----------------------------------------------------

    def risk_score(
        self,
        volatility: float,
    ) -> float:

        """
        Lower volatility = Higher score
        """

        if volatility <= 0.15:

            return 100.0

        if volatility <= 0.20:

            return 90.0

        if volatility <= 0.25:

            return 80.0

        if volatility <= 0.30:

            return 70.0

        if volatility <= 0.40:

            return 55.0

        if volatility <= 0.50:

            return 40.0

        return 20.0