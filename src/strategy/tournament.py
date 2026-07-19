"""
Strategy Tournament Engine

Evaluates multiple strategies for a stock and ranks them based on
historical intelligence metrics.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional

from src.historical.intelligence import HistoricalIntelligenceEngine


@dataclass
class StrategyResult:

    strategy: str

    score: float

    confidence: float

    reasons: List[str]


class StrategyTournamentEngine:

    STRATEGIES = [

        "Momentum",

        "Trend Following",

        "Breakout",

        "Swing",

        "Mean Reversion",

        "Covered Call",

        "Cash Secured Put",

        "Iron Condor",

    ]

    def __init__(

        self,

        intelligence_engine: Optional[
            HistoricalIntelligenceEngine
        ] = None,

    ):

        self.intelligence = (

            intelligence_engine

            or HistoricalIntelligenceEngine()

        )

    # ----------------------------------------------------------

    def evaluate(

        self,

        symbol: str,

        period: str = "10y",

    ) -> List[StrategyResult]:

        profile = self.intelligence.analyze(

            symbol,

            period,

        )

        metrics = profile.statistics

        results = []

        for strategy in self.STRATEGIES:

            score, reasons = self._score_strategy(

                strategy,

                metrics,

            )

            confidence = min(

                score,

                100,

            )

            results.append(

                StrategyResult(

                    strategy=strategy,

                    score=round(score, 2),

                    confidence=round(confidence, 2),

                    reasons=reasons,

                )

            )

        results.sort(

            key=lambda item: item.score,

            reverse=True,

        )

        return results

    # ----------------------------------------------------------

    def winner(

        self,

        symbol: str,

        period: str = "10y",

    ) -> StrategyResult:

        return self.evaluate(

            symbol,

            period,

        )[0]

    # ----------------------------------------------------------

    @staticmethod

    def as_dict(

        strategies: List[StrategyResult],

    ) -> List[Dict[str, Any]]:

        return [

            asdict(item)

            for item in strategies

        ]

    # ----------------------------------------------------------

    def _score_strategy(

        self,

        strategy: str,

        metrics: Dict[str, Any],

    ):

        score = 0.0

        reasons = []

        cagr = metrics.get("cagr", 0)
        sharpe = metrics.get("sharpe_ratio", 0)
        drawdown = abs(metrics.get("max_drawdown", 1))
        volatility = metrics.get("volatility", 1)
        liquidity = metrics.get("liquidity_score", 0)
        win_rate = metrics.get("win_rate", 0)

        if strategy == "Momentum":

            score += cagr * 200
            score += sharpe * 20
            score += win_rate * 30

            reasons.extend([
                "Higher CAGR preferred",
                "Positive Sharpe Ratio",
            ])

        elif strategy == "Trend Following":

            score += cagr * 220
            score += (1 - drawdown) * 40
            score += sharpe * 20

            reasons.append(
                "Strong long-term trend"
            )

        elif strategy == "Breakout":

            score += volatility * 60
            score += liquidity * 0.40

            reasons.append(
                "Higher volatility benefits breakouts"
            )

        elif strategy == "Swing":

            score += volatility * 45
            score += win_rate * 40
            score += liquidity * 0.25

            reasons.append(
                "Balanced volatility"
            )

        elif strategy == "Mean Reversion":

            score += (1 - volatility) * 60
            score += (1 - drawdown) * 40

            reasons.append(
                "Lower volatility preferred"
            )

        elif strategy == "Covered Call":

            score += liquidity * 0.50
            score += (1 - volatility) * 50

            reasons.append(
                "Stable option premium generation"
            )

        elif strategy == "Cash Secured Put":

            score += liquidity * 0.50
            score += sharpe * 20
            score += (1 - drawdown) * 40

            reasons.append(
                "Capital preservation"
            )

        elif strategy == "Iron Condor":

            score += (1 - volatility) * 80
            score += liquidity * 0.40

            reasons.append(
                "Range-bound conditions"
            )

        return score, reasons