"""
Strategy Recommendation Engine

Selects the best trading strategy based on tournament results
and historical intelligence.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

from .tournament import (
    StrategyTournamentEngine,
    StrategyResult,
)
from src.historical.intelligence import (
    HistoricalIntelligenceEngine,
)


@dataclass
class StrategyRecommendation:

    symbol: str

    strategy: str

    confidence: float

    recommendation: str

    risk_level: str

    metrics: Dict[str, Any]

    reasons: list[str]


class StrategyRecommendationEngine:

    def __init__(
        self,
        tournament: Optional[
            StrategyTournamentEngine
        ] = None,
        intelligence: Optional[
            HistoricalIntelligenceEngine
        ] = None,
    ):

        self.tournament = (
            tournament
            or StrategyTournamentEngine()
        )

        self.intelligence = (
            intelligence
            or HistoricalIntelligenceEngine()
        )

    # ----------------------------------------------------------

    def recommend(
        self,
        symbol: str,
        period: str = "10y",
    ) -> StrategyRecommendation:

        winner = self.tournament.winner(
            symbol,
            period,
        )

        profile = self.intelligence.analyze(
            symbol,
            period,
        )

        metrics = profile.statistics

        risk = self._risk_level(metrics)

        recommendation = self._action(
            winner,
            metrics,
        )

        return StrategyRecommendation(

            symbol=symbol.upper(),

            strategy=winner.strategy,

            confidence=winner.confidence,

            recommendation=recommendation,

            risk_level=risk,

            metrics=metrics,

            reasons=winner.reasons,

        )

    # ----------------------------------------------------------

    def as_dict(
        self,
        symbol: str,
        period: str = "10y",
    ) -> Dict[str, Any]:

        return asdict(
            self.recommend(
                symbol,
                period,
            )
        )

    # ----------------------------------------------------------

    def _risk_level(
        self,
        metrics: Dict[str, Any],
    ) -> str:

        volatility = metrics.get(
            "volatility",
            1,
        )

        drawdown = abs(
            metrics.get(
                "max_drawdown",
                1,
            )
        )

        if volatility < 0.20 and drawdown < 0.10:
            return "LOW"

        if volatility < 0.35 and drawdown < 0.20:
            return "MEDIUM"

        return "HIGH"

    # ----------------------------------------------------------

    def _action(
        self,
        winner: StrategyResult,
        metrics: Dict[str, Any],
    ) -> str:

        confidence = winner.confidence

        overall = metrics.get(
            "overall_score",
            0,
        )

        if confidence >= 90 and overall >= 85:
            return "STRONG BUY"

        if confidence >= 75 and overall >= 70:
            return "BUY"

        if confidence >= 60:
            return "WATCH"

        return "AVOID"

    # ----------------------------------------------------------

    def explain(
        self,
        symbol: str,
        period: str = "10y",
    ) -> str:

        recommendation = self.recommend(
            symbol,
            period,
        )

        explanation = [
            f"Symbol: {recommendation.symbol}",
            f"Strategy: {recommendation.strategy}",
            f"Recommendation: {recommendation.recommendation}",
            f"Confidence: {recommendation.confidence:.2f}%",
            f"Risk: {recommendation.risk_level}",
            "",
            "Reasons:",
        ]

        for reason in recommendation.reasons:
            explanation.append(f"- {reason}")

        return "\n".join(explanation)