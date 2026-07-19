"""
AI Decision Engine

Combines historical, strategy and options intelligence into a
single decision score.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class DecisionResult:

    score: float

    recommendation: str

    confidence: float

    component_scores: Dict[str, float]

    explanations: list[str]


class DecisionEngine:

    DEFAULT_WEIGHTS = {

        "historical": 0.30,

        "strategy": 0.25,

        "options": 0.25,

        "market": 0.20,

    }

    def __init__(
        self,
        weights: Dict[str, float] | None = None,
    ) -> None:

        self.weights = self.DEFAULT_WEIGHTS.copy()

        if weights:
            self.weights.update(weights)

    # ----------------------------------------------------

    def evaluate(
        self,
        historical_score: float,
        strategy_score: float,
        options_score: float,
        market_score: float,
    ) -> DecisionResult:

        weighted_score = (

            historical_score * self.weights["historical"]

            + strategy_score * self.weights["strategy"]

            + options_score * self.weights["options"]

            + market_score * self.weights["market"]

        )

        recommendation = self._recommendation(
            weighted_score
        )

        confidence = self._confidence(
            weighted_score
        )

        explanations = self._explain(
            historical_score,
            strategy_score,
            options_score,
            market_score,
        )

        return DecisionResult(

            score=round(weighted_score, 2),

            recommendation=recommendation,

            confidence=round(confidence, 2),

            component_scores={

                "historical": historical_score,

                "strategy": strategy_score,

                "options": options_score,

                "market": market_score,

            },

            explanations=explanations,

        )

    # ----------------------------------------------------

    @staticmethod
    def _recommendation(score: float) -> str:

        if score >= 90:
            return "STRONG BUY"

        if score >= 75:
            return "BUY"

        if score >= 60:
            return "WATCH"

        return "AVOID"

    # ----------------------------------------------------

    @staticmethod
    def _confidence(score: float) -> float:

        return min(
            100.0,
            max(0.0, score),
        )

    # ----------------------------------------------------

    @staticmethod
    def _explain(
        historical: float,
        strategy: float,
        options: float,
        market: float,
    ) -> list[str]:

        notes = []

        if historical >= 80:
            notes.append(
                "Historical performance is strong."
            )

        if strategy >= 75:
            notes.append(
                "Strategy alignment is favorable."
            )

        if options >= 75:
            notes.append(
                "Options setup is attractive."
            )

        if market >= 75:
            notes.append(
                "Market conditions support the trade."
            )

        if not notes:
            notes.append(
                "No strong supporting factors identified."
            )

        return notes

    # ----------------------------------------------------

    @staticmethod
    def as_dict(
        result: DecisionResult,
    ) -> Dict[str, Any]:

        return asdict(result)