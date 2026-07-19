"""
Historical Statistics Engine

Central orchestrator for all historical statistics calculators.

Author:
    AI Research Platform
"""

from __future__ import annotations

from typing import Dict
import pandas as pd

from .returns import ReturnsCalculator
from .risk import RiskCalculator
from .drawdown import DrawdownCalculator
from .ratios import RatioCalculator
from .gaps import GapCalculator
from .consistency import ConsistencyCalculator
from .liquidity import LiquidityCalculator


class HistoricalStatisticsEngine:

    REQUIRED_COLUMNS = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    def __init__(self) -> None:

        self.return_calculator = ReturnsCalculator()

        self.risk_calculator = RiskCalculator()

        self.drawdown_calculator = DrawdownCalculator()

        self.ratio_calculator = RatioCalculator()

        self.gap_calculator = GapCalculator()

        self.consistency_calculator = ConsistencyCalculator()

        self.liquidity_calculator = LiquidityCalculator()

    # ------------------------------------------------------------

    def calculate(
        self,
        dataframe: pd.DataFrame,
    ) -> Dict:

        df = self._prepare_dataframe(dataframe)

        statistics = {}

        statistics.update(
            self.return_calculator.calculate(df)
        )

        statistics.update(
            self.risk_calculator.calculate(df)
        )

        statistics.update(
            self.drawdown_calculator.calculate(df)
        )

        statistics.update(
            self.ratio_calculator.calculate(df)
        )

        statistics.update(
            self.gap_calculator.calculate(df)
        )

        statistics.update(
            self.consistency_calculator.calculate(df)
        )

        statistics.update(
            self.liquidity_calculator.calculate(df)
        )

        statistics["overall_score"] = self.calculate_overall_score(
            statistics
        )

        statistics["quality"] = self.classify(
            statistics["overall_score"]
        )

        return statistics

    # ------------------------------------------------------------

    def _prepare_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        if dataframe.empty:

            raise ValueError(
                "Historical dataframe is empty."
            )

        df = dataframe.copy()

        missing = [

            column

            for column in self.REQUIRED_COLUMNS

            if column not in df.columns

        ]

        if missing:

            raise ValueError(
                f"Missing required columns: {missing}"
            )

        df["Date"] = pd.to_datetime(df["Date"])

        df = df.sort_values("Date")

        df = df.drop_duplicates(
            subset=["Date"]
        )

        df = df.reset_index(drop=True)

        return df

    # ------------------------------------------------------------

    @staticmethod
    def calculate_overall_score(
        statistics: Dict,
    ) -> float:

        score_keys = [

            "risk_score",

            "drawdown_score",

            "ratio_score",

            "gap_score",

            "consistency_score",

            "liquidity_score",

        ]

        scores = [

            statistics[key]

            for key in score_keys

            if key in statistics

        ]

        if not scores:

            return 0.0

        return round(

            sum(scores)

            / len(scores),

            2,

        )

    # ------------------------------------------------------------

    @staticmethod
    def classify(
        score: float,
    ) -> str:

        if score >= 90:

            return "A+"

        if score >= 80:

            return "A"

        if score >= 70:

            return "B"

        if score >= 60:

            return "C"

        if score >= 50:

            return "D"

        return "F"

    # ------------------------------------------------------------

    def summary(
        self,
        dataframe: pd.DataFrame,
    ) -> Dict:

        statistics = self.calculate(
            dataframe
        )

        return {

            "overall_score": statistics[
                "overall_score"
            ],

            "quality": statistics[
                "quality"
            ],

            "annual_return": statistics.get(
                "annual_return",
                0.0,
            ),

            "cagr": statistics.get(
                "cagr",
                0.0,
            ),

            "volatility": statistics.get(
                "volatility",
                0.0,
            ),

            "max_drawdown": statistics.get(
                "max_drawdown",
                0.0,
            ),

            "sharpe_ratio": statistics.get(
                "sharpe_ratio",
                0.0,
            ),

            "win_rate": statistics.get(
                "win_rate",
                0.0,
            ),

            "average_volume": statistics.get(
                "average_volume",
                0.0,
            ),

            "liquidity_score": statistics.get(
                "liquidity_score",
                0.0,
            ),

        }

    # ------------------------------------------------------------

    def health_check(
        self,
        dataframe: pd.DataFrame,
    ) -> bool:

        try:

            self.calculate(dataframe)

            return True

        except Exception:

            return False