"""
Historical Ranking Engine

Ranks qualified stocks using weighted historical metrics.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from .intelligence import HistoricalIntelligenceEngine
from .qualification import HistoricalQualificationEngine


@dataclass
class RankedStock:

    rank: int

    symbol: str

    score: float

    qualified: bool

    metrics: Dict[str, Any]


class HistoricalRankingEngine:

    DEFAULT_WEIGHTS = {

        "overall_score": 0.25,

        "cagr": 0.20,

        "sharpe_ratio": 0.15,

        "win_rate": 0.10,

        "liquidity_score": 0.10,

        "volatility": 0.10,

        "max_drawdown": 0.10,

    }

    def __init__(

        self,

        intelligence_engine: Optional[
            HistoricalIntelligenceEngine
        ] = None,

        qualification_engine: Optional[
            HistoricalQualificationEngine
        ] = None,

        weights: Optional[Dict[str, float]] = None,

    ):

        self.intelligence = (

            intelligence_engine

            or HistoricalIntelligenceEngine()

        )

        self.qualifier = (

            qualification_engine

            or HistoricalQualificationEngine()

        )

        self.weights = self.DEFAULT_WEIGHTS.copy()

        if weights:

            self.weights.update(weights)

    # -----------------------------------------------------

    def rank(

        self,

        symbols: List[str],

        period: str = "10y",

    ) -> List[RankedStock]:

        rankings = []

        for symbol in symbols:

            try:

                qualification = self.qualifier.qualify(

                    symbol,

                    period,

                )

                profile = self.intelligence.analyze(

                    symbol,

                    period,

                )

                score = self.calculate_score(

                    profile.statistics

                )

                rankings.append(

                    RankedStock(

                        rank=0,

                        symbol=symbol,

                        score=score,

                        qualified=qualification.qualified,

                        metrics=profile.statistics,

                    )

                )

            except Exception:

                continue

        rankings.sort(

            key=lambda stock: stock.score,

            reverse=True,

        )

        for index, stock in enumerate(

            rankings,

            start=1,

        ):

            stock.rank = index

        return rankings

    # -----------------------------------------------------

    def calculate_score(

        self,

        metrics: Dict[str, Any],

    ) -> float:

        score = 0.0

        score += (

            metrics.get(

                "overall_score",

                0,

            )

            * self.weights["overall_score"]

        )

        score += (

            metrics.get(

                "cagr",

                0,

            )

            * 100

            * self.weights["cagr"]

        )

        score += (

            metrics.get(

                "sharpe_ratio",

                0,

            )

            * 10

            * self.weights["sharpe_ratio"]

        )

        score += (

            metrics.get(

                "win_rate",

                0,

            )

            * 100

            * self.weights["win_rate"]

        )

        score += (

            metrics.get(

                "liquidity_score",

                0,

            )

            * self.weights["liquidity_score"]

        )

        volatility = metrics.get(

            "volatility",

            1,

        )

        score += (

            max(

                0,

                1 - volatility,

            )

            * 100

            * self.weights["volatility"]

        )

        drawdown = abs(

            metrics.get(

                "max_drawdown",

                1,

            )

        )

        score += (

            max(

                0,

                1 - drawdown,

            )

            * 100

            * self.weights["max_drawdown"]

        )

        return round(

            score,

            2,

        )

    # -----------------------------------------------------

    def top(

        self,

        symbols: List[str],

        top_n: int = 10,

        period: str = "10y",

    ) -> List[RankedStock]:

        return self.rank(

            symbols,

            period,

        )[:top_n]

    # -----------------------------------------------------

    @staticmethod

    def as_dict(

        rankings: List[RankedStock],

    ) -> List[Dict[str, Any]]:

        return [

            asdict(item)

            for item in rankings

        ]

    # -----------------------------------------------------

    def update_weights(

        self,

        **weights,

    ):

        self.weights.update(weights)

    # -----------------------------------------------------

    def get_weights(

        self,

    ) -> Dict[str, float]:

        return self.weights.copy()

    # -----------------------------------------------------

    def reset_weights(

        self,

    ):

        self.weights = self.DEFAULT_WEIGHTS.copy()