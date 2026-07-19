"""
Confidence Engine

Computes a unified confidence score for AI trade decisions.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class ConfidenceResult:

    confidence: float

    confidence_level: str

    execute_trade: bool

    component_scores: Dict[str, float]

    reasons: list[str]


class ConfidenceEngine:

    DEFAULT_WEIGHTS = {

        "historical": 0.20,

        "strategy": 0.20,

        "market": 0.15,

        "options": 0.15,

        "liquidity": 0.10,

        "volatility": 0.10,

        "signal_agreement": 0.05,

        "prediction_accuracy": 0.05,

    }

    def __init__(
        self,
        weights: Dict[str, float] | None = None,
    ):

        self.weights = self.DEFAULT_WEIGHTS.copy()

        if weights:
            self.weights.update(weights)

    # ----------------------------------------------------------

    def evaluate(
        self,
        historical_score: float,
        strategy_score: float,
        market_score: float,
        options_score: float,
        liquidity_score: float,
        volatility_score: float,
        signal_agreement: float,
        prediction_accuracy: float,
    ) -> ConfidenceResult:

        confidence = (

            historical_score * self.weights["historical"]

            + strategy_score * self.weights["strategy"]

            + market_score * self.weights["market"]

            + options_score * self.weights["options"]

            + liquidity_score * self.weights["liquidity"]

            + volatility_score * self.weights["volatility"]

            + signal_agreement * self.weights["signal_agreement"]

            + prediction_accuracy * self.weights["prediction_accuracy"]

        )

        confidence = round(
            max(
                0,
                min(confidence, 100),
            ),
            2,
        )

        return ConfidenceResult(

            confidence=confidence,

            confidence_level=self._level(
                confidence
            ),

            execute_trade=confidence >= 70,

            component_scores={

                "historical": historical_score,

                "strategy": strategy_score,

                "market": market_score,

                "options": options_score,

                "liquidity": liquidity_score,

                "volatility": volatility_score,

                "signal_agreement": signal_agreement,

                "prediction_accuracy": prediction_accuracy,

            },

            reasons=self._reasons(

                confidence,

                historical_score,

                strategy_score,

                market_score,

                options_score,

            ),

        )

    # ----------------------------------------------------------

    @staticmethod
    def _level(
        confidence: float,
    ) -> str:

        if confidence >= 90:
            return "VERY_HIGH"

        if confidence >= 80:
            return "HIGH"

        if confidence >= 70:
            return "MEDIUM"

        if confidence >= 50:
            return "LOW"

        return "VERY_LOW"

    # ----------------------------------------------------------

    @staticmethod
    def _reasons(
        confidence: float,
        historical: float,
        strategy: float,
        market: float,
        options: float,
    ) -> list[str]:

        reasons = []

        if historical >= 80:
            reasons.append(
                "Historical metrics are strong."
            )

        if strategy >= 75:
            reasons.append(
                "Selected strategy has high probability."
            )

        if market >= 70:
            reasons.append(
                "Market regime supports the trade."
            )

        if options >= 70:
            reasons.append(
                "Options chain confirms the setup."
            )

        if confidence < 70:
            reasons.append(
                "Overall confidence is below execution threshold."
            )

        return reasons

    # ----------------------------------------------------------

    @staticmethod
    def merge_scores(
        scores: Dict[str, float],
    ) -> float:

        if not scores:
            return 0.0

        return round(

            sum(scores.values())

            / len(scores),

            2,

        )

    # ----------------------------------------------------------

    @staticmethod
    def as_dict(
        result: ConfidenceResult,
    ) -> Dict[str, Any]:

        return asdict(result)